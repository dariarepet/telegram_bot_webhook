import os
from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Главное меню
keyboard = [
    [KeyboardButton("📚 Обо мне"), KeyboardButton("💳 Абонементы")],
    [KeyboardButton("👩‍🏫 Я репетитор"), KeyboardButton("🎓 Хочу курс")],
    [KeyboardButton("📝 Пробный урок"), KeyboardButton("❓ Задать вопрос")],
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

@app.route("/")
def index():
    return "Бот работает!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

# Старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Я бот Дарьи Емельяновой. Чем могу помочь?\n👇 Выберите нужный пункт:",
        reply_markup=reply_markup
    )

# Обработка кнопок и сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.message.from_user
    username = user.username or user.first_name or "Пользователь"

    if text == "📚 Обо мне":
        await update.message.reply_text("Я Дарья Емельянова, преподаватель русского языка. Готовлю к ОГЭ и ЕГЭ. 🎓")
    elif text == "💳 Абонементы":
        await update.message.reply_text("Урок 45 мин — 1000₽\nАбонемент 4 занятия — 3800₽\n8 занятий — 7200₽.")
    elif text == "👩‍🏫 Я репетитор":
        await update.message.reply_text("Заполните анкету, и я свяжусь с вами. 💼")
    elif text == "🎓 Хочу курс":
        await update.message.reply_text("Выберите курс — базовый, продвинутый или экспресс-подготовка. 📘")
    elif text == "📝 Пробный урок":
        await update.message.reply_text("Оставьте заявку на пробное занятие — напишите свой номер и имя. 📝")
    elif text == "❓ Задать вопрос":
        await update.message.reply_text("Напишите ваш вопрос сюда, и я передам Дарье. ✉️")
    else:
        # Отправка вопроса админу
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=f"📩 Вопрос от @{username} (id {user.id}):\n\n{text}"
        )
        await update.message.reply_text("Ваш вопрос отправлен. Я скоро отвечу ✨")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Установка Webhook
async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

asyncio.run(set_webhook())
