import os
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

if __name__ == '__main__':
    load_dotenv()  
    
    app = Application.builder().token(os.getenv("TG_KEY")).build()
    
    app.add_handler(MessageHandler(filters.TEXT, echo))
    
    app.run_polling()
py