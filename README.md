# Stocks
Pulling data from Yahoo! Finance, graphing OHLC data, backtesting algorithms, stock screeners, formatting data

The variations of backtest.py (backtest.py, 2backtest.py, etc.) create a system whereby an algorithm, which is coded into
the backtest, is tested using stock data pulled from Yahoo! Finance over the past up to 30 years.

pulldata.py, pulllargedata.py, and pulllargedata2.py are progressively more capable code that pulls stock data from Yahoo! 
and formats and puts the data into .txt files in a separate directory

updatedata.py updates existing data collected by the pulldata.py variations with new data

quickgraph.py, supergraph.py, ulimategraph.py etc. graph candlestick Open-High-Low-Close data, for both intraday and historical
stock data. Some of graphs are unavailable commercially without paying for premium services.

screener.py, screener2.py, smallcap.py, autoanalyzer.py all parse through a list of stocks (either the
S%P500 or the Russel3000) and look for stocks with certain characteristics, e.g. screener2.py looks for stocks that have lost
an unusual amount of money, and screener.py looks for hammer and hanging man patterns, which are names of common trend reversal
indicators.

movingaverages.py graphs a stocks price history along with two moving averages, which the user sets when the code is run
