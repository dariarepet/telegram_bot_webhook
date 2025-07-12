import os
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID"))

app = Flask(__name__)
bot = Bot(token=TOKEN)
application = ApplicationBuilder().token(TOKEN).build()

# Кнопки с твоими ссылками
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("📚 Абонементы", url="https://daria-emelianova.yonote.ru/share/abonement")],
        [InlineKeyboardButton("👩‍🏫 Обо мне", url="https://daria-emelianova.yonote.ru/share/rus")],
        [InlineKeyboardButton("🎓 Курс для репетитора", url="https://daria-emelianova.yonote.ru/share/kabinet")],
        [InlineKeyboardButton("📝 Заявка на пробное", url="https://forms.yandex.ru/u/683ad41feb61464bc78c1b3e/")],
    ]
    return InlineKeyboardMarkup(keyboard)

@app.route("/")
def index():
    return "Бот работает!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, bot)
    await application.process_update(update)
    return "ok"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "👋 Я бот Дарьи Емельяновой. Чем могу помочь?"
    await update.message.reply_text(text, reply_markup=get_main_keyboard())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    username = user.username or user.first_name or "Пользователь"
    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📩 Вопрос от @{username} (id {user.id}):\n\n{text}"
    )
    await update.message.reply_text("Ваш вопрос отправлен. Я скоро отвечу ✨")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    import asyncio
    asyncio.run(bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}"))


