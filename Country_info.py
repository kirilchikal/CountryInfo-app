from countryinfo import CountryInfo
from tkinter import *
import pytz
from datetime import datetime
import geocoder
import requests
from bs4 import BeautifulSoup
from PIL import Image


class Clock:
    """ Class that contains the clock widget and clock refresh """

    def __init__(self, parent, code):
        """
        Create the clock widget
        It's an ordinary Label element
        """
        self.zone = pytz.country_timezones(code)[0]
        now = datetime.now(pytz.timezone(self.zone))
        self.time = now.strftime('%H:%M:%S')
        self.widget = Label(parent, text=self.time)
        self.widget.after(200, self.tick)  # Wait 200 ms, then run tick()

    def tick(self):
        """ Update the display clock """
        now = datetime.now(pytz.timezone(self.zone))
        new_time = now.strftime('%H:%M:%S')
        if new_time != self.time:
            self.time = new_time
            self.widget.config(text=self.time)
        self.widget.after(200, self.tick)


def user_geo(country_name="me"):
    if country_name == "me":
        code = geocoder.ip(country_name).country
        country = CountryInfo(code)
    else:
        country = CountryInfo(country_name)
        code = country.iso(2)
    name = country.name().capitalize()
    timezone = country.timezones()
    currency = country.currencies() if code != "BY" else ["BYN"]
    return code, name, timezone, currency


def country_info(country_name):
    d = []
    country = CountryInfo(country_name)
    d.append(("name", country.name().capitalize()))
    d.append(("capital", country.capital().capitalize()))
    d.append(("region", country.region().capitalize()))
    d.append(("currency", country.currencies()))
    d.append(("area", country.area()))
    d.append(("population", country.population()))
    d.append(("languages", country.languages()))
    d.append(("borders", country.borders()))
    d.append(("calling code", country.calling_codes()))
    d.append(("lat/long", country.capital_latlng()))
    d.append(("code", country.iso(2)))
    return d


def get_distance(start, destination):
    d = geocoder.distance(start, destination)
    return round(d, 2)


page = requests.get('https://www.worldometers.info/coronavirus/#countries')
soup = BeautifulSoup(page.content, 'html.parser')
rows = soup.findChildren("tr")


def covid_data(country):
    if country.lower() == "united states":
        country = "USA"
    if country.lower() == "united kingdom":
        country = "UK"
    data = []

    for i in range(len(rows)):
        a = rows[i].findChildren("a")
        if len(a) != 0 and a[0].text.lower() == country.lower():
            items = rows[i].find_all("td")
            for k in range(2, 7):
                data.append(items[k].text)
            break
    return data


icons = {'loc': Image.open(requests.get("https://img.icons8.com/wired/50/ffffff/user-location.png", stream=True).raw),
         'search': Image.open(
             requests.get("https://img.icons8.com/pastel-glyph/20/ffffff/search--v2.png", stream=True).raw),
         'capital': Image.open(
             requests.get("https://img.icons8.com/pastel-glyph/16/044a72/bank-building.png", stream=True).raw),
         'region': Image.open(requests.get("https://img.icons8.com/ios/16/044a72/globe--v1.png", stream=True).raw),
         'currency': Image.open(
             requests.get("https://img.icons8.com/ios-filled/16/044a72/mts-money.png", stream=True).raw),
         'area': Image.open(
             requests.get("https://img.icons8.com/material/16/044a72/square-number.png", stream=True).raw),
         'population': Image.open(
             requests.get("https://img.icons8.com/pastel-glyph/16/044a72/person-male--v3.png", stream=True).raw),
         'languages': Image.open(
             requests.get("https://img.icons8.com/pastel-glyph/16/044a72/communication--v2.png", stream=True).raw),
         'borders': Image.open(
             requests.get("https://img.icons8.com/ios-filled/16/044a72/country.png", stream=True).raw),
         'calling code': Image.open(
             requests.get("https://img.icons8.com/ios-filled/16/044a72/phone-disconnected.png", stream=True).raw),
         'lat/long': Image.open(
             requests.get("https://img.icons8.com/material/16/044a72/worldwide-location--v1.png", stream=True).raw)
         }
