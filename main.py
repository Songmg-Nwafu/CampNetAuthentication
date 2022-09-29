import os
import time
import CampNet
from WifiChoice import WifiChoice

username = '' #学号
password = ''

def netest():
    a = os.system("ping baidu.com -n 1")
    return True if a == 0 else False

def NWAFU():
    a = CampNet.IfLogin(username, password)
    retry = 3
    while retry > 0:
        try:
            if a.getStatus():
                msg = a.doLogin()
                if msg[1]:
                    print('Successful!')
                else:
                    print('Failed!')
                print(msg[0])
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
        NWAFU()
        return 0

if __name__ == '__main__':
    wifi = WifiChoice()
    while True:
        main_work(wifi)
        time.sleep(10)