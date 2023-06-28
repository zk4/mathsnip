# Python 3

#FOR TAKING USER PREDEFINED SCREENSHOTS
# SCREENSHOT
from PIL import ImageGrab
# GUI
import PySimpleGUI as sg
# FOLDER AND DIRECTORY
import os
# GENERIC NAMING
# Use pywildcard if fnmatch not available
# just replace anywhere you see fnmatch with pywildcard
# pip install pywildcard
import fnmatch

from .service import ocr
# DEFINE GUI LAYOUT
layout = [
        [sg.Button('Screenshot'), sg.Button('Exit')],
        [sg.Canvas(size=(1, 1), background_color=None, key= 'canvas')]
        ]

window = sg.Window('MathSnip', layout,transparent_color=None,
                   alpha_channel=.5, grab_anywhere = True, resizable = True) # disable_close=True
window.Finalize()

canvas = window['canvas']

# SCREEN SHOT FUNC
def screenshot():
    window.refresh()
    lx, ly = window.CurrentLocation()
    x, y = window.size
    coord = ((lx+7, ly+30,(x+5+lx +5), (y+ly+30)))
    img = ImageGrab.grab(coord)
    return img

# Window main loop
while True:
    event, values = window.read()
    #Close window with "x"  window button
    # You can disable it by adding " disable_close=True" in the window declaration (Line 20).
    if event == sg.WIN_CLOSED :
        break

    if event == 'Exit':
        break


        # Screen shot GUI events
    elif event == 'Screenshot':
        window.Hide()
        img = screenshot()

        #UnHide when function returns
        window.UnHide()
        #img.show()
    # Learn how many screenshots with the same name
    # Add "1' to the number  then create a new name with it
    # THis is to avoid replacing existing screenshots
        shots = fnmatch.filter((shot for shot in os.listdir('.')), 'MathSnip*.png')
        lrn = len(shots)
        lrn = lrn+1
        img.save('MathSnip%s.png'%lrn)
        latex = ocr('MathSnip%s.png'%lrn)
        if latex is not None:
            sg.popup_notify('Screenshot saved!',  location=sg.DEFAULT_WINDOW_LOCATION, display_duration_in_ms=6, fade_in_duration=10)

# CLOSE AND DELETE WINDOW
window.close();del window
