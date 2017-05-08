"""The SpotlightDesktop Script"""
import ctypes
import sys
import time
import winreg


def mbox(title, text, style):
    """Simple message box function"""
    ctypes.windll.user32.MessageBoxW(0, text, title, style)


def getcurrentdpotlightimage():
    """Gets the current Spotlight image path"""
    try:
        hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Lock Screen\\Creative")
        asset_path = winreg.QueryValueEx(hkey, "LandscapeAssetPath")
    except FileNotFoundError:
        mbox("spotlightdesktop | ERROR", 'Cannot find the registry information' +
             'of the Spotlight image location.', 0)
        sys.exit()

    # Return only the value from the resulting tuple (value, type_as_int).
    return asset_path[0]


def changewallpaper(location):
    """Changes the Windows Wallpaper"""
    try:
        spi_setdeskwallpaper = 20
        ctypes.windll.user32.SystemParametersInfoW(spi_setdeskwallpaper, 0, location, 3)
        print('Desktop wallpaper changed')
    except FileNotFoundError:
        mbox("spotlightdesktop | ERROR", 'Cannot change the desktop wallpaper to' +
             'the Spotlight image.', 0)
        sys.exit()


def spotlightdesktop():
    """The function that ties everything together"""
    spotlightimage = getcurrentdpotlightimage()
    print('Spotlight image location found: '+spotlightimage)
    changewallpaper(spotlightimage)
    print('Finished updating the current Spotlight image')
    return spotlightimage


def checkforchange(location):
    """Function that checks if the Spotlight image changes"""
    if location != getcurrentdpotlightimage():
        print('Spotlight image changed, changing background')
        spotlightdesktop()

# Run it once now
IMAGE_LOCATION = spotlightdesktop()

# Let it run in the background
while '-s' not in sys.argv:
    checkforchange(IMAGE_LOCATION)
    time.sleep(60)
