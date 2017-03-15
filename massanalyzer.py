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

counter = 0

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
        
        #if time.strftime('%Y%m%d') == last_time_unix:
        #    return

        print((str(stock)).upper() + '\tDATA WAS PULLED FROM CHARTAPI.FINANCE.YAHOO.COM')
        
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

def downtrend(dta):
    if (upperrealbody(dta) + lowerrealbody(dta)) < (upperrealbody(dta+1) + lowerrealbody(dta+1)) and (upperrealbody(dta+1) + lowerrealbody(dta+1)) < (upperrealbody(dta+2) + lowerrealbody(dta+2)):
        return True
    return False

def uptrend(dta):
    if (upperrealbody(dta) + lowerrealbody(dta)) > (upperrealbody(dta+1) + lowerrealbody(dta+1)) and (upperrealbody(dta+1) + lowerrealbody(dta+1)) > (upperrealbody(dta+2) + lowerrealbody(dta+2)):
        return True
    return False

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
                return True
            else:
            	return True
    return False

def hammer(dta,rb):
    lrb = lowerrealbody(dta)
    urb = upperrealbody(dta)

    if rb < (1/2)*(lrb - lowp[-dta]) and (highp[-dta] - urb) < rb: # check that shape is correct
        if closep[-dta-1] < openp[-dta-1] and closep[-dta-1] > urb: # check that previous day was bearish
            if dta >= 2 and openp[-dta+1] > urb and closep[-dta+1] > openp[-dta+1]: # check that the previous day was bullish
            	return True
            else:
            	return True
    return False

def bearengulf(dta):
    lrb = lowerrealbody(dta)
    urb = upperrealbody(dta)

    if closep[-dta-1] > openp[-dta-1] and closep[-dta] < openp[-dta]: # check that first rb is green and second rb is red
        if urb > closep[-dta-1] and lrb < openp[-dta-1]:
        	return True
    return False

def bullengulf(dta):
    lrb = lowerrealbody(dta)
    urb = upperrealbody(dta)

    if closep[-dta-1] < openp[-dta-1] and closep[-dta] > openp[-dta]: # check that first rb is red and second rb is green
        if lrb < closep[-dta-1] and urb > openp[-dta-1]:
        	return True
    return False

def piercing(dta):
    plrb = lowerrealbody(dta + 1) # create lower real body for the previous day
    purb = upperrealbody(dta + 1) # create upper real body for the previous day
    
    if closep[-dta-1] < openp[-dta-1] and closep[-dta] > openp[-dta]: # check that previous day was red and current day was green
        if openp[-dta] < closep[-dta-1] and closep[-dta] > (openp[-dta-1] - (1/2)*(purb - plrb)) and closep[-dta] <= openp[-dta-1]: # check current open lower than previous close and current close in upper half of previous body
            return True
    return False

def darkcloudcover(dta):
    plrb = lowerrealbody(dta + 1) # create lower real body for the previous day
    purb = upperrealbody(dta + 1) # create upper real body for the previous day

    if closep[-dta-1] > openp[-dta-1] and closep[-dta] < openp[-dta]: # check that previous day was green and current day was red
        if openp[-dta] > closep[-dta-1] and closep[-dta] < (closep[-dta-1] - (1/2)*(purb - plrb)) and closep[-dta] >= openp[-dta-1]:
            return True
    return False

def bullharami(dta):
    if closep[-dta] > openp[-dta] and closep[-dta-1] < openp[-dta-1]: # check that the previous day was red and the current day was green
        if (closep[-dta] - openp[-dta]) < (openp[-dta-1] - closep[-dta-1]): # check that the previous day was longer than the current day
            if closep[-dta] < openp[-dta-1] and openp[-dta] > closep[-dta-1]: # check the previous day engulfs the current day
                return True
    return False

def bearharami(dta):
    if closep[-dta] < openp[-dta] and closep[-dta-1] > openp[-dta-1]: # check that the previous day was green and the current day was red
        if (openp[-dta] - closep[-dta]) < (closep[-dta-1] - openp[-dta-1]): # check that the previous day was longer than the current day
            if closep[-dta] > openp[-dta-1] and openp[-dta] < closep[-dta-1]: # check the previous day engulfs the current day
                return True
    return False

def bullharamicross(dta):
    if bullharami(dta) and openp[-dta] == closep[-dta]:
        return True
    return False

def bearharamicross(dta):
    if bearharami(dta) and openp[-dta] == closep[-dta]:
        return True
    return False

def invertedhammer(dta,rb):
    if closep[-dta-1] > openp[-dta]: # check the inverted hammer opened below the previous day close
        if (highp[-dta] - openp[-dta]) > 2*rb and (highp[-dta] - closep[-dta]) > 2*rb: # check the upper shadow is 2x length of real body
            if (openp[-dta] - lowp[-dta]) < (0.1)*(highp[-dta] - lowp[-dta]) and (closep[-dta] - lowp[-dta]) < (0.1)*(highp[-dta] - lowp[-dta]): #check the lower shadow is <10% of total price range
                return True
    return False

