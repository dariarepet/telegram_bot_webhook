import os
import asyncio
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

bot = Bot(token=TOKEN)

async def main():
    await bot.set_webhook(f"{WEBHOOK_URL}/{TOKEN}")
    print("Webhook установлен!")

if __name__ == "__main__":
    asyncio.run(main())
