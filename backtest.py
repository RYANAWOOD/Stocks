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
            remove(stock+'.txt')
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
    if (upperrealbody(dta) + lowerrealbody(dta)) < (upperrealbody(dta+1) + lowerrealbody(dta+1)) and (upperrealbody(dta+1) + lowerrealbody(dta+1)) < (upperrealbody(dta+2) + lowerrealbody(dta+2)) and (upperrealbody(dta+2) + lowerrealbody(dta+2)) < (upperrealbody(dta+3) + lowerrealbody(dta+3)):
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
    if bullharami(dta) and abs(openp[-dta] - closep[-dta]) < openp[-dta]*0.001:
        return True
    return False

def bearharamicross(dta):
    if bearharami(dta) and abs(openp[-dta] - closep[-dta]) < openp[-dta]*0.001:
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
            if (upperrealbody(dta)-lowerrealbody(dta))/(highp[-dta]-lowp[-dta]) > 0.5 and (upperrealbody(dta+1)-lowerrealbody(dta+1))/(highp[-dta-1]-lowp[-dta-1]) > 0.5: #long day
                return True
    return False

def matchinghigh(dta):
    if (abs(closep[-dta] - closep[-dta-1]) / closep[-dta-1]) <= 0.001:
        if (closep[-dta] - openp[-dta] > 0 and closep[-dta-1] - openp[-dta-1] > 0):
            if (upperrealbody(dta)-lowerrealbody(dta))/(highp[-dta]-lowp[-dta]) > 0.5 and (upperrealbody(dta+1)-lowerrealbody(dta+1))/(highp[-dta-1]-lowp[-dta-1]) > 0.5: #long day
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

def rsiFunc(prices, n=14):
    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)
    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi
  
try:
    if __name__ == '__main__':

        filetoanalyze = str('list.txt')
        file = open(filetoanalyze, 'r')
        temp = file.read()
        stemp = temp.splitlines()
        file.close()

        wins = 0
        losses = 0
        winamount = 0
        lossamount = 0
        cash = 2500
        stoploss = 0.9925

        stocks = {} # to store dictionary of stocks that are reversals
        showweakpatterns = False

        for i in range(500):
            print('\t' + str(i) + ' days ago:')
            dta = i # Day To Analyze
            daysoffset = dta  # days to go back: to be used for determining uptrends and downtrends
            for stock in stemp:
                if len(stock) > 0:
                    stock = stock.upper()
                    #pull_historical(stock)
                    stockInfo = stock+'.txt'
                    try:
                        date, closep, highp, lowp, openp, volume = np.loadtxt(stockInfo,delimiter=',', unpack=True, converters={ 0: bytespdate2num('%Y%m%d')})    
                        rb = abs(openp[-dta] - closep[-dta]) # Real Body

                        if hammer(dta,rb) and downtrend(daysoffset):
                            counter += 1
                            print('Strong Reversal detected in ' + stock + '  \t' + str(dta) + ' days ago')
                            stocks[stock] = dta # add this stock to the stocks[] list
                            if closep[-dta+1] >= openp[-dta+1]:
                                if lowp[-dta+1] > (stoploss*openp[-dta+1]):
                                    wins += 1
                                    winamount += (closep[-dta+1] - openp[-dta+1])*int(cash/openp[-dta+1])
                                    print('made $' + str((closep[-dta+1] - openp[-dta+1])*int(cash/openp[-dta+1])) + ' open: ' + str(openp[-dta+1]) + '\tclose: ' + str(closep[-dta+1]),end='\t')
                                    print('net gain: ' + str(winamount + lossamount))
                                    #print(rsiFunc(closep)[-1])
                                else:
                                    losses += 1
                                    lossamount -= ((1-stoploss)*openp[-dta+1])*int(cash/openp[-dta+1])
                                    print('lost $' + str(((1-stoploss)*openp[-dta+1])*int(cash/closep[-dta])))
                                    print('net gain: ' + str(winamount + lossamount))
                                break
                            if closep[-dta+1] < openp[-dta+1]:
                                losses += 1
                                if lowp[-dta+1] > (stoploss*openp[-dta+1]):
                                    lossamount += (closep[-dta+1] - openp[-dta+1])*int(cash/openp[-dta+1])
                                    print('lost $' + str((closep[-dta+1] - openp[-dta+1])*int(cash/openp[-dta+1])) + ' open: ' + str(openp[-dta+1]) + '\tclose: ' + str(closep[-dta+1]),end='\t')
                                    print('net gain: ' + str(winamount + lossamount))
                                    #print(rsiFunc(closep)[-1])
                                else:
                                    lossamount -= ((1-stoploss)*openp[-dta+1])*int(cash/openp[-dta+1])
                                    print('lost $' + str(((1-stoploss)*openp[-dta+1])*int(cash/openp[-dta+1])))
                                    print('net gain: ' + str(winamount + lossamount))
                                break

                    except Exception as  e:
                        print('main loop', str(e),stock)
except:
    pass

finally:
    print('\n\nList of reversals:')
    for stock, day in sorted(stocks.items()):
        print('\t' + stock + '\t' + str(day) + ' days ago')
    print('\tTotal:\t' + str(counter))
    print('number of wins:  \t' + str(wins) + '\tamount gained:\t' + str(winamount))
    print('number of losses:\t' + str(losses) + '\tamount lost:\t' + str(lossamount))
    print('\nNet Gain: ', str(lossamount + winamount))

