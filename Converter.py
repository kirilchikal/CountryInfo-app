import requests

url = str.__add__('http://data.fixer.io/api/latest?access_key=', "25c5a69737681bde5e7bc98dc2b28bcc")


class Currency_convertor:
    # empty dict to store the conversion rates
    rates = {}

    def __init__(self):
        data = requests.get(url).json()

        # Extracting only the rates from the json data
        self.rates = data["rates"]

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != 'EUR':
            amount = amount / self.rates[from_currency]

        # limiting the precision to 2 decimal places
        amount = round(amount * self.rates[to_currency], 2)
        # print('{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency))
        return amount





