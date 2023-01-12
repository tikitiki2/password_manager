import tkinter as tk
import shelve as sh
from tkinter import ttk,messagebox
from passlib.hash import pbkdf2_sha256 as passlib

class Manager:
    def __init__(self):
        self.root=tk.Tk()
        with sh.open('username_password.db') as s:
            if not s:
                self.create_account_GUI()
                self.root.mainloop()
            else:
                self.root.title('password_manager')
                self.creat_login_GUI()

                self.storage = {}

                self.root.mainloop()


        s.close()
    def autheticate(self,attempt):
        #autheticate password
        with sh.open('username_password.db') as s:
            try:
                h=s[self.login_username.get()]
                verification = passlib.verify(self.login_password.get(), h)
            except:
                messagebox.showwarning('incorrect username','username you entered is incorrect')
        s.close()
        if verification:
            self.forget_login_gui()
            #forget login GUI
        else:
            messagebox.showwarning('incorrect password','the password you entered is incorrect')


    def forget_login_gui(self):
        for i in self.login_widgets:
            i.grid_forget()
        self.create_main_GUI()
    def add_new(self):

        self.application_name=tk.Entry(self.expando_frame,width=25,font=('arial',17))
        self.username=tk.Entry(self.expando_frame,width=25,font=('arial',17))
        self.password=tk.Entry(self.expando_frame,width=25,font=('arial',17))
        self.entrys=[self.application_name,self.username,self.password]
        self.application_name.grid(row=2, column=1)
        self.username.grid(row=3, column=1)
        self.password.grid(row=4, column=1)

        self.labels=[tk.Label(self.expando_frame, text='Application Name:'),tk.Label(self.expando_frame, text='Username/email:'),tk.Label(self.expando_frame, text='Password:')]
        for index,val in enumerate(self.labels):
            val.grid(row=index+2,column=0)



        self.password.bind('<Return>',self.hide)
    def hide(self,thing):
        #store user info to pass onto dictionary and hide textboxes

        username=self.username.get()
        password=self.password.get()
        app_name=self.application_name.get()

        self.application_name.grid_forget()
        self.username.grid_forget()
        self.password.grid_forget()
        for i in self.labels:
            i.grid_forget()
        self.add_to_memory(username,password,app_name)

    def add_to_memory(self,username,password,app_name):
        #store username password and application name in dictionary
        with sh.open('data.db') as data:
            if app_name in data.keys():
                messagebox.showwarning('already in mem','the app name you have entered is already in the database')
            else:
                self.treeview.insert('', 'end', values=(app_name, username, password))
                data[app_name]=(username,password)
        data.close()


    def delete(self):
        with sh.open('data.db') as data:

            selected_items=self.treeview.selection()
            for i in selected_items:
                del data[self.treeview.item(i)['values'][0]]
                self.treeview.delete((i))


        data.close()


    def creat_login_GUI(self):
        self.root.geometry('400x100')
        self.login_label=tk.Label(self.root,text='password:',font=('arial',15))
        self.login_label_user=tk.Label(self.root,text='username:',font=('arial',15))
        self.login_password=tk.Entry(self.root,width=25,font=('arial',15))
        self.login_username=tk.Entry(self.root,width=25,font=('arial',15))

        self.login_label_user.grid(row=2,column=2)
        self.login_username.grid(row=2,column=3)

        self.login_password.grid(row=3,column=3)
        self.login_label.grid(row=3,column=2)
        self.login_password.bind('<Return>',self.autheticate)



        self.login_widgets=[self.login_label,self.login_label_user,self.login_password,self.login_username]
    def create_account_GUI(self):
        self.root.geometry('500x200')
        self.login_label = tk.Label(self.root, text='password:', font=('arial', 15))
        self.login_label_confirm = tk.Label(self.root, text='confirm password:', font=('arial', 15))

        self.login_label_user = tk.Label(self.root, text='username:', font=('arial', 15))
        self.login_password = tk.Entry(self.root, width=25, font=('arial', 15))
        self.login_username = tk.Entry(self.root, width=25, font=('arial', 15))
        self.login_password_confirm = tk.Entry(self.root, width=25, font=('arial', 15))
        self.title=tk.Label(self.root,text='create account',font=('arial', 20))
        self.title.grid(row=5,column=3)
        self.login_label_user.grid(row=2, column=2)
        self.login_username.grid(row=2, column=3)

        self.login_password.grid(row=3, column=3)
        self.login_label.grid(row=3, column=2)
        self.login_password_confirm.grid(row=4,column=3)
        self.login_label_confirm.grid(row=4,column=2)
        self.create_account_widgets=[
            self.login_label,self.login_label_confirm,self.login_label_user,self.login_password,self.login_username
            ,self.login_password_confirm,self.title
        ]
        self.login_password_confirm.bind('<Return>',self.check)

    def forget_gui(self):
        for i in self.create_account_widgets:
            i.grid_forget()
    def check(self,thing):
        if self.login_password.get() == self.login_password_confirm.get():
            hash=passlib.hash(self.login_password.get())
            with sh.open('username_password.db') as s:
                s[self.login_username.get()]=hash
            s.close()
            self.forget_gui()
            self.creat_login_GUI()
        else:
            messagebox.showwarning('showinfo','the passwords do not match try again')

    def create_main_GUI(self):
        self.root.geometry('500x600')
        self.expando_frame = tk.Frame(self.root)
        self.button = tk.Button(self.root, text='add new', font=('arial', 18), command=self.add_new)
        self.delete_button=tk.Button(self.root,text='delete selected items',font=('arial',18),command=self.delete)
        self.delete_button.grid(row=0,column=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.button.grid(row=1, column=0)
        self.expando_frame.grid(row=2, sticky="nsew")

        self.root.grid_columnconfigure(0, weight=1)  # allow the listbox to take up extra space
        self.treeview=ttk.Treeview(self.root,columns=('application_name','username','password'),show='headings')
        self.treeview.heading('application_name', text='application_name')
        self.treeview.heading('username', text='username')
        self.treeview.heading('password', text='password')
        self.treeview.column('application_name',width=150)
        self.treeview.column('username', width=150)
        self.treeview.column('password', width=150)

        self.treeview.grid(row=3,column=0,sticky='sew')
        self.remember()

    def remember(self):
        with sh.open('data.db') as data:
            app_names = data.keys()
            for app_name in app_names:
                username, password = data[app_name]
                self.treeview.insert("", "end", values=(app_name, username, password))
        data.close()


Manager()
