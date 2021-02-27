from flask import Flask, session, redirect, url_for, escape, request,json
from stem.control import Controller
from stem import Signal
from stem.process import launch_tor_with_config
import modules as md
import os,subprocess

# Set Cmd Title & Style
os.system("title Creating Your Host on Tor Service...")
os.system("color 2 & mode con: cols=100 lines=40")
# -=-=-=-=-=-=-= Start Work =-=-=-=-=-=-=-
errMsg = "file not exist, are you sure tor is installed?\n if installed set your Tor Path by :\n run.py --tor-path \"X://xxx/TorBrowser/Tor/tor.exe\" "
try:config   = json.loads(md.ConfigFile().GetConfig())
except:config   = md.ConfigFile().GetConfig()

tor_path = config['tor_path']
if(tor_path == ""):tor_path = md._all().guessTorPath()
if os.path.isfile(tor_path) and "tor.exe" in tor_path:
    for i in os.popen("tasklist"):
        if("tor.exe" in i):
            os.system("taskkill /F /IM tor.exe")
    launch_tor_with_config(tor_cmd=tor_path , config={'ControlPort': '9051'})
    # -=-=-=-=-= Start Server =-=-=-=-=-
    app = Flask("28P-Chat")
    @app.route('/send',methods=['GET'])
    def send():
        msg = request.args.get('msg')
        name = request.args.get('name')
        # host = request.args.get('host')
        if (msg != None) or (msg != ""):
            send_data = {"msg":msg,"name":"","host":"","me":""}
            if(name != None) :send_data['name'] = name
            # if(host != None) :
            #     config['peerHost'] = host
            #     md.ConfigFile().EditConfFile(data=config)
            msg = open("msg.json",'w')
            msg.write(json.dumps(send_data))
            msg.close()
            return {"msg_send":True}
        return {"msg_send":False}
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
        try:app.run(threaded=True)
        finally:print(" >> Shutting ....")
else:
    print(errMsg)
    input("Press Enter To Close UwU ")
    exit()
