import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import ImageTk
from Country_info import *
import configparser
from PIL import Image


class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Country Info")
        self.config = configparser.ConfigParser()
        self.config.read("config.txt")
        self.root.geometry(self.config['default']['geometry'])

        # open icons
        self.icons = {}
        for x in self.config.options('icons'):
            self.icons[x] = Image.open(requests.get(self.config.get('icons', x), stream=True).raw)

        # get the currency error list
        self.currency_err = {}
        for x in self.config.options('currency'):
            self.currency_err[x] = [self.config.get('currency', x)]

        # get the covid error list
        self.covid_err = {}
        for x in self.config.options('covid'):
            self.covid_err[x] = self.config.get('covid', x)

        # get API keys
        self.weather_key = self.config['weatherAPI']['key']
        self.currency_key = self.config['currencyAPI']['key']

        # user location frame is hidden
        self.hid = False
        # list of user country info
        self.origin_info = user_geo()
        # empty list of search country info
        self.c_info = []
        # input country variable
        self.country_var = StringVar()

        self.main = tk.Frame(self.root, bg="white")
        self.main.pack(side="bottom", fill=tk.BOTH, expand=1)
        self.start_info = Label(self.main, text="Enter a country to find information",
                                bg="white", fg="#0479bc", font="Ubuntu 30")
        self.start_info.place(relx=0.5, rely=0.5, anchor="center")

        self.header()
        self.user_location()
        self.hide()

    def header(self):
        # header frame
        self.head = tk.Frame(self.root, height=85, bg="#0479bc")
        self.head.pack(side="top", fill=tk.BOTH)
        self.head.pack_propagate(0)
        # Frame with map
        self.map = tk.Frame(self.root, name="map", height=400)
        self.map.pack(side="top", fill=tk.BOTH)
        map_img = tk.PhotoImage(file=self.config['background']['img'])
        label = Label(self.map, image=map_img)
        label.image = map_img
        label.place(x=0, y=0)
        # open-close location
        icon1 = ImageTk.PhotoImage(self.icons['loc'])
        self.but = Button(self.head, text="hide", image=icon1, command=self.hide,
                          bg="#0479bc", activebackground="#0479bc", relief=FLAT, cursor="hand2")
        self.but.image = icon1
        self.but.place(x=60, y=45, anchor="center")
        # search form
        search = Frame(self.head)
        search.place(relx=0.5, rely=0.5, anchor="center")
        entry = Entry(search, textvariable=self.country_var, font=("Corbel", 12), width=35, bd=0)
        entry.grid(row=0, column=0, ipady=2)
        icon2 = ImageTk.PhotoImage(self.icons['search'])
        btn = Button(search, text="img-loop", image=icon2, command=self.show_country_info,
                     bg="#0aa258", activebackground="#0479bc", relief=FLAT, cursor="hand2")
        btn.image = icon2
        btn.grid(row=0, column=1, ipadx=2, ipady=2)

    def user_location(self):
        self.frame2 = tk.Frame(self.root, bg="#F1F1F2")
        self.frame2.place(x=0, y=85, relheight=1.0)
        url = "https://www.countryflags.io/{}/flat/64.png".format(self.origin_info[0])
        img = ImageTk.PhotoImage(Image.open(requests.get(url, stream=True).raw))
        # add flag by country code
        flag = Label(self.frame2, image=img, bg="#F1F1F2", padx=25, pady=60)
        flag.image = img
        flag.grid(row=0, padx=20, pady=40)
        # add name of the country
        Label(self.frame2, text="Your location:", fg="#363636", font="Corbel 12", pady=15).grid(row=1, pady=10)
        Label(self.frame2, text=f"{self.origin_info[1].upper()}", fg="#363636", font="Corbel 12").grid(row=2)
        Button(self.frame2, text="Change location", fg="white", bg="#044a72", font="Corbel 10",
               command=self.change_location).grid(row=3, pady=50, padx=15)

    def country(self):
        # main info frame
        main_info = tk.Frame(self.main, bg="white")
        main_info.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

        # add flag and country name
        name_flag = tk.Frame(self.map, bg="#044a72")
        name_flag.place(x=0, y=0, height=80, relwidth=1.0)
        img = ImageTk.PhotoImage(Image.open(
            requests.get("https://www.countryflags.io/{}/flat/64.png".format(self.c_info[10][1]), stream=True).raw))
        flag = Label(name_flag, image=img, bg="#044a72")
        flag.image = img
        flag.grid(row=0, column=0, padx=(100, 0))
        Label(name_flag, text=f"{self.c_info[0][1].upper()}, {self.c_info[10][1]}", padx=50, fg="white",
              bg="#044a72", font="Corbel 25").grid(row=0, column=1)

        # Create the clock widget
        clock = Frame(self.map, bg="#044a72")
        clock.place(relx=0.85, rely=0.05)
        Label(clock, text="Local time", fg="white", bg="#044a72", font="Corbel 13").grid(row=0)
        clock2 = Clock(clock, self.c_info[10][1])
        clock2.widget.configure(fg="white", bg="#044a72", font="Calibri 12")
        clock2.widget.grid(row=1)

        # add covid data
        data = covid_data(self.c_info[0][1], self.covid_err)
        if len(data) > 1:
            covid = Frame(self.map, bg="#0aa258", pady=5)
            covid.place(x=100, y=100)
            Label(covid, text="covid data".upper(), fg="white", bg="#0aa258", font="Corbel 20", padx=40).pack()
            if data[1] != "":
                Label(covid, text="New cases:", fg="white", bg="#0aa258", font="Corbel 12").pack()
                Label(covid, text=f"{data[1]}", fg="white", bg="#0aa258", font="Calibri 11").pack()
            else:
                Label(covid, text="Active cases:", fg="white", bg="#0aa258", font="Corbel 12").pack()
                Label(covid, text=f"{data[4]}", fg="white", bg="#0aa258", font="Calibri 11").pack()
            if data[3] != "":
                Label(covid, text="New deaths:", fg="white", bg="#0aa258", font="Corbel 12").pack()
                Label(covid, text=f"{data[3]}", fg="white", bg="#0aa258", font="Calibri 11").pack()
            else:
                Label(covid, text="Total deaths:", fg="white", bg="#0aa258", font="Corbel 12").pack()
                Label(covid, text=f"{data[2]}", fg="white", bg="#0aa258", font="Calibri 11").pack()

        # add distance info
        d = get_distance(self.c_info[1][1].capitalize(), self.origin_info[2])
        distance = Frame(self.map, bg="#044a72")
        distance.place(relx=0.35, y=100)
        Label(distance, text=f"Distance to {self.c_info[1][1].title()} from {self.origin_info[2].title()} is:",
              bg="#044a72", fg="white", font="Corbel 12", padx=25).pack()
        Label(distance, text=f"{d} km", bg="#044a72", fg="white", font=("Calibri", 11)).pack()

        # add weather
        weather = Frame(self.map, bg="white")
        weather.place(relx=0.35, y=165)
        temp, description = capital_weather(self.c_info[1][1], self.c_info[10][1], self.weather_key)
        Label(weather, text=f"Weather in {self.c_info[1][1].title()}", fg="white",
              font="Corbel 12", bg="#044a72", padx=25).pack()
        Label(weather, text=f"{temp}°C", font=("Calibri", 14), bg="white", fg="#4e4e4e").pack()
        Label(weather, text=description, font="Corbel 12", bg="white", fg="#656565").pack()

        # add facts
        facts = tk.Frame(main_info, bg="white")
        facts.place(x=100, y=10)
        Label(facts, text="FACTS", pady=10, bg="white", font=("Bahnschrift Semilight", 14)).grid(row=0, column=0,
                                                                                                 columnspan=2)
        for i in range(1, 10):
            fact = Frame(facts, bg="white")
            fact.grid(row=i, column=0, sticky="W")

            img = ImageTk.PhotoImage(self.icons[self.c_info[i][0]])
            ll = Label(fact, image=img, bg="white")
            ll.image = img
            ll.pack(side="left")
            Label(fact, text=self.c_info[i][0].upper(), bg="white", padx=15,
                  font=("Bahnschrift Semilight", 10)).pack(side="left", fill=tk.BOTH)

            inf = Label(facts, text=self.c_info[i][1], font=("Bahnschrift Semilight", 10), bg="white", wraplength=250)
            inf.grid(row=i, column=1)

        # add exchange
        exchange = tk.Frame(main_info, highlightbackground="#9e9e9d", highlightthickness=1, bg="white")
        exchange.place(relx=0.5, y=40)
        Label(exchange, text="Currency Converter", font=("Bahnschrift Semilight", 14),
              bg="#F4f4f4").grid(row=0, column=0, sticky='ew', columnspan=3, ipady=15)
        Label(exchange, text="Amount".upper(), font="Corbel 10", bg="white").grid(row=1, column=0, sticky='ew', pady=5)
        amount = Entry(exchange, highlightthickness=1, highlightbackground="#9e9e9d", relief=FLAT)
        amount.insert(END, 1)
        amount.grid(row=2, column=0, ipady=2, padx=15)
        Label(exchange, text="From".upper(), font="Corbel 10", bg="white").grid(row=1, column=1, sticky='ew', pady=5)
        if self.origin_info[1].lower() in self.currency_err:   # if there no currency code errors
            self.origin_info[3] = self.currency_err[self.origin_info[1].lower()]
        if self.c_info[0][1].lower() in self.currency_err:
            self.c_info[3][1] = self.currency_err[self.c_info[0][1].lower()]
        val = self.origin_info[3] + self.c_info[3][1]  # list of currency codes
        from_choosen = ttk.Combobox(exchange, values=val[::-1], width=12)
        from_choosen.grid(row=2, column=1)
        from_choosen.current(0)
        Label(exchange, text="To".upper(), font="Corbel 10", bg="white").grid(row=1, column=2, sticky='ew', pady=5)
        to_choosen = ttk.Combobox(exchange, values=val, width=12)
        to_choosen.grid(row=2, column=2, padx=15)
        to_choosen.current(0)
        btn = Button(exchange, text="Convert".upper(), fg="white", bg="#044a72", font="Corbel 10",
                     command=lambda: self.exchange(exchange, amount.get(), from_choosen.get(), to_choosen.get()))
        btn.grid(row=3, column=2, pady=20, ipadx=5, ipady=5)

    def show_country_info(self):
        if self.country_var.get() != "":
            if not self.c_info:
                # destroy  default start text
                self.start_info.destroy()
                self.map.configure(height=270)
            try:
                self.c_info = country_info(self.country_var.get())
                children = self.map.winfo_children()
                for c in children[1:]:
                    c.destroy()
                for c in self.main.winfo_children():
                    c.destroy()
                self.country()
            except KeyError:
                self.show_input_err()

    def hide(self):
        if not self.hid:
            self.frame2.destroy()
            self.hid = True
        else:
            self.user_location()
            self.hid = False

    def change_location(self):
        window = Toplevel(self.root)
        window.transient(self.root)
        window.geometry("250x200+600+200")
        window.title("Change location")
        Label(window, text="Enter the name of the country".upper(),
              font="Corbel 10").place(relx=0.5, y=40, anchor="center")
        new_location = Entry(window)
        new_location.place(relx=0.5, rely=0.4, anchor="center", height=20)
        Button(window, text="Change", command=lambda: self.check_changes(new_location, window),
               relief=FLAT, bg="#0479bc", fg="white", font="Corbel 12").place(relx=0.5, rely=0.7, anchor="center")

    def check_changes(self, location, window):
        location = location.get()
        if location != "":
            try:
                self.origin_info = user_geo(location)
                self.frame2.destroy()
                self.user_location()
                if self.c_info:
                    self.country()
                window.destroy()
            except KeyError:
                messagebox.showinfo(f"showinfo", f"Sorry, could not find country {location}")

    def show_input_err(self):
        messagebox.showinfo("showinfo", "Sorry, could not find country {}".format(self.country_var.get()))

    def exchange(self, frame, amount, from_c, to_c):
        try:
            amount = int(amount)
        except ValueError:
            messagebox.showinfo("showinfo", "The amaunt value must be a number")
        value = convert(from_c, to_c, amount, self.currency_key)
        Label(frame, text="{} {} = {} {}".format(amount, from_c, value, to_c),
              bg="white", font=("Bahnschrift Semilight", 12), fg="#656565").grid(row=3, columnspan=2)


root = tk.Tk()
app = App(root)
root.mainloop()
