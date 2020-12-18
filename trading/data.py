import numpy as np


def generate_stock_price(days, initial_price, volatility):
    """
    Generates daily closing share prices for a company,
    for a given number of days.
    """
    # Set stock_prices to be a zero array with length days
    stock_prices = np.zeros(days)
    # Set stock_prices in row 0 to be initial_price
    stock_prices[0] = initial_price
    # Set total_drift to be a zero array with length days
    totalDrift = np.zeros(days)
    # Set up the default_rng from Numpy
    rng = np.random.default_rng()
    # Loop over a range(1, days)
    for day in range(1, days):
        # Get the random normal increment
        inc = rng.normal()
        # Add stock_prices[day-1] to inc to get NewPriceToday
        NewPriceToday = stock_prices[day - 1] + inc

        # Make a function for the news
        def news(chance, volatility):
            """
            Simulate the news with %chance
            """
            # Choose whether there's news today
            news_today = rng.choice([0, 1], p=chance)
            if news_today:
                # Calculate m and drift
                m = rng.normal(0, 0.3)
                drift = m * volatility
                # Randomly choose the duration
                duration = rng.integers(7, 7 * 12)
                final = np.zeros(duration)
                for i in range(duration):
                    final[i] = drift
                return final
            else:
                return np.zeros(0)

        # Get the drift from the news
        d = news(1, volatility)
        # Get the duration
        duration = len(d)
        # Add the drift to the next days
        totalDrift[day:day + duration] = d
        # Add today's drift to today's price
        NewPriceToday += totalDrift[day]
        # Set stock_prices[day] to NewPriceToday or to NaN if it's negative
        if NewPriceToday <= 0:
            stock_prices[day] = np.nan
        else:
            stock_prices[day] = NewPriceToday
    return stock_prices


def Drift(vol, chance=0.01):
    """ Here, we create a function to indicate the drift caused by the occurrences
    of important news, and there are two parameters:

    Args:
        vol (float): [volatility of the stock price]
        chance (float, optional): [there is a default 0,01 chance of such an event happening]. Defaults to 0.01.

    Returns:
        [narray]: [the drift caused by the important news]
    """

    # create a random generater
    rng = np.random.default_rng()
    news = rng.choice([0, 1], p=[1 - chance, chance])
    if news == 1:
        # Calculate the coefficient m
        m = rng.normal(0, 2)
        impact = m * vol
        # Randomly choose the duration
        duration = rng.integers(3, 14)
        drift = np.array([impact] * duration)
        return drift
    else:
        return np.zeros(0)


def price_generator(n_days, init_price, vol):
    """
    Here, we write a new function to generate simulated stock price data, which
    contains three parameters:
    ---------------------------------------------------------------------------
    n_days: number of the days. (also the number of the price data)
    init_price: initial price at the start.
    vol: volatility of the stock price.
    """
    # Set stock_prices to be a zero array with length days
    stock_prices = np.zeros(n_days)
    # Set stock_prices in row 0 to be initial_price
    stock_prices[0] = init_price

    # Set total_drift to be a zero array with length days
    news_impact = np.zeros(n_days)
    rng = np.random.default_rng()
    
    # Loop over a range(1, days)
    for day in range(1, n_days):
        # Get the random normal increment
        inc = rng.normal(0, vol)
        # Add stock_prices[day-1] to inc to get NewPriceToday
        price_today = stock_prices[day - 1] + inc
        # Get the drift from the news
        drift = Drift(vol)
        # Get the duration
        duration = len(drift)
        # Add the drift to the next days
        if day + duration <= n_days - 1:
            news_impact[day:day +
                        duration] = news_impact[day:day + duration] + drift
        else:
            news_impact[day:] = news_impact[day:] + drift[0]
        # Add today's drift to today's price
        price_today += news_impact[day]
        # Set stock_prices[day] to NewPriceToday or to NaN if it's negative
        if price_today <= 0:
            stock_prices[day] = np.nan
        else:
            stock_prices[day] = price_today
    return stock_prices


def get_data(method, *filename, **keywords):
    """[get_data]

    Args:
        method (): this method is whether 'generate' or 'read'. If method is 'generate', we simulate a
        new data. If method is 'read', then we read an exist .txt file containing the stock price data

        *filename: When method == 'read', this parameter offer the path of the readed file

        **keywords: the parameters needed for price_generator function

    Returns:
        [ndarray]: The simulative stock prices.
    """
    if method == 'generate':
        sim_data = price_generator(n_days=keywords['n_days'],
                                   init_price=keywords['init_price'],
                                   vol=keywords['vol'])
        return sim_data
    elif method == 'read':
        sim = np.loadtxt(filename[0])
        return sim
