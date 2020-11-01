import tkinter as tk
from tkinter import *

LARGE_FONT = ("Verdana", 12)


class GUI_Initalization(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = LoginPage(container, self)

        self.frames[LoginPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="LogIn Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        uname = tk.Label(self, text="Username")
        password = tk.Label(self, text="Password")
        entry1 = Entry(self)
        entry2 = Entry(self, show="*")

        uname.pack(side=LEFT)
        password.pack(side=LEFT)
        entry1.pack()
        entry2.pack()

        button1 = tk.Button(self, text="Login", command=lambda: controller.show_frame(PageOne))
        button1.pack()


class PageOne(tk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Exit", command=lambda: controller.show_frame(LoginPage))
        button1.pack()


app = GUI_Initalization()
app.mainloop()
