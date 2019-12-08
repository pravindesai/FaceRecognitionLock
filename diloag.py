import tkinter as tk

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['Students']
user = db.user

master = tk.Tk()
tk.Label(master, text="ID").grid(row=0)
tk.Label(master, text="NAME").grid(row=1)

e1 = tk.Entry(master)
e2 = tk.Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
uid = ''
uname = ''


def show_entry_fields():
    if e1.get() and e2.get() is not None:
        f = open('nameList.txt', 'a+')
        global uid
        global uname

        uid = str(e1.get())
        uname = str(e2.get())
        userDic = {
            'id': uid,
            'name': uname
        }
        user.insert_one(userDic)

        print('USER ADDED....')
        f.close()
        master.quit()
    else:
        pass


class main():
    def exe(self):
        tk.mainloop()

    tk.Button(master, text='Quit', command=master.quit).grid(row=3, column=0, sticky=tk.W, pady=4)
    tk.Button(master, text='Add', command=show_entry_fields).grid(row=3, column=1, sticky=tk.W, pady=4)
