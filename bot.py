import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from PIL import Image, ImageOps
import io

TOKEN = os.getenv("BOT_TOKEN")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await update.message.photo[-1].get_file()
    file_bytes = await file.download_as_bytearray()
    img = Image.open(io.BytesIO(file_bytes)).convert("L")
    img = ImageOps.invert(img)
    img = img.point(lambda x: 0 if x < 150 else 255, '1')

    output = io.BytesIO()
    img.save(output, format='PNG')
    output.seek(0)

    await update.message.reply_photo(photo=output, caption="این الگوی خام گلدوزی هست.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.run_polling()
