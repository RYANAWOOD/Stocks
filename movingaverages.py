# same as backtest 4 but it will do it for every stock and see which is the best
import os
import time
import sys
import matplotlib.pyplot as plt
  
try:
    if __name__ == '__main__':

        class data:
            # uses pulllargedata.py formatted data to make lists of data for open high low close date volume
            def __init__(self,stock):
                self.open = []
                self.high = []
                self.low = []
                self.close = []
                self.date = []
                self.volume = []
                stockfile = 'largedata/' + stock + '.txt'
                file = open(stockfile)
                stemp = file.read()
                stemp = stemp.splitlines()
                for line in stemp:
                    if line[0] != 'D':
                        data = line.split(',')
                        self.open.append(float(data[1]))
                        self.high.append(float(data[2]))
                        self.low.append(float(data[3]))
                        self.close.append(float(data[4]))
                        self.date.append(str(data[0]))
                        self.volume.append(int(data[5]))
                file.close()

        ticker = input('stock: ')
        length = int(input('days: '))
        length2 = int(input('days(2): '))

        startTime = time.time()

        stock = data(ticker)

        if len(stock.date) == 0:
            print('NO DATA FOR ' + ticker)
            exit

        lastIndex = len(stock.date) - length - 1

        movingAverages = []
        movingAverages2 = []

        for i in range(0,len(stock.date)):

            movingAverage = 0
            movingAverage2 = 0

            for x in range(length):
                movingAverage += stock.close[i - x]
            for x in range(length2):
                movingAverage2 += stock.close[i - x]

            movingAverage /= length
            movingAverage2 /= length2

            print(str(i) + '\t' + stock.date[i] + '\t\t$%.2f\t'%movingAverage + '\t$%.2f'%stock.close[i])
            movingAverages.append(movingAverage)
            movingAverages2.append(movingAverage2)
    
        plotPrices = []
        for i in range(lastIndex):
            plotPrices.append(stock.close[lastIndex - i])

        plt.plot(movingAverages)
        plt.plot(movingAverages2)
        plt.plot(stock.close)
        plt.ylabel('Price ($)')
        plt.xlabel('Date')
        plt.show()


except Exception as e:
    print('main loop', str(e))
finally:
    print('time elapsed: %.1f'%(time.time() - startTime) + ' seconds')

