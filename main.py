import os
import telebot
from telebot import types

# وەرگرتنی تۆکن لە متغیڕی ژینگەیی Railway
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# لیستی پرسیارەکان
questions = [
    {
        "text": "خێرایی ڕووناكی لە بۆشاییدا چەندە؟",
        "options": ["٣٠٠ هەزار کم/چ", "١٥٠ هەزار کم/چ", "١ ملیۆن کم/چ"],
        "answer": 0,
    },
    {
        "text": "کاسەی جیهانی تۆپی پێ هەموان چەند ساڵ جارێک ئەنجام دەدرێت؟",
        "options": ["٢ ساڵ", "٣ ساڵ", "٤ ساڵ"],
        "answer": 2,
    },
    {
        "text": "گەورەترین هەسارە لە کۆمەڵەی خۆردا کامەیە؟",
        "options": ["مەریخ", "موشتەری (جوپیتەر)", "زووحەل"],
        "answer": 1,
    },
    {
        "text": "پایتەختی وڵاتی ژاپۆن کوێیە؟",
        "options": ["سیئۆل", "پەکین", "تۆکیۆ"],
        "answer": 2,
    },
    {
        "text": "درێژترین ڕووبار لە جیهاندا کامەیە؟",
        "options": ["ڕووباری نیل", "ڕووباری ئامازۆن", "ڕووباری میسیپسی"],
        "answer": 0,
    },
]

user_data = {}


@bot.message_handler(commands=["start"])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"score": 0, "current_q": 0}

    markup = types.InlineKeyboardMarkup()
    start_btn = types.InlineKeyboardButton(
        "دەستپێکردنی یاری 🎮", callback_data="start_game"
    )
    markup.add(start_btn)

    bot.send_message(
        chat_id,
        "بەخێربێیت بۆ یاری پرسیار و وەڵام! 🧠\nبۆ دەستپێکردن پەنجە بنێ بە دوگمەی خوارەوە:",
        reply_markup=markup,
    )


def send_question(chat_id):
    q_index = user_data[chat_id]["current_q"]

    if q_index < len(questions):
        q = questions[q_index]
        markup = types.InlineKeyboardMarkup()

        for idx, option in enumerate(q["options"]):
            btn = types.InlineKeyboardButton(
                option, callback_data=f"ans_{idx}"
            )
            markup.add(btn)

        bot.send_message(
            chat_id,
            f"پرسیاری {q_index + 1}:\n{q['text']}",
            reply_markup=markup,
        )
    else:
        score = user_data[chat_id]["score"]
        total = len(questions)
        bot.send_message(
            chat_id,
            f"یارییەکە تەواو بوو! 🎉\nئەنجامەکەت: {score} لە {total}",
        )


@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id

    if call.data == "start_game":
        user_data[chat_id] = {"score": 0, "current_q": 0}
        send_question(chat_id)
        return

    if call.data.startswith("ans_"):
        selected_option = int(call.data.split("_")[1])
        q_index = user_data[chat_id]["current_q"]

        if selected_option == questions[q_index]["answer"]:
            user_data[chat_id]["score"] += 1
            bot.answer_callback_query(
                call.id, "وەڵامەکەت ڕاستە! 👏", show_alert=False
            )
        else:
            bot.answer_callback_query(
                call.id, "وەڵامەکەت هەڵەیە! ❌", show_alert=False
            )

        user_data[chat_id]["current_q"] += 1
        send_question(chat_id)


# دەستپێکردنی بۆت
if __name__ == "__main__":
    bot.infinity_polling()
