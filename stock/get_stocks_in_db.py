from pyspark.sql import SparkSession
import pyspark
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
import numpy as np
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.0 pyspark-shell'

def get_stocks_by_spark(symbol):
    spark = pyspark.sql.SparkSession.builder\
        .appName('test-mongo')\
        .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/trading." + symbol) \
        .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/trading." + symbol ) \
        .getOrCreate()
    
    sc = spark.sparkContext

    rdd = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    # rdd.show()
    df = rdd.select("*").toPandas()
    df = df[['date', 'symbol', 'open', 'close', 'high', 'low', 'volume']]
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    spark.stop()
    return df

def get_stocks_by_mongo(symbol):
    from pymongo import MongoClient
    client = MongoClient('localhost', 27017)
    db = client.trading
    collection = db[symbol]
    df = pd.DataFrame(list(collection.find()))
    df = df[['date', 'symbol', 'open', 'close', 'high', 'low', 'volume']]
    df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)
    return df


def get_price_at_close(df, predict_nb_day):

    df2 = df[['date','close']]
    df2 = df2.resample('1440Min', on='date').first().drop('date', 1).reset_index()
    df2 = df2.fillna(method='ffill')
    date = df2[-1:]['date']
    for _ in range(predict_nb_day):
        dayplus = {"date": date + pd.DateOffset(1), "close":np.nan}
        df2 = df2.append(pd.DataFrame(dayplus))
    df2 = df2.set_index('date')

    return df2, predict_nb_day

# if __name__ == '__main__':
#     df = get_data('GOOGL')
#     print(df.head())



