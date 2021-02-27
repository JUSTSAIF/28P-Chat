from tkinter import CENTER,Text,Button,messagebox
import modules as md
import tkinter as tk
import json
# Conf & styling
root = tk.Tk()
root.geometry('840x230')
root.configure(bg="black")
root.title('28P - Chat :: Your Msg Input')
root.resizable(width=False, height=False)
heading = tk.Label(root, text="28P - Chat",bg="black",fg="white")
heading.config(font=("Courier", 22))
heading.config(anchor=CENTER)
heading.pack()
msgL = tk.Label(root, text="Enter Your Message",bg="black",fg="white")
msgL.config(font=("Courier", 14),anchor=CENTER)
msgL.pack()
msg = Text(root, height=5, width=66,font=("Courier", 14))
msg.pack()


def sendT():
    try:config   = json.loads(md.ConfigFile().GetConfig())
    except:config   = md.ConfigFile().GetConfig()
    msgContent = msg.get(1.0,'end')
    if config['peerHost'] == "":
        messagebox.showinfo("Error",
        """
        there's no messages from peer to save him host,\n
        And you also did not set peer host .\n
        so please set peer host use : \n
        run.py --peer-host \n
        example :\n
        run --peer-host "facebookcorewwwi"\n
        set it without http:// & .onion\n""")
    md._all().SendMsg(msgContent)
    openMsgFile = open('msg.json','r')
    msgFile = json.loads(openMsgFile.read())
    openMsgFile.close()
    msgFile['me'] = msgContent
    setOld = open('msg.json','w')
    setOld.write(json.dumps(msgFile))
    setOld.close()

send = Button (root,activebackground='green',bg="purple",height=5, width=10,anchor=CENTER,text="Send",fg="white",command=lambda:sendT())

send.pack(pady=8)
root.mainloop()
