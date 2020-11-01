import tkinter as tk

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
        frame_ = PageOne(container, self)

        self.frames[StartPage] = frame
        self.frames[PageOne] = frame_

        frame.grid(row=0, column=0, sticky="nsew")
        frame_.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

def qf(param):
    print(param)

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #command within button cant throw args to funcs. Use lambda to throw those args to the func instead
        button1 = tk.Button(self, text="Login",command=lambda: controller.show_frame(PageOne))
        button1.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        #command within button cant throw args to funcs. Use lambda to throw those args to the func instead
        button1 = tk.Button(self, text="Start Page",command=lambda: controller.show_frame(StartPage))
        button1.pack()


app = Main()
app.mainloop()

