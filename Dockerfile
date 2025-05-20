FROM python:3.11-slim

RUN apt update && apt install -y curl && \ 
    curl -fsSL https://ollama.com/install.sh | sh &&     pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY . .

RUN ollama pull openchat/openchat-3.5

CMD ["python", "bot.py"]
