# Automation

Optional automations that add proactive behavior between Claude Code sessions.

**None of these are required.** Copana works perfectly with just `claude` and your markdown files.

There are **two approaches** — pick whichever fits you:

| Approach | What you need | Best for |
|----------|--------------|----------|
| **Agent SDK** (`claude -p`) | Claude Code installed | Simple setup, no Python needed |
| **Python scripts** | Python + API key + pip | More customizable, Telegram bot support |

---

## Option A: Agent SDK (Recommended)

Uses Claude Code's built-in `-p` flag to run automations headlessly. No Python, no API keys, no dependencies — just Claude Code.

### How it works

```bash
# Claude reads your memory files, generates a briefing, outputs as JSON
claude -p "Read memory.md and tasks.md. What needs attention today?" \
  --allowedTools "Read,Glob,Grep" \
  --output-format json
```

The agent has full access to your Copana files and context — no need to manually load anything.

### Setup

```bash
crontab -e
```

Add from `scripts/crontab-sdk.example`:

```bash
COPANA_DIR=/path/to/copana

# Morning briefing (7:00 AM)
0 7 * * * cd $COPANA_DIR && claude -p "Read memory.md, tasks.md, and insights.md. Generate a morning briefing: what's due today, overdue items, open loops needing attention, and one motivational nudge. Keep it under 15 lines." --allowedTools "Read,Glob,Grep" --output-format json | jq -r '.result' | curl -s -d @- ntfy.sh/YOUR_TOPIC

# Proactive ping (14:00)
0 14 * * * cd $COPANA_DIR && claude -p "Read tasks.md and memory.md. Find the single most important thing that needs attention right now. Reply in 1-2 sentences." --allowedTools "Read,Glob,Grep" --output-format json | jq -r '.result' | curl -s -d @- ntfy.sh/YOUR_TOPIC

# Daily reflection (23:00)
0 23 * * * cd $COPANA_DIR && claude -p "Review all markdown files. Write a daily reflection to journal.md: tasks completed, open loops status, patterns noticed, suggested focus for tomorrow. Keep it under 10 lines." --allowedTools "Read,Write,Edit,Glob,Grep" --output-format json

# Weekly review (Sunday 20:00)
0 20 * * 0 cd $COPANA_DIR && claude -p "Do a weekly review. Read all files. Summarize what got done, what slipped, patterns, and 3 priorities for next week. Write to journal.md." --allowedTools "Read,Write,Edit,Glob,Grep" --output-format json

# Memory cleanup (Sunday 3:00 AM)
0 3 * * 0 cd $COPANA_DIR && claude -p "Archive session logs older than 7 days from memory.md to memory/archive/. Remove completed tasks older than 2 weeks. Deduplicate entries." --allowedTools "Read,Write,Edit,Glob,Grep" --model haiku --output-format json
```

### Notifications

Pipe the output to your notification channel:

```bash
# ntfy.sh (free, no account)
... --output-format json | jq -r '.result' | curl -s -d @- ntfy.sh/YOUR_TOPIC

# Telegram
... --output-format json | jq -r '.result' | curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" -d "chat_id=$CHAT_ID" -d "text=$(cat -)"
```

### Structured output

Use `--json-schema` to get structured results for further processing:

```bash
claude -p "List all overdue tasks from tasks.md" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"tasks":{"type":"array","items":{"type":"string"}},"count":{"type":"integer"}}}'
```

### Continue conversations

Chain related automations using `--continue`:

```bash
# Morning: run analysis
claude -p "Analyze my tasks and open loops" --allowedTools "Read,Glob,Grep"

# Afternoon: follow up on the same context
claude -p "Any updates on what we discussed this morning?" --continue --allowedTools "Read,Glob,Grep"
```

### Tips

- Use `--model haiku` for simple tasks (faster, cheaper)
- Use `--allowedTools` to restrict what Claude can do (read-only for briefings, read+write for reflections)
- Pipe to `>> logs/cron.log 2>&1` for debugging
- Test with `claude -p "..." --output-format json | jq -r '.result'` before adding to cron

---

## Option B: Python Scripts

More control, more customizable, supports the always-running Telegram bot.

### 1. Install dependencies

```bash
pip install -r scripts/requirements.txt
```

### 2. Configure .env

```bash
cp .env.example .env
```

Edit `.env` with your keys:

```env
# Required for AI-powered scripts
ANTHROPIC_API_KEY=sk-ant-...

# For Telegram notifications
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=your_chat_id

# OR for simple notifications (no account needed)
NTFY_TOPIC=my-copana-abc123
```

### 3. Set up cron

```bash
crontab -e
```

Add from `scripts/crontab.example`:

```cron
# Morning briefing at 7:00 AM
0 7 * * * cd /path/to/copana && python3 scripts/morning_briefing.py

# Proactive pings at 10:00, 14:00, 18:00
0 10,14,18 * * * cd /path/to/copana && python3 scripts/proactive_ping.py

# Evening check-in at 21:30
30 21 * * * cd /path/to/copana && python3 scripts/evening_checkin.py

# Daily reflection at 23:00
0 23 * * * cd /path/to/copana && python3 scripts/daily_reflection.py

# Weekly review Sunday 20:00
0 20 * * 0 cd /path/to/copana && python3 scripts/weekly_review.py
```

## Scripts

### Morning Briefing
Sends a daily summary with:
- Tasks due today and overdue items
- Open loops needing attention
- AI nudge from last night's reflection
- Overnight research summaries

### Proactive Pings
Smart nudges throughout the day about:
- Upcoming birthdays (from contacts.md)
- Overdue tasks
- Stale open loops (> 7 days old)
- General task reminders

Uses deduplication — won't nag about the same thing twice.

### Evening Check-in
Quick mood/energy capture via Telegram buttons. Data feeds into the weekly review for pattern recognition.

### Daily Reflection
Runs overnight. Your AI reviews all memory files to:
- Find stale tasks and forgotten follow-ups
- Identify patterns
- Generate tomorrow's morning nudge
- Write reflection to `memory/reflections/`

### Weekly Review
Sunday summary that analyzes:
- Check-in patterns (energy, mood)
- Tasks completed vs planned
- Open loops status
- Focus suggestions for next week

### News Briefing
Fetches and scores news from RSS feeds. Customize feeds in the script or via `NEWS_FEEDS` env var.

### Telegram Bot
Always-running bot for chatting with your AI on mobile. Uses your context files for personalized responses.

```bash
# Run in background (tmux recommended)
python3 scripts/telegram_bot.py
```

## Notification Channels

Scripts support two channels:

1. **Telegram** — Rich formatting, inline buttons, full bot support
2. **ntfy.sh** — Simple push notifications, no account needed

Configure one in `.env`. If neither is set, output goes to stdout only.

### Setting up Telegram

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot, get the token
3. Message your bot, then find your chat ID:
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Add both to `.env`

### Setting up ntfy

1. Pick a random topic name (e.g., `copana-abc123`)
2. Add `NTFY_TOPIC=copana-abc123` to `.env`
3. Install the ntfy app on your phone
4. Subscribe to your topic
