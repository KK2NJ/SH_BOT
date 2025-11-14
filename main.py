import nextcord
from nextcord.ext import commands
import requests
from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def check_all_lobbies():
    chrome_options = Options()
    
    # Add arguments to appear more like a real browser
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # Remove headless mode - might help bypass detection
    # chrome_options.add_argument('--headless')
    
    # Exclude automation flags
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    # Mask webdriver property
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        url = 'https://secrethitler.io/observe/'
        driver.get(url)
        
        print("Waiting for page to load (20 seconds)...")
        time.sleep(20)  # Wait longer for Cloudflare
        
        print(f"Page title: {driver.title}")
        
        # Wait for browser-row elements
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "browser-row"))
            )
        except:
            print("Timeout waiting for games to load")
        
        games = driver.find_elements(By.CLASS_NAME, 'browser-row')
        
        print(f"\nFound {len(games)} games")
        print("Secret Hitler Lobbies:")
        print("-" * 30)
        
        for game in games:
            try:
                game_name = game.find_element(By.CLASS_NAME, 'gamename-column').text
                seated = game.find_element(By.CLASS_NAME, 'seatedcount').text
                allowed = game.find_element(By.CLASS_NAME, 'allowed-players').text
                
                print(f"{game_name}: {seated}/ {allowed}")
            except Exception as e:
                print(f"Error parsing game: {e}")
        
    finally:
        driver.quit()

check_all_lobbies()
