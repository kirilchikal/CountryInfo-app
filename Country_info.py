from countryinfo import CountryInfo
import geocoder
import requests
from tkinter import *
from PIL import ImageTk, Image
from bs4 import BeautifulSoup


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


def get_distance(start, destination):
    d = geocoder.distance(start, destination)
    return round(d, 2)




page = requests.get('https://www.worldometers.info/coronavirus/#countries')

soup = BeautifulSoup(page.content, 'html.parser')

rows = soup.findChildren("tr")


def covid_data(country):
    data = []

    for i in range(len(rows)):
        a = rows[i].findChildren("a")
        if len(a) != 0 and a[0].text == country:
            items = rows[i].find_all("td")
            for k in range(2, 7):
                data.append(items[k].text)
            break
    return data
# print(covid_data("Poland"))


def app():
    url = "https://www.countryflags.io/{}/flat/64.png".format(user_geo()[0])
    root = Tk()
    img = ImageTk.PhotoImage(Image.open(requests.get(url, stream=True).raw))
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()

