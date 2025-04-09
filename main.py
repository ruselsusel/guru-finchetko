import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)

client = OpenAI(api_key=OPENAI_API_KEY)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.answer("Я Гуру-Финчётко. Задавай вопрос — и я отвечу.")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def analyze_text(message: types.Message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Ты Гуру-Финчётко — опытный финансовый консультант, владеешь актуальной информацией, отвечаешь кратко и по делу."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response.choices[0].message.content
        await message.answer(reply)
    except Exception as e:
        logging.error(f"Ошибка при обработке текста: {e}")
        await message.answer(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
