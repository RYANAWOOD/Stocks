import os
  
try:
    if __name__ == '__main__':

        class data:
            def __init__(self,stock):
                self.open = []
                self.high = []
                self.low = []
                self.close = []
                self.date = []
                stockfile = stock.upper()+'.txt'
                file = open(stockfile)
                stemp = file.read()
                stemp = stemp.splitlines()
                for line in stemp:
                    data = line.split(',')
                    self.open.append(float(data[4]))
                    self.high.append(float(data[2]))
                    self.low.append(float(data[3]))
                    self.close.append(float(data[1]))
                    self.date.append(int(data[0]))
                file.close()

        # read the list of tickers into the list "tickers[]"
        filetoanalyze = str('list.txt')
        file = open(filetoanalyze, 'r')
        temp = file.read()
        tickers = temp.splitlines()
        file.close()

        printed = 0
        for index,ticker in enumerate(tickers):
            if printed == 3 and index / len(tickers) > 0.99:
                print('100% complete')
                printed = 4
            if printed == 2 and index / len(tickers) > 0.75:
                print('75% complete')
                printed = 3
            elif printed == 1 and index / len(tickers) > 0.5:
                print('50% complete')
                printed = 2
            elif printed == 0 and index / len(tickers) > 0.25:
                print('25% complete')
                printed = 1
 


            stock = data(ticker)
            try:
                os.remove('candledata/' + ticker + '.txt')
            except:
                pass

            file = open('candledata/' + ticker + '.txt','a')

            for i in range(len(stock.open) - 1):
                dta = -i-1
                if stock.open[dta] > stock.close[dta]:
                    lrb = stock.close[dta]
                    urb = stock.open[dta]
                else:
                    lrb = stock.open[dta]
                    urb = stock.close[dta]
                rb = abs(stock.close[dta] - stock.open[dta])

                if rb < (1/2)*(lrb - stock.low[dta]) and (stock.high[dta] - urb) < rb: # check that shape is correct
                    if stock.close[dta-1] < stock.open[dta-1] and stock.close[dta-1] > urb: # check that previous day was bearish
                        file.write('hammer: ' + str(stock.date[dta]) + '\n')

except Exception as e:
    print('main loop', str(e))


