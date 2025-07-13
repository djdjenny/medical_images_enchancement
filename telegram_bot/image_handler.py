from image_processing import load_model, process_image
from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Изображение получено. Обработка пока недоступна.")


if __name__ == '__main__':
    MODEL_PATH = 'C:\Studying\DLS\GAN.pt'
    TEST_IMAGE = 'C:\Studying\DLS\1213.png'

    model = load_model(MODEL_PATH)
    input_img = Image.open("input.jpg")
    output_img, elapsed = process_image(model, input_img)

    output_img.save("output.jpg")
    print(f"Время обработки: {elapsed:.3f} сек")