import time as t
import serial as s
import os
import platform as plat
import threading
from colorama import Fore, Back, Style

default_path_linux = "/dev/ttyUSB0"
default_path_win = "COM1"


def get_data():
    global pic
    while True:
        try:
            data = pic.readline()
        except:
            print(Fore.RED + "Disconnected")
            os._exit(os.EX_OK)
        if data:
            print(Fore.GREEN + f">> {data}" + Fore.RESET)
 

def pic_send(x,y = 0):
    t.sleep(0.02)
    pic.write(chr(x).encode('charmap'))
    if y:
        print(f"SENT > {x}")



def init():
    global pic
    if plat.system() ==  'Linux':
        print(Fore.BLUE + "You are on Linux") 
        path = input(Fore.GREEN + f"Input path to USB2UART module [Default is {default_path_linux}]\n")
        
        if path == '':
            path = default_path_linux

    else:   # must be Windows
        print(Fore.BLUE + "You are on Windows") 
        path = input(Fore.GREEN + f"Input path to USB2UART module [Default is {default_path_win}]\n")
        
        if path == '':
            path = default_path_win
        

    try:
        pic = s.Serial(path, 115200, timeout=.1)
    except:
        print(Fore.RED + f"Nothing on {path}, exiting...")  
        os._exit(os.EX_OK)     

 
    t.sleep(0.1)
    print(Fore.GREEN + "INIT DONE!" + Fore.RESET)


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