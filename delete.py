import os
if __name__ == '__main__':
   
    file = open('list.txt', 'r')
    temp = file.read()
    stemp = temp.splitlines()
    file.close()
    
    for stock in stemp:
        stock = stock.upper()
        try:
            os.remove(stock.upper()+'.txt')
            print('removed ' + stock + '.txt')
        except:
            print('could not remove ' + stock + '.txt')
