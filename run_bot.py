import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from database import init_db, save_lead

load_dotenv()
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(F.text)
    async def handle_message(message: Message):
        name = message.from_user.first_name
        text = message.text
        contact = str(message.from_user.id)
        save_lead("telegram", name, contact, text)
        print(f"Сохранено: [{name}] {text}")
        await message.answer(
            "Ваша заявка принята!\n"
            "Мы свяжемся с вами в ближайшее время."
        )

    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    init_db()
    asyncio.run(start_bot())