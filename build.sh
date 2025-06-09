#!/usr/bin/env bash

# Instala Chromium y Chromedriver
apt-get update
apt-get install -y wget unzip gnupg2

# Instala Chromium
apt-get install -y chromium

# Instala ChromeDriver compatible con Chromium
CHROME_VERSION=$(chromium --version | grep -oP '\d+\.\d+\.\d+' | head -1)
CHROMEDRIVER_VERSION=$(wget -qO- "https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json" | grep -A10 "$CHROME_VERSION" | grep "linux64" | grep "url" | sed -E 's/.*"(https:[^"]+)".*/\1/' | head -1)

wget -O chromedriver.zip "$CHROMEDRIVER_VERSION"
unzip chromedriver.zip
chmod +x chromedriver
mv chromedriver /usr/bin/chromedriver
