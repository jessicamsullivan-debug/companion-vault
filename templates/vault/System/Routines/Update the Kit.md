---
summary: "Gets the newest rules and routines from the kit, only after the person says yes."
---
# Update the Kit

1. Find the kit folder in [[Settings]]. Download the newest version there (`git pull`, or download it again from GitHub).
2. Compare the kit's `templates/vault/System/` with this vault's `System/` folder: the rules, the routines and the checker.
3. Read the kit's `CHANGELOG.md` for every version newer than the one in [[Settings]]. Explain what changed, in plain English, one short line per change.
4. Only after the person says yes: copy the new versions into `System/`. Never touch their own notes, [[Settings]] or [[Assistants]].
5. If the changelog says a version needs a tidy-up step for older vaults (like running a tool in `System/Tools/`), explain it, and do it only after the person says yes.
6. Update the kit version in [[Settings]], and run [[Tidy the Map]] to check everything still links up.
