import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PATH = os.getcwd() + r"\Resources\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service = s)
wait = WebDriverWait(driver, 10)

#Opens a webpage
driver.get("https://bing.gifposter.com/list/new/desc/classic.html?p=1")

#Prints the page title
print(driver.title)

"""
#Locate the search bar and search for test
search = wait.until(EC.presence_of_element_located((By.NAME, "s")))
search.send_keys("test")
search.send_keys(Keys.RETURN)
"""

#Waiting until the page is loaded up
try:
    main = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "wrapper"))
    )
    print("Main wrapper has been loaded")
    print(main.text)

    wallpapers = main.find_elements_by_tag_name("li")

    for wallpaper in wallpapers:
        name = wallpaper.find_element_by_tag_name("span")
        print(name.text)

finally:
    driver.quit()
