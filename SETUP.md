# Setup

You are setting up Companion Vault for someone. Follow this file from top to bottom. It builds two things:

- **their assistant:** the folder that contains this kit (the kit's parent folder, usually `~/my-agent/`)
- **their vault:** a new Obsidian folder that holds everything their assistant knows

## How to run the interview

- **One question at a time.** Wait for the answer before asking the next one.
- **Plain English.** No tech words. If a term is unavoidable, explain it in a few words first.
- **Offer a suggestion** wherever there's a sensible default, e.g. "UK English? (just say yes to keep it)".
- **Lists: show the suggestions, then ask "Anything else?"**
- **Anything can be skipped.** If they say "skip" or "later", add a task to `Tasks.md`, e.g. `- [ ] Finish setup: Communication (added 2026-09-29)`, and move on.
- **Go deeper.** At the end of each part, ask "Want to add more detail here?" and offer that part's **Go deeper** questions. "Tell me more" on any question means: explain why you're asking, with an example.
- **Never guess.** If an answer is unclear, ask a follow-up question.
- **Save as you go.** Write each answer into its note straight away. At the end of each part, show what you wrote and ask "Anything to change?", then update `Setup` in `System/Settings.md` (e.g. "Part 4 of 10 done").
- **Resuming.** If a vault from this kit already exists, read `Setup` in its `System/Settings.md` and carry on from the next part. Never overwrite anything they've already filled in.
- **Quick start** means: ask only the ★ questions, and add one "Finish setup" task for each skipped part.

## Filling in the templates

The kit's templates contain gaps like `{{name}}`. Fill in what you already know when you copy the files, and fill the rest as each part of the interview answers them. Part 10 checks that none are left. Here's what each gap is for:

| Gap | Filled with |
|---|---|
| `{{today}}`, `{{year}}` | today's date as YYYY-MM-DD, and the year |
| `{{name}}`, `{{called}}` | their name, and what they like to be called |
| `{{spelling}}`, `{{currency}}`, `{{how dates look}}`, `{{time zone}}` | Parts 1 and 3 |
| `{{agent name}}`, `{{personality}}`, `{{welcome line}}`, `{{agent rules}}` | Part 2 (`{{agent rules}}` is "None yet." unless they give one in 2.3) |
| `{{agent job}}` | Part 3, answer 3.2 (in `System/Assistants.md`) |
| `{{agent folder}}`, `{{kit folder}}` | the full path of the assistant's folder, and of this kit |
| `{{vault path}}` | the full path of the vault |
| `{{vault path rule}}` | the vault path as Claude Code wants it in a permission rule (see Part 1, step 1.8) |
| `{{... schedule}}`, `{{backup method}}`, `{{backup details}}` | Parts 1 and 8. `{{backup details}}` is one line saying where the backup goes, e.g. "External drive called Backup, plugged in on Fridays" or "Vault kept inside iCloud Drive, set to Keep Downloaded" |
| `{{Business}}` and the other business gaps | Part 6 |
| `{{setup status}}` | "Part 1 of 10 done", and so on |

**Never replace** `{{title}}` or `{{date...}}` inside the files in `Templates & SOPs/Note Templates/` themselves (Obsidian fills those when the person creates a note). But when **you** create a note from one of those templates (a person, a client, a project), fill `{{title}}` with the note's name and `{{date...}}` with today's date. Also leave any gap written in backticks, like `` `{{client name}}` ``, inside a template or SOP: those are filled each time the template is used.

If a gap has no answer yet (because they skipped), leave the line out, or leave the section empty. Never leave `{{...}}` text in their vault.

---

## Part 0: Checks

Do these quietly, and only talk about what needs the person's help.

1. **Which computer?** Check whether it's a Mac, Windows or Linux.
2. **Obsidian.** Check whether it's installed. If not, explain in one line that it's the free app for reading the vault, then offer to install it:
   - Mac: `brew install --cask obsidian` if Homebrew is installed. Otherwise ask them to download it from obsidian.md and tell you when it's done.
   - Windows: `winget install Obsidian.Obsidian`
3. **Python 3** (for the checker). Check `python3 --version` (Windows: `py --version`). If it's missing, explain it's a small free tool that lets you check the vault quickly, and offer to install it:
   - Mac: `xcode-select --install` (a pop-up asks them to click Install)
   - Windows: `winget install Python.Python.3.12`
   If they'd rather not, carry on. You'll do the checks by reading the notes instead.
4. **Where their assistant will live.** Their assistant's folder is the folder that contains this kit. Check it:
   - If this kit's folder is called `companion-vault-main` (it's named that when downloaded as a ZIP), rename it to `companion-vault`.
   - If the folder containing it is Downloads, Desktop, Documents, or anywhere that isn't clearly meant for this, say: "Your assistant needs a home folder of its own. Shall I make one at `~/my-agent` and move this kit into it?" On a yes, do it, then tell them to open their assistant in the kit's new location and say "set me up" again.
