# Copana

**Personal AI, powered by markdown.**

A personal AI assistant that actually knows you. No app, no server, no Docker. Just markdown files + Claude Code.

Copana gives your AI persistent memory, personality, and proactive behavior — all stored as plain text files you can read, edit, and own.

[copana.ai](https://copana.ai) · ~14k tokens · 7% of context window

---

## Why I Built This

I built a personal AI assistant for myself called Sloosbot. It runs in Claude Code, stores everything in markdown files, and actually knows me — my goals, my patterns, my open tasks, my preferences. After a month of use it felt like having a co-founder who never forgets anything.

The problem: it was tightly coupled to my life. Hardcoded names, personal scripts, specific integrations.

So I extracted the framework. Copana is the generalized version — everything that made Sloosbot useful, packaged so anyone can have the same experience in 30 seconds.

No Docker, no server, no build step. Just `git clone` and go.

---

## Quick Start

```bash
git clone https://github.com/PayRequest/copana.git
cd copana
claude
```

Then run `/setup`. Claude handles everything: names, timezone, personality, first commit.

Or use the shell script: `./setup.sh`

---

## What Makes Copana Different

Most AI tools forget you the moment you close the tab. Copana doesn't.

- **It remembers.** Your goals, preferences, and open tasks persist across sessions.
- **It learns.** Every conversation teaches it something about you — silently captured in markdown.
- **It follows up.** Open loops don't just sit there. Your AI checks back.
- **It thinks ahead.** Proactive nudges, daily reflections, and pattern recognition.
- **You own it.** Plain markdown files, version-controlled with git. No lock-in.

---

## How It Works

Copana is a **template repository** for [Claude Code](https://claude.ai/code). When you run `claude` in this directory, Claude reads `CLAUDE.md` automatically — your AI's instructions, startup ritual, and behavior rules.

```
copana/
├── CLAUDE.md              # AI instructions (auto-read by Claude Code)
├── soul.md                # AI identity & values
├── personality.md         # How the AI talks
├── user.md                # About you (AI fills this in over time)
├── preferences.md         # Your likes/dislikes
├── memory.md              # Long-term memory & session log
├── tasks.md               # Active tasks
├── insights.md            # Strategy & follow-ups
├── routines.md            # Your daily patterns
├── contacts.md            # Important people
├── projects.md            # Bigger initiatives
├── journal.md             # Daily reflections
├── .claude/
│   ├── settings.json      # Status line config
│   ├── agents/            # Custom subagents (memory-manager, research, daily-review)
│   ├── output-styles/     # Personality as output style
│   └── skills/            # Setup, customize, add-telegram, etc.
├── scripts/               # Optional automations
└── docs/                  # Full documentation
```

### The Memory System

Your AI maintains structured context across sessions:

| File | What it stores | Updated by |
|------|---------------|------------|
| `memory.md` | Core facts, open loops, decisions, session log | AI (every session) |
| `user.md` | Who you are — background, goals, personality | AI (learns over time) |
| `preferences.md` | Quick-lookup likes, dislikes, work style | AI (captures silently) |
| `tasks.md` | Active tasks, completed items | You + AI |
| `insights.md` | Advice given, lessons learned, follow-ups | AI |
| `routines.md` | Your daily/weekly patterns | AI (observes over time) |
| `contacts.md` | People in your life with context | AI (as they come up) |

Every file is plain markdown. Read it, edit it, version it, delete it. You're always in control.

### Startup Ritual

Every session, your AI automatically:

1. Reads `memory.md`, `tasks.md`, `insights.md` for context
2. Checks `git status` for changes since last session
3. Gets the current time
4. Starts working — no "how can I help?" filler

This is what makes Copana different from a fresh AI conversation. Your AI picks up exactly where you left off.

### Active Learning

Your AI silently captures information about you during conversations:

- You mention you hate phone calls → saved to `preferences.md`
- You talk about a friend → saved to `contacts.md`
- You describe your morning routine → saved to `routines.md`
- You share a life goal → saved to `user.md`

No prompting needed. It just listens and learns.

---

## Skills

Copana uses Claude Code skills for extensibility. Instead of bloated features, skills teach Claude how to transform your setup.

### Built-in skills

| Skill | What it does |
|-------|-------------|
| `/setup` | Interactive first-time setup |
| `/customize` | Guided customization of any aspect |
| `/add-telegram` | Set up Telegram bot for mobile access |
| `/add-fitness` | Add workout tracking and gym accountability |
| `/add-budget` | Add personal budget tracking |
| `/add-agent` | Create a custom subagent |

### Contributing skills

Want to add Slack support? Don't create a PR that adds Slack. Create a skill file (`.claude/skills/add-slack/SKILL.md`) that teaches Claude how to add Slack to any Copana installation. Users run `/add-slack` and get clean, tailored code.

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

---

## Subagents

Copana ships with specialized Claude Code subagents that handle background work:

| Agent | What it does | Model |
|-------|-------------|-------|
| `memory-manager` | Consolidates memory files, removes duplicates, archives old sessions | Haiku (fast) |
| `research` | Web research with structured output, saved to your files | Default |
| `daily-review` | Reviews all files, writes daily summary to journal.md | Haiku (fast) |

Subagents have restricted tool access (e.g., memory-manager can't browse the web) and persistent memory across sessions.

Create your own with `/add-agent` or drop a markdown file in `.claude/agents/`.

---

## Status Line

Copana adds a status line to your Claude Code terminal showing:

- **Open tasks** from tasks.md
- **Open loops** from memory.md
- **Last session** timestamp

Always visible, refreshes every 30 seconds. Configured in `.claude/settings.json`.

---

## Output Style

Copana includes an output style (`.claude/output-styles/copana.md`) that shapes how your AI communicates — direct, casual, no filler. This works alongside `personality.md` to give your AI a consistent voice without bloating `CLAUDE.md`.

---

## Optional: Automation Scripts

Copana works great with just `claude` and markdown files. But if you want proactive behavior between sessions, there are optional automation scripts:

| Script | What it does |
|--------|-------------|
| Morning briefing | Tasks, loops, and an AI nudge to start your day |
| Proactive pings | Smart nudges about stale items (birthdays, overdue tasks) |
| Evening check-in | Quick energy/mood capture via Telegram |
| Daily reflection | AI reviews your files overnight, prepares tomorrow's nudge |
| Weekly review | Patterns, wins, and focus areas |
| News briefing | Relevant news from configurable RSS feeds |
| Telegram bot | Chat with your AI on mobile |

Setup: `pip install -r scripts/requirements.txt` + add API keys to `.env`.

See [docs/automation.md](docs/automation.md) for details.

---

## Multi-Device

Copana syncs via git. Work on your Mac with Claude Code, capture thoughts on mobile via the Claude app + GitHub, and everything stays in sync.

See [docs/multi-device.md](docs/multi-device.md) for setup.

---

## Comparison

| | Copana | NanoClaw | OpenClaw |
|---|--------|----------|----------|
| **Source files** | 50 | 15 | 3,680 |
| **Lines of code** | ~3,600 | ~3,900 | 434,453 |
| **Dependencies** | 5 | <10 | 70 |
| **Config files** | 1 | 0 | 53 |
| **Time to understand** | 8 minutes | 8 minutes | 1–2 weeks |
| **Security model** | OS container isolation | OS container isolation | Application-level checks |
| **Architecture** | Single process + isolated containers | Single process + isolated containers | Single process, shared memory |
| **Setup** | `git clone` + `/setup` | Docker + Node.js | `npm install -g` + onboard wizard |
| **Infrastructure** | None | Container runtime | Node ≥22 |
| **Memory** | Structured markdown (12 files) | Per-group CLAUDE.md | Per-agent sessions |
| **Personality** | `soul.md` + output style | None | None |
| **Personal context** | `user.md` + `preferences.md` | None | Workspace config |
| **Active learning** | Captures facts silently | None | None |
| **Proactive behavior** | Nudges, reflections, briefings | Scheduled tasks | Cron + webhooks |
| **Subagents** | memory-manager, research, daily-review | None | Multi-agent routing |
| **Channels** | CLI + mobile (git sync) | CLI | WhatsApp, Telegram, Slack, Discord, Signal, iMessage + 6 more |
| **Status line** | Open tasks, loops, last session | None | None |
| **Extensibility** | Skills + agents | Skills | Skills + tools + channels |
| **Privacy** | Local files, git-versioned | Container | Local gateway (127.0.0.1) |
| **Token footprint** | ~14k tokens (7% of window) | ~35k tokens (17%) | — |

---

## FAQ

**Do I need Docker?**
No. Copana has zero infrastructure requirements. Just `git clone` and `claude`.

**Does it work with other AI tools besides Claude Code?**
The markdown files work with anything that can read text. The CLAUDE.md instructions and skills are Claude Code specific, but the memory system is portable.

**How much context does it use?**
~14k tokens total (~7% of Claude's context window). Core files read every session are only ~2.6k tokens. Your AI has plenty of room to work.

**Is my data private?**
Everything stays on your machine unless you push to GitHub. No telemetry, no analytics, no cloud processing. Use a private repo for backup.

**Will it slow down Claude Code?**
No. Claude reads markdown files extremely fast. The startup ritual adds 2-3 seconds to read your context files — after that, it's normal Claude Code speed.

**What if my memory files get too big?**
Archive old session logs to `memory/archive/`. Keep `memory.md` focused on current facts and recent sessions. The AI can help with this — just ask it to consolidate.

**Can I use this with the Claude mobile app?**
Yes. Push to a private GitHub repo, then reference your files in Claude.ai conversations. Or use the Telegram bot for a more seamless mobile experience.

**How is this different from just putting instructions in CLAUDE.md?**
Copana is a structured system, not just a prompt. It includes a memory architecture (12 interconnected files), a startup ritual, active learning behaviors, proactive follow-ups, and optional automation scripts. You could build this yourself — Copana saves you the work.

---

## Philosophy

Copana is built on a simple idea: **your AI should know you**.

Not through a proprietary database or a cloud service — through plain text files that you own, stored in a git repo you control.

The best personal AI isn't the smartest model. It's the one with the most context about *you*.

Read more: [docs/philosophy.md](docs/philosophy.md)

---

## Contributing

Don't add features. Add skills.

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — do whatever you want with it.

---

Built by [PayRequest](https://payrequest.io). Powered by [Claude Code](https://claude.ai/code).
