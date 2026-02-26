#!/usr/bin/env python3
"""
Evening Check-in — Quick mood/energy capture.

Sends a notification with buttons for a quick daily check-in.
Responses are logged for weekly review patterns.

Runs at ~21:30 via cron.
"""

import os
import sys
import asyncio
from pathlib import Path
from datetime import datetime

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / '.env')

sys.path.insert(0, str(Path(__file__).parent))
from copana_utils import COPANA_DIR, send_notification, log

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')


def send_checkin_telegram():
    """Send evening check-in with Telegram buttons."""
    try:
        from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

        async def _send():
            bot = Bot(token=TELEGRAM_TOKEN)
            keyboard = [
                [
                    InlineKeyboardButton("High", callback_data="energy_high"),
                    InlineKeyboardButton("Medium", callback_data="energy_medium"),
                    InlineKeyboardButton("Low", callback_data="energy_low"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text="Evening check-in!\n\nHow's your energy level?",
                reply_markup=reply_markup,
            )

        asyncio.run(_send())
        return True
    except ImportError:
        return False


def main():
    log("Sending evening check-in...", "evening_checkin.log")

    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID:
        if send_checkin_telegram():
            log("Check-in sent via Telegram!", "evening_checkin.log")
            return

    # Fallback: simple notification
    if send_notification("Evening check-in! How's your energy? (High / Medium / Low)"):
        log("Check-in sent!", "evening_checkin.log")
    else:
        log("No notification channel configured", "evening_checkin.log")


if __name__ == '__main__':
    main()
