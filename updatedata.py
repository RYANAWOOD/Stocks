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

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter

def pull_historical(stock):
    try:
        filep = open('largedata/' + stock + '.txt', 'r+')
        fileContents = filep.read()
        data = fileContents.splitlines()

        try:
            if len(data) < 3:
                print('empty')
                lastDay = int(data[-2].split(',')[0])
            else:
                lastDay = int(data[-1].split(',')[0])
        except:
            print('could not determine the last date of the file: ' + stock + '.txt')

        openurl = urllib.request.urlopen('http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=3y/csv').read()        
        lines = str(openurl, encoding='utf-8').splitlines()
        for line in lines:
            if 'values:' not in line:
                splittedLine = line.split(',')
                if len(splittedLine) == 6 and 'labels' not in splittedLine[0][0]:
                    if int(splittedLine[0]) > lastDay:
                        filep.write(str(splittedLine[0]) + ',' + str(splittedLine[4]) + ',' + str(splittedLine[2]) + ',' + str(splittedLine[3]) + ',' + str(splittedLine[1]) + ',' + str(splittedLine[5]) + '\n')
        filep.close()
        print('\t' + str(stock).upper())

    except Exception as e:
        if str(e) == 'HTTP Error 404: Not Found':
            print('\t' + str(stock).upper() + ' Data unavailable')
            failed.append(stock)
        else:
            print(str(e))

if __name__ == '__main__':

    filetoanalyze = str('r3000.txt')            
    file = open(filetoanalyze, 'r')
    temp = file.read()
    stemp = temp.splitlines()
    file.close()

    failed = []
    
    for index,stock in enumerate(stemp):
        try:
            print(str(index) + ' of ' + str(len(stemp)),end=' ')
            pull_historical(stock)
            time.sleep(0.5)
        except Exception as  e:
            print('could not pull ' + stock,str(e))

    for failure in sorted(failed):
        print(failure)


            