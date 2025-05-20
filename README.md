# 🐳 uncensored_ai_bot

Локальный Telegram-бот с нейросетью без цензуры. Работает на базе Ollama + OpenChat.

## 🚀 Запуск

1. Установи Docker и Docker Compose
2. Склонируй или разархивируй проект
3. Создай файл `.env` и вставь свой токен:
```
BOT_TOKEN=123456:ABCDEF
```
4. Запусти:
```
docker-compose up --build
```

Открывается порт Ollama `11434`. Бот будет общаться с моделью `openchat/openchat-3.5`.

Модель загружается при первом запуске 🧠
