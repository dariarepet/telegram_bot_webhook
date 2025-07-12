import os
import asyncio
from flask import Flask, request
from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Обработчики

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📝 Заявка на пробное", url="https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e")],
        [InlineKeyboardButton("📚 Абонементы", url="https://daria-emelianova.yonote.ru/share/abonement")],
        [InlineKeyboardButton("👩‍🏫 Обо мне", url="https://daria-emelianova.yonote.ru/share/rus")],
        [InlineKeyboardButton("🎓 Я репетитор", url="https://daria-emelianova.yonote.ru/share/kabinet")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "👋 Привет! Я бот Дарьи Емельяновой.\nВыберите нужный пункт ниже:", reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    username = user.username or user.first_name or "Пользователь"

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Вопрос от @{username} (id {user.id}):\n\n{text}",
    )
    await update.message.reply_text("✅ Вопрос отправлен. Я скоро отвечу!")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    asyncio.run(application.process_update(update))
    return "ok"

@app.route("/")
def index():
    return "Бот работает!"

# Регистрируем хендлеры
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

def set_webhook():
    asyncio.run(bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}"))

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

