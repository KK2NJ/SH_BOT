import nextcord
from nextcord.ext import commands
import requests
#from bs4 import BeautifulSoup

import requests
from playwright.sync_api import sync_playwright
import time

def check_all_lobbies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        page = context.new_page()
        
        page.goto('https://secrethitler.io/observe/')
        time.sleep(15)  # Wait for Cloudflare
        
        # Get games
        games = page.query_selector_all('.browser-row')
        
        for game in games:
            name = game.query_selector('.gamename-column').inner_text()
            seated = game.query_selector('.seatedcount').inner_text()
            allowed = game.query_selector('.allowed-players').inner_text()
            print(f"{name}: {seated}/ {allowed}")
        
        browser.close()

check_all_lobbies()