import cv2
import numpy as np
from PIL import ImageGrab as ig
import os

import argparse
import tempfile
import base64
import time
import requests
import threading
import json

# now let's initialize the list of reference point
ref_point   = [None,None]
drawing     = False
window_name = "image"
done        = False
result      = None
tokenDict      = {}
key_pressed = []

service = 'https://api.mathpix.com/v3/latex'

def notify(title="",content=""):
    cmd = f'''osascript -e 'display notification "'"{content}"'" with title "'"{title}"'"  ' '''

    os.system(cmd)

def topWindow(pid):
    cmd = f'''osascript -e '
        tell application \"System Events\"
                set frontmost of the first process whose unix id is "'"{pid}"'" to true
     end tell' '''
    os.system(cmd)

def latex(args, headers, timeout=10):
    r = requests.post(service,
        data=json.dumps(args), headers=headers, timeout=timeout)
    return json.loads(r.text)

def base64_img(filename):
    image_data = open(filename, "rb").read()
    return "data:image/jpg;base64," + base64.b64encode(image_data).decode()


def ocr(cropped_image_path):

    global result
    headers =         {
            'app_id': tokenDict.get( "app_id") ,
            'app_key': tokenDict.get( "app_key") ,
            'Content-type': 'application/json'
        }
    print(headers)

    result = latex({
            'src': base64_img(cropped_image_path),
            'formats': ['latex_simplified']
        },
        headers
    )
    if 'latex_simplified'  in result:
        latex_str=result['latex_simplified']
        cmd = f"pbcopy <<< '${latex_str}$'"
        os.system(cmd)
        accurate_rate = str(result["latex_confidence_rate"])
        notify("done","accuracy:"+accurate_rate)
    else:
        notify("failed","")


def shape_selection(event, x, y, flags, param):
    global ref_point, crop,drawing,image,done

    if event == cv2.EVENT_LBUTTONDOWN:

        ref_point[0] = (x, y)
        drawing = True

    # check to see if the left mouse button was released
    elif event == cv2.EVENT_LBUTTONUP:

        ref_point[1]=(x, y)

        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 0, 255), 1)
        p1=ref_point[0]
        p2=ref_point[1]
        if p1[0]>p2[0]:
            p1,p2=p2,p1

        x = p1[0]
        y = p1[1]

        w = p2[0] - p1[0]
        h = p2[1] - p1[1]
        
        if w>0 and h>0:
            cropped_image = image[y:y+h, x:x+w]
            defult_tmp_dir = tempfile._get_default_tempdir()
            temp_name= os.path.join(defult_tmp_dir,"cropped.jpg")
            cv2.imwrite(temp_name, cropped_image)
            threading.Thread(target =ocr,args=(temp_name,)).start()
            cv2.resizeWindow(window_name, 0,0)
            key_pressed.clear()

        drawing = False

    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        image = clone.copy()
        ref_point[1]=(x, y)

        cv2.rectangle(image, ref_point[0], ref_point[1], (0, 0, 255), 1)


    cv2.imshow(window_name, image)


def cancel():
    cv2.resizeWindow(window_name, 0,0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    parser.add_argument('-i', '--app_id', help='app id',required=False,type=str)  
    parser.add_argument('-k', '--app_key', help='app key', required=False,type=str) 
    mainArgs=parser.parse_args()
    tokenDict["app_id"]=mainArgs.app_id
    tokenDict["app_key"]=mainArgs.app_key


    screen = ig.grab().convert("RGB")
    image = np.array(screen)
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setMouseCallback(window_name, shape_selection)
    cancel()

    notify("'press cmd+shift+e to selection region!'","")
    print("cv init done ... press cmd+shift+e to ocr latex picture!")
    key_pressed_file = os.path.join(os.getenv("HOME"),".mathsnip_keypressed")
    while True :
        if os.path.exists(key_pressed_file):
            key_pressed.append(True)
            os.system("rm "+key_pressed_file)
            screen = ig.grab().convert("RGB")
            image = np.array(screen)
            clone = image.copy()
            cv2.imshow(window_name, image)
            cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            topWindow(str(os.getpid()))
            # os.system("./top.sh "+str(os.getpid()))

        key = cv2.waitKey(300) & 0xFF
        if key == ord("r"):
            image = clone.copy()
        elif key == ord("c") or key == 27:
            cancel()
        # if there is a window close the window
        elif cv2.getWindowProperty('image',cv2.WND_PROP_VISIBLE) < 1:
            break

    # close all open windows
    cv2.destroyAllWindows() 
