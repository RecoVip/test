import telebot
import json
import os
from telebot import types

TOKEN = "7201348044:AAGdcQKMBwuymZ5mpaMOxw83Y4NWS0NUlX8"
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "users.json"

# لو الملف مش موجود ننشئه
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user
    data = load_data()

    data[str(user.id)] = {
        "id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name
    }

    save_data(data)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("📁 رجّع بياناتي")

    bot.send_message(message.chat.id, "✅ تم حفظ بياناتك بنجاح", reply_markup=keyboard)

@bot.message_handler(func=lambda m: m.text == "📁 رجّع بياناتي")
def send_file(message):
    with open(DATA_FILE, "rb") as f:
        bot.send_document(message.chat.id, f)

bot.infinity_polling()
