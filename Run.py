import os,time,sys,argparse,json,hashlib,string
import modules as md


# -=-=-=-=-=-=-=-=-=-=-=-= Arg Commands -=-=-=-=-=-=-=-=-=-=-=-= #
parser = argparse.ArgumentParser(description='There\'s no Help -_- !')
parser.add_argument('--tor-path',nargs='*', help='Tor Browser Path')
parser.add_argument('--conf',nargs='*', help='get confing data\n work : run.py --conf your-password-here')
parser.add_argument('--reconfig',nargs='*', help='reCreate Config File With basics info,\nWork? = run.py --reconfig q')
parser.add_argument('--peer-host',nargs='*', help='update peer host,\nWork? = run.py --peer-host yourFriendHost')
args = parser.parse_args()

#  -=-=-=-=-= reConfig =-=-=-=-=-
if args.reconfig is not None:
    if(args.reconfig[0] == "q"):
        md.ConfigFile().EditConfFile(resetDefault=True)
        print("done")
        exit()
    exit()

if(os.path.exists("data.enc") !=True):
    print("Please Reconfigure use : run.py --reconfig q")
    exit()


try:config   = json.loads(md.ConfigFile().GetConfig())
except:config   = md.ConfigFile().GetConfig()
_all     = md._all()
login = _all.login()
if  "Logged In Successfully" not in login:
    print(login)
    exit()
 
#  -=-=-=-=-= tor-path =-=-=-=-=-
if args.tor_path is not None:
    try:
        path = args.tor_path[0]
        if(os.path.exists(path)):
            config['tor_path'] = path
            md.ConfigFile().EditConfFile(data=json.dumps(config))
            print("Done .")
            exit()
        else:
            print("\033[1;31;40m File not Exist, Incorrect Tor File \033[1;37;40m")
            exit()
    except(Exception):print("add the path inside \"\" ")
#  -=-=-=-=-= Get conf =-=-=-=-=-
if args.conf is not None:
    pass__=''
    for i in args.conf :pass__ += i
    pass_ = hashlib.md5(pass__.encode()).hexdigest()
    if(pass_ == config['password']):
        print(config)
        exit()
    else:
        print("Incorrect Password")
        exit()
#  -=-=-=-=-= peer_host =-=-=-=-=-
if args.peer_host is not None:
    host = "http://"+args.peer_host[0]+".onion"
    chk  = _all.check_peerHost(host)
    if(chk == True):
        config['peerHost'] = host.replace(".onion","").replace("http://","")
        chk = md.ConfigFile().EditConfFile(data=json.dumps(config))
        if(chk):print("\033[1;32;40m has been added successfully \033[1;37;40m")
        else:print("\033[1;31;40m Failed to add ! \033[1;37;40m")
        exit()
    else:print(chk)
    exit()
    

# Index Work 
os.system('start py server.py')
time.sleep(2)
os.system('start py responder.py')
time.sleep(2)
os.system('start py sender.py')
