import time as t
import serial as s
import os
import platform as plat
import threading
from colorama import Fore, Back, Style
import math as m

default_path_linux = "/dev/ttyUSB0"
default_path_win = "COM22"

# -----------------  Comm ----------------- #
stop_msg = 109  # 'm'
start_msg = 77  # 'M'
get_data_stop = 0

vel_get_delay_s = 0.1
get_vel_stop_flg = 0


def int16_to_int(x):
    tmp1 = m.floor(x/256)
    tmp2 = x%256
    return tmp1, tmp2


def get_vel():
    while True:
        if get_vel_stop_flg != 1:
            pic_send(118)
            
        t.sleep(vel_get_delay_s)


def get_data():
    global pic, get_data_stop
    while True:
        try:
            data = pic.readline()
        except:
            print(Fore.RED + "Disconnected")
            os._exit(os.EX_OK)
        if data:
            if get_data_stop != 1:
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
    global get_data_stop, get_vel_stop_flg
    print("\n\n1. START")
    print("2. STOP")
    print("3. PID set")
    print("4. Set speed")
    print("5. Get speed")

    
   
    choice = int(input(">> "))
 
    if choice == 1:
        get_vel_stop_flg = 1
        t.sleep(0.1)

        pic_send(start_msg)

        speed = int(input("Input speed [0 - 6000]"))
        tmp1, tmp2 = int16_to_int(speed)

        pic_send(tmp1)
        pic_send(tmp2)
        t.sleep(0.1)
        get_vel_stop_flg = 0


 
    elif choice == 2:
        get_vel_stop_flg = 1
        t.sleep(0.1)
        pic_send(stop_msg)   # 'm'
        t.sleep(0.1)
        get_vel_stop_flg = 0
 
    elif choice == 3:
        get_data_stop = 1
        what_pid = int(input("1. Kp\n2. Ki\n3. Kd"))
        if what_pid == 1:
            new_kp = int(input("Input Kp\n")) 
            tmp1, tmp2 = int16_to_int(new_kp)
            get_vel_stop_flg = 1
            t.sleep(0.1)
            pic_send(112)
            pic_send(tmp1)
            pic_send(tmp2)
            t.sleep(0.1)
            get_vel_stop_flg = 0

        elif what_pid == 2:
            new_ki = int(input("Input Ki\n")) 
            tmp1, tmp2 = int16_to_int(new_ki)
            get_vel_stop_flg = 1
            t.sleep(0.1)
            pic_send(105)
            pic_send(tmp1)
            pic_send(tmp2)
            t.sleep(0.1)
            get_vel_stop_flg = 0

        elif what_pid == 3:
            new_kd = int(input("Input Kd\n")) 
            tmp1, tmp2 = int16_to_int(new_kd)
            get_vel_stop_flg = 1
            t.sleep(0.1)
            pic_send(100)
            pic_send(tmp1)
            pic_send(tmp2)
            t.sleep(0.1)
            get_vel_stop_flg = 0

        get_data_stop = 0

    elif choice == 4:
        pic_send(115)
        what_speed = int(input("What speed?"))
        tmp1, tmp2 = int16_to_int(what_speed)
        get_vel_stop_flg = 1
        t.sleep(0.1)
        pic_send(tmp1)
        pic_send(tmp2)
        t.sleep(0.1)
        get_vel_stop_flg = 0



init()
thread = threading.Thread(target=get_data)
thread.start()

thread_get_vel = threading.Thread(target=get_vel)
thread_get_vel.start()

while True:
    menu_and_choice()