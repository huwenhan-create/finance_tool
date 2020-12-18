# Functions to process transactions.


def log_transaction(transaction_type, date, stock, number_of_shares, price,
                    fees, ledger_file):
    """
    Record a transaction in the file ledger_file. If the file doesn't exist, create it.

    Input:
        transaction_type (str): 'buy' or 'sell'
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we buy or sell (the column index in the data array)
        number_of_shares (int): the number of shares bought or sold
        price (float): the price of a share at the time of the transaction
        fees (float): transaction fees (fixed amount per transaction, independent of the number of shares)
        ledger_file (str): path to the ledger file

    Output: returns None.
        Writes one line in the ledger file to record a transaction with the input information.
        This should also include the total amount of money spent (negative) or earned (positive)
        in the transaction, including fees, at the end of the line.
        All amounts should be reported with 2 decimal digits.

    Example:
        Log a purchase of 10 shares for stock number 2, on day 5. Share price is 100, fees are 50.
        Writes the following line in 'ledger.txt':
        buy,5,2,10,100.00,-1050.00
            >>> log_transaction('buy', 5, 2, 10, 100, 50, 'ledger.txt')
    """
    # judge the if the input is right
    if type(date) != int:
        print('you should input correct type of parameters.')
    else:
        money_earn = 0
        if transaction_type == 'buy':
            money_earn = -number_of_shares * float(price) - fees
        elif transaction_type == 'sell':
            money_earn = number_of_shares * float(price) - fees
        data = [
            transaction_type, date, stock, number_of_shares,
            round(price, 2),
            round(money_earn, 2)
        ]
        # write the data into the file.
        f = open(ledger_file, 'a')
        for d in data:
            f.write(str(d))
            f.write(' ')
        f.write('\n')
        f.close()


def buy(date, stock, available_capital, stock_prices, fees, portfolio,
        ledger_file):
    """
    Buy shares of a given stock, with a certain amount of money available.
    Updates portfolio in-place, logs transaction in ledger.

    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to buy
        available_capital (float): the total (maximum) amount to spend,
            this must also cover fees
        stock_prices (ndarray): the stock price data
        fees (float): total transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file

    Output: None

    Example:
        Spend at most 1000 to buy shares of stock 7 on day 21, with fees 30:
            >>> buy(21, 7, 1000, sim_data, 30, portfolio)
    """
    price_today = stock_prices[date, stock]
    number_of_shares = (available_capital - fees) // price_today
    portfolio[stock] += number_of_shares
    log_transaction('buy', date, stock, number_of_shares, price_today, fees,
                    ledger_file)


def sell(date, stock, stock_prices, fees, portfolio, ledger_file):
    """
    Sell all shares of a given stock.
    Updates portfolio in-place, logs transaction in ledger.

    Input:
        date (int): the date of the transaction (nb of days since day 0)
        stock (int): the stock we want to sell
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)
        portfolio (list): our current portfolio
        ledger_file (str): path to the ledger file

    Output: None

    Example:
        To sell all our shares of stock 1 on day 8, with fees 20:
            >>> sell(8, 1, sim_data, 20, portfolio)
    """
    price_today = stock_prices[date, stock]
    number_of_shares = portfolio[stock]
    portfolio[stock] = 0
    log_transaction('sell', date, stock, number_of_shares, price_today, fees,
                    ledger_file)


def create_portfolio(available_amounts, stock_prices, fees, ledger):
    """
    Create a portfolio by buying a given number of shares of each stock.

    Input:
        available_amounts (list): how much money we allocate to the initial
            purchase for each stock (this should cover fees)
        stock_prices (ndarray): the stock price data
        fees (float): transaction fees (fixed amount per transaction)

    Output:
        portfolio (list): our initial portfolio

    Example:
        Spend 1000 for each stock (including 40 fees for each purchase):
        >>> N = sim_data.shape[1]
        >>> portfolio = create_portfolio([1000] * N, sim_data, 40)
    """
    N = len(available_amounts)
    portfolio = [0] * N
    date = 0
    for i in range(N):
        buy(date, i, available_amounts[i], stock_prices, fees, portfolio, ledger)
    return portfolio
