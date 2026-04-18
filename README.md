# Smart Weather & Travel AI Assistant

A modern, production-ready Telegram Bot built with Python, Aiogram 3.x, and powered by Google's Gemini 1.5 Flash AI and the OpenWeatherMap API.

## Logic Description

This bot is architected as an **AI Agent**. It employs **Function Calling (Tool Use)** to perform real-world tasks beyond simple text generation.
When a user asks about the weather or travel conditions in any city, the Gemini AI model autonomously determines that it needs real-time data. It triggers the `get_weather` function, fetching live weather information from the OpenWeatherMap API. The bot then ingests this raw json data and interprets it into a conversational, helpful response, providing tailored clothing or activity recommendations based on the current conditions.

## Tech Stack
- **Framework:** `aiogram` 3.x (Async Telegram Bot API framework)
- **AI Brain:** `google-generativeai` (Gemini 1.5 Flash utilizing Function Calling)
- **External Data:** `aiohttp` for async HTTP requests to OpenWeatherMap
- **Configuration:** `pydantic-settings`
- **Deployment:** Docker & docker-compose ready

## Setup Guide

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-repo-directory>
```

### 2. Environment Variables
Create a file named `.env` in the root directory and populate it with your API keys:
```env
BOT_TOKEN=your_telegram_bot_token
GEMINI_API_KEY=your_google_gemini_api_key
WEATHER_API_KEY=your_openweathamap_api_key
```

### 3. Run Locally (without Docker)
```bash
pip install -r requirements.txt
python main.py
```

### 4. Run via Docker
To deploy using Docker:
```bash
docker-compose up --build -d
```
This is the recommended method for production deployment (e.g., on Render.com or Railway.app).
