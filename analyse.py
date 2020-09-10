from getdata import *
import matplotlib.pyplot as plt
import sys
import datetime


def tserie_analyse(symbol):
    df = get_data(symbol) 
    df.open.plot(figsize=(12,8), title= 'Stocks by day', fontsize=14)

if __name__ == "__main__":
    # print(sys.executable)
    tserie_analyse("AAPL")  
