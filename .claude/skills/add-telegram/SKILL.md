# /add-telegram — Add Telegram Bot

Set up a Telegram bot so the user can chat with their AI on mobile.

## Steps

1. **Check prerequisites:**
   - `python3` available
   - `scripts/requirements.txt` dependencies installed (if not, install them)

2. **Guide bot creation:**
   - Tell user to message @BotFather on Telegram
   - Create a new bot and get the token
   - Message the bot once, then get chat ID:
     ```bash
     curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | python3 -c "import sys,json; print(json.load(sys.stdin)['result'][0]['message']['chat']['id'])"
     ```

3. **Configure .env:**
   - Set `TELEGRAM_BOT_TOKEN=<token>`
   - Set `TELEGRAM_CHAT_ID=<chat_id>`
   - Set `TELEGRAM_ALLOWED_USER=<username>` (security)

4. **Test the bot:**
   ```bash
   python3 scripts/telegram_bot.py &
   ```
   Send a test message via Telegram.

5. **Set up persistent running** (optional):
   - Create a tmux session: `tmux new -s copana-bot`
   - Run: `python3 scripts/telegram_bot.py`
   - Detach: Ctrl+B, D
   - Or suggest launchd/systemd for auto-start

6. **Enable automation scripts** that use Telegram:
   - Morning briefing, proactive pings, evening check-in
   - Add cron jobs from `scripts/crontab.example`
