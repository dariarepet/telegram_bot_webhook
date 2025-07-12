import os
from flask import Flask, request
from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

app = Flask(__name__)
bot = Bot(token=TOKEN)

application = ApplicationBuilder().token(TOKEN).build()

# Кнопки с ссылками
keyboard = [
    [InlineKeyboardButton("ℹ️ Обо мне", url="https://daria-emelianova.yonote.ru/share/rus")],
    [InlineKeyboardButton("📝 Записаться на пробное", url="https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e")],
    [InlineKeyboardButton("💳 Абонементы", url="https://daria-emelianova.yonote.ru/share/abonement")],
    [InlineKeyboardButton("🎓 Курс для репетиторов", url="https://daria-emelianova.yonote.ru/share/kabinet")],
    [InlineKeyboardButton("❓ Задать вопрос", callback_data="ask_question")]
]
reply_markup = InlineKeyboardMarkup(keyboard)

@app.route("/")
def index():
    return "Бот работает!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Я бот Дарьи Емельяновой. Чем могу помочь?", reply_markup=reply_markup
    )

async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text(
        "Пожалуйста, напишите ваш вопрос прямо сюда, и я перешлю его Дарье."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = user.username or user.first_name or "Пользователь"
    # Отправляем вопрос в админский чат с ником и айди
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Вопрос от @{username} (id {user.id}):\n\n{text}"
    )
    await update.message.reply_text("Ваш вопрос отправлен. Я скоро отвечу ✨")

application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(ask_question, pattern="ask_question"))
application.add_handler(MessageHandler(~filters.COMMAND & filters.TEXT, handle_message))

async def set_webhook():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(set_webhook())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

