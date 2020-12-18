# Functions to implement our trading strategy.
import numpy as np
import trading.process as proc
import trading.indicators as indicators


def random(stock_prices,
           period=7,
           start_day=-500,
           amount=5000,
           fees=20,
           ledger='ledger_random.txt'):
    '''
    Randomly decide, every period, which stocks to purchase,
    do nothing, or sell (with equal probability).
    Spend a maximum of amount on every purchase.

    Input:
        stock_prices (ndarray): the stock price data
        period (int, default 7): how often we buy/sell (days)
        start_day(int,default 500): the number of days we used
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        ledger (str): path to the ledger file

    Output: None
    '''
    if len(stock_prices.shape) == 1:
        days, N = stock_prices.shape, 1
    else: days, N = stock_prices.shape
    portfolio = proc.create_portfolio([amount] * N,
                                      stock_prices[start_day - 1:, :], fees,
                                      ledger)
    day_index = period
    while day_index <= days:
        for i in range(N):
            decide = np.random.choice(['buy', 'sell', 'do nothing'],
                                      p=[1 / 3, 1 / 3, 1 / 3])
            if decide == 'buy':
                proc.buy(day_index, i, amount, stock_prices, fees, portfolio,
                         ledger)
            elif decide == 'sell' and portfolio != 0:
                proc.sell(day_index, i, stock_prices, fees, portfolio, ledger)
        day_index += period


def crossing_averages(stock_prices,
                      slow_period=200,
                      fast_period=50,
                      period=7,
                      start_day=500,
                      amount=5000,
                      fees=20,
                      ledger='ledger_crossing.txt'):
    '''
    This strategy involves computing 2 different moving averages over time, 
    one 'slow' and one 'fast'. Since the fast moving average(FMA) will change
    more quickly than the slow

    Input:
        stock_prices (ndarray): the stock price data
        slow_period(int,default 200)；the period of slow moving average
        fast_period(int, default 50): the period of fast moving average
        period (int, default 7): how often we buy/sell (days)
        amount (float, default 5000): how much we spend on each purchase
            (must cover fees)
        fees (float, default 20): transaction fees
        start_day(int,default 500): the number of days we used
        ledger (str): path to the ledger file

    Output:
         a file countaining the transaction data

    '''
    used_stock_prices = stock_prices[-start_day:, :]
    if len(stock_prices.shape) == 1:
        days, N = stock_prices.shape, 1
    else: days, N = stock_prices.shape

    # create a new portfolio
    portfolio = proc.create_portfolio([amount] * N, used_stock_prices, fees,
                                      ledger)
    s_time = days - start_day  # calculate the real start time here
    day_index = days - start_day  # create a key to day
    ind = np.zeros((start_day, N))

    # calculate the first sma and fma
    sma = np.mean(stock_prices[day_index - slow_period + 1:day_index + 1, :],
                  axis=0)
    fma = np.mean(stock_prices[day_index - fast_period + 1:day_index + 1, :],
                  axis=0)
    ind[0, :] = fma - sma
    day_index += 1
    while day_index < days:
        for i in range(N):
            # calculate the sma and fma of present stock
            sma = np.mean(stock_prices[day_index - slow_period + 1:day_index +
                                       1, i])
            fma = np.mean(stock_prices[day_index - fast_period + 1:day_index +
                                       1, i])
            ind[day_index - s_time, i] = fma - sma

            # judge whether we should buy or sell
            if ind[day_index - s_time, i] > 0 and ind[day_index - s_time - 1,
                                                      i] < 0:
                proc.buy(day_index - s_time, i, amount, used_stock_prices,
                         fees, portfolio, ledger)
            elif ind[day_index - s_time,
                     i] < 0 and ind[day_index - s_time - 1,
                                    i] > 0 and portfolio != 0:
                proc.sell(day_index - s_time, i, used_stock_prices, fees,
                          portfolio, ledger)
        day_index += 1


def momentum(stock_prices,
             period=7,
             start_day=365 * 2,
             amount=5000,
             fees=20,
             low_threshold=0.2,
             high_threshold=0.7,
             osc_type='stochastic',
             cool_down=3,
             ledger='ledger_momentum.txt'):
    """This function usesa given oscillator (stochastic or RSI) with period n to make buying 
    or selling decisions, depending on a low threshold and a high threshold.

    Args:
        stock_prices (narray): the sharing prices of the stocks
        period (int, optional): Here period is used in calculating the oscillator over the n past days lead
        up to the present. Defaults to 7.
        start_day (int, optional): set the time period we need in data. Defaults to 2 years.
        amount (int, optional): how much we spend on each purchase. Defaults to 5000.
        fees (int, optional): the fees we spent in transaction. Defaults to 20.
        low_threshold(float, optional): the low threshold and if under it, it's better to buy stocks
        high_threshold(float, optional): the high threshold and if higher it, i't better to sell stocks
        osc_type (str, optional): the type of oscillator calculated. Defaults to 'stochastic'.
        cool_down (int,optional): the time people used to cool down
        ledger (str, optional): a file store the transactions log. Defaults to 'ledger_crossing.txt'.
    """
    used_stock_prices = stock_prices[-start_day:, :]
    if len(stock_prices.shape) == 1:
        days, N = stock_prices.shape, 1
    else: days, N = stock_prices.shape

    # create a new portfolio
    portfolio = proc.create_portfolio([amount] * N, used_stock_prices, fees,
                                      ledger)
    s_time = days - start_day  # calculate the real start time here
    day_index = 0  # create a key to day
    indicator = np.zeros((start_day, N))
    for i in range(N):
        osc = indicators.oscillator(stock_prices[:, i],
                                    n=period,
                                    osc_type=osc_type)
        osc_used = osc[-start_day:]
        indicator[:, i] = osc_used
    day_index += cool_down
    while day_index < start_day:
        for i in range(N):
            if all(indicator[day_index - cool_down + 1:day_index + 1,
                             i]) < low_threshold:
                proc.buy(day_index, i, amount, stock_prices, fees, portfolio,
                         ledger)
            elif all(indicator[day_index - cool_down + 1:day_index + 1,
                               i]) > high_threshold and portfolio[i] > 0:
                proc.sell(day_index, i, stock_prices, fees, portfolio, ledger)
        day_index += 1
