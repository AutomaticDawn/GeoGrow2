import tkinter as tk
from tkinter import *

LARGE_FONT=("Verdana", 12)


class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        frame = StartPage(container, self)
        frame1 = PageOne(container, self)
        frame2 = Coordinates(container, self)

        self.frames[StartPage] = frame
        self.frames[PageOne] = frame1
        self.frames[Coordinates] = frame2

        frame.grid(row=0, column=0, sticky="nsew")
        frame1.grid(row=0, column=0, sticky="nsew")
        frame2.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#def qf(param):
    #print(param)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        #Login page
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.grid(pady=10, padx=20, row=0)

        userLabel = tk.Label(self, text="Username:")
        userLabel.grid(row=1)

        user = tk.Entry(self, width="24")
        user.grid(pady=10, padx=20, row=2)

        passwLabel = tk.Label(self, text="Password:")
        passwLabel.grid(row=3)

        passw = tk.Entry(self, show="*", width="24")
        passw.grid(padx=20, row=4)

        button1 = tk.Button(self, text="Login", command=lambda: controller.show_frame(PageOne))
        button1.grid(pady=5, padx=20, row=5)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = tk.Button(self, text="Enter Coordinates", command=lambda: controller.show_frame(Coordinates))
        button1.pack()

class Coordinates(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Insert Coordinates", font=LARGE_FONT)
        label.grid(row=0, columnspan=2)
        labelN = tk.Label(self, text="N:")
        labelS = tk.Label(self, text="S:")
        labelE = tk.Label(self, text="E:")
        labelW = tk.Label(self, text="W:")

        labelN.grid(row=1, sticky="E")
        labelS.grid(row=2, sticky="E")
        labelE.grid(row=3, sticky="E")
        labelW.grid(row=4, sticky="E")

        eN = Entry(self)
        eS = Entry(self)
        eE = Entry(self)
        eW = Entry(self)

        eN.grid(row=1, column=1)
        eS.grid(row=2, column=1)
        eE.grid(row=3, column=1)
        eW.grid(row=4, column=1)

        submitBTN = Button(self, text="Submit")
        exitBTN = Button(self, text="Exit", command=lambda: controller.show_frame(PageOne))
        submitBTN.grid(row=5)
        exitBTN.grid(row=5, column=1)


app = Main()
app.mainloop()