5. **An existing vault or assistant from this kit?** If the parent folder already has an `AGENTS.md` that's been filled in, or they mention an existing vault, read its `System/Settings.md` and resume. Never overwrite.

Then say hello, in one or two lines: what's about to happen, that it takes about 10 minutes for the quick version or 30–45 for the full one, and that anything can be skipped. Also say: "While I set things up, your app may ask you to allow me to create and change files. Choose Allow each time. After setup, it won't need to ask."

---

## Part 1: The basics

| # | Ask | Then |
|---|---|---|
| ★1.1 | "Quick start (about 10 minutes, the essentials) or full setup (30–45 minutes, everything)?" | Remember the choice |
| ★1.2 | "What's your name, and what would you like me to call you?" | `{{name}}`, `{{called}}` |
| ★1.3 | "UK or US English?" | `{{spelling}}` |
| ★1.4 | "Which currency?" (suggest £ for UK, $ for US) | `{{currency}}` |
| ★1.5 | "How should dates look?" (suggest 29/09/2026 for UK, 09/29/2026 for US) | `{{how dates look}}` |
| ★1.6 | Backup: see below | `{{backup method}}`, `{{backup details}}`; decides where the vault goes |
| ★1.7 | "Would you like a **new vault**, or should I build into an **Obsidian vault you already have**?" Check Obsidian's own list of vaults first (Mac: `~/Library/Application Support/obsidian/obsidian.json`; Windows: `%APPDATA%\obsidian\obsidian.json`) and offer them by name. For a new vault, ask: "What would you like to call it?" (suggest "{{called}}'s Vault") | the vault's folder name, or the existing vault (see "Building into an existing vault") |

### 1.6 Backup (asked before the vault exists, because some choices decide where it lives)

Say plainly: "Your vault will live on this computer. If the computer is lost or breaks, the vault goes with it, so let's pick a backup." Then offer:

1. **Time Machine** (Mac) or **File History** (Windows): free and built in. It backs up everything automatically to an external drive. Vault location: your home folder.
2. **Obsidian Sync:** paid, around £4–5 a month. It also puts your vault on your phone. Vault location: your home folder. They switch it on inside Obsidian afterwards; walk them through it.
3. **iCloud Drive** (Mac) or **OneDrive** (Windows): free with the account they already have. Vault location: inside the cloud folder. After creating the vault, make sure the vault folder is always kept on the computer: on a Mac, right-click it in Finder and choose "Keep Downloaded"; in OneDrive, choose "Always keep on this device". Otherwise files can be moved to the cloud where you can't read them.
4. **A private GitHub repository** (more technical): free, and keeps every version. Only offer it if they're comfortable with GitHub. It **must be private**.
5. **Copy it myself** to an external drive every so often. The Backup Check routine will remind them.

### Building into an existing vault
If they choose a vault they already have:
1. Look at its folder and note names only (not the notes themselves), and tell them in one line what's there.
2. If it's empty or nearly empty, build into it as normal.
3. If it already has notes: never move, rename, change or delete them. Copy in only the kit files and folders that don't already exist. If a kit note has the same name as one of theirs, keep theirs and put the kit's version in `Archive/` with "(kit version)" added to its name.
4. Merge the Obsidian settings below into their `.obsidian/` files, keeping every setting they already have.
5. At the end of setup, offer to sort their existing notes into the new structure later, using the Import routine. Everything gets copied, and the originals stay where they are.
6. The vault stays where it is, so skip step 1 below. Its location also decides the backup: tell them if it's already inside iCloud Drive or OneDrive.

### 1.8 Create the vault (no question)

