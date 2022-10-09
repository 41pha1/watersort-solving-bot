
# Watersort-Bot

Have you ever stopped and thought to yourself: 

"Wow, playing mobile games is way to exhausting! Why cant I just order someone else to have fun for me?"


In this case this script is just perfect for you! Let the script run overnight and crush all of your friends highscores without using your precious brain resources even once!

This python script automatically solves and progresses through the levels of watersort style mobile games on Android.



## Installation

```bash
python -m pip install pure-python-adb
```

To run this script Android Debug Bridge (adb) must be installed and added to path.

Download SDK Platform-Tools for your operating system.

```bash
adb start-server
```

Enable USB-Debugging on your Android Device in the Devoloper Settings, connect it per wire to your PC, and press allow when the adb tries to connect.


## Usage

You might have to adjust the settings in main.py accourding to your version of watersort.

```python
#Settings
#------------------------------------------------------------------------------------------------------------------------
save_screenshot = False                #Save a screenshot to find out the pixel positions                               | 
row_positions = [1200, 1900]           #The y position of the middle of the BOTTOM vile content per row in pixels       |
y_off = 100                            #The y offset between to colors in a vile                                        |
border_col = (188, 188, 188, 255)      #The border color of a vile                                                      | 
threshold = 50                         #The darkness threshold at which a color is considered part of the background    |
colors_per_vile = 4                    #The maximum number of colors per vile                                           |
pouring_sleep_time = 2.5               #The number of seconds to wait for a move to finish before continuing            |
next_button_y = 1700                   #The y-location of the next level button                                         |
loop = True                            #Set to true if you want it to automatically solve multiple levels in a row      |
#------------------------------------------------------------------------------------------------------------------------

```

Now just open Watersort on your android device and run main.py!
## Screenshots

![App Screenshot](https://github.com/41pha1/watersort-solving-bot/screenshot.png)

