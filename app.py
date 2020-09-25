from flask import Flask, url_for, redirect, render_template, request
from stock.get_stocks_in_db import *
from model.predict_stock import *
import json

app = Flask(__name__)


get_stock_to_mongodb("GOOGL")
data = get_stocks_by_mongo("GOOGL")

datastring = data.to_json(orient='records', date_format='iso', date_unit='s')

datajson = json.loads(datastring)[::]
dates=list(data["date"])
closes=list(data["close"])
dates = dates[::-1]
closes = closes[::-1]
maxclose= max(closes)

# data_to_pred = get_price_at_close(data)

# predict = prediction(data_to_pred)


@app.route('/')
def index():
	return render_template("index.html", datajson=datajson, dates=dates,  closes=closes, maxclose=maxclose*1.1 )


if __name__ == '__main__':
	app.run(debug=True)