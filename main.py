import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# API Token هەمان ئەوەی لە BotFather وەرگرتووە
TOKEN = "8216477256:AAFqWGKVLpqHAMiKJQen3uC_LzvrQBE3Ug4"
bot = telebot.TeleBot(TOKEN)

# لیستێک لە پرسیارەکان
questions = [
    {
        "q": "خێرایی ڕۆیشتنی ڕووناکی لە بۆشاییدا چەندە؟",
        "options": ["٣٠٠ هەزار کم/چ", "١٥٠ هەزار کم/چ", "١ ملیۆن کم/چ"],
        "correct": 0
    },
    {
        "q": "جامی جیهانی تۆپی پێ هەموو چەند ساڵ جارێک ئەنجام دەدرێت؟",
        "options": ["٢ ساڵ", "٣ ساڵ", "٤ ساڵ"],
        "correct": 2
    },
    {
        "q": "گەورەترین هەسارە لە کۆمەڵەی خۆردا کامەیە؟",
        "options": ["زوحەل", "مۆشتەری", "مەریخ"],
        "correct": 1
    }
]

# کاتێک بەکارهێنەر دەستپێک (Start) دادەگرێت
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = InlineKeyboardMarkup()
    btn = InlineKeyboardButton("🎮 دەستپێکردنی یاری", callback_data="start_game_0")
    markup.add(btn)
    
    welcome_text = (
        f"سڵاو {message.from_user.first_name}!\n\n"
        "بەخێر بێیت بۆ یاری مێشکی! 🧠\n"
        "بە وەڵامدانەوەی پرسیارەکان خاڵ کۆبکەرەوە و ببەرەوە."
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

# بەڕێوەبردنی وەڵامەکان
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    data = call.data
    
    if data.startswith("start_game_"):
        q_index = int(data.split("_")[2])
        show_question(call.message.chat.id, call.message.message_id, q_index)
        
    elif data.startswith("ans_"):
        parts = data.split("_")
        q_index = int(parts[1])
        ans_index = int(parts[2])
        
        if ans_index == questions[q_index]["correct"]:
            bot.answer_callback_query(call.id, "ئافەرین! وەڵامەکەت ڕاستە. 🎉", show_alert=True)
        else:
            bot.answer_callback_query(call.id, "بەداخەوە! وەڵامەکەت هەڵەیە. ❌", show_alert=True)
            
        next_q = q_index + 1
        if next_q < len(questions):
            show_question(call.message.chat.id, call.message.message_id, next_q)
        else:
            bot.send_message(call.message.chat.id, "یارییەکە کۆتایی پێهات! دەستخۆش 🏆")

def show_question(chat_id, message_id, q_index):
    q_data = questions[q_index]
    markup = InlineKeyboardMarkup()
    
    for i, option in enumerate(q_data["options"]):
        btn = InlineKeyboardButton(option, callback_data=f"ans_{q_index}_{i}")
        markup.add(btn)
        
    bot.send_message(chat_id, f"پرسیاری {q_index + 1}:\n{q_data['q']}", reply_markup=markup)

bot.polling()
