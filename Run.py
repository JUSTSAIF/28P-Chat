import os,time,argparse,json
import modules as md
import sys

# -=-=-=-=-=-=-=-=-=-=-=-= Arg Commands -=-=-=-=-=-=-=-=-=-=-=-= #
parser = argparse.ArgumentParser(description='There\'s no Help -_- !')
parser.add_argument('--conf',nargs='*', help='get confing data\n How To Work : run.py --conf')
parser.add_argument('--reconfig',nargs='*', help='reCreate Config File With basics info,\nHow To Work? = run.py --reconfig')
parser.add_argument('--peerhost',nargs='*', help='update peer host,\nHow To Work? = run.py --peerhost "yourFriendHost"')
args = parser.parse_args()


if(os.path.exists("data.enc") != True):
    md.ConfigFile().EditConfFile(resetDefault=True)


try:config   = json.loads(md.ConfigFile().GetConfig())
except:config   = md.ConfigFile().GetConfig()
_all     = md._all()

#  -=-=-=-=-= LOGIN =-=-=-=-=-
login = _all.login()
if  "Logged In Successfully" not in login:
    print(login)
    sys.exit()

for arg in vars(args):
    #  -=-=-=-=-= Get conf =-=-=-=-=-
    if arg == "conf" and args.conf != None:
        print(config)
        sys.exit()
    #  -=-=-=-=-= peerhost =-=-=-=-=-
    elif arg == "peerhost" and args.peerhost != None:   
        host = "http://"+args.peerhost[0]+".onion"
        chk  = _all.check_peerHost(host)
        if(chk == True):
            config['peerHost'] = args.peerhost[0]
            chk = md.ConfigFile().EditConfFile(data=json.dumps(config))
            if(chk):print("\033[1;32;40m has been added successfully \033[1;37;40m")
            else:print("\033[1;31;40m Failed to add ! \033[1;37;40m")
            sys.exit()
        else:print(chk)
        sys.exit()
    #  -=-=-=-=-= reConfig =-=-=-=-=-
    elif arg == "reconfig" and args.reconfig != None:
        print("GG")
        try:
            md.ConfigFile().EditConfFile(resetDefault=True)
            print("\033[1;32;40m has been added successfully \033[1;37;40m")
            sys.exit()
        except:sys.exit()

#  -=-=-=-=-= Run =-=-=-=-=-
os.system('start py server.py e4oyBHK7YPBj7Tvj') # Exe : start server.exe e4oyBHK7YPBj7Tvj
time.sleep(2)
os.system('start py responder.py e4oyBHK7YPBj7Tvj') # Exe : start responder.exe e4oyBHK7YPBj7Tvj
time.sleep(2)
os.system('start py sender.pyw e4oyBHK7YPBj7Tvj') # Exe : start sender.exe e4oyBHK7YPBj7Tvj
