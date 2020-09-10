from pyspark.sql import SparkSession
import pyspark
import os
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.mongodb.spark:mongo-spark-connector_2.12:3.0.0 pyspark-shell'

def get_data(symbol):
    spark = pyspark.sql.SparkSession.builder\
        .appName('test-mongo')\
        .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/trading." + symbol) \
        .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/trading." + symbol ) \
        .getOrCreate()
    
    sc = spark.sparkContext

    rdd = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    # rdd.show()
    df = rdd.select("*").toPandas()

    df = df[['date','symbol','open','close','high','low', 'volume']]

    df['date'] =  df['date'].apply(lambda x: datetime.fromisoformat(x[:-1]))

    df = df.set_index("date")

    spark.stop()
    return df

if __name__ == '__main__':
    df = get_data('AAPL')
    print(df.head())



