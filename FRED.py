from fredapi import Fred

import configparser
# Загрузка ключей из файла config
config = configparser.ConfigParser()
config.read_file(open('secret.cfg'))
api_key = config.get('FREED', 'API_KEY')

fred = Fred(api_key=api_key)
data = fred.get_series('GDP')

print(data.tail())
