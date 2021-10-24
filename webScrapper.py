import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


PATH = os.getcwd() + r"\Web-Drivers\chromedriver.exe"
s = Service(PATH)

driver = webdriver.Chrome(service = s)

#Opens a webpage
driver.get("https://techwithtim.net")

#Prints the page title
print(driver.title)

#Closes a webpage
driver.quit()
