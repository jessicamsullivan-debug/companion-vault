#!/usr/bin/env python3
"""Companion Vault checker.

Reads every note in the vault and reports anything that breaks the vault's
rules: broken links, notes missing from their contents list, facts that are
due a check, old tasks, and so on. It only reports. It never changes a file.

Usage:
    python3 vault_check.py [path-to-vault] [--today YYYY-MM-DD]

With no path, it checks the vault it lives in (two folders up).
"""
import argparse
import datetime as dt
import os
import re
import sys
from collections import defaultdict

# ---------------------------------------------------------------- settings

LONG_NOTE_WORDS = 1000
RULES_WORDS = 850
TASK_DAYS = 14
TASKS_NOW_MAX = 10
DAILY_LINES_MAX = 8

# Folders that don't need a main note, and whose notes don't need listing.
UNLISTED_TOP = {"Daily", "Inbox", "Attachments"}
# Folders whose direct subfolders are "real things" that need a main note.
REAL_THING_PARENTS = {"People", "Projects", "Knowledge Hub", "Businesses"}

BANNED = [
    "delve", "seamless", "seamlessly", "unlock", "unlocks", "leverage",
    "leverages", "game-changer", "game changer", "elevate", "elevates",
    "robust", "fast-paced world", "supercharge", "cutting-edge",
    "frontmatter", "yaml", "wikilink", "wikilinks", "llm", "llms",
    "context window", "tokens",
]
BANNED_RE = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in BANNED) + r")\b", re.IGNORECASE)

LINK_RE = re.compile(r"!?\[\[([^\]\|#]*)(#[^\]\|]*)?(\|[^\]]*)?\]\]")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
TASK_RE = re.compile(r"^\s*- \[ \] (.*)$", re.MULTILINE)
ADDED_RE = re.compile(r"added (\d{4}-\d{2}-\d{2})")

# ------------------------------------------------------------ note reading


def split_details(text):
    """Split the details block at the top of a note from the body."""
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            return text[4:end], text[end + 4:].lstrip("\n")
    return "", text


def parse_details(block):
    """Read the simple key: value details used in this vault.

    Handles plain values, [inline, lists] and '- item' lists. Nested lists
    (like sources) are kept as raw text, which is all the checks need.
    """
    data = {}
    key = None
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if not line.startswith((" ", "\t", "-")) and ":" in line:
            key, _, value = line.partition(":")
            key = key.strip().lower()
            value = strip_comment(value).strip()
            if value.startswith("[") and value.endswith("]"):
                items = [v.strip().strip("'\"") for v in split_list(value[1:-1])]
                data[key] = [i for i in items if i]
            elif value:
                data[key] = value.strip("'\"")
            else:
                data[key] = []
        elif key is not None:
            if isinstance(data.get(key), list):
                item = line.strip()
                if item.startswith("- "):
                    item = item[2:]
                data[key].append(strip_comment(item).strip().strip("'\""))
    return data


def strip_comment(value):
    # A "#" starts a comment only when it follows a space and isn't in a link.
    out, depth = [], 0
    for i, ch in enumerate(value):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth = max(0, depth - 1)
        elif ch == "#" and depth == 0 and (i == 0 or value[i - 1] == " "):
            break
        out.append(ch)
    return "".join(out)


def split_list(inner):
    items, buf, depth = [], [], 0
    for ch in inner:
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
        if ch == "," and depth == 0:
            items.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    if buf:
        items.append("".join(buf))
    return items


def without_code(text):
    text = FENCE_RE.sub("", text)
    return INLINE_CODE_RE.sub("", text)


def links_in(text):
    return [m.group(1).strip() for m in LINK_RE.finditer(without_code(text))
            if m.group(1).strip()]


def link_name(target):
    """The note a link points at, as a lowercase name without folders."""
    name = target.replace("\\", "/").split("/")[-1]
    if name.lower().endswith(".md"):
        name = name[:-3]
    return name.lower()


