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
                #self.rsi = rsiFunc(self.close)
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
        originalCash = 1000
        cash = originalCash
        stoploss = 0.9925
        range1 = 2
        range2 = 750

        base = data('vfinx')
        react = data(input('reacting stock: '))
        for i in range(range1,range2):
            print(str(i),end='\t')
            dta = -i-1 # Day To Analyze

            if base.open[dta] > base.close[dta-1]:
                # buy the reacting stock
                if react.open[dta+1] > react.open[dta]:
                    wins += 1
                    winamount += int((react.open[dta+1]/react.open[dta])*cash - cash)
                    cash += int((react.open[dta+1]/react.open[dta])*cash - cash)
                    print('GAIN\t$'+str(react.open[dta])+' $'+str(react.open[dta+1])+'  \t $'+str(int(react.open[dta+1]/react.open[dta]*cash - cash))+', '+str('%.2f'%(100*react.open[dta+1]/react.open[dta]-100))+'%\n')
                    
                elif react.open[dta+1] < react.open[dta]:
                    losses +=1
                    lossamount += int((react.open[dta+1]/react.open[dta])*cash - cash)
                    cash += int((react.open[dta+1]/react.open[dta])*cash - cash)
                    print('LOSS\t$'+str(react.open[dta])+' $'+str(react.open[dta+1])+'  \t-$'+str(abs(int(react.open[dta+1]/react.open[dta]*cash - cash)))+', '+str('%.2f'%(100*react.open[dta+1]/react.open[dta]-100))+'%\n')
                else:
                    print('NONE: $0\n')
            else:
                print('-------NO TRADES-----\n')
except Exception as e:
    print('main loop', str(e))
finally:
    print('number of wins:  \t' + str(wins) + '\tamount gained:\t' + str(winamount))
    print('number of losses:\t' + str(losses) + '\tamount lost:\t' + str(lossamount))
    print('\nNet Gain:', str(int(winamount + lossamount)) + '\t\t' + str(int(100*cash/originalCash-100)) + '%')
    print('  Versus:\t\t' + str(int(100*react.open[-range1]/react.open[-range2] - 100)) + '%\t$' + str(react.open[-range2]) + ' $' + str(react.open[-range1]))


