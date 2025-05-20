from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import asyncio
import requests
import os

API_TOKEN = os.getenv("BOT_TOKEN")
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "openchat/openchat-3.5"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_message(message: Message):
    user_input = message.text
    await message.answer("🤔 Думаю...")

    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": user_input,
        "stream": False
    })

    data = response.json()
    output = data.get("response", "Что-то пошло не так...")
    
    if len(output) > 4096:
        for i in range(0, len(output), 4096):
            await message.answer(output[i:i+4096])
    else:
        await message.answer(output)

async def main():
    print("🚀 Бот запущен.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
