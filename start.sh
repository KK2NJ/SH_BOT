#!/bin/bash
echo "Installing Playwright browsers..."
python -m playwright install chromium --with-deps
echo "Browsers installed! Starting bot..."
python main.py