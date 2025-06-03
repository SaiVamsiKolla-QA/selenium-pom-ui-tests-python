# 1. Start from python:3.10-slim as the base image
FROM python:3.10-slim

# 2. Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    default-jdk \
    gnupg2 \
    wget \
    jq \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 3. Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# 4. Install Firefox
RUN apt-get update && apt-get install -y firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# 5. Set up working directory
WORKDIR /usr/src/app

# 6. Copy requirements first to leverage Docker cache
COPY requirements.txt .

# 7. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 8. Copy the entire repo into /usr/src/app
COPY . /usr/src/app/

# 9. Create necessary directories with proper permissions
RUN mkdir -p /usr/src/app/assets/screenshots/{chrome,firefox} && \
    mkdir -p /usr/src/app/allure-results/{chrome,firefox} && \
    chmod -R 777 /usr/src/app/assets && \
    chmod -R 777 /usr/src/app/allure-results

# 10. Set environment variables
ENV PYTHONUNBUFFERED=1
ENV DISPLAY=:99
ENV SELENIUM_REMOTE_URL=http://selenium-hub:4444/wd/hub

# 11. Create a non-root user and set proper ownership
RUN useradd -m testuser && \
    chown -R testuser:testuser /usr/src/app
USER testuser

# 12. Ensure run_tests.sh is executable
RUN chmod +x ./run_tests.sh

# 13. Default CMD should simply invoke ./run_tests.sh
CMD ["./run_tests.sh"]
