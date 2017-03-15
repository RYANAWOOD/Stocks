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

# http://chart.finance.yahoo.com/table.csv?s=VFINX&a=0&b=10&c=2017&d=1&e=10&f=2017&g=d&ignore=.csv
# http://chart.finance.yahoo.com/table.csv?s=VFINX&a=0&b=3&c=2017&d=1&e=3&f=2017&g=d&ignore=.csv

# outdated; use pulllargedata2.py instead

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def pull_historical(stock):
    try:
        try:
            os.remove('largedata/' + stock + '.txt')
        except:
            pass

        filep = open('largedata/' + stock + '.txt', 'a+')
        openurl = urllib.request.urlopen('http://chart.finance.yahoo.com/table.csv?s=' + stock.upper() + '&a=2&b=13&c=1986&d=1&e=3&f=2017&g=d&ignore=.csv').read()
        data = str(openurl, encoding='utf-8').splitlines()

        for datum in data:
            line_write = datum+'\n'
            filep.write(line_write)
        filep.close()
        print('\t' + str(stock).upper())

    except Exception as e:
        if str(e) == 'HTTP Error 404: Not Found':
            print('\t' + str(stock).upper() + ' Data unavailable')
        else:
            print(str(e))


if __name__ == '__main__':
    delay = int(input('delay between pulls(seconds): '))
    if delay == 0:
        delay = 0.5

    filetoanalyze = str('r3000.txt')            
    file = open(filetoanalyze, 'r')
    temp = file.read()
    stemp = temp.splitlines()
    file.close()
    
    for index,stock in enumerate(stemp):
        try:
            print(str(index) + ' of ' + str(len(stemp)),end=' ')
            pull_historical(stock)
            time.sleep(delay)
        except Exception as  e:
            print('could not pull ' + stock,str(e))