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
        filep = open('largedata/' + stock + '.txt', 'a+')
        openurl = urllib.request.urlopen('http://chart.finance.yahoo.com/table.csv?s=' + stock.upper() + '&a=2&b=13&c=1986&d=1&e=3&f=2017&g=d&ignore=.csv').read()
        data = str(openurl, encoding='utf-8').splitlines()

        try:
            lastDay = int(data[1][:4] + data[1][5:7] + data[1][8:10])
            try:
                # I put this in the "could not determine the last date..." try-except so that if pulling data fails the original .txt files will be untouched
                os.remove('largedata/' + stock + '.txt')
                filep = open('largedata/' + stock + '.txt', 'a+')
            except:
                pass
        except:
            print('could not determine the last date of largedata pull')

        for i in range(len(data)):
            datum = data[len(data) - i - 1]
            if datum[0] != 'D' and len(datum) >= 3:
                for character in datum:
                    if character != '-':
                        filep.write(character)

                filep.write('\n')

        openurl = urllib.request.urlopen('http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=3y/csv').read()        
        lines = str(openurl, encoding='utf-8').splitlines()
        for index,line in enumerate(lines):
            if 'values:' not in line and 'labels:' not in line:
                splittedLine = line.split(',')
                if len(splittedLine) == 6:
                    if int(splittedLine[0]) > lastDay:
                        filep.write(str(splittedLine[0]) + ',' + str(splittedLine[4]) + ',' + str(splittedLine[2]) + ',' + str(splittedLine[3]) + ',' + str(splittedLine[1]) + ',' + str(splittedLine[5]))
                        if index < (len(lines) - 1):
                            filep.write('\n')
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

    print('Unavailable(' + str(len(failed)) + '):')

    for failure in sorted(failed):
        print(failure)


