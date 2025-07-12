from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask, request
import os

BOT_TOKEN = "8004644159:AAHpTPScjFTiI45zG7uUbJh4q41xNrLupXU"
MY_TELEGRAM_ID = 1267693167
WEBHOOK_URL = "https://kabinet-rus-bot.onrender.com"

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Я бот Дарьи Емельяновой. Чем могу помочь?")

async def handle_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    msg = f"❓ Вопрос от @{user.username or user.first_name} (ID {user.id}):\n{text}"
    await context.bot.send_message(chat_id=MY_TELEGRAM_ID, text=msg)
    await update.message.reply_text("Спасибо! Дарья скоро ответит.")

application = ApplicationBuilder().token(BOT_TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_question))

@app.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put_nowait(update)
    return "ok"

@app.before_first_request
def setup_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=WEBHOOK_URL)

if __name__ == "__main__":
    app.run(port=10000)
