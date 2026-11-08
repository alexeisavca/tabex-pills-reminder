import os
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

tabex_schedule = {
    1: (2.0, 6),
    2: (2.0, 6),
    3: (2.0, 6),
    4: (2.5, 5),
    5: (2.5, 5),
    6: (2.5, 5),
    7: (2.5, 5),
    8: (2.5, 5),
    9: (2.5, 5),
    10: (2.5, 5),
    11: (3.0, 4),
    12: (3.0, 4),
    13: (3.0, 4),
    14: (3.0, 4),
    15: (3.0, 4),
    16: (5.0, 3),
    17: (5.0, 3),
    18: (5.0, 3),
    19: (5.0, 3),
    20: (5.0, 3),
    21: (7.0, 2),
    22: (7.0, 2),
    23: (7.0, 2),
    24: (7.0, 2),
    25: (7.0, 2),
}

pill_taken_event = asyncio.Event()
load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")

async def tabex_loop(app: Application):
    while True:
        await app.bot.send_message(
            chat_id=CHAT_ID,
            text="Ia pastila",
        )

        await pill_taken_event.wait()
        pill_taken_event.clear()

async def on_post_init(app: Application):
    asyncio.create_task(tabex_loop(app))

async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pill_taken_event.set()

if __name__ == '__main__':
    app = Application.builder().token(os.getenv("TG_KEY")).build()
    
    app.add_handler(MessageHandler(filters.TEXT, on_msg))

    app.post_init = on_post_init
    
    app.run_polling()
