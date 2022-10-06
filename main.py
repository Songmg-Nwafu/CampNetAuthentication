import time
import json
import CampNet
import subprocess
from WifiChoice import WifiChoice

def netest():
    try:
        subprocess.run('ping baidu.com -n 1', stdout=subprocess.PIPE).check_returncode()
    except subprocess.CalledProcessError:
        return False
    return True

def NWAFU():
    a = CampNet.IfLogin(username=username, password=password)
    try:
        msg = a.doLogin()
        if msg[1]:
            print('Successful!')
        else:
            print('Failed!')
        print(msg[0])
        return 0
    except Exception:
        print(Exception)
        return 1

def main_work(wifi, autoConnect):
    if netest():
        return 0
    choice, msg = wifi.makeChoice()
    if choice != 2 and not autoConnect:
        return 0
    if choice == 1:
        print(wifi.connect(msg))
        time.sleep(2)
        if 'NWAFU' in msg:
            if NWAFU():
                raise Exception("CampNet Authentication error!")
        return 0
    if choice == 2:
        print(msg)
        if NWAFU():
            raise Exception("CampNet Authentication error!")
        return 0

if __name__ == '__main__':
    f = open('config.json', 'r')
    config = json.load(f)
    f.close()
    if config['username'] == '' or config['password'] == '':
        raise Exception("Missing username or password!")
    username = config['username']
    password = config['password']
    wifi = WifiChoice()
    while True:
        main_work(wifi, config['Auto_Connect'])
        time.sleep(config['sleep_time'])