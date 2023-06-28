import requests
import os
import json
import base64
service = 'https://api.mathpix.com/v3/latex'
tokenDict      = {}

tokenDict["app_id"]=os.environ.get("MATHPIX_APP_ID")
tokenDict["app_key"]=os.environ.get("MATHPIX_APP_KEY")

print(tokenDict)
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
    print("sending...")
    r = requests.post(service, data=json.dumps(args), headers=headers, timeout=timeout, verify=False)
    print(r.text)
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

    result = latex({
            'src': base64_img(cropped_image_path),
            'formats': ['latex_simplified']
        },
        headers
    )
    if 'latex_simplified'  in result:
        latex_str=result['latex_simplified']
        cmd = f"pbcopy <<< '{latex_str}'"
        os.system(cmd)
        accurate_rate = str(result["latex_confidence_rate"])
        notify("done","accuracy:"+accurate_rate)
        return latex_str
    else:
        notify("failed","")
        return None

