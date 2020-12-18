#%%
# Write your revised and debugged version of the code here.
import matplotlib.pyplot as plt
import numpy as np
import trading.data as data
import trading.process as process
import trading.indicators as indicators
import trading.strategy as strategy
import trading.performance as tp
import os

# first use the get_data function to read txt file
sim_data = data.get_data('read',r'stock_data_5y.txt')

# extract the initial price for each stock
init_price = sim_data[1,:]

# From the question, here, we extract the stock whose initial prices are near to 100, 120
index = [np.argmin(np.abs(init_price-100)),np.argmin(np.abs(init_price-120)),
np.argmin(np.abs(init_price-400)),np.argmin(np.abs(init_price-250)),np.argmin(np.abs(init_price-300))]
stock_price = sim_data[1:,index]

N = stock_price.shape[1]  # here the N is the number of our available stocks
portfolio = process.create_portfolio([5000]*N,stock_price,20, ledger = 'ledger.txt')

stock_prices = data.get_data('read', r'stock_data_5y.txt')
stock = stock_prices[:, 2]
# [section 3] test for moving average
MA_1 = indicators.moving_average(stock, n=100)
MA_2 = indicators.moving_average(stock, n=30)
MA_3 = indicators.moving_average(stock, n=3, weights=[0.4, 0.5, 0.1])
# draw the diadram of 3 tests
plt.figure(1)
ax = plt.gca()
ax.plot(stock[-2*365:],label = r'stock price')
ax.plot(MA_1, label = r'period = 200')
ax.plot(MA_2, label = r'period = 30')
ax.plot(MA_3, label = r'weighted')
ax.legend()
plt.show()

#%%
OSC_1 = indicators.oscillator(stock,n=7)
OSC_2 = indicators.oscillator(stock,n=7,osc_type='RSI')
OSC_3 = indicators.oscillator(stock,n=30)
plt.figure(2)
ax = plt.gca()
ax.set_ylim(0,1.25)
ax.plot(OSC_1, label = r'period = 7')
ax.plot(OSC_2, label = r'osc_type is"RSI"')
ax.plot(OSC_3, label = r'period = 30')
ax.legend()
plt.show()

#%%
if os.path.exists('ledger_random.txt'):
    os.remove('ledger_random.txt')
if os.path.exists('ledger_crossing.txt'):
    os.remove('ledger_crossing.txt')
if os.path.exists('ledger_momentum.txt'):
    os.remove('ledger_momentum.txt')
if os.path.exists('ledger_momentum_RSI.txt'):
    os.remove('ledger_momentum_RSI.txt')
stock = stock.reshape(stock.shape[0],1)
strategy.random(stock)
strategy.crossing_averages(stock)
strategy.momentum(stock)
strategy.momentum(stock,osc_type='RSI',ledger='ledger_momentum_RSI.txt')
result_random,portfolio_random = tp.read_ledger('ledger_random.txt')
result_crossing,portfolio_crossing = tp.read_ledger('ledger_crossing.txt')
result_momentum,portfolio_momentum = tp.read_ledger('ledger_momentum.txt')
result_momentum_RSI,portfolio_momentum_RSI = tp.read_ledger('ledger_momentum_RSI.txt')