# same as backtest 4 but it will do it for every stock and see which is the best
import os
import time
import sys
  
try:
    if __name__ == '__main__':

        class data:
            def __init__(self,stock):
                self.open = []
                self.high = []
                self.low = []
                self.close = []
                self.date = []
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
                file.close()

        filetoanalyze = str('r3000.txt')
        file = open(filetoanalyze, 'r')
        temp = file.read()
        tickers = temp.splitlines()
        file.close()

        baseTicker = input('Base stock ticker: ')
        base = data(baseTicker)

        winners = {}
        bestGain = 0
        bestGainer = 'NONE'
        range1 = 1
        maxrange2 = int(input('Days: '))
        print('%i years'%(maxrange2/252))

        startTime = time.time()

        if len(base.date) < maxrange2:
            print('Cannot test that far back. Base stock (' + baseTicker.upper() + ') has insufficient data')
            sys.exit()

        for ticker in tickers:
            wins = 0
            losses = 0
            winamount = 0
            lossamount = 0
            originalCash = 100
            cash = originalCash

            react = data(ticker)
            if len(react.date) == 0:
                print('NO DATA FOR ' + ticker)
                continue

            if len(base.date) < len(react.date):
                start = len(base.date)-2
                range2 = len(base.date)-1
            else:
                start = len(react.date)-2
                range2 = len(react.date)-1

            if range2 > maxrange2:
                range2 = maxrange2

            for i in range(range1,range2):
                dta = start-i
                #print(str(dta) + ' $%.2f '%cash,end='\t')
                #print(str(i) + ' ' + str(react.date[dta]) + ' ' + str(cash),end=' ')

                if base.open[dta] < 0.999*base.close[dta+1]:
                    # buy the reacting stock
                    if react.open[dta-1] > react.open[dta]:
                        wins += 1
                        winamount += (react.open[dta-1]/react.open[dta])*cash - cash
                        #print('GAIN\t$%.2f'%react.open[dta]+' $%.02f'%react.open[dta-1]+'  \t $%.2f'%(react.open[dta-1]/react.open[dta]*cash - cash)+', %.2f'%(100*react.open[dta-1]/react.open[dta]-100)+'%\n')
                        cash += (react.open[dta-1]/react.open[dta])*cash - cash
                        
                    elif react.open[dta-1] < react.open[dta]:
                        losses +=1
                        lossamount += (react.open[dta-1]/react.open[dta])*cash - cash
                        #print('LOSS\t$%.2f'%(react.open[dta])+' $%.2f'%(react.open[dta-1])+'  \t-$%.2f'%(abs(react.open[dta-1]/react.open[dta]*cash - cash))+', %.2f'%(100*react.open[dta-1]/react.open[dta]-100)+'%',end='   ')
                        #print('deducted $%.2f\n'%(cash - (react.open[dta-1]/react.open[dta])*cash))
                        cash += (react.open[dta-1]/react.open[dta])*cash - cash
                    #else:
                        #print('NONE: $0\n')
                #else:
                #    print('-------NO TRADES-----\n')
            annualGain = ((cash/originalCash)**(1/((range2-range1)/252))*100-100)

            if annualGain > 16:
                winners[ticker] = annualGain

            if annualGain > bestGain and (range2-range1) > (0.95*maxrange2):
                bestGain = (cash/originalCash)**(1/((range2-range1)/252))*100-100
                bestGainer = ticker
                print(ticker + '\t' + react.date[start] + ' ' + react.date[start-range2] + '\t%.2f'%annualGain + '%\tNEW BEST')
            else:
                print(ticker + '\t' + react.date[start] + ' ' + react.date[start-range2] + '\t%.2f'%annualGain  + '%')
except Exception as e:
    print('main loop', str(e))
finally:
    print('best gainer: ' + bestGainer + ' %.f'%bestGain + '% ')# + stock.date[-range1] + stock.date[-range2])
    print('time elapsed: %.1f'%(time.time() - startTime) + ' seconds')
    print('winners: ')
    for stock, value in winners.items():
        print(stock + ':\t%.2f'%value + '%')

