import os
import telebot
from telebot import types

TOKEN = "8216477256:AAFqWGKVlpqHAMiKJQen3uC_LzvrQBE3hU0"
bot = telebot.TeleBot(TOKEN)

# لیستی پرسیارەکان
questions = [
    {
        "text": "❓ **پرسیاری ١:** خێرایی ڕۆیشتنی ڕووناکی لە بۆشاییدا چەندە؟",
        "options": ["٣٠٠ هەزار کم/چ", "١٥٠ هەزار کم/چ", "١ ملیۆن کم/چ"],
        "answer": 0,
    },
    {
        "text": "❓ **پرسیاری ٢:** جامی جیهانی تۆپی پێ هەموو چەند ساڵ جارێک ئەنجام دەدرێت؟",
        "options": ["٢ ساڵ", "٣ ساڵ", "٤ ساڵ"],
        "answer": 2,
    },
    {
        "text": "❓ **پرسیاری ٣:** گەورەترین هەسارە لە کۆمەڵەی خۆردا کامەیە؟",
        "options": ["زوحەل", "مۆشتەری (جۆپیتەر)", "مەریخ"],
        "answer": 1,
    },
]

user_data = {}


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
  chat_id = message.chat.id
  user_data[chat_id] = {"score": 0, "current_q": 0}

  markup = types.InlineKeyboardMarkup()
  btn = types.InlineKeyboardButton(
      "🚀 دەستپێکردنی یاری", callback_data="start_game"
  )
  markup.add(btn)

  photo_url = "https://images.unsplash.com/photo-1606326608606-aa0b62935f2b?w=800"

  try:
    bot.send_photo(
        chat_id,
        photo_url,
        caption=(
            "🎮 **بەخێر هاتیت بۆ یاری مێشکی!**\n\nئامادەبیت بۆ تاقیکردنەوەی"
            " زانیارییەکانت؟"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )
  except Exception as e:
    bot.send_message(
        chat_id,
        "🎮 **بەخێر هاتیت بۆ یاری مێشکی!**\n\nئامادەبیت بۆ تاقیکردنەوەی"
        " زانیارییەکانت؟",
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.callback_query_handler(
    func=lambda call: call.data == "start_game" or call.data.startswith("ans_")
)
def handle_game(call):
  chat_id = call.message.chat.id
  message_id = call.message.message_id

  if chat_id not in user_data:
    user_data[chat_id] = {"score": 0, "current_q": 0}

  data = user_data[chat_id]

  if call.data.startswith("ans_"):
    selected_option = int(call.data.split("_")[1])
    current_q_index = data["current_q"]

    if selected_option == questions[current_q_index]["answer"]:
      data["score"] += 1

    data["current_q"] += 1

  if data["current_q"] < len(questions):
    q_index = data["current_q"]
    q_data = questions[q_index]

    markup = types.InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(q_data["options"]):
      markup.add(
          types.InlineKeyboardButton(option, callback_data=f"ans_{i}")
      )

    try:
      bot.edit_message_text(
          chat_id=chat_id,
          message_id=message_id,
          text=f"🎯 **پرسیاری {q_index + 1} لە {len(questions)}**\n\n{q_data['text']}",
          reply_markup=markup,
          parse_mode="Markdown",
      )
    except Exception:
      bot.send_message(
          chat_id=chat_id,
          text=f"🎯 **پرسیاری {q_index + 1} لە {len(questions)}**\n\n{q_data['text']}",
          reply_markup=markup,
          parse_mode="Markdown",
      )
  else:
    score = data["score"]
    total = len(questions)

    result_text = (
        f"🏆 **یارییەکە کۆتایی هات! دەستخۆش!**\n\n👤 ئەنجامەکەت: **{score}** لە"
        f" **{total}**\n⭐ ڕێژەی سەرکەوتن: {(score/total)*100:.0f}%\n\nدەتەوێت"
        " دیسان یاری بکەیتەوە؟"
    )

    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            "🔄 دووبارە یاریکردنەوە", callback_data="start_game"
        )
    )

    try:
      bot.edit_message_text(
          chat_id=chat_id,
          message_id=message_id,
          text=result_text,
          reply_markup=markup,
          parse_mode="Markdown",
      )
    except Exception:
      bot.send_message(
          chat_id=chat_id,
          text=result_text,
          reply_markup=markup,
          parse_mode="Markdown",
      )


# بەکارهێنانی رێگەیەک کە پێشوەختە وەڵامی کۆن دەسڕێتەوە ئەگەر هەبێت
bot.remove_webhook()
bot.infinity_polling()