def shootingstar(dta,rb):
    if closep[-dta-1] < openp[-dta]: # check the shooting star opened above the previous day close
        if (highp[-dta] - openp[-dta]) > 2*rb and (highp[-dta] - closep[-dta]) > 2*rb: # check the upper shadow is >2x length of real body
            if (openp[-dta] - lowp[-dta]) < (0.1)*(highp[-dta] - lowp[-dta]) and (closep[-dta] - lowp[-dta]) < (0.1)*(highp[-dta] - lowp[-dta]): #check the lower shadow is <10% of total price range
                return True
    return False

'''def bulldojistar(dta):

def beardojistar(dta):

def bullishmeetingline(dta):

def bearishmeetingline(dta):

def homingpigeon(dta):

def descendinghawk(dta):
'''
def matchinglow(dta):
    if (abs(closep[-dta] - closep[-dta-1]) / closep[-dta-1]) <= 0.001:
        if (closep[-dta] - openp[-dta]) < 0 and (closep[-dta-1] - openp[-dta-1]) < 0:
            return True
    return False

def matchinghigh(dta):
    if (abs(closep[-dta] - closep[-dta-1]) / closep[-dta-1]) <= 0.001:
        if (closep[-dta] - openp[-dta] > 0 and closep[-dta-1] - openp[-dta-1] > 0):
            return True
    return False

'''
def bullishkicking(dta):

def bearishkicking(dta):

def onewhitesoldier(dta):

def oneblackcrow(dta):

def morningstar(dta):

def eveningstar(dta):

def morningdojistar(dta):

def eveningdojistar(dta):

def bullishabandonedbaby(dta):

def bearishabandonedbaby(dta):

def bullishtristar(dta):

def bearishtristar(dta):

def upsidegaptwocrows(dta):

def downsidegaptworabbits(dta):

def threewhitesoldiers(dta):

def threeblackcrows(dta):

def advanceblock(dta):

def descentblock(dta):

def bullishdeliberation(dta):

def bearishdeliberation(dta):'''


  

if __name__ == '__main__':

    filetoanalyze = str('list.txt')
    file = open(filetoanalyze, 'r')
    temp = file.read()
    stemp = temp.splitlines()
    file.close()

    stocks = [] # to store list of stocks that are, as of now, matching lows
    dta = 1 # Day To Analyze
    daysoffset = dta + 2 # days to go back: to be used for determining uptrends and downtrends
    showweakpatterns = False
    
    for stock in stemp:
        if len(stock) > 0:
            stock = stock.upper()
            #pull_historical(stock)
            stockInfo = stock+'.txt'
            try:
                date, closep, highp, lowp, openp, volume = np.loadtxt(stockInfo,delimiter=',', unpack=True, converters={ 0: bytespdate2num('%Y%m%d')})    
                rb = abs(openp[-dta] - closep[-dta]) # Real Body
                if hangingman(dta,rb):
                    counter += 1
                    if uptrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \thanging man')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\thanging man')
                if hammer(dta,rb):
                    counter += 1
                    if downtrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \thammer')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\thammer')
                if bearengulf(dta):
                    counter += 1
                    if uptrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tbearish engulfing pattern')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tbearish engulfing pattern')
                if bullengulf(dta):
                    counter += 1
                    if downtrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tbullish engulfing pattern')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tbullish engulfing pattern')
                if piercing(dta):
                    counter += 1
                    if downtrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tpiercing pattern')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tpiercing pattern')
                if darkcloudcover(dta):
                    counter += 1
                    if uptrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tdark cloud cover')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tdark cloud cover')
                if bullharami(dta):
                    counter += 1
                    if downtrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tbullish harami')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tbullish harami')
                if bearharami(dta):
                    counter += 1
                    if uptrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tbearish harami')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tbearish harami')
                if bullharamicross(dta):
                    counter += 1
                    if downtrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tbullish harami cross')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tbullish harami cross')
                if bearharamicross(dta):
                    counter += 1
                    if uptrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tbearish harami cross')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tbearish harami cross')
                if invertedhammer(dta,rb):
                    counter += 1
                    if downtrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tinverted hammer')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tinverted hammer')
                if shootingstar(dta,rb):
                    counter += 1
                    if uptrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tshooting star')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tshooting star')
                if matchinglow(dta):
                    counter += 1
                    if downtrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tmatching low')
                        stocks.append(stock) # add this stock to the stocks[] list
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tmatching low')
                if matchinghigh(dta):
                    counter += 1
                    if uptrend(daysoffset):
                        print('*** STRONG Reversal detected in ' + stock + ' *** : \tmatching high')
                    elif showweakpatterns:
                        print('*** Reversal detected in ' + stock + ' *** : \t\tmatching high')
            except Exception as  e:
                print('main loop', str(e),stock)
            time.sleep(0)
    #print('\n\nList of matching lows:')
    #for element in stocks:
    #    print('\t' + element)
    print('\n' + str(counter) + ' reversal patterns detected\n')

