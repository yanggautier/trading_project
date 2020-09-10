from pymongo import MongoClient
from alpha_vantage.timeseries import TimeSeries
import json
import pprint


def update_stock(symbol):

    KEY = "7TW80K6HLVAZXBQO"

    ts = TimeSeries(key=KEY, output_format='pandas')
    data, meta_data = ts.get_daily(symbol=symbol, outputsize = 'full')

    client = MongoClient('localhost', 27017)
    db = client['trading']
    collection = db[symbol]

    collection.drop()

    data = data.rename(columns={"1. open": "open", "2. high": "high", "3. low": "low","4. close":"close", "5. volume":"volume"})
    #data = pd.concat([data, pd.DataFrame(columns=["symbol"])])
    data["symbol"] = symbol

    stock = json.loads(data.to_json(orient='table') )
    # pprint.pprint(stock)
    collection.insert_many(stock['data'])


if __name__ == "__main__":

    symbol =  'AAPL'
    update_stock(symbol)


