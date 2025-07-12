import os
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Например: https://kabinet-rus-bot.onrender.com

app = Flask(__name__)
bot = Bot(token=TOKEN)

application = ApplicationBuilder().token(TOKEN).build()

@app.route("/")
def index():
    return "Бот запущен!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook_handler():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Я бот Дарьи Емельяновой. Чем могу помочь?")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    # Можно отправить админу сообщение с ником и текстом
    admin_chat_id = int(os.getenv("ADMIN_CHAT_ID", "123456789"))  # вставь свой id сюда
    await context.bot.send_message(
        chat_id=admin_chat_id,
        text=f"📩 Сообщение от @{user.username or user.first_name}:\n\n{text}"
    )
    await update.message.reply_text("Ваш вопрос отправлен. Я скоро отвечу ✨")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

# Установка webhook при старте приложения
async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

asyncio.run(set_webhook())