1. Work out the vault path: `~/<vault name>` for options 1, 2, 4 and 5. For option 3, it goes inside the cloud folder (Mac: `~/Library/Mobile Documents/com~apple~CloudDocs/<vault name>`; Windows: `%USERPROFILE%\OneDrive\<vault name>`).
2. Copy everything in the kit's `templates/vault/` to that path, filling in the gaps. Rename `Decisions {{year}}.md` with this year. In `Templates & SOPs/Note Templates/Daily Note.md`, change the heading to match how they want dates to look (e.g. `{{date:YYYY/MM/DD}}` or `{{date:DD/MM/YYYY}}`).
3. Say the full path out loud: "Your vault is at …".
4. Set up the assistant's folder (this kit's parent folder):
   - Copy `templates/agent/AGENTS.md`, `CLAUDE.md` and `GEMINI.md` there, and fill in `AGENTS.md` after Part 2. After setup, `AGENTS.md` stays the same unless the person asks to change the assistant's personality or rules. Everything else lives in the vault.
   - Copy `templates/agent/.claude/settings.json` to `.claude/settings.json` there. Set `{{vault path}}` to the full vault path, and `{{vault path rule}}` to the same path written for a permission rule. If the vault is anywhere inside the home folder (including iCloud Drive or OneDrive), use `~/` followed by the path from the home folder (e.g. `~/My Vault` or `~/Library/Mobile Documents/com~apple~CloudDocs/My Vault`). Only if it's outside the home folder (for example on another drive), use `//` followed by the full path without its first slash (e.g. `//Volumes/Backup Drive/My Vault`). If a `.claude/settings.json` already exists there, add these lines to it rather than replacing it. These settings take effect from the next chat, which is why the person may see Allow requests during setup.
   - Not using Claude Code? Give the assistant access to the vault in whatever way that app allows (for example, opening the vault as an extra folder or workspace), and tell the person in one line what you did.
5. Obsidian settings, written into the vault's `.obsidian/` folder:
   - `app.json`: `{"alwaysUpdateLinks": true, "useMarkdownLinks": false, "newLinkFormat": "shortest", "attachmentFolderPath": "Attachments", "newFileLocation": "folder", "newFileFolderPath": "Inbox", "showInlineTitle": false}` (so notes the person creates land in the Inbox, and get filed)
   - `daily-notes.json`: `{"folder": "Daily", "format": "YYYY-MM-DD", "template": "Templates & SOPs/Note Templates/Daily Note"}`
   - `templates.json`: `{"folder": "Templates & SOPs/Note Templates", "dateFormat": "YYYY-MM-DD"}`
   - `bookmarks.json`: `{"items": [{"type": "file", "path": "Home.md", "title": "Home"}]}`, so Home is always one click away in the Bookmarks panel
   - `core-plugins.json`: if it exists, set `"templates": true` in it. If not, leave it; you'll ask them to switch Templates on in Part 10.
6. For backup option 3: check the vault folder is set to always stay on the computer (see above). For option 4: help them create the private repository and make the first save.

---

## Part 2: Their assistant's personality

### ★2.1 Pick a style
Show all six, each with its example reply to "Can you check this email?":

| Style | Like this |
|---|---|
| **Straight-talking partner**: direct, no fluff, pushes back | "Two problems: the ask is buried in paragraph three, and the deadline's missing. Fixed version below." |
| **Warm and encouraging**: friendly, patient, explains things | "This is nearly there! I've moved your main question to the top so it stands out, and added the deadline." |
| **Calm and professional**: polished and concise | "Two suggested changes: lead with the request, and add the deadline. Revised version below." |
| **Witty and relaxed**: casual and light, still sharp | "Good bones, but your actual question is hiding in paragraph three like it owes someone money. Moved it up, added the deadline." |
| **Bestie**: on your side, chatty, honest like a real best friend | "Okay, you sound SO lovely in this, but they won't find your question until paragraph three 😅 Popped it at the top and added the deadline!" |
| **Co-founder**: thinks like a business partner, goal-focused | "Fixed: request up top, deadline added. Bigger question: is this the client we agreed to prioritise this quarter? If not, keep it short and move on." |

### ★2.2 Name
"What would you like to call me?" Suggest a name that suits the style, and let them choose anything.

### 2.3 Adjust
"Want to adjust anything? Here's what I'll do by default." Show each with its default for the chosen style, and let them change any:

