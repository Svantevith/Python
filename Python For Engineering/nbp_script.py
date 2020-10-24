'''
This is my first spript.
'''

# from pathlib import Path
# import sys
import argparse
from itertools import islice
from urllib import request as rq
import json
from urllib.error import HTTPError

# The argparse module makes it easy to write user-friendly command-line interfaces.

# -----------------------------------------

description = '''This is a description of what the script does.
This script:
- displays the entire table of currency rates
- displays the rate of a single currency
- displays the current price of gold
'''


def parser_function():
    '''Function parsing command line arguments'''
    parser = argparse.ArgumentParser(description=description)

    # Add arguments to your module: mandatory, i.e. positional and optional i.e.
    parser.add_argument('table', type=str,
                        help=u'''Tables:
                        a = table of average exchange rates of foreign currencies,
                        b = table of average rates of inconvertible currencies,
                        c = buying and selling rates table''')

    parser.add_argument('--currency', type=str,
                        help=u'''Currency code''')

    parser.add_argument('--gold',
                        dest='gold',
                        action='store_true',
                        help=u'''Display the current price of gold''')

    parser.add_argument('-p', '--somePath', type=str, help=u'''Path to folder''')

    _args = parser.parse_args()
    return _args


def json_rates_to_dict(all_rates):
    return {rates['code']: {key: value for key, value in rates.items() if key != 'code'} for rates in all_rates}


def show_json_dict(rates_json):
    print('\nCURRENCY CODE | CURRENCY NAME | VALUES\n')
    rates_dict = json_rates_to_dict(rates_json)
    for currency_code, rates in rates_dict.items():
        print(f"{currency_code}, {rates['currency']}, {', '.join([f'{key}: {val}' for key, val in list(rates.items())[1:]])}")

def show_dict(_dict):
    for key, val in _dict.items():
        print(f'{key}:\t{val}')


class JSONDict:
    def __init__(self, table: str, **kwargs):
        self.table = table
        self.code = kwargs.get('code')
        self.gold = kwargs.get('gold')

        self.all_rates = self.load_json(f'http://api.nbp.pl/api/exchangerates/tables/{self.table.lower()}')
        if self.code:
            self.currency_rates = self.load_json(f'http://api.nbp.pl/api/exchangerates/rates/{self.table}/{self.code.lower()}')
        else:
            self.currency_rates = None
        self.gold_price = self.load_json('http://api.nbp.pl/api/cenyzlota/')

    @staticmethod
    def load_json(url):
        try:
            all_rates_query = rq.urlopen(url)
        except HTTPError:
            print('Error 404: Page not found:', url)
        else:
            return json.loads(all_rates_query.read())

    def show_all_rates(self):
        if self.all_rates is not None:
            print(f"\nCurrency rates for entire {self.table.upper()} table:")
            show_json_dict(self.all_rates[0]['rates'])

    def show_currency_rates(self):
        if self.currency_rates is not None:
            print(f"\n\nRate of {self.currency_rates['code']}:\n")
            show_dict(self.currency_rates['rates'][0])

    def show_gold_price(self):
        if self.gold_price is not None:
            print(f"\n\nCurrent price of gold:\n")
            show_dict(self.gold_price[0])

    def describe(self):
        self.show_all_rates()
        self.show_currency_rates()
        if self.gold:
            self.show_gold_price()


def main(_args):
    print('\nRemark:\n' +
          '* All prices in the tables below refer to the PLN currency.\n')

    _args_dict = vars(_args)

    # All rates (mandatory)
    _table = _args_dict['table']
    # Currency rates (optional)
    _code = _args_dict['currency']
    # Gold (optional with default value)
    _gold = _args_dict['gold']

    # Create JSONDict object
    json_dict = JSONDict(table=_table, code=_code, gold=_gold)
    json_dict.describe()


# ------------------------------------------

if __name__ == '__main__':
    args = parser_function()
    main(args)
