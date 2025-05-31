# 1. Start from python:3.10-slim as the base image
FROM python:3.10-slim

# 2. Install any required OS packages (e.g., wget, unzip, curl)
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# 3. Copy the entire repo into /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app/

# 4. Run pip install --upgrade pip and then pip install -r Requirements.txt plus pytest, pytest-xdist, allure-pytest, python-dotenv, and selenium
RUN pip install --upgrade pip
RUN pip install -r Requirements.txt pytest pytest-xdist allure-pytest python-dotenv selenium

# 5. Download Allure CLI version 2.27.0, unzip it under /opt/allure, and create a symlink so allure is on the PATH
RUN wget https://github.com/allure-framework/allure2/releases/download/2.27.0/allure-2.27.0.zip -P /tmp && \
    unzip /tmp/allure-2.27.0.zip -d /opt && \
    ln -s /opt/allure-2.27.0/bin/allure /usr/bin/allure && \
    rm /tmp/allure-2.27.0.zip

# 6. Set /usr/src/app as the working directory (already done in step 3)

# Ensure run_tests.sh is executable
RUN chmod +x ./run_tests.sh

# 7. Default CMD should simply invoke ./run_tests.sh
CMD ["./run_tests.sh"]
