from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ContentType
import os

from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет! Пришли файл (документ, фото, скрин) — я его сохраню.")

@dp.message_handler(content_types=[ContentType.DOCUMENT, ContentType.PHOTO])
async def handle_file(message: types.Message):
    if message.document:
        file = message.document
    elif message.photo:
        file = message.photo[-1]  # самое крупное фото

    file_info = await bot.get_file(file.file_id)
    file_path = file_info.file_path
    ext = os.path.splitext(file_path)[-1]
    dest = os.path.join(UPLOAD_DIR, f"{file.file_id}{ext}")

    await bot.download_file(file_path, dest)
    await message.reply("✅ Файл сохранён!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
