import tkinter as tk
from Country_info import *


origin_info = user_geo()


class App:

    def __init__(self, root):
        self.root = root
        self.hid = False
        self.root.geometry("750x600")
        self.header = tk.Frame(self.root, height=80,  bg="#1995AD")
        self.header.pack(fill=tk.BOTH)
        self.header.pack_propagate(0)
        self.frame1 = tk.Frame(self.root, bg="white")
        self.frame1.pack(fill=tk.BOTH, expand=1)

        self.but = Button(self.header, text="hide", command=self.hide)
        self.but.pack(side="left")

        self.menu()
        # self.frame2

    def menu(self):
        self.frame2 = tk.Frame(self.frame1, width=120, bg="#F1F1F2")
        self.frame2.pack(side="left", fill=tk.BOTH)
        url = "https://www.countryflags.io/{}/flat/64.png".format(origin_info[0])
        img = ImageTk.PhotoImage(Image.open(requests.get(url, stream=True).raw))
        # add flag by country code
        flag = Label(self.frame2, image=img, bg="#F1F1F2")
        flag.image = img
        flag.pack(fill=tk.BOTH, padx=25, pady=30)
        # add name of the country
        lable = Label(self.frame2, text="Your location:\n{}".format(origin_info[1]))
        lable.pack()

    def hide(self):
        if not self.hid:
            self.frame2.destroy()
            self.hid = True
        else:
            self.menu()
            self.hid = False


root = tk.Tk()
app = App(root)
root.mainloop()
