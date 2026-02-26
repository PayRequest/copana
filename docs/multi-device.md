# Multi-Device Setup

Use Copana from your Mac (Claude Code) and your phone (Claude app + GitHub).

## How It Works

Your AI's memory lives in a git repo. Push/pull keeps everything in sync.

```
Mac (Claude Code)  ←→  GitHub  ←→  Mobile (Claude app)
```

## Mac Setup

This is your primary device. Claude Code reads the files directly.

```bash
cd /path/to/copana
claude
```

At end of session, sync:
```bash
./scripts/session_end.sh
```

## Mobile Setup

### Option 1: Claude.ai App + GitHub

1. Push your repo to GitHub (private recommended)
2. Open Claude.ai on your phone
3. Reference your repo in conversations
4. For quick updates, edit files directly on GitHub mobile

### Option 2: Telegram Bot

Run the Telegram bot on your Mac:
```bash
python3 scripts/telegram_bot.py
```

Then chat with your AI on Telegram from any device. The bot has access to all your context files.

### Option 3: Quick Capture

For capturing thoughts on the go without full AI context:
1. Use GitHub mobile app to edit `tasks.md` or `memory.md` directly
2. Or use a note-taking app and process later

## Sync Protocol

1. **Before starting on Mac:** `git pull` (get mobile changes)
2. **After session on Mac:** `./scripts/session_end.sh` (push changes)
3. **On mobile:** Changes go through GitHub commits

The AI checks `git status` at startup and notes any changes since last session.

## Conflict Resolution

If both devices edit the same file:
- Git merge usually handles it fine (different sections)
- If conflicts arise, resolve on Mac (easier in terminal)
- Memory files rarely conflict — they append, not overwrite
