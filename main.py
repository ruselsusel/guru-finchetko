import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import openai

load_dotenv()
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot)
openai.api_key = OPENAI_API_KEY

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("✍️ Финансовая консультация", "📈 Анализ отчета")
    await message.answer("Я Гуру-Финчётко. Выбирай, с чем помочь:", reply_markup=kb)

@dp.message_handler(lambda message: message.text in ["✍️ Финансовая консультация", "📈 Анализ отчета"])
async def handle_options(message: types.Message):
    if message.text == "✍️ Финансовая консультация":
        await message.answer("Задавай свой финансовый вопрос.")
    elif message.text == "📈 Анализ отчета":
        await message.answer("Пришли файл или фото отчета. Я посмотрю.")

@dp.message_handler(content_types=types.ContentType.TEXT)
async def analyze_text(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ты Гуру-Финчётко — опытный финансовый аналитик. Отвечай кратко, по делу, строго, с лёгкой иронией. Можно вставить анекдот."},
                {"role": "user", "content": message.text}
            ]
        )
        await message.answer(response["choices"][0]["message"]["content"])
    except Exception as e:
        logging.error(f"Ошибка GPT: {e}")
        await message.answer("Ошибка при обработке. Попробуй позже.")

@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message):
    await message.document.download()
    await message.answer("📄 Файл получен. Пока я не читаю содержимое, но скоро научусь анализировать PDF, Excel и др.")

@dp.message_handler(content_types=types.ContentType.PHOTO)
async def handle_photo(message: types.Message):
    await message.answer("🖼 Фото получено. В будущем смогу распознавать скрины и вытаскивать из них цифры.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)