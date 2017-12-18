import tkinter as tk
from tkinter import ttk as tkk
import sqlite3



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
        submenu.add_command(label="Big 12", command=lambda: self.new_window("Big12"))
        submenu.add_command(label="Big 10", command=lambda: self.new_window("Big"))
        submenu.add_command(label="ACC", command=lambda: self.new_window("ACC"))
        submenu.add_command(label="Pac 12", command=lambda: self.new_window("pac"))
        submenu.add_command(label="Sun Belt", command=lambda: self.new_window("sun"))
        submenu.add_command(label="MAC", command=lambda: self.new_window("MAC"))
        submenu.add_command(label="AAC", command=lambda: self.new_window("AAC"))
        submenu.add_command(label="MWC", command=lambda: self.new_window("MWC"))
        submenu.add_command(label="USA", command=lambda: self.new_window("USA"))
        submenu.add_command(label="ALL", command=lambda: self.new_window("all"))

        stop = tk.Menu(menu)
        menu.add_command(label="Quit", command = self.quit)

    def new_window(self, conf):
        name = conf
        print(conf)
        if conf == "Top25":
            window = tk.Toplevel(self.master)
            window.title(name)
            new = top(window)
            window.mainloop()

        print(conf)

class index(MainApplication):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.creat_images(self.master)

    def creat_images(self, window):
        self.toppick = tk.PhotoImage(file="C:\Projects\Python_Request\photos\Top25Logo.gif")
        self.top = tk.Button(self.master, justify = "left", image=self.toppick, bd=0, bg="black", activebackground="black", anchor = "w", \
            padx = 10, command = lambda: self.new_window("Top25"))
        self.top.pack()
        self.top.image = self.toppick


        self.frame1 = tk.Frame(window, padx = 50, bg = 'black')
        self.sec = tk.PhotoImage(file = "C:\Projects\Python_Request\photos\logo-sec-shield.png")
        self.secb = tk.Button(self.frame1, justify = "left", image = self.sec, bd = 0, bg = 'black', activebackground = "black")
        self.sec.image = self.sec
        self.acc = tk.PhotoImage(file = "C:\Projects\Python_Request\photos\\acc.gif")
        self.accb = tk.Button(self.frame1, justify = "left", image = self.acc, bd = 0, bg = 'black', activebackground = "black", anchor='e', padx=30)
        self.acc.image = self.acc
        self.secb.pack(side='left')
        self.accb.pack(side='left')

        self.frame1.pack()

        self.frame2 = tk.Frame(window, padx = 50, bg='black')
        self.pac = tk.PhotoImage(file = "C:\Projects\Python_Request\photos\pac.gif")
        self.pacb = tk.Button(self.frame2, justify = "left", image = self.pac, bd = 0, bg = 'black', activebackground = "black", anchor = 'w', padx=20)
        self.pac.image = self.pac

        self.big12 = tk.PhotoImage(file = "C:\Projects\Python_Request\photos\\big12.gif")
        self.big12b = tk.Button(self.frame2, justify = "left", image = self.big12, bd = 0, bg = 'black', activebackground = "black", anchor='e', padx=30)
        self.big12.image = self.big12
        self.pacb.pack(side='left')
        self.big12b.pack(side="left")

        self.big = tk.PhotoImage(file = "C:\Projects\Python_Request\photos\\big.gif")
        self.bigb = tk.Button(self.master, justify = "left", image = self.big, bd = 0, activebackground = "black", anchor='e', padx=30)
        self.big.image = self.big
        self.frame2.pack()
        self.bigb.pack()

class top(MainApplication):
    pass
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.top_table(self.master)

    def top_table(self, window):
        self.tree = tkk.Treeview(window, height = 25 )
        self.tree["columns"] = ("one", "two", "three")
        self.tree.column("one", width=100)
        self.tree.column("two", width=100)
        self.tree.column("three", width=100)

        self.tree.heading("one", text="Team")
        self.tree.heading("two", text="PPG")
        self.tree.heading("three", text="YPG")

        conn = sqlite3.connect("cfb5.sqlite")
        db = conn.cursor()
        db.execute("SELECT team, ypg, ppg FROM offensive")
        ranking = db.fetchall()
        print(ranking)
        x=1
        for ranks in ranking:
            if x <= 25 :
                print(ranks)
                self.tree.insert("" , "end", text=str(x), values=(ranks))
                x += 1
                print(x)


        self.tree.pack()






def main():
    conn = sqlite3.connect("cfb5.sqlite")
    db = conn.cursor()
    root = tk.Tk()
    root.title("Main Page")
    main = MainApplication(root)
    new = index(root)
    frame = tk.Frame(root)
    root.config(bg="black")
    root.mainloop()

if __name__ == "__main__":
    main()
