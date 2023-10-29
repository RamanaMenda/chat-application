import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = 'localhost'
PORT = 45555

class Client:
    def __init__(self,host,port):
        self.soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.soc.connect((host, port))

        msg = tkinter.Tk(className='Group chat')
        msg.withdraw()

        self.name = tkinter.simpledialog.askstring('NAME','Please enter a name:',parent = msg)

        self.gui_status  = False
        self.running = True

        gui = threading.Thread(target= self.guistart )
        receive = threading.Thread(target= self.receive)
        gui.start()
        receive.start()

    def guistart(self):
        self.win = tkinter.Tk(className='Group chat')
        self.win.configure(bg='lightblue')

        self.chat_label = tkinter.Label(self.win,text = 'Chat Area')
        self.chat_label.config(font = ('arial',13))
        self.chat_label.pack(padx=20,pady=5)

        self.chat_area = tkinter.scrolledtext.ScrolledText(self.win,bg='lightgray')
        self.chat_area.pack(padx=20,pady=5)
        self.chat_area.config(state = 'disable')

        self.msg_label = tkinter.Label(self.win, text='Message:', bg='lightgray')
        self.msg_label.config(font=('arial', 13))
        self.msg_label.pack(padx=20, pady=5)

        self.msg_input = tkinter.Text(self.win,height = '5')
        self.msg_input.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.win,text = 'send',command = self.send)
        self.send_button.config(font =('arial',13))
        self.send_button.pack(padx=20, pady=5)

        self.gui_status = True
        self.win.protocol('WM_DELETE_WINDOW',self.stop)

        self.win.mainloop()

    def receive(self):
        while self.running:
            try:
                msg = self.soc.recv(1024)
                msg = msg.decode('utf-8')
                if msg == "NAME:":
                    self.soc.send(self.name.encode('utf-8'))
                else:
                    if self.gui_status:
                        self.chat_area.config(state = 'normal')
                        self.chat_area.insert('end',msg)
                        self.chat_area.yview('end')
                        self.chat_area.config(state='disable')
            except ConnectionAbortedError:
                break
            except Exception as e:
                print(str(e))
                self.soc.close()
                break


    def send(self):
        msg = f"{self.name} :{self.msg_input.get('1.0','end')}"
        self.soc.send(msg.encode('utf-8'))
        self.msg_input.delete('1.0','end')

    def stop(self):
        self.running =False
        self.win.destroy()
        exit(0)

client = Client(HOST,PORT)




