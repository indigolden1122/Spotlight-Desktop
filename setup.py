from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [], optimize = 1)

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('SpotlightWallpaper.py', base=base, icon="icon.ico")
]

setup(name='SpotlightWallpaper',
      version = '1.0',
      description = 'SpotlightWallpaper',
      options = dict(build_exe = buildOptions),
      executables = executables)
