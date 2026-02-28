#!/usr/bin/env python3
"""
Copana Telegram Bot — Agent SDK Edition.

Uses `claude -p` instead of direct API calls. This gives the bot:
- Full CLAUDE.md context (startup ritual, personality, rules)
- Access to all memory files automatically
- Conversation continuity via --resume
- Same tools as interactive Claude Code (Read, Write, Grep, etc.)

Dependencies: python-telegram-bot, python-dotenv
No Anthropic API key needed — Claude Code handles auth.

Usage:
    python3 telegram_bot_sdk.py

Set these in .env:
    TELEGRAM_BOT_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id (optional, for notifications)
    TELEGRAM_ALLOWED_USER=your_telegram_username
"""

import os
import sys
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

# Config
COPANA_DIR = Path(__file__).parent.parent
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USER = os.getenv('TELEGRAM_ALLOWED_USER', '')
ALLOWED_TOOLS = os.getenv('TELEGRAM_BOT_TOOLS', 'Read,Glob,Grep,Write,Edit,WebSearch,WebFetch')
SESSION_FILE = COPANA_DIR / 'data' / 'telegram_session.json'
CHECKIN_LOG = COPANA_DIR / 'logs' / 'checkins.json'
LOG_DIR = COPANA_DIR / 'logs'

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def log(message: str):
    """Log with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}"
    logger.info(message)
    LOG_DIR.mkdir(exist_ok=True)
    with open(LOG_DIR / 'telegram_bot.log', 'a') as f:
        f.write(log_line + '\n')


def get_session_id() -> str | None:
    """Get the current session ID for conversation continuity."""
    if SESSION_FILE.exists():
        try:
            data = json.loads(SESSION_FILE.read_text())
            return data.get('session_id')
        except (json.JSONDecodeError, Exception):
            pass
    return None


def save_session_id(session_id: str):
    """Save session ID for conversation continuity."""
    SESSION_FILE.parent.mkdir(exist_ok=True)
    SESSION_FILE.write_text(json.dumps({
        'session_id': session_id,
        'updated': datetime.now().isoformat(),
    }))


def ask_claude(message: str) -> str:
    """Send a message to Claude via the Agent SDK and return the response."""
    cmd = [
        'claude', '-p', message,
        '--allowedTools', ALLOWED_TOOLS,
        '--output-format', 'json',
    ]

    # Resume existing conversation for context continuity
    session_id = get_session_id()
    if session_id:
        cmd.extend(['--resume', session_id])

    try:
        result = subprocess.run(
            cmd,
            cwd=str(COPANA_DIR),
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            error = result.stderr.strip()
            log(f"claude -p error: {error}")

            # Session might be expired, try without --resume
            if session_id and ('session' in error.lower() or 'not found' in error.lower()):
                log("Session expired, starting fresh")
                cmd = [
                    'claude', '-p', message,
                    '--allowedTools', ALLOWED_TOOLS,
                    '--output-format', 'json',
                ]
                result = subprocess.run(
                    cmd,
                    cwd=str(COPANA_DIR),
                    capture_output=True,
                    text=True,
                    timeout=120,
                )
                if result.returncode != 0:
                    return f"Error: {result.stderr.strip()[:200]}"

        # Parse JSON response
        response = json.loads(result.stdout)
        new_session_id = response.get('session_id')
        if new_session_id:
            save_session_id(new_session_id)

        return response.get('result', 'No response from Claude.')

    except subprocess.TimeoutExpired:
        return "Claude took too long to respond. Try a simpler question."
    except json.JSONDecodeError:
        # Fallback: return raw stdout
        if result.stdout.strip():
            return result.stdout.strip()[:4000]
        return "Couldn't parse Claude's response."
    except Exception as e:
        log(f"Error calling claude: {e}")
        return f"Error: {str(e)[:200]}"


def handle_checkin_callback(data: str) -> str:
    """Handle evening check-in button presses."""
    checkins = []
    if CHECKIN_LOG.exists():
        try:
            checkins = json.loads(CHECKIN_LOG.read_text())
        except (json.JSONDecodeError, Exception):
            checkins = []

    today = datetime.now().strftime('%Y-%m-%d')

    today_entry = None
    for entry in checkins:
        if entry.get('date') == today:
            today_entry = entry
            break

    if not today_entry:
        today_entry = {'date': today}
        checkins.append(today_entry)

    if data.startswith('energy_'):
        today_entry['energy'] = data.replace('energy_', '')
        response = "Got it. How was your mood today?"
    elif data.startswith('mood_'):
        today_entry['mood'] = data.replace('mood_', '')
        response = "Logged. Rest well."
    else:
        response = "Noted."

    CHECKIN_LOG.parent.mkdir(exist_ok=True)
    CHECKIN_LOG.write_text(json.dumps(checkins, indent=2))

    return response


def split_message(text: str, max_length: int = 4096) -> list[str]:
    """Split long messages into Telegram-friendly chunks."""
    if len(text) <= max_length:
        return [text]

    chunks = []
    while text:
        if len(text) <= max_length:
            chunks.append(text)
            break
        # Find a good split point (newline or space)
        split_at = text.rfind('\n', 0, max_length)
        if split_at == -1:
            split_at = text.rfind(' ', 0, max_length)
        if split_at == -1:
            split_at = max_length
        chunks.append(text[:split_at])
        text = text[split_at:].lstrip()
    return chunks


def main():
    """Run the Telegram bot using polling."""
    if not TELEGRAM_TOKEN:
        print("Error: TELEGRAM_BOT_TOKEN not set in .env")
        sys.exit(1)

    try:
        from telegram import Update
        from telegram.ext import (
            Application, CommandHandler, MessageHandler,
            CallbackQueryHandler, filters,
        )
    except ImportError:
        print("Install python-telegram-bot: pip install python-telegram-bot")
        sys.exit(1)

    async def start(update: Update, context):
        await update.message.reply_text(
            "Hey! I'm your Copana AI assistant. Powered by Claude Code.\n"
            "Just message me anything."
        )

    async def reset(update: Update, context):
        """Reset conversation — start fresh session."""
        if SESSION_FILE.exists():
            SESSION_FILE.unlink()
        await update.message.reply_text("Conversation reset. Fresh start.")

    async def on_message(update: Update, context):
        user = update.effective_user

        # Security: only respond to allowed user
        if ALLOWED_USER and user.username != ALLOWED_USER:
            return

        # Show typing indicator
        await update.effective_chat.send_action('typing')

        # Get response from Claude
        response = ask_claude(update.message.text)

        # Send response (split if too long for Telegram)
        for chunk in split_message(response):
            await update.message.reply_text(chunk)

    async def on_callback(update: Update, context):
        query = update.callback_query
        await query.answer()
        response = handle_checkin_callback(query.data)
        await query.edit_message_text(text=response)

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    app.add_handler(CallbackQueryHandler(on_callback))

    log("Telegram bot (SDK edition) starting...")
    app.run_polling()


if __name__ == '__main__':
    main()
