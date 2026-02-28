# Copana Scripts

Optional automations that add proactive behavior between Claude Code sessions.

**None of these are required.** Copana works great with just `claude` and your markdown files.

## Two Approaches

### Agent SDK (`claude -p`) — Recommended

No Python, no API keys, no pip. Just cron + Claude Code:

```bash
# Example: morning briefing
claude -p "Read memory.md and tasks.md. What needs attention today?" \
  --allowedTools "Read,Glob,Grep" --output-format json | jq -r '.result'
```

See `crontab-sdk.example` for a full schedule.

### Python Scripts

More customizable, supports the always-running Telegram bot.

```bash
pip install -r requirements.txt
```

Add your API keys to `.env` (copy from `.env.example`).

## Cron Examples

| File | Approach |
|------|----------|
| `crontab-sdk.example` | Agent SDK — `claude -p` commands |
| `crontab.example` | Python scripts |

Edit with `crontab -e`.

## Python Scripts

| Script | What it does | When to run |
|--------|-------------|-------------|
| `morning_briefing.py` | Summary of tasks, loops, nudges | Daily, 7:00 AM |
| `proactive_ping.py` | Smart nudges about stale items | 2-3x/day |
| `evening_checkin.py` | Quick mood/energy check-in | Daily, 21:30 |
| `daily_reflection.py` | AI reviews your files overnight | Daily, 23:00 |
| `weekly_review.py` | Week-in-review with patterns | Sunday, 20:00 |
| `news_briefing.py` | Relevant news from RSS feeds | Daily or on-demand |
| `telegram_bot.py` | Chat with your AI via Telegram | Always running |
| `session_end.sh` | Git commit memory changes | End of each session |

## Shared Utilities

`copana_utils.py` provides:
- `send_notification()` — Telegram or ntfy.sh
- `call_ai()` — Claude API wrapper
- `load_context()` — Load markdown files
- `get_open_loops()` / `get_pending_tasks()` — Parse memory files
- `log()` — Timestamped logging
- `save_data()` / `load_data()` — JSON data persistence

## Notifications

Both approaches support notifications:

**Agent SDK:** Pipe output to ntfy or Telegram via curl (see crontab-sdk.example).

**Python scripts:** Configure in `.env`:
1. **Telegram** — Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`
2. **ntfy.sh** — Set `NTFY_TOPIC` (free, no account needed)

If neither is configured, output goes to stdout only.
