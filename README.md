# Companion Vault

**An organised, always-true second brain for your AI assistant.**

Companion Vault gives your AI assistant a memory that lasts. It builds you an Obsidian vault (a folder of notes you can read and edit) and sets your assistant up to look after it. The assistant remembers who you are, how you work and how you write. It saves what it learns, keeps facts up to date, and never guesses.

> Companion Vault is an independent community project. It is not made by, affiliated with, or endorsed by Anthropic, OpenAI or Google. Claude, ChatGPT, Codex and Gemini are trademarks of their owners.

> Tested on Mac with Claude Code. Windows, Codex and Gemini should work, but haven't been fully tested yet.

## What it does

- **Remembers you.** How you like to work, what you're working towards, the people in your life, and your business.
- **Stops re-researching.** It checks your Knowledge Hub before searching the web, and saves what it finds with the exact source.
- **Keeps everything true.** Every fact has a "last confirmed" date. When something might be out of date, it asks you instead of guessing.
- **Flags contradictions.** If two notes disagree, it tells you and asks which is right.
- **Writes like you.** On email, Slack, WhatsApp and anywhere else, in the tone you use there.
- **Stays organised.** Drop anything new in the Inbox and it files it for you. Anything can be found within about three clicks.
- **Grows with you.** Templates and step-by-step guides (SOPs) for the things you do again and again.

## What you need

- A computer (Mac or Windows)
- [Obsidian](https://obsidian.md), free. Setup can install it for you.
- An AI assistant that can work with files on your computer, such as:

| Assistant | Works? |
|---|---|
| Claude Code, in the Claude desktop app or the terminal | ✅ Best tested |
| OpenAI Codex | ✅ |
| Gemini CLI | ✅ |
| Cursor and similar editors | ✅ |
| ChatGPT, Claude or Gemini in a web browser | ❌ They can't open folders on your computer |

## Install

### The easy way (no typing commands)

1. Click the green **Code** button on this page, then **Download ZIP**.
2. Make a folder called `my-agent` in your home folder (on a Mac, that's the folder with your name, not Documents or Desktop).
3. Unzip the download. You'll get a folder called `companion-vault-main`. Rename it to `companion-vault` and move it into `my-agent`.
4. Open your assistant in the `companion-vault` folder. In the Claude desktop app: open the **Code** tab, choose that folder, and start a chat.
5. Type **set me up**.

### The quick way (if you're happy using a terminal)

Mac:

```bash
mkdir -p ~/my-agent && cd ~/my-agent && git clone https://github.com/jessicamsullivan-debug/companion-vault && cd companion-vault && claude "set me up"
```

Using Codex instead? Replace `claude "set me up"` with `codex "set me up"`.

If you'd rather use a different folder than `my-agent`, that's fine. Setup will check where the kit is and offer to move it if it's somewhere like Downloads.

### What happens next

Your assistant interviews you, one question at a time. The **quick start** takes about 10 minutes, and the **full setup** takes 30 to 45. You can skip anything and come back to it later. At the end, your vault opens in Obsidian and your assistant says hello.

> **Tip: talk instead of typing.** Setup asks a lot of questions, and speaking your answers is much quicker. I use [Wispr Flow](https://wisprflow.ai/r?JESSICA4157), which turns what you say into text in any app. That's my referral link, and it gets you a free month.

## How to use it

- **After setup, open your assistant in `my-agent`** (not in `companion-vault`). That's where it lives. Opened anywhere else, it won't know you.
- **Put anything new in the Inbox:** notes, documents, screenshots. Your assistant files it at your first chat each day.
- **One chat per topic.** Start a fresh chat when the subject changes.
- **Say "bye" when you're done,** and it saves anything important.
- **Ask for a routine by name:** "weekly review", "truth check", "tidy the map", "go through To Review".
- **Change anything by asking:** "be more blunt", "add a business", "run the truth check every 6 months".

## What's inside

```
companion-vault/
├── SETUP.md        the setup interview your assistant follows
├── AGENTS.md       tells your assistant how to start setup
├── templates/      the vault, the Business pack, starter templates, and your assistant's files
└── demo-vault/     a complete example vault, to see what you'll get
```

Want to see it before you install? Open the `demo-vault` folder in Obsidian (**Open folder as vault**).

## Updating

Say **"update the kit"** to your assistant. It gets the newest version, tells you what changed, and only updates your vault's rules and routines after you say yes. It never changes your own notes.

## Your privacy

Your vault is stored on your computer, not here. When your assistant reads a note to help you, that note is sent to your AI provider, just like anything you type into a chat. So never store passwords, bank details or ID numbers in it (your assistant won't). Setup also helps you choose a backup.

## Good to know

Companion Vault helps you organise information. It doesn't give financial, legal or medical advice. Only drop files you trust into your Inbox.

## Licence

MIT. See [LICENSE](LICENSE).
