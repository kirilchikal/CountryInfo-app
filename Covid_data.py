import requests
from bs4 import BeautifulSoup

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


print(covid_data("Poland"))

