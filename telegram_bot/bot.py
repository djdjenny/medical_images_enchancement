
from config import BOT_TOKEN
from action_handler import button_handler, start
from image_handler import handle_image
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler


if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()
