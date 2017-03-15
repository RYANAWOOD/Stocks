import os
import time
import datetime

# screens for hammers and hanging man (4 dimensional vector, 1 day)

def bigChange(stock, daysBack, margin):

    filep = open('largedata/' + stock + '.txt', 'r+')
    fileContents = filep.read()
    data = fileContents.splitlines()

    if len(data) < 3:
        return False

    for index,line in enumerate(data):
        if len(line) != 0 and 'values:' not in line:
            lastIndex = index - daysBack

    averageChange = 0
    for i in range(50):
        averageChange += abs(float(data[lastIndex - i].split(',')[4]) - float(data[lastIndex - i].split(',')[1]))
    averageChange = abs(averageChange) / 50

    if float(data[lastIndex].split(',')[4]) - float(data[lastIndex].split(',')[1]) < -1*averageChange*margin:
        return True
    else:
        return False

if __name__ == '__main__':

    filetoanalyze = str('r3000.txt')            
    file = open(filetoanalyze, 'r')
    temp = file.read()
    stemp = temp.splitlines()
    file.close()

    changers = []
    daysBack = int(input('days back to analyze: '))
    margin = 4
    
    for index,stock in enumerate(stemp):
        if index%500 == 0:
            print(index)

        if bigChange(stock,daysBack,margin):
            print('\t' + stock)
            changers.append(stock)

    print('\nBig Changers:')
    for changer in sorted(changers):
        print(changer)


