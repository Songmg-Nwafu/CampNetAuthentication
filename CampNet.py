from hashlib import sha1
import requests
import socket
import js2py
import time
import json
import re


class SRUN_Login(object):
	ERROR = 0
	LOGIN_OK = 1
	ALREADY_ONLINE = 2

	get_token_url = "http://172.26.8.11/cgi-bin/get_challenge"
	login_url = "http://172.26.8.11/cgi-bin/srun_portal"
	ac_id = '1'
	n = '200'
	type = '1'
	headers = {
			"Host": "172.26.8.11",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
	}

	def __init__(self, username, password):
		self.username = username
		self.ip = self.getIP()
		self.token = self.getToken()
		self.hmd5 = self.md5(password, self.token)
		self.userInfo = {
			'username': username,
			'password': password,
			'ip': self.ip,
			'acid': '1',
			'enc_ver': 'srun_bx1'
		}
		self.i = self.getUserInfoEncode()
		self.EncodedChksum = sha1(self.make_chksum().encode('utf-8')).hexdigest()

	def getIP(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("8.8.8.8", 80))
		return s.getsockname()[0]

	def getTimeStamp(self):
		return str(int(time.time() * 1000))

	def md5(self, n, t='', r=''):
		context = js2py.EvalJs()
		context.execute(open('js\\md5.js','r',encoding='utf-8').read())
		if r:
			result = context.A(n, t, r)
		elif t:
			result = context.A(n, t)
		else:
			result = context.A(n)
		return result

	def Encode(self, str): 
		context = js2py.EvalJs()
		context.execute(open('js\\encode.js','r',encoding='utf-8').read())
		return context.encode(str, self.token)

	def b64encode(self, str):
		context = js2py.EvalJs()
		context.execute(open('js\\base64.js','r',encoding='utf-8').read())
		return context._encode(str)

	def getToken(self):
		params = {
			'callback': 'jQuery112405532615789910869_' + self.getTimeStamp(),
			'username': self.username,
			'self.ip': self.ip
		}
		response = requests.get(self.get_token_url, headers=self.headers ,params=params).text
		response = re.search(r"[{](.*?)[}]", response).group()
		response = json.loads(response)
		print(response)
		return response['challenge']

	def getUserInfoEncode(self):
		info = str(self.userInfo).replace('\'','\"').replace(' ','')
		return '{SRBX1}' + self.b64encode(self.Encode(info))	

	def make_chksum(self):
		self.chksum = self.token + self.username
		self.chksum += self.token + self.hmd5
		self.chksum += self.token + self.ac_id
		self.chksum += self.token + self.ip
		self.chksum += self.token + self.n
		self.chksum += self.token + self.type
		self.chksum += self.token + self.i
		return self.chksum

	def login(self):
		params = {
			'callback': 'jQuery1124044585671652636405_' + self.getTimeStamp(),
			'action': 'login',
			'username': self.username,
			'password': '{MD5}' + self.hmd5,
			'os': 'Windows 10',
			'name': 'Windows',
			'double_stack': '0',
			'chksum': self.EncodedChksum,   #utf-8 gbk ... feel free to choose!
			'info': self.i,
			'ac_id': self.ac_id,
			'ip': self.ip,
			'n': self.n,
			'type': self.type,
			'_': self.getTimeStamp()
		}
		response = requests.get(self.login_url, headers=self.headers ,params=params).text
		response = re.search(r"[{](.*?)[}]", response).group()
		response = json.loads(response)
		if response['error'] == 'ok':
			if response['suc_msg'] == 'login_ok':
				return self.LOGIN_OK
			elif response['suc_msg'] == 'self.ip_already_online_error':
				return self.ALREADY_ONLINE
			else:
				return 'Unexpected suc_msg'
		else:
			return self.ERROR


class IfLogin(object):

	get_status_url = "http://172.26.8.11/cgi-bin/rad_user_info"
	headers = {
			"Host": "172.26.8.11",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
	}

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def getStatus(self):
		params = {
			'callback': 'jQuery112402812915',
			'_': str(int(time.time()))
		}
		response = requests.get(self.get_status_url, headers=self.headers, params=params).text
		response = re.search(r'"error":"(.*?)"', response).group()   #认证前: "error":"not_online_error"
		response = response[9:-1]
		if response == "ok":
			return 0
		return 1

	def doLogin(self):
		if self.getStatus():
			srun =  SRUN_Login(self.username, self.password)
			suc_msg = srun.login()
			if suc_msg == srun.ERROR:
				return ['Campus network authentication failed!', 0]
			elif suc_msg == srun.LOGIN_OK:
				return ['Authenticated!', 1]
			elif suc_msg == srun.ALREADY_ONLINE:
				return ['WARNING: Repeated login operations!', 1]
			else:
				return ['Error: Unexpected suc_msg!', 0]
		else:
			return ['Already logged in!', 1]