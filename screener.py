import os
import time
import datetime

# screens for hammers and hanging man (4 dimensional vector, 1 day)

def retrieveData(stock, daysBack):
    try:
        filep = open('largedata/' + stock + '.txt', 'r+')
        fileContents = filep.read()
        data = fileContents.splitlines()

        if len(data) < 3:
            return 'failed'

        for index,line in enumerate(data):
            if len(line) != 0 and 'values:' not in line:
                lastLine = data[index - daysBack]
        splittedLine = lastLine.split(',')
        floatSplittedLine = [float(i) for i in splittedLine]
        filep.close()
#        print('\t' + str(stock).upper())
        if len(splittedLine) == 6 and 'labels' not in splittedLine[0][0]:
            return floatSplittedLine

    except Exception as e:
        if str(e) == 'HTTP Error 404: Not Found':
#            print('\t' + str(stock).upper() + ' Data unavailable')
            failed.append(stock)
        else:
#            print(str(e))
             pass

def hangingman(vector,margin):

    pattern1 = [-0.4082,0.8165,-0.4082,0]
    pattern2 = [0,0.8165,-0.4082,-0.4082]

    distance1 = ( (vector[0]-pattern1[0])**2 + (vector[1]-pattern1[1])**2 + (vector[2]-pattern1[2])**2 + (vector[3]-pattern1[3])**2 ) ** (1/2)
    distance2 = ( (vector[0]-pattern2[0])**2 + (vector[1]-pattern2[1])**2 + (vector[2]-pattern2[2])**2 + (vector[3]-pattern2[3])**2 ) ** (1/2)

    if distance1 < margin or distance2 < margin:
        return True
    else:
        return False

def hammer(vector,margin):

    pattern1 = [0.4082,0.4082,-0.8165,0]
    pattern2 = [0,0.4082,-0.8165,0.4082]

    distance1 = ( (vector[0]-pattern1[0])**2 + (vector[1]-pattern1[1])**2 + (vector[2]-pattern1[2])**2 + (vector[3]-pattern1[3])**2 ) ** (1/2)
    distance2 = ( (vector[0]-pattern2[0])**2 + (vector[1]-pattern2[1])**2 + (vector[2]-pattern2[2])**2 + (vector[3]-pattern2[3])**2 ) ** (1/2)

    if distance1 < margin or distance2 < margin:
        return True
    else:
        return False


def vectorize(data):
    average = (data[1] + data[2] + data[3] + data[4]) / 4
    vector = [(data[1] - average), (data[2] - average), (data[3] - average), (data[4] - average)]
    length = (vector[0]**2 + vector[1]**2 + vector[2]**2 + vector[3]**2)**(1/2)
    normalizedVector = [(vector[0]/length),(vector[1]/length),(vector[2]/length),(vector[3]/length)]
    return vector

if __name__ == '__main__':

    filetoanalyze = str('r3000.txt')            
    file = open(filetoanalyze, 'r')
    temp = file.read()
    stemp = temp.splitlines()
    file.close()

    hammers = []
    hangingmans = []

    margin = 0.15
    daysBack = int(input('days back to analyze: '))
    
    for index,stock in enumerate(stemp):
        try:
#            print(str(index) + ' of ' + str(len(stemp)),end=' ')
            data = retrieveData(stock,daysBack)

            if data == 'failed':
                continue

            vector = vectorize(data)

            if hammer(vector,margin):
#                print('hammer')
                hammers.append(stock)
            if hangingman(vector,margin):
#                print('hangingman')
                hangingmans.append(stock)

        except Exception as  e:
#            print('could not pull ' + stock,str(e))
            pass

    print('\nHammers:')
    for hammer in sorted(hammers):
        print(hammer)
    print('\nHanging Mans:')
    for hangingman in sorted(hangingmans):
        print(hangingman)


            