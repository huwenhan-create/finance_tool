import numpy as np


def moving_average(stock_price, n=7, weights=[],start_date = 2*365):
    """
    Calculates the n-day (possibly weighted) moving average for a given stock over time.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        weights (list, default []): must be of length n if specified. Indicates the weights
            to use for the weighted average. If empty, return a non-weighted average.

    Output:
        ma (ndarray): the n-day (possibly weighted) moving average of the share price over time.
    """

    # section1: justify the validation of the input
    if len(weights) != n and weights != []:
        return 'the length of weights must be equal to n'

    # section2: calculate the moving average
    num_of_day = stock_price.shape[0]
    ma = []  # this variable means moving average
    weights = np.array(weights)
    if len(weights) == 0:
        for i in range(num_of_day - n + 1 - start_date, num_of_day - n + 1):
            ma.append(np.mean(stock_price[i:i + n]))
    else:
        for i in range(num_of_day - n + 1 - start_date, num_of_day - n + 1):
            ma.append(np.dot(weights, stock_price[i:i + n]))
    return np.array(ma)


def oscillator(stock_price, n=7, osc_type='stochastic'):
    """
    Calculates the level of the stochastic or RSI oscillator with a period of n days.

    Input:
        stock_price (ndarray): single column with the share prices over time for one stock,
            up to the current day.
        n (int, default 7): period of the moving average (in days).
        osc_type (str, default 'stochastic'): either 'stochastic' or 'RSI' to choose an oscillator.

    Output:
        osc (ndarray): the oscillator level with period $n$ for the stock over time.
    """
    days = stock_price.shape[0]
    osc = []
    # write the function when osc type is 'stochastic'
    if osc_type == 'stochastic':
        for i in range(1 + n, days):
            # calculate the minimum and maximum in the past n days.
            min_value = np.min(stock_price[i - n + 1:i + 1])
            max_value = np.max(stock_price[i - n + 1:i + 1])
            # calculate the osc
            osc.append((stock_price[i] - min_value) / (max_value - min_value))
        return np.array(osc)

    # write the function when osc type is 'stochastic'
    if osc_type == 'RSI':
        for i in range(1 + n, days):
            group = stock_price[i - n + 1:i + 1]
            # calculate the diff of the stock price
            diff_group = np.diff(group)
            # extract positive and negative group respectively
            positive_group = diff_group[np.where(diff_group >= 0)]
            negative_group = diff_group[np.where(diff_group < 0)]
            # calculate the RSI
            if negative_group.size == 0:
                RSI = 1
            elif positive_group.size == 0:
                RSI = 0
            else:
                positive_avg = np.mean(positive_group)
                negative_avg = np.mean(negative_group)
                RS = positive_avg / np.abs(negative_avg)
                RSI = 1 - (1 / (1 + RS))
            osc.append(RSI)
        return np.array(osc)
    