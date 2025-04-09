import os
import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Setup OpenAI and logging
openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Пришли файл (документ, фото, скрин) — я его сохраню.")


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    file_info = await bot.get_file(message.document.file_id)
    file_path = file_info.file_path
    await message.answer(f"🗋 Документ получен: {message.document.file_name}")


@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    await message.answer("📷 Фото получено и сохранено. Спасибо!")


@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_text(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты Гуру-Финчётко — строгий, умный финансовый советник. Отвечай кратко и по делу."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        logging.error(f"GPT error: {e}")
        await message.answer("❌ Ошибка при обращении к GPT. Попробуй позже.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

