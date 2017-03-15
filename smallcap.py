# same as backtest 4 but it will do it for every stock and see which is the best
import os
import time
import sys
  
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

        filetoanalyze = str('r3000.txt')
        file = open(filetoanalyze, 'r')
        temp = file.read()
        tickers = temp.splitlines()
        file.close()

        startTime = time.time()

        for ticker in tickers:

            stock = data(ticker)
            print(ticker)

            if len(stock.date) == 0:
                print('NO DATA FOR ' + ticker)
                continue

            lastIndex = len(stock.date) - 51

            movingAverages = []

            for i in range(1,lastIndex):

                movingAverage = 0

                for x in range(50):
                    movingAverage += stock.close[i + x]

                movingAverage /= 50
                print('moving average #' + str(i) + ' = \t' + str(int(movingAverage)))
                movingAverages.append(movingAverage)
            print(movingAverages)


                



except Exception as e:
    print('main loop', str(e))
finally:
    print('time elapsed: %.1f'%(time.time() - startTime) + ' seconds')

