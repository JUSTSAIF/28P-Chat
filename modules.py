from cryptography.fernet import Fernet 
from torpy.http.requests import do_request, tor_requests_session
from requests import Request, Session
from stem.control import Controller
from cryptography.fernet import Fernet
from getpass import getpass
import json,stem,requests,base64,hashlib,shutil,os,time,subprocess,threading,json,sys,random
from stem.process import launch_tor_with_config

class ConfigFile:
	# key = Fernet.generate_key()
	def __init__(self): 
		confData = ""
		if os.path.exists('data.enc'):
			if os.path.getsize('data.enc')>10:confData = open("data.enc", "rb").read()
		self.key  = Fernet(b'9miE2mO1HTNGgfJIVuFk0AJ9Gazif_1t1cCQBb3oByE=')
		self.dataEnc =  confData
	def GetConfig(self):
		if(self.dataEnc == ""):return "err:: reconfig data"
		else:return json.loads(self.key.decrypt(self.dataEnc))
	def EditConfFile(self,resetDefault=False,data=False):
		confFile = open("data.enc", "w")
		defData = self.key.encrypt(json.dumps({"name":"","password": "","peerHost":"","myHost":"","myPrivate_key":"ED25519-V3","tor_path":_all().guessTorPath()}).encode())
		if(resetDefault == True):
			confFile.write(defData.decode())
			confFile.close()
			return True
		try:json.loads(json.dumps(data))
		except:return False
		if data == False:return False
		data = self.key.encrypt(json.dumps(data).encode())
		confFile.write(data.decode())
		confFile.close()
		return True

class _all:
	def guessTorPath(self):
		torPath=""
		torPath1  = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe')
		torPath2 = 'C:\\Program Files\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe'
		torPath3 = 'C:\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe'
		torPath4 = 'D:\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe'
		torPath5 = 'C:\\Program Files (x86)\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe'
		torPath6 = 'C:\\ProgramData\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe'
		torPath7 = "D:\\SAIF\\TOOLS\\Tor Browser\\Browser\\TorBrowser\\Tor\\tor.exe"
		if(os.path.exists(torPath1)):torPath=torPath1
		if(torPath == "" and os.path.exists(torPath2)):torPath=torPath2
		if(torPath == "" and os.path.exists(torPath3)):torPath=torPath3
		if(torPath == "" and os.path.exists(torPath4)):torPath=torPath4
		if(torPath == "" and os.path.exists(torPath5)):torPath=torPath5
		if(torPath == "" and os.path.exists(torPath6)):torPath=torPath6
		if(torPath == "" and os.path.exists(torPath7)):torPath=torPath7
		return torPath
	def login(self):
		try:conf   = json.loads(ConfigFile().GetConfig())
		except:conf   = ConfigFile().GetConfig()
		if conf == "err:: reconfig data":return conf
		if(conf['password'] == ""):
			name = input("Type Your Name ? >> ")
			password = hashlib.md5(input("Type New Password >> ").encode()).hexdigest()
			conPass = hashlib.md5(input("Confirm Password >> ").encode()).hexdigest()
			if password == conPass:
				conf['password'] = password
				conf['name'] = name
				ConfigFile().EditConfFile(data=json.dumps(conf))
				return "password created successfully, run it again to login"
			else:
				return "incorrect confirmed password, try again !!"
		else:
			password = hashlib.md5(getpass("Password >> ").encode()).hexdigest()
			return "Logged In Successfully" if password == conf['password']  else "Incorrect Password"
	def check_peerHost(self,host):
		try:
			try:config   = json.loads(ConfigFile().GetConfig())
			except:config   = ConfigFile().GetConfig()
			tor_path = config['tor_path']
			if(tor_path == ""):tor_path = self.guessTorPath()
			if os.path.isfile(tor_path) and "tor.exe" in tor_path and tor_path != "":
				for i in os.popen("tasklist"):
					if("tor.exe" in i):os.system("taskkill /F /IM tor.exe")
				launch_tor_with_config(tor_cmd=tor_path , config={'ControlPort': '9051'})
				proxies = {
					'http': "socks5h://localhost:9050",
					'https': "socks5h://localhost:9050"
				}
				if(requests.get(host+"/send", proxies=proxies).status_code == 200):return True
				else:return "\033[1;31;40m Failed to add ! \033[1;37;40m"
			else:return "\033[1;31;40m Tor Path Not Found ! \033[1;37;40m"
		except:return "Err:: Close your server if running & close tor browser too "
	def SendMsg(self,msg=None):
		try:conf   = json.loads(ConfigFile().GetConfig())
		except:conf   = ConfigFile().GetConfig()
		peer = conf['peerHost']
		try:
			proxies = {'http': "socks5h://localhost:9050",'https': "socks5h://localhost:9050"}
			response = requests.get("http://"+peer+".onion/send?msg="+msg+"&host="+conf['myHost']+"&name="+conf['name'], proxies=proxies).status_code
			if response == 200 :return True
			else:return False
		except:
			return False








