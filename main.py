import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, CallbackQueryHandler, filters
)
import asyncio

# Переменные окружения
TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

app = Flask(__name__)
application = ApplicationBuilder().token(TOKEN).build()

# Главная страница
@app.route("/")
def index():
    return "Бот работает!"

# Обработка входящих обновлений от Telegram
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📚 Абонементы", url="https://daria-emelianova.yonote.ru/share/abonement")],
        [InlineKeyboardButton("👩‍🏫 Обо мне", url="https://daria-emelianova.yonote.ru/share/rus")],
        [InlineKeyboardButton("🎓 Курс для репетитора", url="https://daria-emelianova.yonote.ru/share/kabinet")],
        [InlineKeyboardButton("📝 Пробное занятие", url="https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Я бот Дарьи Емельяновой. Чем могу помочь?", reply_markup=reply_markup)

# Обработка обычных сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = user.username or user.first_name or "Пользователь"

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Вопрос от @{username} (id {user.id}):\n\n{text}"
    )
    await update.message.reply_text("Ваш вопрос отправлен. Я скоро отвечу ✨")

# Обработчики
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Установка вебхука
async def set_webhook():
    await application.bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

# Запуск вебхука и Flask-сервера
if __name__ == "__main__":
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

