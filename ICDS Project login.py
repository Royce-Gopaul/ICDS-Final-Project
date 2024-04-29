# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 11:43:49 2024

@author: royce
"""

# import all the required modules
import threading
import select
from tkinter import *
from tkinter import font
from tkinter import ttk
from chat_utils import *
import json
from tkinter.messagebox import showerror, showinfo
import ast

# GUI class for the chat
class GUI:
    # constructor method
    def __init__(self, send, recv, sm, s):
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
        self.send = send
        self.recv = recv
        self.sm = sm
        self.socket = s
        self.my_msg = ""
        self.system_msg = ""

    def login(self):
        # login window
        self.login = Toplevel()

        # set the title
        self.login.title("Login")
        self.login.resizable(width=False, height=False)
        self.login.configure(width=900, height=600)

        # create a Label for log in prompt
        self.pls = Label(self.login, text="Please login to continue", justify=CENTER, font="Helvetica 14 bold")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        # create a Label for user name
        self.labelName = Label(self.login, text="Name: ", font="Helvetica 14")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        # create a entry box for typing the message
        self.entryName = Entry(self.login, font="Helvetica 14")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()

        # create a label for password prompting
        self.labelPassword = Label(self.login, text="Password: ", font="Helvetica 14")
        self.labelPassword.place(relheight=0.2, relx=0.1, rely=0.4)

        # create an entry box for password
        self.entryPass = Entry(self.login, font="Helvetica 14")
        self.entryPass.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.4)
        self.entryPass.focus()

        # create a Log in button
        self.Login = Button(self.login, text="LOG IN", font="Helvetica 14 bold",
                            command=lambda: self.goAhead(self.entryName.get(), self.entryPass.get()))
        self.Login.place(relx=0.1, rely=0.55)

        # create a sign up button
        self.signUp = Button(self.login, text="SIGN UP", font="Helvetica 14 bold",
                             command=lambda: self.sign_up(self.entryName.get(), self.entryPass.get()))
        self.signUp.place(relx=0.7, rely=0.55)

        self.Window.mainloop()

    def goAhead(self, name, password):
        # now time check for both name and password before proceeding
        if len(name) and len(password):
            # dump in name and password
            msg = json.dumps({"action": "login", "name": name, "password": password})
            self.send(msg)
            # grab the response
            response = json.loads(self.recv())
            # if status or response returns "success"
            if response["status"] == 'success':
                self.login.destroy()
                self.sm.set_state(S_LOGGEDIN)
                self.sm.set_myname(name)
                # generate ppn upon login
                # get n, e
                n, e = self.sm.get_n_e()
                self.send(json.dumps({"action": "send n,e", "n": n, "e": e}))
                self.layout(name)
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, menu + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)
                process = threading.Thread(target=self.proc)
                process.daemon = True
                process.start()
            # if failed to login, show an error message
            elif response['status'] == 'failed':
                showerror(title="Login Failed", message="Incorrect username or password.")
                return

    def sign_up(self, name, password):
        """
        When "sign up" button/widget is pressed, this event 
        controls the process of signing up and keeping records of past sign ups
        """
        with open("userPasswordBank.txt") as f:
            # passBank dict
            passBank: dict = ast.literal_eval(f.read())
        
        # don't allow duplicate usernames or passwords (for simplicity)
        if name in passBank.keys() or password in passBank.values():
            showerror(title="Login failed", message="Username or Password is already in use.")
            return

        # if not caught by above check, execute below
        with open("userPasswordBank.txt", "w") as f:
            # store name: password pair into password bank txt file for later use
            passBank[name] = password
            f.write(str(passBank))
        
        # display a success message
        showinfo(title="You have successfully signed up", message="Click 'Log in' to enter the chat room!")

    # The main layout of the chat
    def layout(self, name):
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=True, height=True)
        self.Window.configure(width=900, height=800, bg="#17202A")
        self.labelHead = Label(self.Window, bg="#17202A", fg="#EAECEE", text=self.name, font="Helvetica 13 bold", pady=5)
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window, width=450, bg="#ABB2B9")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        self.textCons = Text(self.Window, width=20, height=2, bg="#17202A", fg="#EAECEE", font="Helvetica 14", padx=5, pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        self.labelBottom = Label(self.Window, bg="#ABB2B9", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)
        self.entryMsg = Entry(self.labelBottom, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()
        self.entryMsg.bind('<Return>', lambda event: self.sendButton(self.entryMsg.get()))
        self.buttonMsg = Button(self.labelBottom, text="Send", font="Helvetica 10 bold", width=20, bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.textCons.config(cursor="arrow")
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)
        self.searchBar = Entry(self.labelHead, bg="#2C3E50", fg="#EAECEE", font="Helvetica 13", width=20)
        self.searchBar.place(relx=0.8, relheight=1, relwidth=0.2)
        self.searchBar.bind('<Return>', lambda event: self.searchButton(self.searchBar.get()))

    def searchButton(self, term):
        self.my_msg = term
        self.searchBar.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.send(json.dumps({"action": "search", "target": term}))
        msg = json.loads(self.recv())["results"]
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def sendButton(self, msg):
        self.my_msg = msg
        self.entryMsg.delete(0, END)
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, msg + "\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def proc(self):
        while True:
            read, write, error = select.select([self.socket], [], [], 0)
            peer_msg = []
            if self.socket in read:
                peer_msg = self.recv()
            if len(self.my_msg) > 0 or len(peer_msg) > 0:
                self.system_msg = self.sm.proc(self.my_msg, peer_msg)
                self.my_msg = ""
                self.textCons.config(state=NORMAL)
                self.textCons.insert(END, self.system_msg + "\n\n")
                self.textCons.config(state=DISABLED)
                self.textCons.see(END)

    def run(self):
        self.login()


# Assuming you have defined these variables elsewhere in your code
send = ... # Your send function
recv = ... # Your recv function
sm = ...   # Your sm object
s = ...    # Your socket object
menu = "Welcome to the chat room!"

# create a GUI class object
if __name__ == "__main__":
    g = GUI(send, recv, sm, s)
    g.run()
