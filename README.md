# Discord Video Resizer

![MainGUI](./doc/main_gui.png)

Calculate and forward FFMPEG commands, staying under Discords 25MB limit.
Supports multiple files at the same time, as well as automatically using CPU vs NVENC encoding


# Installation
Download the latest version from:

https://github.com/alex-ong/discord_vid/releases/

1. Unzip the folder somewhere useful.
2. Run `install.bat`
3. Select which presets you want in your `shift+rightclick` context menu
4. Select the `default preset` you want to compress to
5. Click `Install selected presets` and press yes a few times

![Installer](./doc/installer.png)

This will add a `shift+right click` context menu


# Usage
![Usage](./doc/usage.png)
1. Select as many video files as you want in the `file explorer`
2. Hold `shift`, then `right click` on a selected file
3. Select the preset you want

# Presets
Presets can be modified by going to `data/USER_CONFIG.json` after running the application once.
You can then run the uninstaller and installer to update the Windows Registry


# Uninstallation
Uninstall by running `uninstall.bat`


