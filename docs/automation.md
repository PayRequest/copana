# Automation

Optional scripts that add proactive behavior between Claude Code sessions.

**None of these are required.** Copana works perfectly with just `claude` and your markdown files.

## Setup

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
