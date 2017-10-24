"""The SpotlightDesktop Script"""
import ctypes
import sys
import time
import winreg
import subprocess
import os


def mbox(title, text, style):
    """Simple message box function"""
    ctypes.windll.user32.MessageBoxW(0, text, title, style)


def getcurrentdpotlightimage():
    """Gets the current Spotlight image path"""

    # Why run a command? Try getting that through the winreg library... (permissions issues)
    while(1): 
        try:
            location = subprocess.check_output("RegLookup.exe HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Creative", shell=True, stderr=subprocess.STDOUT).decode('utf8').splitlines()[-1]

            # Sadely, not the real location
            try:
                location = subprocess.check_output("RegLookup.exe "+location, shell=True, stderr=subprocess.STDOUT).decode('utf8').splitlines()[-1]

                # And yes, even when we find the location, that's protected too
                try:
                    
                    output = subprocess.check_output("RegLookup.exe " + location + " /v landscapeImage", shell=True, stderr=subprocess.STDOUT).decode('utf8')
                except subprocess.CalledProcessError:
                    print("Breaked from Level 3")
                    break

                # Get whatever is after the last space (that should be the image path)
                location = output[output.rindex(' ')+1:]

                if (location == ""):
                    mbox("spotlightdesktop | ERROR", 'Found the registry information' +
                         'but it did not include a path to the Spotlight image location.', 0)
                    sys.exit()

                return location

            except subprocess.CalledProcessError:
                print("Breaked from Level 2")
                break

        except subprocess.CalledProcessError:
            print("Breaked from Level 1")
            break

    print("Using old registry location")

    location = "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Lock Screen\\Creative"

    try:
        hkey = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                              location)
        asset_path = winreg.QueryValueEx(hkey, "LandscapeAssetPath")
    except FileNotFoundError:
        mbox("spotlightdesktop | ERROR", 'Cannot find the registry information' +
             'of the Spotlight image location.', 0)
        sys.exit()

    # Check to make sure there is content
    if (asset_path[0] == ""):
        mbox("spotlightdesktop | ERROR", 'Found the registry information' +
             'but it did not include a path to the Spotlight image location.', 0)
        sys.exit()

    # Return only the value from the resulting tuple (value, type_as_int).
    return asset_path[0]


def changewallpaper(location):
    """Changes the Windows Wallpaper"""
    SPIF_UPDATEINIFILE  = 0x01
    SPIF_SENDCHANGE     = 0x02
    SPI_SETDESKWALLPAPER    = 0x0014
    WM_SETTINGCHANGE    = 0x1A
    HWND_BROADCAST      = 0xFFFF
    SPI_GETDESKWALLPAPER    = 0x0073

    try:
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 1, location, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
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