| Setting | Options | Default |
|---|---|---|
| Bluntness | gentle · balanced · blunt | gentle (Warm, Bestie) · balanced (Calm, Witty) · blunt (Straight-talking, Co-founder) |
| Pushing back | only when asked · when it matters · always challenge me | when it matters |
| Reply length | short · medium · detailed | short (Straight-talking, Calm, Co-founder) · medium (the others) |
| Humour | none · a little · plenty | none (Calm) · a little (Straight-talking, Warm, Co-founder) · plenty (Witty, Bestie) |
| Emoji | none · sometimes | sometimes (Bestie) · none (the others) |
| Welcome line | anything | one that suits the style, e.g. "Morning, {{called}}. What are we working on?" |
| Suggest better ideas | no · yes: if you see a better way than what I asked for, say so briefly, after doing what I asked | yes (Straight-talking, Co-founder) · no (the others) |
| Thinking partner | no · yes: help me think things through, ask the question that sharpens the idea | yes (Co-founder) · no (the others) |
| Motivator | no · yes: notice progress, keep me going when things stall, remind me what I'm working towards | yes (Warm, Bestie, Co-founder) · no (the others) |
| Rules just for me | anything | none |

### Write the personality
Write 5–10 lines into `{{personality}}` in `AGENTS.md`: the name, the style in a sentence, each setting in plain words, and these lines, word for word: "Always do exactly what was asked first. Suggestions come after, never instead." and "Your personality never overrides the vault's rules. You still flag contradictions, check your work, and never agree with something untrue to be nice." Also fill `{{welcome line}}` and `{{agent rules}}` ("None yet." if they gave none). Add the assistant to `System/Assistants.md`, with `{{agent job}}` set to "general help" for now.

Read the personality back and ask if it sounds right.

---

## Part 3: About them

| # | Ask | Save to |
|---|---|---|
| ★3.1 | "In a sentence or two, what do you do? Work, study, running a home, all of it counts." | `Things My Assistant Should Know` → What I do |
| ★3.2 | "What will you mostly use me for?" | `Things My Assistant Should Know` → What I'll mostly use you for. Also update "What it's for" in `System/Assistants.md` |
| ★3.3 | "Where do you work from: home, an office, both, or on the move?" | `My Places` |
| 3.4 | For each place: "Roughly where is it? A town or area is enough, no full address needed. Which days are you there? Anything useful to know, like parking or who's there?" | `My Places` table |
| 3.5 | "Which time zone are you in?" (suggest one from 3.4) | `My Places`, `Settings` |
| 3.6 | "Which tools do you use every day? Email, calendar, apps?" | `Things My Assistant Should Know` → Tools |
| 3.7 | "Anything about your situation I should keep in mind when helping? Your schedule, accessibility, family, anything at all." | `Things My Assistant Should Know` → Keep in mind |
| ★3.8 | "How do you like information: bullet points or paragraphs? And do you want one recommendation, or a few options?" | `How I Work` → How I like information |
| 3.9 | "When do you work best, and how do you like to plan? Lists, deadlines, blocks of time?" | `How I Work` |
| 3.10 | "What slows you down or frustrates you when you're working?" | `How I Work` |
| ★3.11 | "What do you want me to be for you? An assistant, a partner, a coach, a sounding board?" | `Working With My Assistant` |
| 3.12 | "What can I just do without asking, and what should I always check with you first?" | `Working With My Assistant` |
| 3.13 | "When I disagree, or have bad news, how do you want to hear it?" | `Working With My Assistant` |
| 3.14 | "Is there anything you never want me to do?" | `Working With My Assistant` → Never |
| 3.15 | "What are you working towards this year? And in the next 90 days?" | `My Goals` |

**Go deeper:** working hours, best and worst times of day, hobbies and interests, dates that matter, how they like to be motivated, what a good week looks like.

---

## Part 4: How they communicate

| # | Ask | Save to |
|---|---|---|
| 4.1 | "Which tones do you write in? For example professional, friendly, casual. Anything else?" | `Writing Voice`: one `## ` heading per tone |
| 4.2 | For each tone: "Could you paste one to three messages you've written in this tone? Please take out other people's names and personal details first." | under that tone, trimmed to about 150 words each |
| 4.3 | "How do you usually open and sign off?" | under each tone |
| 4.4 | "Any words or phrases you love, or never use?" | `Writing Voice` |
| ★4.5 | "Where do you communicate? Email, Slack, Microsoft Teams, WhatsApp, text, LinkedIn, Instagram or Facebook, phone? Anything else?" | `Communication`: one `## ` heading per channel |
| 4.6 | For each channel, suggest a setting and let them keep or change it, e.g. "Email: professional, short paragraphs, no emoji, 'Kind regards'". | `Communication` |
| 4.7 | "Does it change depending on who you're talking to? Clients, your team, friends?" | `Communication` |

