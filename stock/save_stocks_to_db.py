from pymongo import MongoClient
import pymongo
import json
from cred import getApiKey

def get_stock_to_mongodb(symbol):

    KEY = getApiKey()

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

    symbol =  'GOOGL'
    get_stock_to_mongodb(symbol)


