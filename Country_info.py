from countryinfo import CountryInfo
import geocoder
import requests
from tkinter import *
from PIL import ImageTk, Image


def user_geo():
    g = geocoder.ip("me")
    origin_code = g.country
    origin = CountryInfo(origin_code).name().capitalize()
    city = g.city

    # return lista z info!!!!!!
    return origin_code, origin, city


def country_info(country_name):
    country = CountryInfo(country_name)
    name = country.name().capitalize()
    area = country.area()
    capital = country.capital()
    currencies = country.currencies()
    languages = country.languages()
    timezone = country.timezones()
    return name, area, capital, currencies


def app():
    url = "https://www.countryflags.io/{}/flat/64.png".format(user_geo()[0])
    root = Tk()
    img = ImageTk.PhotoImage(Image.open(requests.get(url, stream=True).raw))
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()


print(user_geo()[3])



