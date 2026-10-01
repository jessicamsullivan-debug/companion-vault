---
summary: "Checks facts that are due, notes marked 'needs checking', and any contradictions."
---
# Truth Check

1. Run the checker with Python 3: `python3 "<vault folder>/System/Tools/vault_check.py"`. If Python isn't installed, do the same checks by reading the notes (slower, but fine).
2. Take "Facts due a check" and "Uncertain notes not in To Review" from the report.
3. Look for contradictions between notes on the same subject.
4. Go through them one at a time, most important first. Ask: "Your notes say X (last confirmed March). Still right?"
   - Yes: update "last confirmed".
   - Changed: fix the note, update the date.
   - No longer true: set it to "retired", move it to Archive, and update every note linking to it.
5. After every 5 items, ask whether to carry on. Anything left goes in [[To Review]].
6. Update "Last run" in [[Settings]], and give a short summary.
