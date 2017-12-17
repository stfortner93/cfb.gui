import tkinter as tk
from tkinter import ttk as tkk



class MainApplication:
    def __init__(self, master):
        self.master = master
        self. dimensions()
        self.drop_menu(self.master)

    def dimensions(self):
        w = 800 # width for the Tk root
        h = 650 # height for the Tk root
        ws = self.master.winfo_screenwidth() # width of the screen
        hs = self.master.winfo_screenheight() # height of the screen
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def quit(self):
        raise SystemExit

    def drop_menu(self, root):
        menu = tk.Menu(root)
        root.config(menu=menu)

        submenu= tk.Menu(menu)
        menu.add_cascade(label="Conferences", menu=submenu)
        submenu.add_command(label="Top 25", command= lambda: self.new_window("Top25"))
        submenu.add_command(label="Sec", command=lambda: self.new_window("SEC"))

        stop = tk.Menu(menu)
        menu.add_command(label="Quit", command = self.quit)

    def new_window(self, conf):
        name = conf
        window = tk.Toplevel(self.master)
        new = MainApplication(window)
        new_frame = tk.Frame(window)
        print(conf)
        window.title(name)
        window.mainloop()

class index:
    def __init__(self, master):
        self.master = master
        self.sec = tk.PhotoImage(file="C:\Projects\Python\photos\Top25Logo.png")
        self.b = tk.Button(self.master, justify = "left", image=self.sec, bd=0, bg="black", activebackground="black")
        self.b.pack()
        #label = tk.Label(self.master, text="LAbel").grid()
        #label2 = tk.Label(self.master, text="LAbel").grid()
        self.b.image = self.sec

def main():
    root = tk.Tk()
    root.title("Main Page")
    main = MainApplication(root)
    new = index(root)
    frame = tk.Frame(root)
    root.config(bg="black")
    root.mainloop()

if __name__ == "__main__":
    main()
