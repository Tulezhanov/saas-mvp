from flask import Flask, render_template, request, jsonify
from database import init_db, get_all_leads, save_lead
import sqlite3 import os

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

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)