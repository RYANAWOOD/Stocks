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

def pullData(stock):
	try:
		os.remove(stock+'.txt')
	except:
		pass
	try:
		print('currently pulling', stock)
		urlToVisit = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range=1d/csv'
		saveFileLine = stock+'.txt'

		try:
			readExistingData = open(saveFileLine, 'r').read()
			splitExisting = readExistingData.split('\n')
			mostRecentLine = splitExisting[-2]
			lastUnix = mostRecentLine.split(',')[0]
		except:
			lastUnix = 0

		saveFile = open(saveFileLine, 'a')
		sourceCode = urllib.request.urlopen(urlToVisit).read()
		splitSource = str(sourceCode, encoding='utf8').split('\n')

		temp = 0.0
		for eachLine in splitSource:
			if 'values' not in eachLine:
				splitLine = eachLine.split(',')
				if len(splitLine) == 6:
					splitLine[0] = datetime.datetime.fromtimestamp(int(splitLine[0])).strftime('%Y%m%d%H%M%S')
					if int(splitLine[0]) > int((temp + 100)):
						lineToWrite = ",".join(splitLine)+"\n"
						saveFile.write(lineToWrite)
						temp = int(splitLine[0])
		saveFile.close()

		print('pulled', stock)

	except Exception as  e:
		print('main loop', str(e))

def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter
    
def graph_data(stock):
    #fig = plt.figure()
    #fig.patch.set_facecolor('#DAD1CF')

    stockFile = stock+'.txt'
    string = str('%Y%m%d%H%M%S')

    if period == 'INTRADAY':
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={ 0: bytespdate2num('%Y%m%d%H%M%S')})
        pass
    else:
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={ 0: bytespdate2num('%Y%m%d')})


    ohlc = []
    ax1 = plt.subplot2grid((6,4), (0,0), rowspan=5, colspan=4)
    plt.ylabel('Price ($)')
    plt.title(stock + ' (' + time.strftime("%m/%d/%Y") + ')')

    ax2 = plt.subplot2grid((6,4), (5,0), rowspan=1, colspan=4, sharex = ax1)

    for x in range(len(date)):
        appendLine = date[x],openp[x],highp[x],lowp[x],closep[x],volume[x]
        ohlc.append(appendLine)

    if period == 'INTRADAY':
        wideness = 0.0005
    else:
    	wideness = 0.2
    candlestick_ohlc(ax1, ohlc, width=wideness, colorup='#77d879', colordown='#db3f3f')

    if period == 'INTRADAY':
    	string = str('%I:%m')
    elif period == '1y':
    	string = str('%m/%d')
    else:
    	string = str('%m/%d/%Y')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(string))
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(12))
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=2, prune='upper'))
    ax1.grid(True)
    ax2.grid(True)
    for label in ax2.xaxis.get_ticklabels():
        label.set_rotation(45)
    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(45)
    
    ax2.bar(date, (highp - lowp), width = 0.0005)
    plt.xlabel('Date, period: ' + period)
    
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90)
    plt.setp(ax1.get_xticklabels(), visible = False)

    print('graphing stock information ', end = '')
    if outputType == 'WEBSITE':
        print('to website')
        mpld3.show()
    else:
        print('to terminal')
        plt.show()

def pull_historical(stock,period):
	try:
		os.remove(stock+'.txt')
	except:
		pass

	try:
		print('currently pulling', stock)
		if '1 Y' not in period and '1Y' not in period:
			period = '10y'
		else:
			period = '1y'

		url = 'http://chartapi.finance.yahoo.com/instrument/1.0/' + stock + '/chartdata;type=quote;range='+ period +'/csv'
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
		return period

	except Exception as e:
		print('Error:', str(e))

if __name__ == '__main__':
    try:
        stock = input('Stock to pull: ').upper()
        #outputType = input('Output format: ').upper()
        outputType = str('INTRADAY')
        period = input('Period: ').upper()

        if stock == 'exit' or stock == '':
            exit

        if period == 'INTRADAY':
            pullData(stock)
        else:
            period = pull_historical(stock,period)

        graph_data(stock)
    except Exception as  e:
        print('main loop. ', str(e))