import os
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
import urllib.request, urllib.error, urllib.parse
from matplotlib.finance import candlestick_ohlc
import matplotlib
from matplotlib import style

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def pull_historical(stock):
    try:
        url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=3y/csv'
        stockInfo = stock+'.txt'
        
        try:
            file = open(stockInfo, 'r')
            temp = file.read()
            stemp = temp.splitlines()
            mtemp = stemp[-1]
            last_time_unix = mtemp.split(',')[0]
            file.close()
        except:
            last_time_unix = 0

        try:
            os.remove(stock+'.txt')
        except:
            pass

        filep = open(stockInfo, 'a+')
        openurl = urllib.request.urlopen(url).read()
        data = str(openurl, encoding='utf-8').splitlines()

        for datum in data:
            if 'values:' not in datum and 'values:Date' not in datum:
                sdatum = datum.split(',')
                if len(sdatum) == 6:
                    line_write = datum+'\n'
                    filep.write(line_write)
        filep.close()
        print('\t' + (str(stock)).upper())

    except Exception as e:
        print('Error:', str(e))




if __name__ == '__main__':
    delay = int(input('delay between pulls(seconds): '))

    filetoanalyze = str('list.txt')            
    file = open(filetoanalyze, 'r')
    temp = file.read()
    stemp = temp.splitlines()
    file.close()
    
    for stock in stemp:
        try:
            pull_historical(stock)
            time.sleep(delay+0.1)
        except Exception as  e:
            print('could not pull ' + stock,str(e))