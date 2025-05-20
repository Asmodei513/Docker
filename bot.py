import os
import logging
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("7234356509:AAFu-Hg2XUpoyEYrQBfXxFnStkp0U1rhJ7Q")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID"))
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OLLAMA_PORT = int(os.getenv("OLLAMA_PORT", 11434))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
BOT_MODE = os.getenv("BOT_MODE", "normal")
CHAT_LOG_PATH = os.getenv("CHAT_LOG_PATH", "chat_logs.json")

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def query_ollama(prompt: str) -> str:
    url = f"http://localhost:{OLLAMA_PORT}/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        logger.error(f"Ollama request failed: {e}")
        return "Ошибка при запросе к Ollama."

def allowed_user(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        if user_id != ALLOWED_USER_ID:
            logger.warning(f"Доступ запрещён для пользователя {user_id}")
            await update.message.reply_text("Извини, у тебя нет доступа к этому боту.")
            return
        return await func(update, context)
    return wrapper

@allowed_user
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой локальный ИИ в режиме " + BOT_MODE)

@allowed_user
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    logger.info(f"Получено сообщение: {user_text}")

    if BOT_MODE == "rp":
        prompt = f"Ты демонический ассистент, отвечай дерзко: {user_text}"
    elif BOT_MODE == "plus":
        prompt = f"Ты ChatGPT Plus, отвечай подробно и точно: {user_text}"
    else:
        prompt = user_text

    answer = query_ollama(prompt)
    await update.message.reply_text(answer)

    try:
        with open(CHAT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"User: {user_text}\nBot: {answer}\n\n")
    except Exception as e:
        logger.error(f"Ошибка записи лога: {e}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    logger.info("Бот запущен")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())