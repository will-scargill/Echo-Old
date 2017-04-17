from tkinter import *
from tkinter import messagebox
import sys
import socket
import threading
import sqlite3

#========================================
# SQLite Setup

conn = sqlite3.connect("database.db", check_same_thread=False)
c = conn.cursor()

tables = [
    {
        "name": "servers",
        "columns": "name TEXT, ip TEXT, port NUMBER"
    },
]

for table in tables:
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [
              table["name"]])
    data = c.fetchall()

    if len(data) <= 0:  # If table doesn't exist
        c.execute("CREATE TABLE " +
                  table["name"] + " (" + table["columns"] + ")")
        c.execute("INSERT INTO servers (name, ip, port) VALUES ('ECHO Official Server', '194.135.84.73', 6666)")
        conn.commit()
        



#========================================

def startchat(ip, port):
    win_menu.destroy()
    #========================================
    #Connection Setup

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, port))



        #========================================

        #========================================
        #Receiving Data
        def recv():
            while True:
                try:
                    data = s.recv(2048)
                    data = data.decode('utf-8')
                    element_chat_display.insert(END, data)
                    element_chat_display.see(END)
                except:
                    pass
                


        #========================================

        #========================================
        #Chat Window Setup
        root = Tk()
        root.title("ECHO")
        root.configure(background="white")
        root.resizable(width=False, height=False)

        #========================================

        #========================================
        #Terminal Setup
        element_chat_display = Listbox(root, height=20, width=100)
        element_chat_display.grid(row=1, column=3)
        for i in range(element_chat_display.cget('height')-1):
            element_chat_display.insert(END, '')
        element_chat_entry = Entry(root, width=100)
        element_chat_entry.grid(row=2, column=3)

        def func_returninput(event):
            inp = element_chat_entry.get()
            #element_chat_display.insert(END, element_chat_entry.get())
            #element_chat_display.see(END)
            element_chat_entry.delete(0, END)
            s.send(str.encode(inp))


        #element_chat_output = Text(root, height=20, width=50)
        #element_chat_output.grid(row=1, column=1)
        #element_chat_output.config(state=DISABLED)

        root.bind('<Return>', func_returninput)
        #========================================

        thread_recv_data = threading.Thread(target=recv)
        thread_recv_data.start()
        #========================================
        def on_closing():
            s.close()
            root.destroy()
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    except ConnectionRefusedError:
        temp = Tk()
        temp.withdraw()
        var = messagebox.showinfo("Error" , "Connection failed")
        load()
        temp.destroy()
        
        
def help():
    root = Tk()
    root.title("ECHO")
    root.configure(background="white")
    root.resizable(width=False, height=False)
    element_help_text = Label(root, text="help - Displays a list of commands\nload - Loads ECHO")
    element_help_text.grid(row=0, column=0)
    element_help_text.configure(background="white")
    def end():
        root.destroy()
    element_button_connect = Button(root, text="Ok", command=end, height=2, width=12)
    element_button_connect.grid(row=1, column=0)


def step():
    t = var_menu_text.get()
    c.execute("SELECT * FROM servers WHERE name = (?)", [t])
    data = c.fetchall()
    if data == []:
        pass
    else:
        ip = data[0][1]
        port = data[0][2]
        startchat(ip, port)
    
def newserv():
    new_serv_win = Tk()
    new_serv_win.title("ECHO")
    new_serv_win.configure(background="white")
    arguments = []
    def cb():
        name = element_input_name.get()
        var_menu_choices.append(name)
        ip = element_input_ip.get()
        port = element_input_port.get()
        c.execute("INSERT INTO servers (name, ip, port) VALUES (?, ?, ?)", [name, ip, port])
        conn.commit()
        new_serv_win.destroy()
        win_menu.destroy()
        load()
        

    lbl1 = Label(new_serv_win, text="Input server name", bg="white")
    lbl1.grid(row=1, column=0)
    element_input_name = Entry(new_serv_win)
    element_input_name.grid(row=1, column=1)
    
    lbl2 = Label(new_serv_win, text="Input IP", bg="white")
    lbl2.grid(row=2, column=0)
    element_input_ip = Entry(new_serv_win)
    element_input_ip.grid(row=2, column=1)
    
    lbl3 = Label(new_serv_win, text="Input port", bg="white")
    lbl3.grid(row=3, column=0)
    element_input_port = Entry(new_serv_win)
    element_input_port.grid(row=3, column=1)
    
    element_button_new_serv = Button(new_serv_win, text="Add server", command=cb, height=2, width=12)
    element_button_new_serv.grid(row=4, column=1)


def delserv():
    del_serv_win = Tk()
    del_serv_win.title("ECHO")
    del_serv_win.configure(background="white")
    c.execute("SELECT * FROM servers")
    data = c.fetchall()
    global var_menu_choices
    var_menu_choices = []
    for item in data:
        var_menu_choices.append(item[0])
    var_del_serv_menu_text = StringVar(del_serv_win)
    var_del_serv_menu_text.set("Choose a server")
    def cb():
        name = var_del_serv_menu_text.get()
        c.execute("DELETE FROM servers WHERE name =(?)", [name])
        conn.commit()
        del_serv_win.destroy()
        win_menu.destroy()
        load()
    element_server_menu = OptionMenu(del_serv_win, var_del_serv_menu_text, *var_menu_choices)
    element_server_menu.grid(row=0, column=0)
    element_button_new_serv = Button(del_serv_win, text="Delete server", command=cb, height=2, width=12)
    element_button_new_serv.grid(row=0, column=1)
    
    
def load():
    global win_menu
    win_menu = Tk()
    win_menu.title("ECHO")
    win_menu.configure(background="white")
    win_menu.resizable(width=False, height=False)

    try:
        file_logo = PhotoImage(file="logo.gif")
        element_logo = Label(win_menu, image=file_logo)
        element_logo.photo = file_logo
        element_logo.grid(row=0, column=0)
    except:
        element_missingphoto_text = Label(win_menu, text="File 'logo.gif' missing from build", fg="white")
        element_missingphoto_text.grid(row=0, column=0)
        element_missingphoto_text.configure(background="black")

    element_about_text = Label(win_menu, text="""
    Version 1
    Developed by William Scargill""")
    element_about_text.grid(row=0, column=1)
    element_about_text.configure(background="white")

    element_button_connect = Button(win_menu, text="Connect", command=step, height=2, width=12)
    element_button_connect.grid(row=1, column=1)

    c.execute("SELECT * FROM servers")
    data = c.fetchall()
    global var_menu_choices
    var_menu_choices = []
    for item in data:
        var_menu_choices.append(item[0])
    global var_menu_text
    var_menu_text = StringVar(win_menu)
    var_menu_text.set("Choose a server")
    element_server_menu = OptionMenu(win_menu, var_menu_text, *var_menu_choices)
    element_server_menu.grid(row=1, column=0)

    element_button_connect = Button(win_menu, text="Add new server", command=newserv, height=2, width=12)
    element_button_connect.grid(row=2, column=0)
    
    element_button_del_serv = Button(win_menu, text="Delete a server", command=delserv, height=2, width=12)
    element_button_del_serv.grid(row=3, column=0)

    
    win_menu.mainloop()

load() 













