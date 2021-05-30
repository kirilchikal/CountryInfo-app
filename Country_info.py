from countryinfo import CountryInfo
from tkinter import *
import pytz
from datetime import datetime
import geocoder
import requests
from bs4 import BeautifulSoup


"""
    Class that contains the clock widget
"""


class Clock:

    def __init__(self, parent, code):
        # create clock widget by timezone
        self.zone = pytz.country_timezones(code)[0]
        now = datetime.now(pytz.timezone(self.zone))
        self.time = now.strftime('%H:%M:%S')
        self.widget = Label(parent, text=self.time)
        self.widget.after(200, self.tick)  # wait 200 ms, then tick

    def tick(self):
        # update the display clock
        now = datetime.now(pytz.timezone(self.zone))
        new_time = now.strftime('%H:%M:%S')
        if new_time != self.time:
            self.time = new_time
            self.widget.config(text=self.time)
        self.widget.after(200, self.tick)




"""
    Return info about user location
"""


def user_geo(country_name="me"):
    if country_name == "me":
        code = geocoder.ip(country_name).country
        country = CountryInfo(code)
    else:
        country = CountryInfo(country_name)
        code = country.iso(2)
    capital = country.capital()
    name = country.name().capitalize()
    currency = country.currencies()
    return [code, name, capital, currency]




"""
    Return info of search country
"""


def country_info(country_name):
    d = []
    country = CountryInfo(country_name)
    d.append(["name", country.name().capitalize()])
    d.append(["capital", country.capital().capitalize()])
    d.append(["region", country.region().capitalize()])
    d.append(["currency", country.currencies()])
    d.append(["area", country.area()])
    d.append(["population", country.population()])
    d.append(["languages", country.languages()])
    d.append(["borders", country.borders()])
    d.append(["calling code", country.calling_codes()])
    d.append(["lat/long", country.capital_latlng()])
    d.append(["code", country.iso(2)])
    return d




"""
    Return distance between origin and dest
"""


def get_distance(start, destination):
    d = geocoder.distance(start, destination)
    return round(d, 2)




"""
    Read covid data
"""
page = requests.get('https://www.worldometers.info/coronavirus/#countries')
soup = BeautifulSoup(page.content, 'html.parser')
rows = soup.findChildren("tr")


def covid_data(country, covid_check_names):
    country = country.lower()

    if country in covid_check_names:
        country = covid_check_names[country]

    data = []

    for i in range(len(rows)):
        a = rows[i].findChildren("a")
        if len(a) != 0 and a[0].text.lower() == country:
            items = rows[i].find_all("td")
            for k in range(2, 7):
                data.append(items[k].text)
            break
    return data


# key = "aef51fddd1542d99e3e3dd0a3a48368f"


def capital_weather(name, code, key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={name},{code}&units=metric&appid={key}"
    data = requests.get(url).json()
    return round(data['main']['temp'], 1), data['weather'][0]['description']


def convert(from_currency, to_currency, amount, key):
    url = "https://free.currconv.com/api/v7/convert?q={}_{}&compact=ultra&apiKey={}".format(from_currency, to_currency, key)
    data = requests.get(url).json()
    amount = round(amount * data[f"{from_currency}_{to_currency}"], 2)
    return amount

