# This script is used to take a screenshot of a html-file and save it as a png. It uses the selenium library to open a browser and take a screenshot of the page. The script is called by the main script cal.py. The main script is called by a cronjob every day at 6am. The screenshot is then used to display the calendar on a e-ink display.


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def take_screenshot():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=786,1024")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-scrollbars")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument('--force-device-scale-factor=1')

    

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(786, 1024)

    driver.get("file://" + os.path.abspath("index.html"))

    time.sleep(5)
    driver.save_screenshot("screenshot.png")

    driver.quit()

take_screenshot()