from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


keyboard = [[InlineKeyboardButton("Назад", callback_data='back')]]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Режим 1: обработка КТ", callback_data='mode1'),
            InlineKeyboardButton("Режим 2: обработка УЗИ", callback_data='mode2')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
            await update.message.reply_text("Выбери один из режимов:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("Выбери один из режимов:", reply_markup=reply_markup)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'mode1':
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выбран режим 1: обработка КТ. Обработка займет приблизительно N секунд",
                                       reply_markup=reply_markup)
        context.user_data['mode'] = 'mode1'
        context.user_data["waiting_for_image"] = True

    elif query.data == 'mode2':
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text("Выбран режим 2: обработка УЗИ. Режим в разработке.", 
                                       reply_markup=reply_markup)
        context.user_data['mode'] = 'mode2'

    elif query.data == 'back':
        await start(update, context)
        context.user_data['mode'] = None
