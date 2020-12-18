# Evaluate performance.
import pandas as pd
import matplotlib.pyplot as plt


def read_ledger(ledger_file):
    """
    read a ledger file and return some description of this file including amount of transactions
    amount of buying, amount of selling and profit.
    Args:
        ledger_file: the path of the ledger file

    Returns:
        output: a dataframe of the description we need display
        portfolio: the final portfolio at the last day before selling
    """
    ledger = pd.read_table(ledger_file,
                           sep=' ',
                           header=None,
                           index_col=False,
                           names=[
                               'transaction_type', 'date', 'stock',
                               'number_of_shares', 'price', 'earns'
                           ])

    ledger = ledger.dropna()
    # get the total number of transaction in ledger file
    amount_transaction = ledger.shape[0]
    datetime = pd.date_range('2015-1-1', periods=amount_transaction, freq='D')
    ledger = ledger.set_index(datetime)

    # seperate the transaction into sell and buy and get thier amount.
    sell = ledger[ledger['transaction_type'] == 'sell']
    buy = ledger[ledger['transaction_type'] == 'buy']
    amount_sell = sell.shape[0]
    amount_buy = buy.shape[0]
    total_earn = sell['earns'].sum()
    total_spend = buy['earns'].sum()
    # get the profit
    profit = round(total_earn + total_spend, 2)
    # get the cumulative profit
    ledger['cumulative_profit'] = ledger['earns'].copy()
    # create a list for portfolio
    N = ledger['stock'].drop_duplicates()
    portfolio = pd.DataFrame({'num': 0}, index=N.values)
    for i in range(0, amount_transaction):
        ledger.loc[datetime[i], 'cumulative_profit'] = ledger.loc[datetime[i], 'earns'] + ledger.loc[
            datetime[i-1], 'cumulative_profit']
        if ledger['transaction_type'][i] == 'buy' and ledger['date'][i] < amount_transaction:
            # update the porfolio
            portfolio['num'][ledger['stock']
            [i]] += ledger['number_of_shares'][i]
        elif ledger['transaction_type'][i] == 'sell' and ledger['date'][i] < amount_transaction:
            portfolio['num'][ledger['stock'][i]] = portfolio['num'][
                                                       ledger['stock'][i]] - ledger['number_of_shares'][i]

    # visualize the result
    plt.figure(1)
    ledger['cumulative_profit'].plot()
    plt.title('the cumulative profit')
    plt.hlines(0, datetime[0], datetime[-1], colors='red', linestyles='--')
    plt.show()
    output = pd.DataFrame(
        {
            'amount of transactions': amount_transaction,
            'amount of buying': amount_buy,
            'amount of selling': amount_sell,
            'final profit': profit
        },
        index=['value'])
    return output, portfolio
