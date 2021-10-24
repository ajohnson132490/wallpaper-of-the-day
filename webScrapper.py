import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PATH = os.getcwd() + r"\Web-Drivers\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service = s)
wait = WebDriverWait(driver, 10)

#Opens a webpage
driver.get("https://techwithtim.net")

#Prints the page title
print(driver.title)

#Locate the search bar and search for test
search = wait.until(EC.presence_of_element_located((By.NAME, "s")))
search.send_keys("test")
search.send_keys(Keys.RETURN)

#Waiting until the page is loaded up
try:
    main = wait.until(
        EC.presence_of_element_located((By.ID, "main"))
    )

    articles = main.find_elements_by_tag_name("article")

    for article in articles:
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)

finally:
    driver.quit()
