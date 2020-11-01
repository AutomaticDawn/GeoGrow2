import tkinter as tk
from tkinter import *
import main

LARGE_FONT=("Verdana", 12)
MEDIUM_FONT=("Verdana", 10)


class MainGUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        self.title("GeoGrow")
        self.geometry('250x250')

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
        label.grid(pady=10, padx=100, row=0)

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
        label = tk.Label(self, text="GeoGrow", font=LARGE_FONT)
        label.grid(pady=10, padx=85, row=0)

        button1 = tk.Button(self, text="Enter Coordinates", command=lambda: controller.show_frame(Coordinates))
        button1.grid(pady=5, padx=10, row=1)

        button2 = tk.Button(self, text="Check", command=lambda: main.check_for_flood())
        button2.grid(pady=5, padx=10, row=2)

        global label2
        label2 = tk.Label(self, text="Not Checked", font=MEDIUM_FONT)
        label2.grid(pady=10, padx=10, row=3)

        button1 = tk.Button(self, text="Log Out", command=lambda: controller.show_frame(StartPage))
        button1.grid(pady=10, padx=10, row=4)

    def update(msg):
        label2.config(text=msg)


class Coordinates(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="Insert Coordinates", font=LARGE_FONT)
        label.grid(pady=10, padx=0, row=0, column=0, columnspan=2)

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

        eN.grid(pady=0, padx=10, row=1, column=1)
        eS.grid(pady=0, padx=10, row=2, column=1)
        eE.grid(pady=0, padx=10, row=3, column=1)
        eW.grid(pady=0, padx=10, row=4, column=1)

        submitBTN = Button(self, text="Submit", command=lambda: main.CoordinatesManager.save_new_coordinates(None, eW.get(), eN.get(), eE.get(), eS.get()))
        exitBTN = Button(self, text="Exit", command=lambda: controller.show_frame(PageOne))
        submitBTN.grid(pady=10, padx=10, row=5, column=1)
        exitBTN.grid(pady=5, padx=10, row=6, column=1)

        global labelError
        labelError = tk.Label(self, text="Enter Values               ", font=MEDIUM_FONT)
        labelError.grid(pady=5, padx=10, row=7, columnspan=2)

    def updateErrorText(self, errormsg):
        labelError.config(text=errormsg)

app = MainGUI()
app.mainloop()
