#!/usr/bin/env python3
"""
Copana Telegram Bot — Talk to your AI via Telegram.

A simple bot that:
- Responds to messages with AI-powered context
- Loads your memory files for context
- Handles evening check-in callbacks
- Only responds to your messages (security)

Usage:
    python3 telegram_bot.py

Set these in .env:
    TELEGRAM_BOT_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id
    TELEGRAM_ALLOWED_USER=your_telegram_username
    ANTHROPIC_API_KEY=your_key
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from collections import deque

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

sys.path.insert(0, str(Path(__file__).parent))
from copana_utils import COPANA_DIR, load_context, call_ai, log

# Config
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ALLOWED_USER = os.getenv('TELEGRAM_ALLOWED_USER', '')
CHECKIN_LOG = COPANA_DIR / 'logs' / 'checkins.json'

# Conversation memory
CONVERSATIONS = {}
MAX_MEMORY = 10

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


def get_system_prompt():
    """Build system prompt from context files."""
    context = load_context(['memory.md', 'tasks.md', 'user.md', 'preferences.md'])

    prompt = """You are a personal AI assistant responding via Telegram.
Be brief (Telegram messages should be short). Be direct. No fluff.

Here's your context:
"""
    for filename, content in context.items():
        # Truncate each file to keep prompt manageable
        prompt += f"\n--- {filename} ---\n{content[:1500]}\n"

    return prompt


def handle_message(user_id: int, username: str, text: str) -> str:
    """Handle an incoming message and return response."""
    # Security: only respond to allowed user
    if ALLOWED_USER and username != ALLOWED_USER:
        return None

    # Get conversation history
    if user_id not in CONVERSATIONS:
        CONVERSATIONS[user_id] = deque(maxlen=MAX_MEMORY)

    history = list(CONVERSATIONS[user_id])

    # Build messages for AI
    messages = []
    for msg in history:
        messages.append(msg)
    messages.append({"role": "user", "content": text})

    # Call AI
    system = get_system_prompt()
    response = call_ai(
        prompt=text,
        system=system,
        max_tokens=500,
    )

    # Save to memory
    CONVERSATIONS[user_id].append({"role": "user", "content": text})
    CONVERSATIONS[user_id].append({"role": "assistant", "content": response})

    return response


def handle_checkin_callback(data: str) -> str:
    """Handle evening check-in button presses."""
    checkins = []
    if CHECKIN_LOG.exists():
        try:
            checkins = json.loads(CHECKIN_LOG.read_text())
        except (json.JSONDecodeError, Exception):
            checkins = []

    today = datetime.now().strftime('%Y-%m-%d')

    # Find or create today's entry
    today_entry = None
    for entry in checkins:
        if entry.get('date') == today:
            today_entry = entry
            break

    if not today_entry:
        today_entry = {'date': today}
        checkins.append(today_entry)

    # Parse callback
    if data.startswith('energy_'):
        today_entry['energy'] = data.replace('energy_', '')
        response = "Got it. How was your mood today?"
    elif data.startswith('mood_'):
        today_entry['mood'] = data.replace('mood_', '')
        response = "Logged. Rest well."
    else:
        response = "Noted."

    # Save
    CHECKIN_LOG.parent.mkdir(exist_ok=True)
    CHECKIN_LOG.write_text(json.dumps(checkins, indent=2))

    return response


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
            "Hey! I'm your Copana AI assistant on Telegram. Just message me."
        )

    async def on_message(update: Update, context):
        user = update.effective_user
        response = handle_message(user.id, user.username, update.message.text)
        if response:
            await update.message.reply_text(response)

    async def on_callback(update: Update, context):
        query = update.callback_query
        await query.answer()
        response = handle_checkin_callback(query.data)
        await query.edit_message_text(text=response)

    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_message))
    app.add_handler(CallbackQueryHandler(on_callback))

    log("Telegram bot starting...", "telegram_bot.log")
    app.run_polling()


if __name__ == '__main__':
    main()
