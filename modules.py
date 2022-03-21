from cryptography.fernet import Fernet 
from getpass import getpass
import json,hashlib,os,json
from requests_tor import RequestsTor

rt = RequestsTor()


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
		defData = self.key.encrypt(json.dumps({"name":"","password": "","peerHost":"","myHost":"","myPrivate_key":"ED25519-V3"}).encode())
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
			if(rt.get(host+"/send").status_code == 200):return True
			else:return "\033[1;31;40m Failed to add ! \033[1;37;40m"
		except:return "\033[1;31;40m Failed to add ! \033[1;37;40m"
	def SendMsg(self,msg=None):
		try:conf   = json.loads(ConfigFile().GetConfig())
		except:conf   = ConfigFile().GetConfig()
		try:
			response = rt.get("http://"+conf['peerHost']+".onion/send?msg="+msg+"&host="+conf['myHost']+"&name="+conf['name']).status_code
			if response == 200 :return True
			else:return False
		except:
			return False