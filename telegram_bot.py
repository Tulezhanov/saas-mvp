import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv
from database import init_db, save_lead
import os

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(F.text)
async def handle_message(message: Message):
    name = message.from_user.first_name
    text = message.text
    contact = str(message.from_user.id)

    # Сохраняем заявку в базу данных
    save_lead(
        source="telegram",
        name=name,
        contact=contact,
        message=text
    )

    print(f"💾 Сохранено в базу: [{name}] {text}")

    await message.answer(
        "✅ Ваша заявка принята!\n"
        "Мы свяжемся с вами в ближайшее время."
    )

async def main():
    init_db()  # создаём таблицу при запуске
    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())