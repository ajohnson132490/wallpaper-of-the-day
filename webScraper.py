# Imports
import ctypes
import os
import random as rand
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

#Setting download folder
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("headless")
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_experimental_option("prefs", {
    "download.prompt_for_download": False,
})

#Creating a path where the chromedriver resource is
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# function to take care of downloading file
def enable_download_headless(browser,download_dir):
    browser.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    browser.execute("send_command", params)


# Setting important variables
s = Service(executable_path="..\Resources\chromedriver.exe")
driver = webdriver.Chrome(service=s, options=chrome_options)

enable_download_headless(driver, os.path.expanduser("~")+"\\Downloads\\")
wait = WebDriverWait(driver, 10)
wallpaperPage = ""
downloadName = ""

# Opens the webpage
driver.get("https://bing.gifposter.com/list/new/desc/classic.html?p=1")

# Waiting until the page is loaded up
try:
    mainList = wait.until(
        EC.presence_of_element_located((By.TAG_NAME, "ul"))
    )

    # Getting all the wallpapers into a list
    wallpaperOptions = mainList.find_elements(By.TAG_NAME, "li")

    # Randomly selecting a wallpaper
    wallpaper = wallpaperOptions[rand.randrange(len(wallpaperOptions))]
    print("Selecting Wallpaper #{0}".format(rand.randrange(len(wallpaperOptions))))

    #Getting the link to the wallpaper page
    wallpaperPage = wallpaper.find_element(By.TAG_NAME, "a").get_attribute("href")

except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

# Open the wallpaper page
driver.get(wallpaperPage)

# Waiting until the page is loaded up
try:
    mainDiv = wait.until(
        EC.presence_of_element_located((By.CLASS_NAME, "solo"))
    )

    # Getting the link to the full screen wallpaper page
    fullScreenView = mainDiv.find_element(By.TAG_NAME, "a").get_attribute("href")

except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

# Open the Full Screen View
driver.get(fullScreenView)

# Waiting until the page is loaded up
try:
    cont = True
    while(cont):
        cont = False
        mainDiv = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains (@class, 'icon download')]"))
            )

        # Downloading the wallpaper
        mainDiv.find_element(By.XPATH, "//a[contains (@class, 'icon download')]").click()
        dlDiv = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains (@class, 'dlbox')]"))
            )
        downloadName = dlDiv.find_elements(By.TAG_NAME, "a")[0].get_attribute("download")
        print(downloadName)
        dlDiv.find_elements(By.TAG_NAME, "a")[0].click()
        time.sleep(3)

        if not os.path.exists(os.path.expanduser("~")+"\\Downloads\\" + downloadName):
            cont = True
            driver.refresh()


except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

finally:
    # Close the webpage
    driver.quit()


# Set the wallpaper as desktop background
WALLPAPER_PATH = os.path.expanduser("~")+"\\Downloads\\" + downloadName
ctypes.windll.user32.SystemParametersInfoW(20, 0, WALLPAPER_PATH , 3)

# Remove wallpaper from folder
os.remove(WALLPAPER_PATH)

print("Program Complete")
