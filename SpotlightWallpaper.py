import schedule
import winreg
import ctypes
import sys
import time

# Simple message box function
def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxW(0, text, title, style)

# Gets the current Spotlight image path
def getCurrentSpotlightImage():
    try:
        hKey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              "SOFTWARE\Microsoft\Windows\CurrentVersion\Lock Screen\Creative")
        asset_path = winreg.QueryValueEx(hKey, "LandscapeAssetPath")
        print('Current Spotlight Image found')
    except:
        schedule.CancelJob()
        Mbox("SpotlightDesktop | ERROR", 'Cannot find the registry information of the Spotlight image location.', 0)
        sys.exit()

    # Return only the value from the resulting tuple (value, type_as_int).
    return asset_path[0]

# Changes the Windows Wallpaper
def ChangeWallpaper(image_location):
    try:
        SPI_SETDESKWALLPAPER = 20
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_location, 3)
        print('Desktop wallpaper changed')
    except:
        schedule.CancelJob()
        Mbox("SpotlightDesktop | ERROR", 'Cannot change the desktop wallpaper tot he Spotlight image', 0)
        sys.exit()

# The function that ties everything together
def SpotlightDesktop():
    SpotlightImage = getCurrentSpotlightImage()
    ChangeWallpaper(SpotlightImage)
    print('Finished updating the current Spotlight image')

# Run it once now
SpotlightDesktop()

# Schedule SpotlightDesktop to run every day
schedule.every().day.do(SpotlightDesktop)

# Let it run in the background
while True:
    schedule.run_pending()
    time.sleep(3600)
