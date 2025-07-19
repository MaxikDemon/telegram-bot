import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from langdetect import detect

API_TOKEN = os.getenv(7194545111:AAH2xhvxDhfH76nDUvVKGPRHO1WKbCAZq8w)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

BLOCK_MODE = "delete"  # delete / ban / warn
KEYWORDS = ["руб", "россия"]

async def check_language(text):
    try:
        return detect(text)
    except:
        return None

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def filter_messages(message: types.Message):
    text = message.text.lower()

    if any(word in text for word in KEYWORDS):
        await take_action(message, reason="Стоп-слово")
        return

    lang = await check_language(text)
    if lang == "ru":
        await take_action(message, reason="Російська мова")

async def take_action(message: types.Message, reason=""):
    if BLOCK_MODE == "delete":
        await message.delete()
    elif BLOCK_MODE == "ban":
        await bot.kick_chat_member(message.chat.id, message.from_user.id)
        await message.answer(f"Користувач {message.from_user.full_name} забанений. Причина: {reason}")
    elif BLOCK_MODE == "warn":
        await message.reply(f"⚠️ Попередження! Причина: {reason}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
