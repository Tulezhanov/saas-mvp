from flask import Flask, render_template, request, jsonify
from database import init_db, get_all_leads, save_lead
import sqlite3
import os
import threading
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
print(f"TOKEN загружен: {TOKEN is not None}")

app = Flask(__name__)
DB_PATH = "db/database.sqlite"

def update_status(lead_id, new_status):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE leads SET status = ? WHERE id = ?",
        (new_status, lead_id)
    )
    conn.commit()
    conn.close()

@app.route("/")
def index():
    leads = get_all_leads()
    return render_template("index.html", leads=leads)

@app.route("/status/<int:lead_id>", methods=["POST"])
def change_status(lead_id):
    new_status = request.json.get("status")
    update_status(lead_id, new_status)
    return jsonify({"ok": True})

@app.route("/test-lead")
def test_lead():
    save_lead("telegram", "Тест", "00000", "Тестовая заявка")
    return "✅ Тестовая заявка добавлена! <a href='/'>Вернуться</a>"

# Telegram бот
async def start_bot():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    @dp.message(F.text)
    async def handle_message(message: Message):
        name = message.from_user.first_name
        text = message.text
        contact = str(message.from_user.id)
        save_lead("telegram", name, contact, text)
        print(f"💾 Сохранено: [{name}] {text}")
        await message.answer(
            "✅ Ваша заявка принята!\n"
            "Мы свяжемся с вами в ближайшее время."
        )

    print("🤖 Бот запущен!")
    await dp.start_polling(bot)

def run_bot():
    asyncio.run(start_bot())

if __name__ == "__main__":
    init_db()
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    # Запускаем веб-панель
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)