from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re


def get_info(attribute_text):
    likes = re.findall('[0-9\,]+', attribute_text)

    if 'No likes' in attribute_text:
        return 0

    if ',' in likes[0]:
        return int(likes[0].replace(',', ''))
    else:
        return int(likes[0])


def scrape_channel_videos(driver):
    driver.get('https://www.youtube.com/c/DavidBombal/videos')

    new_height = 0
    while True:
        last_scroll_height = new_height
        driver.execute_script('window.scrollBy(0, 1000)')
        time.sleep(0.5)
        new_height = driver.execute_script('return document.documentElement.scrollTop')
        if new_height == last_scroll_height:
            break
        print("last_scroll_height", last_scroll_height)
        print("new_height", new_height)


    links = driver.find_elements_by_id('video-title')

    video_info_lst = []
    for link in links:
        video_info_lst.append({
        'title' : link.get_attribute('innerHTML'),
        'link' : link.get_attribute('href')
        })

    return video_info_lst


def get_individual_video_info(driver, dict_item):
    driver.get(dict_item['link'])
    # print(get_info(driver.find_element_by_class_name('view-count').get_attribute('innerHTML')))
    # print('**********************************************************************')
    dict_item['views'] = get_info(driver.find_element_by_class_name('view-count').get_attribute('innerHTML'))
    dict_item['likes'] = get_info(driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string').get_attribute('aria-label'))
    dict_item['date'] = driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[1]/div[2]/yt-formatted-string').get_attribute('innerHTML')
    # print(driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[1]/div/div[5]/div[2]/ytd-video-primary-info-renderer/div/div/div[3]/div/ytd-menu-renderer/div/ytd-toggle-button-renderer[1]/a/yt-formatted-string').get_attribute('aria-label'))
