import time as t
import serial as s
import os
import platform as plat
import threading

default_path_linux = "/dev/ttyUSB0"
default_path_win = "COM1"
class col:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
 

def get_data():
    global pic
    while True:
        try:
            data = pic.readline()
        except:
            print(col.FAIL + "Disconnected" + col.ENDC)
            os._exit(os.EX_OK)
        if data:
            print(col.OKGREEN + f">> {data}" + col.ENDC)
 

def pic_send(x,y = 0):
    t.sleep(0.02)
    pic.write(chr(x).encode('charmap'))
    if y:
        print(f"SENT > {x}")



def init():
    global pic
    if plat.system() ==  'Linux':
        print(col.OKBLUE + "You are on Linux" + col.ENDC) 
        path = input(col.OKGREEN + f"Input path to USB2UART module [Default is {default_path_linux}]\n" + col.ENDC)
        
        if path == '':
            path = default_path_linux

    else:   # must be Windows
        print(col.OKBLUE + "You are on Windows" + col.ENDC) 
        path = input(col.OKGREEN + f"Input path to USB2UART module [Default is {default_path_win}]\n" + col.ENDC)
        
        if path == '':
            path = default_path_linux
        

    try:
        pic = s.Serial(path, 115200, timeout=.1)
    except:
        print(col.FAIL + f"Nothing on {path}, exiting..." + col.ENDC)  
        os._exit(os.EX_OK)     

 
    t.sleep(0.1)
    print(col.OKGREEN + "INIT DONE!" + col.ENDC)


def menu_and_choice():
    print("\n\n0. tst")
    print("1. tst1")
    print("2. tst2")
    print("3. tst3")
    
   
    choice = int(input(">> "))
 
    if choice == 0:
        tst()
 
    elif choice == 1:
        pic_send(65)
        pic_send(66)
        pic_send(67)
 
    elif choice == 2:
        pic_send(65)
        pic_send(66)
        pic_send(67)
 
    elif choice == 3:
        pic_send(65)
        pic_send(66)
        pic_send(67)


init()
thread = threading.Thread(target=get_data)
thread.start()

while True:
    menu_and_choice()