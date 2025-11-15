from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyvirtualdisplay import Display
import time

def check_all_lobbies():
    # Create virtual display to bypass Cloudflare
    display = Display(visible=0, size=(1920, 1080))
    display.start()
    
    chrome_options = Options()
    # DON'T use headless - virtual display handles this
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('start-maximized')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Use system chromium
    chrome_options.binary_location = '/usr/bin/chromium'
    
    driver = webdriver.Chrome(
        service=Service('/usr/bin/chromedriver'),
        options=chrome_options
    )
    
    # Mask webdriver property
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    try:
        url = 'https://secrethitler.io/observe/'
        driver.get(url)
        
        print("Waiting for page to load (20 seconds)...")
        time.sleep(20)
        
        print(f"Page title: {driver.title}")
        
        # Wait for games
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "browser-row"))
            )
        except:
            print("Timeout waiting for games")
        
        games = driver.find_elements(By.CLASS_NAME, 'browser-row')
        
        print(f"Found {len(games)} games")
        print("Secret Hitler Lobbies:")
        print("-" * 30)
        
        for game in games:
            try:
                game_name = game.find_element(By.CLASS_NAME, 'gamename-column').text
                seated = game.find_element(By.CLASS_NAME, 'seatedcount').text
                allowed = game.find_element(By.CLASS_NAME, 'allowed-players').text
                
                print(f"{game_name}: {seated}/ {allowed}")
            except:
                pass
        
    finally:
        driver.quit()
        display.stop()

check_all_lobbies()