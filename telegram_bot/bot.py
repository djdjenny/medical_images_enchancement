import logging
import os
import torch
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, filters, MessageHandler

from action_handler import button_handler, start
from config import BOT_TOKEN
from image_handler import handle_image
from model import UNetGenerator, UNetSkipConnectionLayer


os.makedirs("user_images", exist_ok=True)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


torch.serialization.add_safe_globals({
    'UNetGenerator': UNetGenerator,
    'UNetSkipConnectionLayer': UNetSkipConnectionLayer
})


def main() -> None:
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.run_webhook(
        listen="0.0.0.0",
        port=8443,
        webhook_url=os.getenv("WEBHOOK_URL")
    )  

if __name__ == '__main__':
    main()
