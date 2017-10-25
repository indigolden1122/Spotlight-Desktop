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
    try:
        locations = subprocess.check_output("RegLookup.exe HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Authentication\LogonUI\Creative", shell=True, stderr=subprocess.STDOUT).decode('utf8').splitlines()
        for current_location in locations:

            # Gives a lot of output, just take the actual results
            if not (current_location.startswith("HKEY_LOCAL_MACHINE")):
                continue

            try:
                output = subprocess.check_output("RegLookup.exe " + current_location + " /v LandscapeAssetPath", shell=True, stderr=subprocess.STDOUT).decode('utf8')
                AssetPath = output[output.rindex(' ')+1:]

                if  os.getenv('LOCALAPPDATA') not in AssetPath:
                    continue

            except subprocess.CalledProcessError:
                continue

            # Check to make sure there is content
            if (AssetPath == ""):
                mbox("spotlightdesktop | ERROR", 'Found the registry information' +
                     'but it did not include a path to the Spotlight image location.', 0)
                sys.exit()

            # We have an AssetPath but newer versions of Windows will go into subnodes, see if any exist
            try:
                locations_sub = subprocess.check_output("RegLookup.exe "+current_location, shell=True, stderr=subprocess.STDOUT).decode('utf8').splitlines()[-1]

                # Could be the same thing
                if (locations_sub != current_location):

                    # Got a subnode, one of them is the actual location
                    try:
                        output = subprocess.check_output("RegLookup.exe " + locations_sub + " /v landscapeImage", shell=True, stderr=subprocess.STDOUT).decode('utf8')
                        AssetPath_Real = output[output.rindex(' ')+1:]

                        if  os.getenv('LOCALAPPDATA') in AssetPath_Real:
                            # Exit from Level 2
                            return AssetPath_Real

                    except subprocess.CalledProcessError:
                        pass

            except subprocess.CalledProcessError:
                pass

            # Exit from Level 1
            return AssetPath;


    except subprocess.CalledProcessError:
        pass

    # Using old registry location

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
    location = ''.join(location.splitlines())

    SPIF_UPDATEINIFILE  = 0x01
    SPIF_SENDCHANGE     = 0x02
    SPI_SETDESKWALLPAPER    = 0x0014

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
