FROM python:3.11-slim-bullseye
WORKDIR /app
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m -r bot && chown -R bot:bot /app
USER bot
CMD ["python", "main.py"]