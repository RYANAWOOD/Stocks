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
matplotlib.rcParams.update({'font.size': 9})

style.use('grayscale')

#print(plt.style.available)
#print(plt.__file__)

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter
    
def graph_data(stock):
    #fig = plt.figure()
    #fig.patch.set_facecolor('#DAD1CF')

    fig = plt.figure()
    fig.patch.set_facecolor('#DAD1CF')
    ax1 = plt.subplot2grid((5,1), (0,0), rowspan=5, colspan=1)
    plt.grid(True)
    plt.title('Graph of ' + stock.upper() + ' in Period: 1y')
    plt.ylabel('Stock Price ($)')
    plt.xlabel('Date')
    
    stockInfo = stock+'.txt'
    date, closep, highp, lowp, openp, volume = np.loadtxt(stockInfo, delimiter=',', unpack=True, converters={0: bytespdate2num('%Y%m%d')})

    g_array = []
    numberToShow = 15
    for i in range(numberToShow): 
        line_append = date[i-numberToShow], openp[i-numberToShow], highp[i-numberToShow], lowp[i-numberToShow], closep[i-numberToShow], volume[i-numberToShow]
        g_array.append(line_append)
    
    candlestick_ohlc(ax1, g_array, width=0.4, colorup='#46AE21', colordown='#E32323')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)

    plt.setp(ax1.get_xticklabels(), visible=True)
    plt.subplots_adjust(bottom=0.20, top=0.92, left=0.11, right=0.93)
    plt.grid(True)
    
    plt.show()

def pull_historical(stock):
    url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=1y/csv'
    stockInfo = stock+'.txt'
    try:
        temp = open(stockInfo, 'r').read()
        stemp = temp.splitlines()
        mtemp = stemp[-2]
        last_time_unix = mtemp.split(',')[0]
        temp.close()
    except:
        last_time_unix = 0
    
    if time.strftime("%Y%m%d") == last_time_unix:
        return

    try:
        os.remove(stock+'.txt')
    except:
        pass

    try:
        print('currently pulling', stock)

        url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=1y/csv'
        stockInfo = stock+'.txt'
        try:
            temp = open(stockInfo, 'r').read()
            stemp = temp.splitlines()
            mtemp = stemp[-2]
            last_time_unix = mtemp.split(',')[0]
            temp.close()
        except:
            last_time_unix = 0

        filep = open(stockInfo, 'a+')
        openurl = urllib.request.urlopen(url).read()
        data = str(openurl, encoding='utf-8').splitlines()

        for datum in data:
            if 'values:Timestamp' not in datum and 'values:Date' not in datum:
                sdatum = datum.split(',')
                if len(sdatum) == 6:
                    if int(sdatum[0]) > int(last_time_unix):
                        line_write = datum+'\n'
                        filep.write(line_write)
        filep.close()

    except Exception as e:
        print('Error:', str(e))


try:
    stock = input('Stock to pull: ').upper()

    if stock == 'exit' or stock == '':
        exit
    
    #pull_historical(stock)
    graph_data(stock)
except Exception as  e:
    print('main loop. ', str(e))
