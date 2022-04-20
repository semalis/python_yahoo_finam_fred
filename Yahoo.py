import urllib.request, json , time, os, difflib, itertools
import pandas as pd
from multiprocessing.dummy import Pool
from datetime import datetime, date
import time

try:
    import httplib
except:
    import http.client as httplib


def check_internet():
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        # print("True")
        return True
    except:
        conn.close()
        # print("False")
        return False


def get_historic_price(query_url, csv_path):
    while not check_internet():
        print("Could not connect, trying again in 5 seconds...")
        time.sleep(5)

    stock_id = query_url.split("&period")[0].split("symbol=")[1]

    if os.path.exists(csv_path + stock_id + '.csv') and os.stat(csv_path + stock_id + '.csv').st_size != 0:
        print("<<<  Historical data of " + stock_id + " already exists, Updating data...")

    try:
        with urllib.request.urlopen(query_url) as url:
            parsed = json.loads(url.read().decode())
    except:
        print("|||  Historical data of " + stock_id + " doesn't exist")
        return

    else:
        # if os.path.exists(json_path + stock_id + '.json'):
        #     os.remove(json_path + stock_id + '.json')
        # with open(json_path + stock_id + '.json', 'w') as outfile:
        #     json.dump(parsed, outfile, indent=4)

        try:
            Date = []
            for i in parsed['chart']['result'][0]['timestamp']:
                Date.append(datetime.utcfromtimestamp(int(i)).strftime('%d-%m-%Y'))

            Low = parsed['chart']['result'][0]['indicators']['quote'][0]['low']
            Open = parsed['chart']['result'][0]['indicators']['quote'][0]['open']
            Volume = parsed['chart']['result'][0]['indicators']['quote'][0]['volume']
            High = parsed['chart']['result'][0]['indicators']['quote'][0]['high']
            Close = parsed['chart']['result'][0]['indicators']['quote'][0]['close']
            Adjusted_Close = parsed['chart']['result'][0]['indicators']['adjclose'][0]['adjclose']

            df = pd.DataFrame(list(zip(Date, Low, Open, Volume, High, Close, Adjusted_Close)),
                              columns=['Date', 'Low', 'Open', 'Volume', 'High', 'Close', 'Adjusted Close'])

            if os.path.exists(csv_path + stock_id + '.csv'):
                os.remove(csv_path + stock_id + '.csv')
            df.to_csv(csv_path + stock_id + '.csv', sep=',', index=None)
            df.to_excel(csv_path + stock_id + '.xlsx')
            print(">>>  Historical data of " + stock_id + " saved")
            return
        except:
            print(">>>  Historical data of " + stock_id + " exists but has no trading data")

# json_path = "historic_data"+os.sep+"json"+os.sep
# csv_path = "historic_data"+os.sep+"csv"+os.sep
json_path = "history\historic_data.json"
csv_path = "history\historic_data.csv"

d = date(2000, 2, 1)
unixtime_start = str(int(time.mktime(d.timetuple())))
# print(unixtime_start)

# interval = '1d'
interval = '1mo'
# ticker_list = [ 'AAPL', 'DAL', 'VIXY']
ticker_list = [
    'SPY',
    # 'VCR',
    # 'BLV',
    # 'VDE',
    # 'VAW',
    # 'VOO',
    # 'QQQ',
    # 'KWEB',
    # 'VNQ',
    # 'TLT',
    # 'BAR',
    # 'IAU',
    # 'COMT',
    # 'VIXY',
    # 'BTC-USD',
               ]

query_urls=[]
for ticker in ticker_list:
    query_urls.append("https://query1.finance.yahoo.com/v8/finance/chart/"+ticker+"?symbol="+ticker+"&period1="+unixtime_start+"&period2=9999999999&interval="+interval+"&includePrePost=true&events=div%2Csplit")

with Pool(processes=len(query_urls)) as pool:
    pool.starmap(get_historic_price, zip(query_urls, itertools.repeat(csv_path)))
print("All downloads completed !")