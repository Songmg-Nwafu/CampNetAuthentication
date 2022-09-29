import time
import CampNet
import WifiChoice

username = '' #学号
password = ''

def NWAFU():
    a = CampNet.IfLogin(username, password)
    if a.getStatus():
        msg = a.doLogin()
        if msg[1]:
            print('Successful!')
        else:
            print('Failed!')
        print(msg[0])

def main_work():
    wifi = WifiChoice()
    choice, msg = wifi.makeChoice()
    if not choice:
        print(msg)
        return -1
    if choice == 1:
        print(wifi.connect(msg))
        if 'NWAFU' in msg:
            NWAFU()
        return 0
    if choice == 2:
        NWAFU()
        return 0

if __name__ == '__main__':
    while True:
        main_work()
        time.sleep(10)