After the samples, write a one-line description of each tone above its examples (e.g. "Short sentences, warm opener, no exclamation marks") and ask them to confirm it. In `Communication`, point each channel at a tone with a link like `[[Writing Voice#Professional]]`.

**Go deeper:** how quickly they reply on each channel, which channel for what (urgent or not), an email signature, out-of-office wording.

---

## Part 5: Their people (optional)

| # | Ask | Save to |
|---|---|---|
| 5.1 | "Who will you mention most? Just their name and who they are to you, e.g. 'Mum', 'Sam, my business partner'." | a folder each in `People/`, from the Person template, listed in `People.md` |
| 5.2 | "Anything I should know about any of them?" (one person at a time, optional) | that person's note |

Use the name they use ("Mum"), with other names as aliases.

**Go deeper, per person:** how they keep in touch (channel and tone), birthdays and dates, what they like, what they're working on together.

---

## Part 6: Business pack

| # | Ask | Save to |
|---|---|---|
| ★6.1 | "Do you run, or work on, a business? Or more than one?" | if no, skip to Part 7 |
| ★6.2 | "What's it called, and in one line, what does it do and who is it for?" | **First business:** copy all of `templates/packs/business/` into the vault. **Any later business:** copy only `Businesses/{{Business}}/`, and add a line for it to `Businesses.md` (never copy `Businesses.md` again). Use the business name for `{{Business}}`. Fill `{{Business one line}}`, `{{what it does}}`, `{{who for}}`. Add it to `Home.md` (see below) |
| 6.3 | "Is it an idea, just starting, or up and running?" | `{{stage}}` |
| 6.4 | "Where is it based: an office, a shop, a studio, your home, or online only?" (suggest one of the places from 3.3 if it fits) | `{{where based}}`; also `My Places` if it's one of their places |
| 6.5 | "What do you sell, and roughly what do you charge? (Optional)" | `<Business> Pricing` |
| 6.6 | "Who's your ideal client?" (start from what they said in 6.2, and ask what to add) | `<Business> Ideal Client` |
| 6.7 | "Any key or favourite clients? Names are enough for now." | a note each in `Clients/`, from the Client template, listed in `<Business> Clients` |
| 6.8 | "Who's on the team, and what do they do?" | each person in `People/`, listed with their role in `<Business> Team` |
| 6.9 | "Where do you market it? Website, Instagram, email, word of mouth? And how should the business sound on each one?" (suggest a tone from `Writing Voice` for each) | `<Business> Channels` table, and `{{business style}}` pointing at those tones |
| 6.10 | "Any rules for the business? Things to always or never do or say?" Suggest starting with: draft only until they say otherwise, and never make a final decision without them. | `{{business rules}}` (or "- No special rules yet."). Always add this line too: "Learn as you go: note every change they ask for, and what they like and don't, in `<Business> Likes and Dislikes`. When a pattern is clear, suggest an SOP." |
| 6.11 | "What are your main tools and suppliers?" (suggest the tools from 3.6 that are for work) | `<Business> Suppliers & Tools` |
| 6.12 | "Another business?" | repeat 6.2–6.11 |

**Adding a business to Home.** The first time, add this section to `Home.md`, straight after the Projects section:

```markdown
## Businesses
Every business, each with the same layout. Go here for anything about clients, pricing, marketing, finance or the team.
- [[Businesses]]
```

Then, for each business, add underneath it:

```markdown
### <Business>
<the one line from 6.2>. Go here for anything about <Business>.
- [[<Business>]] · [[<Business> Clients]] · [[<Business> Marketing]] · [[<Business> Finance]] · [[<Business> Team]]
```

Copy the Business pack's `Templates & SOPs/Note Templates/Client.md` into the vault's Note Templates folder (once), and add it to `Templates & SOPs.md`.

**Go deeper:** brand colours and fonts, an elevator pitch, competitors, budget and targets, the sales process, opening hours, questions customers often ask.

