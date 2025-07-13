import logging
import time
from telegram import Update
from telegram.ext import ContextTypes
from image_processing import process_image

logger = logging.getLogger(__name__)

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_image"):
        await update.message.reply_text("Сначала выберите режим через /start.")
        return

    photo = update.message.photo[-1]

    if len(update.message.photo) > 1:
        await update.message.reply_text("Вы отправили несколько изображений. " \
        "Самое большое из них будет обработано")

    file = await context.bot.get_file(photo.file_id)

    user_id = update.message.from_user.id
    timestamp = int(time.time())
    input_path = f"user_images/{user_id}_{timestamp}.jpg"
    await file.download_to_drive(input_path)
    logger.debug(f"file was downloaded to {input_path}")
    await update.message.reply_text("Изображение получено! Идёт обработка...")

    try:
        result_path = process_image(input_path)
        with open(result_path, 'rb') as result_image:
            await update.message.reply_photo(result_image, caption="Вот улучшенное изображение!")

    except Exception as e:
        await update.message.reply_text(f"Ошибка при обработке: {e}")

    await update.message.reply_text("Изображение получено! Идёт обработка...")
    context.user_data["waiting_for_image"] = False