def parse_period(text):
    """'3 months' -> days. Returns None if it can't be read."""
    m = re.match(r"^\s*(\d+)\s*(day|week|month|year)s?\s*$", str(text), re.I)
    if not m:
        m2 = re.match(r"^\s*(\d+)\s*d\s*$", str(text), re.I)  # older '90d'
        return int(m2.group(1)) if m2 else None
    n, unit = int(m.group(1)), m.group(2).lower()
    return n * {"day": 1, "week": 7, "month": 30, "year": 365}[unit]


def parse_date(text):
    try:
        return dt.date.fromisoformat(str(text).strip()[:10])
    except ValueError:
        return None


class Note:
    def __init__(self, vault, path):
        self.path = path
        self.rel = os.path.relpath(path, vault).replace(os.sep, "/")
        self.parts = self.rel.split("/")
        self.name = os.path.splitext(self.parts[-1])[0]
        self.folder = "/".join(self.parts[:-1])
        with open(path, encoding="utf-8") as f:
            self.text = f.read()
        block, self.body = split_details(self.text)
        self.details = parse_details(block)
        self.links = links_in(self.text)
        self.link_names = {link_name(l) for l in self.links}

    @property
    def is_blank_template(self):
        return self.rel.startswith("Templates & SOPs/Note Templates/")

    @property
    def top(self):
        return self.parts[0] if len(self.parts) > 1 else ""

    def words(self):
        return len(without_code(self.body).split())

    def has_summary(self):
        if self.details.get("summary"):
            return True
        first = next((l for l in self.body.splitlines()
                      if l.strip() and not l.startswith("#")), "")
        return first.lower().startswith("summary:")

    def section(self, heading):
        """Text under a '## heading', up to the next heading of that level."""
        m = re.search(r"^##\s+" + re.escape(heading) + r"\s*$(.*?)(?=^##\s|\Z)",
                      self.body, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        return m.group(1) if m else ""


# ------------------------------------------------------------------ checks


def load(vault):
    notes, files = [], set()
    for root, dirs, names in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for n in names:
            if n.startswith("."):
                continue
            files.add(n.lower())
            if n.lower().endswith(".md"):
                notes.append(Note(vault, os.path.join(root, n)))
    return notes, files


def is_main_note(note):
    """A note named after its folder, e.g. Mum/Mum.md or Acme Studio/Marketing/Acme Studio Marketing.md."""
    if len(note.parts) < 2:
        return False
    folder = note.parts[-2]
    if note.name == folder:
        return True
    return len(note.parts) >= 3 and note.name == f"{note.parts[-3]} {folder}"


def needs_listing(note):
    if len(note.parts) == 1:
        return note.name != "Home"
    if note.top in UNLISTED_TOP:
        return False
    if note.top == "Archive":
        return note.name != "Archive"
    return not (is_main_note(note) and len(note.parts) == 2)


def check(vault, today):
    notes, files = load(vault)
    by_name = defaultdict(list)
    for n in notes:
        by_name[n.name.lower()].append(n)
    main_notes = {n.folder: n for n in notes if is_main_note(n)}
    home = next((n for n in notes if n.rel == "Home.md"), None)
    to_review = next((n for n in notes if n.rel == "To Review.md"), None)
    report = defaultdict(list)

    # Broken links
    for n in notes:
        if n.top == "Inbox":
            continue
        if n.is_blank_template:
            continue
        for target in n.links:
            if "{{" in target:
                continue
            key = link_name(target)
            if key in by_name or key in files or target.lower() in files:
                continue
            report["Broken links"].append(f"{n.rel} links to [[{target}]], which doesn't exist")

    # Duplicate names
    for name, group in by_name.items():
        if len(group) > 1:
            places = ", ".join(g.rel for g in group)
            report["Notes with the same name"].append(f"'{group[0].name}' is used more than once: {places}")

    # Missing main notes
    folders = {n.folder for n in notes if n.folder}
    for root, dirs, _ in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for d in dirs:
            folders.add(os.path.relpath(os.path.join(root, d), vault).replace(os.sep, "/"))
    for folder in sorted(folders):
        parts = folder.split("/")
        needs = (len(parts) == 1 and parts[0] not in {"Daily", "Attachments"}) or \
                (len(parts) == 2 and parts[0] in REAL_THING_PARENTS) or \
                (len(parts) == 3 and parts[0] == "Businesses")
        if needs and folder not in main_notes:
            report["Folders without a main note"].append(f"{folder}/ has no main note named after the folder")

    # Notes missing from a contents list
    for n in notes:
        if not needs_listing(n):
            continue
        if len(n.parts) == 1:
            listers = [home] if home else []
        else:
            listers = []
            for i in range(len(n.parts) - 1, 0, -1):
                folder = "/".join(n.parts[:i])
                if folder in main_notes and main_notes[folder] is not n:
                    listers.append(main_notes[folder])
            if len(n.parts) == 2 and is_main_note(n):
                listers = [home] if home else []
        if not any(n.name.lower() in l.link_names for l in listers if l):
            where = listers[0].rel if listers else "a main note"
            report["Notes missing from a contents list"].append(f"{n.rel} isn't listed in {where}")

    # Home lists every section
    if home:
        for folder in sorted(f for f in folders if "/" not in f and f in main_notes):
            if folder.lower() not in home.link_names:
                report["Notes missing from a contents list"].append(f"The {folder} section isn't listed in Home.md")
        biz = sorted(f for f in folders if f.startswith("Businesses/") and f.count("/") == 1)
        for folder in biz:
            name = folder.split("/")[1]
            if name.lower() not in home.link_names:
                report["Notes missing from a contents list"].append(f"The business '{name}' isn't listed in Home.md")
    else:
        report["Missing core notes"].append("Home.md is missing")

    # Summaries
    for n in notes:
        if n.top in {"Daily", "Inbox"} or n.name in {"Home"} or n.is_blank_template:
            continue
        if not n.has_summary():
            report["Notes without a summary"].append(n.rel)

    # Facts due a check, and uncertain notes not in To Review
    review_links = to_review.link_names if to_review else set()
    for n in notes:
        if n.is_blank_template:
            continue
        status = str(n.details.get("status", "")).lower()
        if status in {"not confirmed", "needs checking"} and n.name.lower() not in review_links:
            report["Uncertain notes not in To Review"].append(f"{n.rel} is '{status}' but isn't in To Review.md")
        if status == "confirmed":
            last = parse_date(n.details.get("last confirmed", ""))
            every = parse_period(n.details.get("check every", ""))
            if last and every and (today - last).days > every:
                report["Facts due a check"].append(
                    f"{n.rel}: last confirmed {last.isoformat()}, check every {n.details.get('check every')}")
            elif n.details.get("check every") and not every:
                report["Details that can't be read"].append(
                    f"{n.rel}: 'check every: {n.details.get('check every')}' should look like '3 months'")

    # Old tasks, and a crowded Now list
    tasks = next((n for n in notes if n.rel == "Tasks.md"), None)
    if tasks:
        for line in TASK_RE.findall(tasks.body):
            m = ADDED_RE.search(line)
            if m:
                added = parse_date(m.group(1))
                if added and (today - added).days > TASK_DAYS:
                    report["Tasks older than 14 days"].append(line.strip())
            elif "{{" not in line:
                report["Tasks without an 'added' date"].append(line.strip())
        now = tasks.section("Now")
        count = len(TASK_RE.findall(now))
        if count > TASKS_NOW_MAX:
            report["Notes over their limit"].append(f"Tasks.md has {count} tasks in Now (limit {TASKS_NOW_MAX})")

    # Length limits
    for n in notes:
        words = n.words()
        if n.rel == "System/Rules.md" and words > RULES_WORDS:
            report["Notes over their limit"].append(f"System/Rules.md is {words} words (limit about 800)")
        elif n.top == "Daily":
            lines = [l for l in n.body.splitlines() if l.strip() and not l.startswith("#")]
            if len(lines) > DAILY_LINES_MAX:
                report["Notes over their limit"].append(f"{n.rel} has {len(lines)} lines (daily notes should be a few)")
        elif words > LONG_NOTE_WORDS and n.top != "Archive":
            report["Very long notes (worth asking about a split)"].append(f"{n.rel}: {words} words")

    # Templates and SOPs link both ways
    for n in notes:
        kind = str(n.details.get("type", "")).lower()
        if kind not in {"sop", "template"}:
            continue
        used_in = n.details.get("used in") or []
        if isinstance(used_in, str):
            used_in = [used_in]
        used_names = set()
        for area in used_in:
            found = links_in(area) or [area]
            for a in found:
                key = link_name(a)
                used_names.add(key)
                target = by_name.get(key)
                if not target:
                    continue  # reported as a broken link
                if n.name.lower() not in target[0].link_names:
                    report["Templates and SOPs not linked both ways"].append(
                        f"{n.rel} says it's used in {target[0].name}, but {target[0].rel} doesn't link to it")
        for other in notes:
            sect = other.section("Templates and SOPs for this area")
            if n.name.lower() in {link_name(l) for l in links_in(sect)} and other.name.lower() not in used_names:
                report["Templates and SOPs not linked both ways"].append(
                    f"{other.rel} lists {n.name}, but {n.rel} doesn't have {other.name} in 'used in'")

    # Copies made by iCloud, OneDrive or Dropbox when syncing clashes ("Home 2.md", "People 2")
    names_on_disk = set()
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        rel_root = os.path.relpath(root, vault)
        for item in dirs + files:
            names_on_disk.add(os.path.normpath(os.path.join(rel_root, item)))
    for item in sorted(names_on_disk):
        base, ext = os.path.splitext(item)
        m = re.match(r"^(.*) (\d+)$", base)
        if not m:
            continue
        original = m.group(1) + ext
        if original in names_on_disk:
            report["Possible sync copies"].append(f"{item} looks like a copy of {original}")
        elif re.search(r" (19|20)\d\d$", base):
            year = int(m.group(2))
            if m.group(1) + f" {year - 1}" + ext in names_on_disk and year > today.year:
                report["Possible sync copies"].append(f"{item} may be a sync copy of {m.group(1)} {year - 1}{ext}")

    # Gaps left from setup
    for n in notes:
        if n.is_blank_template:
            continue
        gaps = sorted(set(re.findall(r"\{\{[^}]+\}\}", without_code(n.text))))
        if gaps:
            report["Gaps not filled in"].append(f"{n.rel}: {', '.join(gaps)}")

    # Plain English
    for n in notes:
        if n.top == "Inbox":
            continue
        found = sorted({m.group(1).lower() for m in BANNED_RE.finditer(without_code(n.body))})
        if found:
            report["Words to avoid (plain English rule)"].append(f"{n.rel}: {', '.join(found)}")

    return notes, report


ORDER = [
    "Missing core notes", "Possible sync copies", "Gaps not filled in", "Broken links", "Notes with the same name",
    "Folders without a main note", "Notes missing from a contents list",
    "Templates and SOPs not linked both ways", "Uncertain notes not in To Review",
    "Facts due a check", "Tasks older than 14 days", "Tasks without an 'added' date",
    "Notes without a summary", "Notes over their limit",
    "Very long notes (worth asking about a split)", "Details that can't be read",
    "Words to avoid (plain English rule)",
]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser(description="Check a Companion Vault for problems. Reports only; changes nothing.")
    ap.add_argument("vault", nargs="?", default=os.path.normpath(os.path.join(here, "..", "..")))
    ap.add_argument("--today", help="pretend today is this date (YYYY-MM-DD), for testing")
    args = ap.parse_args()
    today = parse_date(args.today) if args.today else dt.date.today()
    vault = os.path.abspath(os.path.expanduser(args.vault))
    if not os.path.isdir(vault):
        print(f"Can't find a vault at {vault}")
        return 2

    notes, report = check(vault, today)
    total = sum(len(v) for v in report.values())
    print(f"Vault check: {vault}")
    print(f"{len(notes)} notes checked on {today.isoformat()}.")
    if not total:
        print("All good. Nothing to fix.")
        return 0
    print(f"{total} thing{'s' if total != 1 else ''} to look at:\n")
    for heading in ORDER + sorted(set(report) - set(ORDER)):
        items = report.get(heading)
        if not items:
            continue
        print(f"{heading} ({len(items)})")
        for item in items:
            print(f"  - {item}")
        print()
    return 1


if __name__ == "__main__":
    sys.exit(main())