---

## Part 7: Templates & SOPs

Explain in one line: "Templates are ready-to-fill documents. SOPs are step-by-step guides for things you do the same way every time."

| # | Ask | Then |
|---|---|---|
| 7.1 | "Want some ready-made templates? Meeting notes, email reply, follow-up email, weekly plan, and a monthly budget guide." If they have a business, add: "For your business: a proposal, a welcome email, a client onboarding guide, a social post, and an invoice reminder." "Pick any, or none. Anything else?" | copy the chosen ones from `templates/starter-templates/` (see below). The client onboarding guide uses the welcome email, so if they pick onboarding, add the welcome email too, and say so |
| 7.2 | "Is there anything you do the same way every time that I should write up as an SOP? Just describe it, and I'll write it up for you to check." | write it as its own file in the right `SOPs/` folder, with the same details at the top as the starter SOPs (summary, type, used in, status, last confirmed, check every), and list it both ways |
| 7.3 | "Do you already have templates or process documents? You can drop them in the Inbox, or tell me where they are." | via the Inbox |

Where they go:
- `General/…` → `Templates & SOPs/General/Templates/` or `…/SOPs/`, listed under `## General` in `Templates & SOPs.md`.
- `Business/…` → `Templates & SOPs/<Business>/<Area>/Templates/` or `…/SOPs/`, with `{{Business}}` filled in. List each one under a `## <Business>` heading in `Templates & SOPs.md`, **and** under "Templates and SOPs for this area" in every note in its "used in".
- Only create folders that end up holding something.

---

## Part 8: Keeping it healthy

| # | Ask | Save to `Settings` |
|---|---|---|
| ★8.1 | "How often should I check that the facts in your vault are still true? Every 6 weeks, every 6 months, or something else?" | Truth Check |
| 8.2 | "How often should I tidy up the links and contents lists? Weekly, monthly, or every 6 weeks?" (suggest monthly) | Tidy the Map |
| 8.3 | "Would you like a weekly review, to look back at the week and plan the next? Weekly, fortnightly, or not at all?" (suggest weekly) | Weekly Review |
| 8.4 | "When should we go through the things I wasn't sure about? With the weekly review, daily, or weekly?" (suggest with the weekly review, or weekly if they said no to a weekly review) | Review Queue |

Backup Check: monthly, unless they chose Obsidian Sync or iCloud/OneDrive (then every 3 months). Anything skipped gets the suggested default.

---

## Part 9: Bring in what they have (optional)

★ Ask: "Do you have any notes, documents, or memory from another AI that you'd like me to bring in? If so, where are they?" If yes, follow `System/Routines/Import.md`. If it's a lot, offer to do it in a later chat.

---

## Part 10: Finish

1. Make sure no `{{...}}` gaps are left in the vault or the assistant's `AGENTS.md` (apart from the ones listed under "Never replace").
2. Run the checker: `python3 "<vault path>/System/Tools/vault_check.py"`. Fix anything it finds, then run it again until it says "All good". Without Python, check the main notes and links by reading them.
3. Open the vault in Obsidian (Mac: `open "obsidian://open?path=<vault path>"`, Windows: `start "" "obsidian://open?path=<vault path>"`, with the path written for a web address). If Obsidian asks, they should choose to trust the vault.
4. If Templates wasn't switched on in Part 1, ask them to switch it on: Obsidian → Settings → Core plugins → Templates.
5. Ask: "Which one to three things matter most this week?" Put those in the **Now** section of `Tasks.md`, so the first chat doesn't start with an empty list.
6. Set `Setup` in `Settings` to "done".
7. Show this guide, filled in, as one screen:

   > **You're all set.** Here's how to use {{agent name}}:
   > - **To start:** open your assistant app in `{{agent folder}}`. That's where I live.
   > - **Adding something new:** put it in the Inbox in Obsidian. I'll file it at your first chat each day.
   > - **One chat per topic.** When the subject changes, start a fresh chat.
   > - **Say "bye" when you're done,** and I'll save anything important.
   > - **Just ask for:** "weekly review", "truth check", "tidy the map", "go through To Review", "make a new assistant", "update the kit".
   > - **Change anything any time:** "be more blunt", "run the truth check every 6 months", "add a business".
   > - **You can always add more detail.** Just tell me.

8. Then, in the new personality, say the welcome line.
