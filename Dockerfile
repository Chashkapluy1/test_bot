FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy main application code
COPY . .

# Environment variables will be populated from .env file during compose/run
# Run the bot
CMD ["python", "main.py"]
