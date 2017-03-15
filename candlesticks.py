import csv
import urllib.request
import time

def lookup(symbol):
    """Look up quote for symbol."""

    # reject symbol if it starts with caret
    if symbol.startswith("^"):
        return None

    # reject symbol if it contains comma
    if "," in symbol:
        return None

    # query Yahoo for quote
    # http://stackoverflow.com/a/21351911
    try:
        url = "http://download.finance.yahoo.com/d/quotes.csv?f=snl1&s={}".format(symbol)
        webpage = urllib.request.urlopen(url)
        datareader = csv.reader(webpage.read().decode("utf-8").splitlines())
        row = next(datareader)
    except:
        return "lookup failed"

    # ensure stock exists
    try:
        price = float(row[2])
    except:
        return "failed"

    # return stock's name (as a str), price (as a float), and (uppercased) symbol (as a str)
    return price

def main():
    # get stock to track from the user
    stock = input("Stock to track: ")

    # create a list of tuples for prices at given times
    history = []

    # create a list of tuples to store candlesticks
    candlesticks = []

    # create counter to keep track of seconds elapsed for the while loop
    counter = 0

    # while loop collects data for a set amount of cycles
    while(counter != 8):
        # collect 4 cycles of stock price
        for i in range(4):
            price = lookup(stock)
            datetime = time.strftime("%m/%d/%Y %H:%M:%S")
            history.append([datetime,price])
            print("At time " + str(counter),end=": $")
            print(price)
            time.sleep(1)
            counter += 1

        # print out the list for price history, not necessary, purely for keeping track of the code while developing it
        for record in history:
            print(record[0],end=": $")
            print(record[1])

        # make the candlestick for these 4 cycles
        for i in range(0,3):
            #figure out the open high low close
            Open = history[counter - 4][1]
            close = history[counter - 1][1]
            low = history[counter - 1][1]
            for j in range(2,4):
                if history[counter - j][1] < low:
                    low =  history[counter - j][1]
            high = history[counter - 1][1]
            for k in range(2,4):
                if history[counter - k][1] > high:
                    high = history[counter - k][1]
            candlesticks.append([datetime,Open,high,low,close])
    # print out the candlesticks to show that the list of candlestick data is working
    for candlestick in candlesticks:
        print(str(candlestick[0]),end=": open: $")
        print(str(candlestick[1]),end=" high: $")
        print(str(candlestick[2]),end=" low: $")
        print(str(candlestick[3]),end=" close: $")
        print(str(candlestick[4]))
if __name__ == "__main__":
    main()

