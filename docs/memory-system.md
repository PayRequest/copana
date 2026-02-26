# The Memory System

Copana's memory is structured markdown files. No database, no embeddings, no vector store. Just text files that both you and your AI can read and edit.

## Why Markdown?

- **Human-readable.** Open any file and understand it instantly.
- **Version-controlled.** Git tracks every change. Roll back anytime.
- **Portable.** No lock-in. Move to a different AI tool if you want.
- **Editable.** Fix mistakes, add context, reorganize.
- **Simple.** No infrastructure to maintain.

## File Roles

### memory.md — The Brain

The central memory file. Contains:

- **Core Facts** — Permanent knowledge (your name, job, family, etc.)
- **Open Loops** — Things to follow up on
- **Recent Decisions** — Important choices for consistency
- **Session Log** — What happened in recent sessions

Your AI reads this every session to maintain continuity.

### user.md — About You

Everything the AI learns about you. Filled in over time through conversation:
- Background and skills
- Personality traits
- Goals and motivations
- Work style

### preferences.md — Quick Lookup

One-liners about your preferences:
- Communication style
- Tool preferences
- Work habits
- Life philosophy

### tasks.md — What's Active

Simple task tracking:
```markdown
- [ ] Write blog post about X #work
- [ ] Call dentist #personal due:2026-03-01
- [x] Set up Copana (2026-02-26)
```

### insights.md — Strategy

Advice given, lessons learned, ideas backlog, and follow-ups. This is your AI's strategic memory.

### routines.md — Patterns

Your daily/weekly routines, observed over time. Helps the AI know when to nudge, when to leave you alone.

### contacts.md — People

Important people with context. Your AI references this when someone comes up in conversation.

### journal.md — Reflections

Daily notes and reflections. Can be written by you or by the AI's daily reflection script.

## How Memory Grows

### Session 1
```
user.md:
- Name: Alex
- Timezone: America/New_York
```

### Session 5
```
user.md:
- Name: Alex
- Timezone: America/New_York
- Work: Software engineer at a startup
- Enjoys: Running, cooking
- Hates: Meetings
```

### Session 20
```
user.md:
- Name: Alex
- Timezone: America/New_York
- Work: Software engineer at CloudCo (since 2024)
- Stack: Python, FastAPI, PostgreSQL
- Side project: Building a habit tracker app
- Enjoys: Running (training for half marathon), cooking (Italian food)
- Hates: Meetings, long Slack threads
- Morning routine: Coffee, run, then work
- Goal: Launch side project by Q2
```

## Memory Maintenance

The AI handles most maintenance automatically:
- Adds new facts as it learns them
- Updates outdated information
- Moves completed tasks
- Clears resolved open loops

You can also:
- Edit any file directly
- Delete incorrect information
- Reorganize sections
- Archive old session logs to `memory/archive/`

## Tips

- Keep `memory.md` concise — it's read every session
- Archive session logs older than 2 weeks
- Review `user.md` occasionally — is it accurate?
- Use `insights.md` for things you want the AI to remember long-term
