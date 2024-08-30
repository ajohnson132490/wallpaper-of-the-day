# wallpaper-of-the-day
This tool gets a new, HD wallpaper for you on computer startup and automatically sets it as your background.

## Required installs
This tool does use selenium and python, so please make sure you have both installed.

## Known issues
If your downloads folder isn't in your C drive, the download will fail. To remedy this, move your downloads folder to your C drive, or modify the path on webScraper.py lines 43, 107, and 121 to reflect your downloads directory. Once you have done that, install pyinstaller, open a cmd window in the repo download, and run the line of code below.

```
pyinstaller --onefile --noconsole --add-binary "./Resources/chromedriver.exe;./Resources" webScraper.py
```
