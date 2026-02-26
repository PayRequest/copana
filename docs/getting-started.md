# Getting Started

## Prerequisites

- [Claude Code](https://claude.ai/code) installed
- Git
- A terminal (macOS, Linux, or WSL)

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/PayRequest/copana.git my-ai
cd my-ai
```

### 2. Run setup

```bash
./setup.sh
```

This asks you:
- **Your name** — so the AI knows what to call you
- **AI name** — what you want to call your AI (default: Copana)
- **Timezone** — for time-aware features
- **Vibe** — casual buddy, professional partner, or tough coach

Setup replaces all template placeholders and creates your first git commit.

### 3. Start using it

```bash
claude
```

Your AI will:
1. Read its memory files (memory.md, tasks.md, etc.)
2. Check git status for changes
3. Get the current time
4. Start working — no "how can I help?" prompt

### 4. Have a conversation

Just talk naturally. Your AI will:
- Remember what you tell it across sessions
- Capture facts about you silently (in user.md, preferences.md)
- Follow up on things you mentioned
- Track tasks and open loops

### 5. End a session

Your AI will update memory files. To sync to git:

```bash
./scripts/session_end.sh
```

Or just ask your AI to commit.

## Optional: Automations

Want proactive nudges, morning briefings, or a Telegram bot?

```bash
pip install -r scripts/requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

See [automation.md](automation.md) for the full setup.

## Optional: Mobile Access

Want to chat with your AI on your phone?

See [multi-device.md](multi-device.md) for sync setup.

## Tips

- **Read your files.** Open memory.md, user.md, etc. to see what your AI has learned.
- **Edit freely.** These are your files. Correct mistakes, add context, delete stuff.
- **Commit often.** Git history = version control for your AI's memory.
- **Be yourself.** The more natural you are, the better your AI learns.
