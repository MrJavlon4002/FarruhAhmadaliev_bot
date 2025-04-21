import pandas as pd
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ConversationHandler, CallbackQueryHandler, filters
)

# Define states for the conversation
LANGUAGE, NAME, CONTACT, REASON = range(4)

token = "7972827522:AAEAN2s_f8PmAGDx2QJtNgHaaF5F-c3yF0U"

# Store user data
user_data = {}

# Start command handler
async def start(update: Update, context):
    user = update.message.from_user
    welcome_message = (
        "Assalomu aleykum, bu Farruh Akhmadalievning shaxsiy boti, bu orqali siz muallif bilan bog’lanish, "
        "mavjud loyhalarga yozilish yoki fikrlaringizni yetkansangiz bo’ladi\n\n"
        "Здравствуйте, это персональный бот Фарруха Ахмадалиева, через который вы можете связаться с автором, "
        "записаться на доступные курсы или поделиться своими мыслями."
    )
    
    keyboard = [[InlineKeyboardButton("\ud83c\uddfa\ud83c\uddff Uz", callback_data="uz"), InlineKeyboardButton("\ud83c\uddf7\ud83c\uddfa Ru", callback_data="ru")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message + "\n\nIltimos, tilni tanlang / Пожалуйста, выберите язык:", reply_markup=reply_markup)
    return LANGUAGE

# Language selection handler
async def language(update: Update, context):
    query = update.callback_query
    await query.answer()
    lang = query.data
    user_data[query.from_user.id] = {"language": lang}
    
    if lang == "uz":
        await query.edit_message_text("Ismingiz nima?")
    else:
        await query.edit_message_text("Как вас зовут?")
    
    return NAME

# Name handler
async def name(update: Update, context):
    user_id = update.message.from_user.id
    user_data[user_id]["name"] = update.message.text
    
    lang = user_data[user_id]["language"]
    keyboard = [[KeyboardButton("📞 Kontaktni ulashish" if lang == "uz" else "📞 Поделиться контактом", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    
    if lang == "uz":
        await update.message.reply_text("Iltimos, kontakt ma’lumotlaringizni yuboring:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Пожалуйста, отправьте ваш контакт:", reply_markup=reply_markup)
    
    return CONTACT

# Contact handler
async def contact(update: Update, context):
    user_id = update.message.from_user.id
    user_data[user_id]["contact"] = update.message.contact.phone_number
    
    lang = user_data[user_id]["language"]
    if lang == "uz":
        await update.message.reply_text("Loyhaga qiziqishingizga nima sabab bo’ldi?")
    else:
        await update.message.reply_text("Что заставило вас заинтересоваться этим курсом?")
    
    return REASON

# Reason handler with Excel saving
async def reason(update: Update, context):
    user_id = update.message.from_user.id
    user_info = user_data[user_id]
    user_info["reason"] = update.message.text

    # Save data to Excel
    file_path = "user_data.xlsx"
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
    else:
        df = pd.DataFrame(columns=["User ID", "Language", "Name", "Contact", "Reason"])
    
    new_data = pd.DataFrame([{ "User ID": user_id, "Language": user_info["language"], "Name": user_info["name"], "Contact": str(user_info["contact"]), "Reason": user_info["reason"] }])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(file_path, index=False)

    lang = user_info["language"]

    video_path = "moves.mp4"

    post = (
        """
🎯 TREYDING BO‘YICHA LOYIHA — 10 OYLIK TO‘LIQ DASTUR  

📆 5 oy ta’lim + 5 oy savdo amaliyoti  
📚 Video materiallar + PDF + Telegram hamjamiyat  
🔐 Bir martalik to‘lov — cheksiz kirish

---

Assalomu alaykum!  
Bu loyiha — *treydingni mutlaqo noldan boshlab*, strategiya tuzish va real bozor amaliyotigacha olib boradigan **10 oylik tizimli yo‘l xaritasi**.

---

📘 Dastur ikki bosqichdan iborat:  
1️⃣ **Ta’lim (5 oy):**  
• Asosiy tushunchalar, MT4 platformasi  
• Trend, daraja, TVX, texnik tahlil  
• 4 ta strategiya: Trend Box, Scalping, Round Numbers, Darvos  
• Savdo rejalari, kundalik yuritish

2️⃣ **Amaliyot (5 oy):**  
✅ Telegram guruhda haftalik tahlil  
✅ Mentorlik, topshiriqlar, feedback  
✅ Guruh ichida savdo qilgan holda tajriba to‘plash  
✅ Mualliflik indikatorlari bilan ishlash

---

🎓 Loyiha natijasida siz:  
• Mustahkam bilim olasiz  
• O‘z strategiyangizni yaratib, real savdoga chiqasiz  
• Hamjamiyatda savdo qilish tajribasini orttirasiz

📩 Batafsil ma’lumot: @username
"""

    ) if lang == "uz" else (
        """
🎯 ТРЕЙДИНГ-ПРОЕКТ НА 10 МЕСЯЦЕВ — С НУЛЯ ДО РЕЗУЛЬТАТА  

📆 5 месяцев обучения + 5 месяцев торговли  
📚 Видео + PDF + Telegram-сообщество  
🔐 Один платёж — бессрочный доступ

---

Привет!  
Этот проект — это **полноценный путь длиной в 10 месяцев**: от теории и стратегий до реальной торговли в сообществе.

---

📘 Структура проекта:  
1️⃣ **Обучение (5 месяцев):**  
• Основы трейдинга, платформа MT4  
• Теханализ, тренды, уровни, точки входа  
• 4 стратегии: Trend Box, Scalping, Round Numbers, Darvas  
• Планирование, трейдерский дневник

2️⃣ **Практика (5 месяцев):**  
✅ Торговля в Telegram-группе  
✅ Еженедельный анализ и поддержка  
✅ Авторские индикаторы и сигналы  
✅ Менторство и обратная связь

---

🎓 Что получите:  
• Прочные знания и личная стратегия  
• Опыт торговли с наставником  
• Уверенность на реальном рынке

📩 Подробности: @username
"""


    )

    keyboard = [[InlineKeyboardButton("Loyhaga qo'shilish" if lang == "uz" else "Присоединиться к курсу", url="https://t.me/+mY2YxrLP5WM4Yjdi")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Send video with caption and inline button
    await update.message.reply_video(video=open(video_path, "rb"), caption=post, parse_mode="Markdown", reply_markup=reply_markup)

    return ConversationHandler.END



async def cancel(update: Update, context):
    await update.message.reply_text("Bekor qilindi / Отменено")
    return ConversationHandler.END


# Main function to run the bot
def main():
    app = ApplicationBuilder().token(token).build()
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANGUAGE: [CallbackQueryHandler(language)],
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            CONTACT: [MessageHandler(filters.CONTACT, contact)],
            REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, reason)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    
    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
