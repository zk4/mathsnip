#coding: utf-8
from .logx import setup_logging
import logging
import argparse
from pynput import keyboard
import os
import subprocess

# don`t remove this line
import sys
setup_logging()
logger = logging.getLogger(__name__)

current=set()

# The key combination to check
COMBINATIONS = [
    {keyboard.Key.cmd,keyboard.Key.shift, keyboard.KeyCode(char='e')},
    {keyboard.Key.cmd,keyboard.Key.shift, keyboard.KeyCode(char='E')}
]


def execute():
    with open(os.path.join(os.getenv("HOME"),".mathsnip_keypressed"),"w") as f:
        f.write("")

    current.clear()

def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if key in current:
        current.remove(key)

def monitorKey():
    print("monitor keys..")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def main(args):
    if os.geteuid()!=0:
        print("Must run with root permission!\ntry: sudo mathsnip -i <app_id> -k <app_key>")
        return
    # why call like this instread call as moudle? 
    # both cv and key monitor need mainthread to perform , and both of them needs block somehow. so..
    cdir = os.path.dirname(os.path.abspath(__file__))

    subprocess.Popen(["python3",os.path.join(cdir,"cv_engine.py"),"-i",args.app_id,"-k",args.app_key])
    print('monitor.....')
    monitorKey()
    print('monitor end.....')

def entry_point():
    parser = createParse() 
    mainArgs=parser.parse_args()
    main(mainArgs)


def createParse():
    parser = argparse.ArgumentParser( formatter_class=argparse.ArgumentDefaultsHelpFormatter, description="")
    parser.add_argument('-i', '--app_id', help='app id',required=True,type=str)  
    parser.add_argument('-k', '--app_key', help='app key', required=True,type=str) 

    return parser
