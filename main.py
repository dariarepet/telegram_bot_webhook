import os
from flask import Flask, request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
)
import asyncio

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Главное меню с кнопками
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("ℹ️ Обо мне", url="https://daria-emelianova.yonote.ru/share/rus")],
        [InlineKeyboardButton("📝 Записаться на пробное", url="https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e")],
        [InlineKeyboardButton("💳 Абонементы", url="https://daria-emelianova.yonote.ru/share/abonement")],
        [InlineKeyboardButton("🎓 Я репетитор, хочу курс", url="https://daria-emelianova.yonote.ru/share/kabinet")],
        [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")]
    ]
    return InlineKeyboardMarkup(keyboard)

@app.route("/")
def index():
    return "Бот работает!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

# Команда /start — приветствие и меню
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Я бот Дарьи Емельяновой. Чем могу помочь?",
        reply_markup=main_menu_keyboard()
    )

# Обработка нажатия кнопки "Задать вопрос"
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "ask_question":
        await query.message.reply_text("Пожалуйста, напишите свой вопрос прямо тут, я передам его Дарье.")
        # Следующее сообщение от пользователя обработаем отдельно

# Обработка сообщений (вопросы)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = user.username or user.first_name or "Пользователь"
    # Отправляем вопрос администратору
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Вопрос от @{username} (id {user.id}):\n\n{text}"
    )
    await update.message.reply_text("Спасибо! Ваш вопрос отправлен. Я скоро отвечу ✨")

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button_handler))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    asyncio.run(set_webhook())
    # Запускаем Flask приложение
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

