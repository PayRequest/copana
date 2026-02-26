# Contributing to Copana

## The Rule: Don't Add Features. Add Skills.

If you want to add Telegram support, don't create a PR that adds Telegram alongside everything else. Instead, contribute a skill file (`.claude/skills/add-telegram/SKILL.md`) that teaches Claude Code how to transform a Copana installation to use Telegram.

Users then run `/add-telegram` on their setup and get clean code that does exactly what they need — not a bloated system trying to support every use case.

## What Goes in the Base Repo

Only these types of changes are accepted to the core:

- **Security fixes**
- **Bug fixes**
- **Clear improvements** to existing template files
- **Documentation improvements**
- **New skill files** (the preferred way to add capabilities)

Everything else — new integrations, new automation scripts, new file types, platform support — should be contributed as skills.

## How to Contribute a Skill

1. Create a directory: `.claude/skills/your-skill-name/`
2. Write a `SKILL.md` that teaches Claude how to make the changes
3. Include clear steps, code examples, and which files to modify
4. Submit a PR

### Good skill examples

- `/add-slack` — Add Slack notifications
- `/add-obsidian` — Sync with Obsidian vault
- `/add-calendar` — Calendar integration via AppleScript
- `/add-language-learning` — Language practice and tracking
- `/add-investment-tracker` — Portfolio tracking in markdown

### Skill file format

```markdown
# /skill-name — Short Description

What this skill does in one line.

## Steps

1. What to ask the user
2. What files to create
3. What existing files to modify
4. How to test it works

## Code examples

Include snippets for any code that needs to be added.
```

## How to Submit

1. Fork the repo
2. Create a branch: `git checkout -b add-skill-name`
3. Add your skill to `.claude/skills/`
4. Test: clone a fresh copy, run `/setup`, then run your skill
5. Submit a PR

## Guidelines

- **Keep it simple.** If it needs Docker or a build step, rethink it.
- **Plain text first.** Markdown files are the core.
- **Privacy matters.** Never add telemetry or external data sharing.
- **Test the flow.** Run `/setup` on a clean clone, then your skill.
- **Document clearly.** Your SKILL.md should be understandable by Claude Code.

## Code Style

- Python: Follow PEP 8, keep scripts under 200 lines
- Shell: Use bash, keep it POSIX-compatible where possible
- Markdown: Keep templates clean and well-commented

## RFS (Request for Skills)

Skills we'd like to see:

**Integrations**
- `/add-slack` — Slack notifications
- `/add-discord` — Discord bot
- `/add-signal` — Signal messaging
- `/add-obsidian` — Obsidian vault sync
- `/add-notion-import` — Import from Notion

**Tracking**
- `/add-habits` — Habit tracking with streaks
- `/add-reading-list` — Book/article tracking
- `/add-investment-tracker` — Portfolio tracking
- `/add-language-learning` — Language practice

**Automations**
- `/add-email-digest` — Email summary via AppleScript/IMAP
- `/add-calendar-sync` — Calendar integration
- `/add-git-standup` — Auto-generate standups from git history

## Questions?

Open an issue or start a discussion on GitHub.
