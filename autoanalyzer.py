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

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def pull_historical(stock):
    try:
        url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=1y/csv'
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
        
        if time.strftime('%Y%m%d') == last_time_unix:
            return

        print((str(stock)).upper() + ' DATA WAS PULLED FROM CHARTAPI.FINANCE.YAHOO.COM')
        
        try:
            os.remove(stock+'.txt')
        except:
            pass

        filep = open(stockInfo, 'a+')
        openurl = urllib.request.urlopen(url).read()
        data = str(openurl, encoding='utf-8').splitlines()

        for datum in data:
            if 'values:Timestamp' not in datum and 'values:Date' not in datum:
                sdatum = datum.split(',')
                if len(sdatum) == 6:
                    line_write = datum+'\n'
                    filep.write(line_write)
        filep.close()

    except Exception as e:
        print('Error:', str(e))

def lowerrealbody(dta):
    if openp[-dta] > closep[-dta]:
        lrb = closep[-dta]
    else:
        lrb = openp[-dta]
    return lrb

def upperrealbody(dta):
    if openp[-dta] < closep[-dta]:
        urb = closep[-dta]
    else:
        urb = openp[-dta]
    return urb

def hangingman(dta,rb):
    lrb = lowerrealbody(dta)
    urb = upperrealbody(dta)

    if rb < (1/2)*(lrb - lowp[-dta]) and (highp[-dta] - urb) < rb: # check that shape is correct
        if closep[-dta-1] > openp[-dta-1] and closep[-dta-1] < lrb: # check that previous day was bullish
            if dta >= 2 and openp[-dta+1] < lrb and closep[-dta+1] < openp[-dta+1]: # check that the previous day was bearish
                print('STRONG hanging man found ' + str(dta) + ' days ago')
            else:
            	print('Hanging man found ' + str(dta) + ' days ago')

def hammer(dta,rb):
    lrb = lowerrealbody(dta)
    urb = upperrealbody(dta)

    if rb < (1/2)*(lrb - lowp[-dta]) and (highp[-dta] - urb) < rb: # check that shape is correct
        if closep[-dta-1] < openp[-dta-1] and closep[-dta-1] > urb: # check that previous day was bearish
            if dta >= 2 and openp[-dta+1] > urb and closep[-dta+1] > openp[-dta+1]: # check that the previous day was bullish
            	print('STRONG hammer found ' + str(dta) + ' days ago')
            else:
            	print('Hammer found ' + str(dta) + ' days ago')

def bearengulf(dta):
    lrb = lowerrealbody(dta)
    urb = upperrealbody(dta)

    if closep[-dta-1] > openp[-dta-1] and closep[-dta] < openp[-dta]: # check that first rb is green and second rb is red
        if urb > closep[-dta-1] and lrb < openp[-dta-1]:
        	print('Bearish engulfing pattern found ' + str(dta) + ' days ago')

def bullengulf(dta):
    lrb = lowerrealbody(dta)
    urb = upperrealbody(dta)

    if closep[-dta-1] < openp[-dta-1] and closep[-dta] > openp[-dta]: # check that first rb is red and second rb is green
        if lrb < closep[-dta-1] and urb > openp[-dta-1]:
        	print('Bullish engulfing pattern found ' + str(dta) + ' days ago')

def piercing(dta):
    plrb = lowerrealbody(dta + 1) # create lower real body for the previous day
    purb = upperrealbody(dta + 1) # create upper real body for the previous day
    
    if closep[-dta-1] < openp[-dta-1] and closep[-dta] > openp[-dta]: # check that previous day was red and current day was green
        if openp[-dta] < closep[-dta-1] and closep[-dta] > (openp[-dta-1] - (1/2)*(purb - plrb)) and closep[-dta] <= openp[-dta-1]: # check current open lower than previous close and current close in upper half of previous body
            print('Piercing pattern found ' + str(dta) + ' days ago')

def darkcloudcover(dta):
    plrb = lowerrealbody(dta + 1) # create lower real body for the previous day
    purb = upperrealbody(dta + 1) # create upper real body for the previous day

    if closep[-dta-1] > openp[-dta-1] and closep[-dta] < openp[-dta]: # check that previous day was green and current day was red
        if openp[-dta] > closep[-dta-1] and closep[-dta] < (closep[-dta-1] - (1/2)*(purb - plrb)) and closep[-dta] >= openp[-dta-1]:
            print('Dark cloud cover found ' + str(dta) + ' days ago')

if __name__ == '__main__':

    while True:
        stock = input('stock to analyze: ')
        if stock == '' or stock == 'exit':
            break
        pull_historical(stock)
        stockInfo = stock+'.txt'
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockInfo,delimiter=',', unpack=True, converters={ 0: bytespdate2num('%Y%m%d')})
        for i in range(20):
            dta = i + 1 # Day To Analyze
            rb = abs(openp[-dta] - closep[-dta]) # Real Body
            hangingman(dta,rb)
            hammer(dta,rb)
            bearengulf(dta)
            bullengulf(dta)
            piercing(dta)
            darkcloudcover(dta)
