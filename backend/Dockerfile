FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for Playwright and Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    gnupg \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libcups2 \
    libxss1 \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Copy backend source code
COPY backend/ ./

EXPOSE 8000

CMD ["python", "run.py"]
