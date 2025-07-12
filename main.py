import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters
)

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Пример: https://kabinet-rus-bot.onrender.com

app = Flask(__name__)
bot = Bot(token=TOKEN)

@app.route("/")
def index():
    return "Бот запущен!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook_handler():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

# Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Я бот Дарьи Емельяновой. Чем могу помочь?")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ваш вопрос отправлен. Я скоро отвечу ✨")

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Установка Webhook
async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

import asyncio
asyncio.run(set_webhook())
