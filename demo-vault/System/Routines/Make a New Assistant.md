---
summary: "Sets up another assistant that shares this vault, with its own name, job and personality."
---
# Make a New Assistant

1. Ask, one at a time:
   - What's it for? (for example "writing social posts for Acme Studio")
   - Which parts of the vault should it work in mainly?
   - Pick a personality style (the same six as setup), and its name.
   - Any rules just for this assistant?
2. Create its folder next to the main one (for example `~/writing-assistant/`), copying the agent files from the kit's `templates/agent/` folder.
3. Fill in its `AGENTS.md`: who it is, its personality, its own rules, the vault path, and the start-of-session steps. That file stays the same unless the person asks to change the assistant's personality or rules. Give it access to the vault, as setup did for the main one.
4. Add it to [[Assistants]].
5. Tell the person how to open it: open their assistant app in that folder.
