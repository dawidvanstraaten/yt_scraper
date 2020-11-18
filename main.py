from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import ujson
from scraping import scrape_channel_videos
from scraping import get_individual_video_info



driver = webdriver.Chrome('./chromedriver')
driver.implicitly_wait(5)

driver.maximize_window()
links = scrape_channel_videos(driver)

for link in links:
    get_individual_video_info(driver, link)
    time.sleep(0.5)

df = pd.read_json(ujson.dumps(links))
df.to_csv('dbombalyt.csv')

driver.close()
