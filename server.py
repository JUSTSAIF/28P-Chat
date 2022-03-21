from flask import Flask, request,json
from stem.control import Controller
import modules as md
import os,sys

try:
	if sys.argv[1] != "e4oyBHK7YPBj7Tvj":
		sys.exit()
except:sys.exit()

try:
    # Set Cmd Title & Style
    os.system("title Creating Your Host on Tor Service...")
    os.system("color 2 & mode con: cols=100 lines=40")
    try:config   = json.loads(md.ConfigFile().GetConfig())
    except:config   = md.ConfigFile().GetConfig()

    # -=-=-=-=-= Start Server =-=-=-=-=-
    app = Flask("28P-Chat")
    @app.route('/',methods=['GET'])
    def index():
        return json.dumps({"my_name":config['name'],"peer_host":config['peerHost'],"my_host":config['myHost']})
    @app.route('/send',methods=['GET'])
    def send():
        try:
            msg = str(request.args.get('msg'))
            name = str(request.args.get('name')) if len(str(request.args.get('name'))) > 0 else  "UNKNOWN"
            host = str(request.args.get('host'))
            if (msg != None) or (msg != ""):
                send_data = {"msg":msg,"name":name,"host":host,"me":""}
                config['peerHost'] = host
                md.ConfigFile().EditConfFile(data=config)
                msg = open("msg.json",'w')
                msg.write(json.dumps(send_data))
                msg.close()
                return {"msg_send":True}
            return {"msg_send":False}
        except:return {"msg_send":False}
    with Controller.from_port() as controller:
            controller.authenticate()
            pr_key = config['myPrivate_key']
            if(pr_key == "ED25519-V3"):
                response = controller.create_ephemeral_hidden_service({80: 5000},key_content = 'ED25519-V3',await_publication = True)
                config['myHost'] = response.service_id
                config['myPrivate_key'] = response.private_key
                md.ConfigFile().EditConfFile(data=config)
            else:
                response = controller.create_ephemeral_hidden_service({80: 5000}, await_publication = True,key_type="ED25519-V3",key_content=pr_key)
            print("Tor Service Id :: %s" % response.service_id)
            os.system("title Tor Service Created Successfully...")
            try:
                app.run(threaded=True)
                os.system("title Running...")
            finally:print(" >> Shutting ....")
except:
    os.system("title Tor Service Failed to Start")
    print("\u001b[31m \n\n   Tor Service Failed to Start.\u001b[33m \n\n    *) Be Sure Tor Browser is Running\n    *) Try restarting Tor Browser and Terminate tor.exe from Task Manager,\n    *) Restart this Program and Try Again.")
    input("\n\n \u001b[37m Press Enter to Exit 0w0")
    sys.exit()