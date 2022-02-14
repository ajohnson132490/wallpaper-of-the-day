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

#Setting download folder
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory' : os.getcwd()}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--disable-notifications")

#Creating a path where the chromedriver resource is
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

# Setting important variables
PATH = os.getcwd() + r"chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(resource_path("./Resources/chromedriver.exe"), options=chrome_options)
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
    wallpaperOptions = mainList.find_elements_by_tag_name("li")

    # Randomly selecting a wallpaper
    wallpaper = wallpaperOptions[rand.randrange(len(wallpaperOptions))]
    print("Selecting Wallpaper #{0}".format(rand.randrange(len(wallpaperOptions))))

    #Getting the link to the wallpaper page
    wallpaperPage = wallpaper.find_element_by_tag_name("a").get_attribute("href")

except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

# Open the wallpaper page
driver.get(wallpaperPage)

# Waiting until the page is loaded up
try:
    mainDiv = wait.until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='clearfix']"))
    )

    # Getting the link to the full screen wallpaper page
    fullScreenView = mainDiv.find_element_by_tag_name("a").get_attribute("href")

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
            EC.presence_of_element_located((By.XPATH, "//div[@class='nav-btn']"))
            )

        # Downloading the wallpaper
        downloadName = mainDiv.find_element(By.XPATH, "//a[contains (@class, 'icon download')]").get_attribute("download")
        mainDiv.find_element(By.XPATH, "//a[contains (@class, 'icon download')]").click()
        time.sleep(3)
        numFiles = 0

        if not os.path.exists(os.getcwd() + r"\\" + downloadName):
            cont = True
            driver.refresh()

except Exception as e:
    print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")

finally:
    # Close the webpage
    driver.quit()

# Set the wallpaper as desktop background
WALLPAPER_PATH = os.getcwd() + r"\\" + downloadName
ctypes.windll.user32.SystemParametersInfoW(20, 0, WALLPAPER_PATH , 3)

# Remove wallpaper from folder
os.remove(WALLPAPER_PATH)

print("Program Complete")
