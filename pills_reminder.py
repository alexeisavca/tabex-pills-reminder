import os
import asyncio
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from datetime import date, datetime, timedelta, time

tabex_schedule = [
    (2.0, 6),
    (2.0, 6),
    (2.0, 6),
    (2.5, 5),
    (2.5, 5),
    (2.5, 5),
    (2.5, 5),
    (2.5, 5),
    (2.5, 5),
    (2.5, 5),
    (3.0, 4),
    (3.0, 4),
    (3.0, 4),
    (3.0, 4),
    (3.0, 4),
    (5.0, 3),
    (5.0, 3),
    (5.0, 3),
    (5.0, 3),
    (5.0, 3),
    (7.0, 2),
    (7.0, 2),
    (7.0, 2),
    (7.0, 2),
    (7.0, 2),
]

pill_taken_event = asyncio.Event()
load_dotenv()
CHAT_ID = os.getenv("CHAT_ID")

def persist_state(state):
    with open("state.json", "w") as f:
        json.dump(state, f, indent=4)

testing = True

async def sleep_until(target: datetime):
    if testing:
         await asyncio.to_thread(input, "Enter something: ")
         return
    
    while datetime.now() < target:
        await asyncio.sleep(60)

async def tabex_loop(app: Application):
    while True:
        with open("state.json", "r") as f:
            state = json.load(f)

        start_date = date.fromisoformat(state["start_date"])

        if start_date > date.today():
            print("Start date in the future, sleeping until 6am that day")
            await sleep_until(datetime.combine(start_date, time(6, 0)))

        last_pill_at = None if state["last_pill_at"] is None else datetime.fromisoformat(state["last_pill_at"])

        if last_pill_at and last_pill_at.date() < date.today():
            state["last_pill_at"] = None
            state["pills_total"] = 0
            persist_state(state)
            continue

        days_since_start = (date.today() - start_date).days
        interval, max = tabex_schedule[days_since_start]

        if state["pills_total"] >= max:
            print("All done for today, sleeping until 6am tomorrow")
            await sleep_until(
                datetime.combine(date.today() + timedelta(days=1), time(6, 0))
            )
            continue

        if last_pill_at:
            await sleep_until(last_pill_at + timedelta(hours=interval))
        else: 
            await sleep_until(datetime.combine(date.today(), time(6, 0)))
        
        await app.bot.send_message(
            chat_id=CHAT_ID,
            text=f'Ziua {days_since_start+1}. Ia pastila {state["pills_total"] + 1}/{max}',
        )

        await pill_taken_event.wait()
        pill_taken_event.clear()

        state["pills_total"] += 1
        state["last_pill_at"] = datetime.now().isoformat()
        persist_state(state)

async def on_post_init(app: Application):
    asyncio.create_task(tabex_loop(app))

async def on_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pill_taken_event.set()

if __name__ == '__main__':
    app = Application.builder().token(os.getenv("TG_KEY")).build()
    
    app.add_handler(MessageHandler(filters.TEXT, on_msg))

    app.post_init = on_post_init
    
    app.run_polling()
