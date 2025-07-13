import logging
import os
from config import BOT_TOKEN
from action_handler import button_handler, start
from image_handler import handle_image
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, filters, MessageHandler


os.makedirs("user_images", exist_ok=True)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.run_webhook(
        listen="0.0.0.0",
        port=8443,
        webhook_url=os.getenv("WEBHOOK_URL")
    )
