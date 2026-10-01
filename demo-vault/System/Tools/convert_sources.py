"""Turns the nested `sources:` detail into a simple `source:` line, and moves web and
document sources into a "## Sources" list in the note body. Safe to run more than once.

Usage: python3 convert_sources.py <folder> [<folder> ...]
"""
import os
import re
import sys


def parse_sources(block_lines):
    entries, cur = [], None
    for line in block_lines:
        m = re.match(r"^\s*-\s*(\w[\w ]*):\s*(.*)$", line)
        if m:
            cur = {m.group(1).strip(): m.group(2).strip().strip("'\"")}
            entries.append(cur)
            continue
        m = re.match(r"^\s+(\w[\w ]*):\s*(.*)$", line)
        if m and cur is not None:
            cur[m.group(1).strip()] = m.group(2).strip().strip("'\"")
    return entries


def body_line(e):
    t = e.get("type", "")
    if t == "web":
        title = e.get("title") or "Title"
        url = e.get("url") or ""
        bits = [f"[{title}]({url})" if url else title]
        if e.get("publisher"):
            bits.append(e["publisher"])
        if e.get("published"):
            bits.append(f"published {e['published']}")
        if e.get("accessed"):
            bits.append(f"looked at {e['accessed']}")
        line = "- " + ", ".join(bits)
        if "quote" in e:
            line += f'. Quote: "{e.get("quote", "")}"'
        return line
    if t == "document":
        title = e.get("title") or "Document"
        return f"- {title}" + (f", {e['location']}" if e.get("location") else "")
    return None


def convert(text):
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    if end == -1:
        return text
    head, body = text[4:end].split("\n"), text[end + 4:]
    out, i, entries = [], 0, None
    while i < len(head):
        line = head[i]
        if re.match(r"^sources:\s*$", line):
            j = i + 1
            while j < len(head) and (head[j].startswith((" ", "\t")) or head[j].strip() == ""):
                j += 1
            entries = parse_sources(head[i + 1:j])
            i = j
            continue
        out.append(line)
        i += 1
    if entries is None:
        return text
    types = []
    for e in entries:
        t = e.get("type", "told by me")
        if t not in types:
            types.append(t)
    value = " and ".join(types) if types else "told by me"
    # put `source:` where `sources:` was (after check every, if present)
    idx = next((k for k, l in enumerate(out) if l.startswith("check every:")), len(out) - 1)
    out.insert(idx + 1, f"source: {value}")
    lines = [l for l in (body_line(e) for e in entries) if l]
    new_body = body
    if lines and "\n## Sources\n" not in body:
        new_body = body.rstrip("\n") + "\n\n## Sources\n" + "\n".join(lines) + "\n"
    return "---\n" + "\n".join(out) + "\n---" + new_body


def main():
    changed = 0
    for root_dir in sys.argv[1:]:
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in files:
                if not f.endswith(".md"):
                    continue
                p = os.path.join(root, f)
                s = open(p, encoding="utf-8").read()
                n = convert(s)
                if n != s:
                    open(p, "w", encoding="utf-8").write(n)
                    changed += 1
    print("converted", changed, "notes")


if __name__ == "__main__":
    main()
