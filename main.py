import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# لیستی پرسیارەکان بە زانیاری زیاتر و ڕوونکردنەوە
questions = [
    {
        "q": "🌌 خێرایی رووناكی لە بۆشاییدا چەندە؟",
        "options": ["٣٠٠ هەزار كم/چ", "١ ملیۆن كم/چ", "١٥٠ هەزار كم/چ"],
        "correct": 0,
        "note": "💡 زانیاری: ڕووناكی دەتوانێت لە یەک چركەدا ٧.٥ جار بە دەوری زەویدا بسووڕێتەوە!"
    },
    {
        "q": "🏅 ئۆڵۆمپیادی هاوینە چەند ساڵ جارێک ئەنجام دەدرێت؟",
        "options": ["٢ ساڵ", "٣ ساڵ", "٤ ساڵ"],
        "correct": 2,
        "note": "💡 زانیاری: یەکەم ئۆڵۆمپیادی هاوچەرخ لە ساڵی ١٨٩٦ لە ئەسینا بەڕێوەچوو."
    },
    {
        "q": "🪐 گەورەترین هەسارە لە کۆمەڵەی خۆردا کامەیە؟",
        "options": ["زوحەل", "مشتەری", "مەریخ"],
        "correct": 1,
        "note": "💡 زانیاری: مشتەری ئەوەندە گەورەیە کە زیاتر لە ١,٣٠٠ زەوی لەناو خۆیدا دەگرێت!"
    }
]

user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'score': 0, 'current_q': 0}
    
    welcome_text = (
        "سڵاو! بەخێربێیت بۆ یاری زانیاری گشتی 🧠✨\n\n"
        "ئامادەیت تواناکانت تاقی بکەیتەوە؟ ئاماژە بپێکە و وەڵامی ڕاست هەڵبژێره!"
    )
    bot.send_message(chat_id, welcome_text)
    send_question(chat_id)

def send_question(chat_id):
    q_index = user_data[chat_id]['current_q']
    
    if q_index < len(questions):
        q = questions[q_index]
        markup = InlineKeyboardMarkup()
        
        for idx, option in enumerate(q['options']):
            callback_data = f"ans_{idx}"
            markup.add(InlineKeyboardButton(option, callback_data=callback_data))
            
        bot.send_message(
            chat_id, 
            f"❓ **پرسیاری {q_index + 1} لە {len(questions)}:**\n\n{q['q']}", 
            parse_mode="Markdown", 
            reply_markup=markup
        )
    else:
        show_final_score(chat_id)

def show_final_score(chat_id):
    score = user_data[chat_id]['score']
    total = len(questions)
    
    if score == total:
        feedback = "پیرۆزە! تۆ زیرەکێکی تەواویت! 🏆🔥"
    elif score >= total / 2:
        feedback = "ئاستێکی زۆر باشە! دەستت خۆش بێت 👏"
    else:
        feedback = "کێشە نییە، جارێکی تر تاقی بکەرەوە! 💪"

    msg = (
        f"🏁 **یارییەکە تەواو بوو!**\n\n"
        f"📊 نمرەی تۆ: **{score}** لە **{total}**\n"
        f"💬 {feedback}"
    )
    
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("دووبارەکردنەوە 🔄", callback_data="restart_game"))
    
    bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    
    if call.data == "restart_game":
        user_data[chat_id] = {'score': 0, 'current_q': 0}
        bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
        send_question(chat_id)
        return

    if chat_id not in user_data:
        bot.send_message(chat_id, "تکایە بە /start یارییەکە دەست پێبکەرەوە.")
        return

    q_index = user_data[chat_id]['current_q']
    selected_option = int(call.data.split('_')[1])
    correct_option = questions[q_index]['correct']
    note = questions[q_index]['note']
    
    if selected_option == correct_option:
        user_data[chat_id]['score'] += 1
        bot.answer_callback_query(call.id, "وەڵامەکەت ڕاستە! 🎉")
        result_text = "✅ **وەڵامی ڕاست!**\n" + note
    else:
        bot.answer_callback_query(call.id, "وەڵامەکەت هەڵەیە! ❌")
        result_text = "❌ **وەڵامی هەڵە!**\n" + note

    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=None)
    bot.send_message(chat_id, result_text, parse_mode="Markdown")
    
    user_data[chat_id]['current_q'] += 1
    send_question(chat_id)

bot.infinity_polling()
