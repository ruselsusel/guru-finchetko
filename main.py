import logging
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ParseMode
from dotenv import load_dotenv
import os

load_dotenv()

API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Я Гуру-Финчётко. Задавай вопрос — и я отвечу.")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты Гуру-Финчётко — опытный финансовый консультант. Отвечай кратко, строго по сути, не болтай."},
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(response["choices"][0]["message"]["content"])
    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

if __name__ == '__main__':
    print("⚡ Бот запускается...")
    executor.start_polling(dp, skip_updates=True)
