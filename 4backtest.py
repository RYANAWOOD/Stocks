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

        filetoanalyze = str('list.txt')
        file = open(filetoanalyze, 'r')
        temp = file.read()
        tickers = temp.splitlines()
        file.close()

        wins = 0
        losses = 0
        winamount = 0
        lossamount = 0
        originalCash = 100
        cash = originalCash
        range1 = 1

        baseTicker = input('base stock: ')
        base = data(baseTicker)
        react = data(input('reacting stock: '))
        maxrange2 = int(input('days: '))

        if len(base.date) < len(react.date):
            start = len(base.date)-1
            range2 = len(base.date)-1
        else:
            start = len(react.date)-1
            range2 = len(react.date)-1

        if range2 > maxrange2:
            range2 = maxrange2

        for i in range(range1,range2):
            dta = start-i
            print(str(dta) + ' ' + react.date[dta] + ' $%.2f '%cash,end='\t')

            if base.open[dta] > base.close[dta+1]:
                # buy the reacting stock
                if react.open[dta-1] > react.open[dta]:
                    wins += 1
                    winamount += (react.open[dta-1]/react.open[dta])*cash - cash
                    print('GAIN\t$%.2f'%react.open[dta]+' $%.02f'%react.open[dta-1]+'  \t $%.2f'%(react.open[dta-1]/react.open[dta]*cash - cash)+', %.2f'%(100*react.open[dta-1]/react.open[dta]-100)+'% ' + react.date[dta] + ' ' + base.date[dta] + '\n')
                    cash += (react.open[dta-1]/react.open[dta])*cash - cash
                    
                elif react.open[dta-1] < react.open[dta]:
                    losses +=1
                    lossamount += (react.open[dta-1]/react.open[dta])*cash - cash
                    print('LOSS\t$%.2f'%(react.open[dta])+' $%.2f'%(react.open[dta-1])+'  \t-$%.2f'%(abs(react.open[dta-1]/react.open[dta]*cash - cash))+', %.2f'%(100*react.open[dta-1]/react.open[dta]-100)+'% ' + react.date[dta] + ' ' + base.date[dta],end='   ')
                    print('deducted $%.2f\n'%(cash - (react.open[dta-1]/react.open[dta])*cash))
                    cash += (react.open[dta-1]/react.open[dta])*cash - cash
                else:
                    print('NO GAIN: $0\n')
            else:
                print('-------NO TRADES-----\n')
except Exception as e:
    print('main loop', str(e))
finally:
    gainPercent = 100*cash/originalCash-100
    holdYearlyGain = (react.open[range1]/react.open[range2])**(1/(abs(range2-range1)/252))*100 - 100
    yearlyGain = (cash/originalCash)**(1/(abs(range2-range1)/252))*100 - 100
    print('number of wins:  \t' + str(wins) + '\tamount gained:\t%.2f'%winamount)
    print('number of losses:\t' + str(losses) + '\tamount lost:\t%.2f'%lossamount)
    print('\nNet Gain: $%.2f'%(winamount + lossamount) + '\t\t ' + str(int(gainPercent)) + '%\t' + str(int(yearlyGain)) + '% per year')
    print('  Versus:\t\t\t ' + str(int(100*react.open[range1]/react.open[range2] - 100)) + '%\t' + str(int(holdYearlyGain)) + '% per year\t$' + str(react.open[range2]) + ' $' + str(react.open[range1]))


