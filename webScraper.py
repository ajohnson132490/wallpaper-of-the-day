# Imports
import os
import time
import random as rand
import ctypes
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Setting important variables
PATH = os.getcwd() + r"\Resources\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service = s)
wait = WebDriverWait(driver, 10)
wallpaperPage = ""
downloadName = ""

# Disabling popup ads
options = webdriver.ChromeOptions()
capabilities = options.to_capabilities()
capabilities = {
 'browser': 'chrome',
 'browser_version': 'latest',
 'os': 'Windows',
 'os_version': '10',
 'build': 'Python Wallpaper of The Day',
 'name': 'Pop-ups blocker'
}
capabilities["excludeSwitches"] = ["disable-popup-blocking"]

# Opens the webpage
driver.get("https://bing.gifposter.com/list/new/desc/classic.html?p=1")

# Prints the page title
print(driver.title)

# Waiting until the page is loaded up
try:
    mainList = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "ul"))
    )

    print("Main list has been loaded.")

    # Getting all the wallpapers into a list
    wallpaperOptions = mainList.find_elements_by_tag_name("li")

    # Cycling through all of the wallpapers and printing the name of the wallpaper
    for wallpaper in wallpaperOptions:
        name = wallpaper.find_element_by_tag_name("span")
        print(name.text)

    # Randomly selecting a wallpaper
    wallpaper = wallpaperOptions[rand.randrange(len(wallpaperOptions))]
    print("Selecting Wallpaper #{0}".format(rand.randrange(len(wallpaperOptions))))

    #Getting the link to the wallpaper page
    wallpaperPage = wallpaper.find_element_by_tag_name("a").get_attribute("href")

except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

# Open the wallpaper page
driver.get(wallpaperPage)

# Prints the page title
print(driver.title)

# Waiting until the page is loaded up
try:
    mainDiv = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='clearfix']"))
    )

    print("Wallpaper page has been loaded.")

    # Getting the link to the full screen wallpaper page
    fullScreenView = mainDiv.find_element_by_tag_name("a").get_attribute("href")

except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

# Open the Full Screen View
driver.get(fullScreenView)

# Prints the page title
print(driver.title)

# Waiting until the page is loaded up
try:
    mainDiv = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='nav-btn']"))
    )

    print("Full Screen page has been loaded.")

    # Downloading the wallpaper
    downloadName = mainDiv.find_element(By.XPATH, "//a[contains (@class, 'icon download')]").get_attribute("download")
    mainDiv.find_element(By.XPATH, "//a[contains (@class, 'icon download')]").click()

    time.sleep(3)

    print("Download Complete")

except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

finally:
    # Close the webpage
    driver.quit()

# Set the wallpaper as desktop background
realtive_path = os.path.relpath("\Downloads\{0}".format(downloadName))
print(realtive_path)
ctypes.windll.user32.SystemParametersInfoW(20,0,realtive_path,0)
print("Program Complete")
