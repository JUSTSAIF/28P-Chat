import json,os,time,threading
import modules as md

# Set Cmd Title & Style
os.system("28P - Chat")
os.system("color 5 & mode con: cols=90 lines=50")

# Styling :::
print('''
	  .d888b. .d888b. d8888b.             .o88b. db   db  .d8b.  d888888b
	  VP  `8D 88   8D 88  `8D            d8P  Y8 88   88 d8' `8b `~~88~~'
	     odD' `VoooY' 88oodD'            8P      88ooo88 88ooo88    88   
	   .88'   .d~~~b. 88~~~     C8888D   8b      88~~~88 88~~~88    88   
	  j88.    88   8D 88                 Y8b  d8 88   88 88   88    88   
	  888888D `Y888P' 88                  `Y88P' YP   YP YP   YP    YP  v0.1
	============================== By - Mr28 ================================\n\n\n''')


config   = md.ConfigFile().GetConfig()
# -================== Start App ==================-

def update():
	msgFile = {"msg":"","name":"","host":"","me":""}
	setOld = open('msg.json','w')
	setOld.write(json.dumps(msgFile))
	setOld.close()

def getNewMsg():
	if(os.path.getsize("msg.json")>9):
		openMsgFile = open('msg.json','r')
		msgFile 	= json.loads(openMsgFile.read())
		openMsgFile.close()
		msg     	= msgFile['msg']
		name    	= msgFile['name']
		me      	= msgFile['me']
		if(msg != ""):
			peerName  ="UNKNOWN"
			if(name != ""):peerName = name
			threading.Thread(print("        "+str(peerName)+" >> "+str(msg)))
		if(me != ""):
			threading.Thread(print("        Me  >> %s "%me))
		threading.Thread(update())
try:
	update()
	while(True):
		getNewMsg()
		time.sleep(1)
finally:
	print("\033[1;36;40m Closing ...")
	time.sleep(1)
	threading.Thread(update())
	exit()
