import os
from sys import stderr
import time
import CampNet
import subprocess
from WifiChoice import WifiChoice

username = '' #学号
password = ''

def netest():
    try:
        subprocess.run('ping baidu.com -n 1', stdout=subprocess.PIPE).check_returncode()
    except subprocess.CalledProcessError:
        return False
    return True

def NWAFU():
    a = CampNet.IfLogin(username, password)
    retry = 1
    while retry > 0:
        try:
            msg = a.doLogin()
            if msg[1]:
                print('Successful!')
            else:
                print('Failed!')
            print(msg[0])
            break
        except:
            retry -=1

def main_work(wifi):
    if netest():
        return 0
    choice, msg = wifi.makeChoice()
    if not choice:
        print(msg)
        return -1
    if choice == 1:
        print(wifi.connect(msg))
        time.sleep(2)
        if 'NWAFU' in msg:
            NWAFU()
        return 0
    if choice == 2:
        print(msg)
        NWAFU()
        return 0

if __name__ == '__main__':
    wifi = WifiChoice()
    while True:
        main_work(wifi)
        time.sleep(10)