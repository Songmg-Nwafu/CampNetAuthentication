from subprocess import Popen, check_output, PIPE
from pywifi import PyWiFi
from pywifi import const
import time
import os
import re

# 0 const.IFACE_DISCONNECTED
# 1 const.IFACE_SCANNING
# 2 const.IFACE_INACTIVE
# 3 const.IFACE_CONNECTING
# 4 const.IFACE_CONNECTED

class WifiChoice(object):
    def __init__(self) -> None:
        self.iface = PyWiFi().interfaces()[0]

    def getCurrentSSID(self):
        cmd = 'netsh wlan show interfaces'
        result = os.popen(cmd)
        text = result.read()
        result.close()
        text = text.split('\n')
        # result = os.popen(cmd)
        # text = result.read().split('\n')
        # result.close()
        for i in text:
            if 'SSID' in i :
                ret = i.strip('\r').replace(' ','')
                break
        return ret[5:]

    def getWifiProfile(self):
        cmd = 'netsh wlan show profile'
        result = os.popen(cmd)
        text = result.read()
        result.close()
        lst = text.split('\n')
        ssid = []
        for i in range(len(lst)):
            t = re.search("(?<= : ).*", lst[i])
            if t is not None:
                ssid.append(t[0].encode('utf-8').decode('ansi'))
        return ssid

    def getAvailableWifi(self):
        self.iface.scan()
        time.sleep(3)
        wifi_set = set()
        for w in self.iface.scan_results():
            ssid_and_signal = w.ssid.encode('raw_unicode_escape').decode('utf-8')
            wifi_set.add(ssid_and_signal)
        wifi_list = list(wifi_set)
        return wifi_list
        # cmd = "netsh wlan show network"
        # text = self.run_silently(cmd)
        # print(text)
        # result = os.popen(cmd)
        # text = result.read()
        # result.close()
        # wifi_list = re.findall(r"SSID [\d] : (.*?)\n", text, re.MULTILINE|re.DOTALL)
        # temp = []
        # for i in wifi_list:
        #     if i:
        #         temp.append(i.encode('utf-8').decode('ansi'))
        # return temp

    def getStatus(self):
        retry = 5
        while retry > 0:
            if self.iface.status() == const.IFACE_CONNECTED:
                return 1
            elif self.iface.status() == const.IFACE_DISCONNECTED:
                return 0
            elif self.iface.status() == const.IFACE_SCANNING or self.iface.status() == const.IFACE_CONNECTING:
                retry -= 1
                time.sleep(2)
            elif self.iface.status() == const.IFACE_INACTIVE:
                return -1
        return -1

    def connect(self, ssid):
        cmd = 'netsh wlan connect name="%s"' % ssid
        result = os.popen(cmd)
        text = result.read()
        result.close()
        text = text.strip('\n')
        return text

    def makeChoice(self):
        status = self.getStatus()
        if status == -1:
            return 0, 'Inactive or unstable network!'
        if status:
            if 'NWAFU' not in self.getCurrentSSID():
                return 0, 'Free network connected.'
            return 2, 'Check camp net.'
        wifi_list = self.getWifiProfile()
        if 'NWAFU' in wifi_list:
            wifi_list.remove('NWAFU')
        if 'NWAFU-HW' in wifi_list:
            wifi_list.remove('NWAFU-HW')
        available_list = self.getAvailableWifi()
        for ssid in available_list:
            if ssid in wifi_list:
                return 1, ssid
        if 'NWAFU' in available_list:
            return 1, 'NWAFU'
        if 'NWAFU-HW' in available_list:
            return 1, 'NWAFU-HW'