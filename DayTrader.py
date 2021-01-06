import robin_stocks as r
import schedule
from stock import Stock
from ImportFile import get_todays_projections


def update_all_stock_prices(all_stocks: [Stock]) -> None:
    symbols = [stock.symbol for stock in all_stocks]
    latest_prices = r.stocks.get_latest_price(inputSymbols=symbols)
    for i, stock in enumerate(all_stocks):
        stock.set_stock_price(current_price=float(latest_prices[i]))


def stocks_that_trigger_buy(all_stocks: [Stock]) -> [str]:
    return [stock.symbol for stock in all_stocks if stock.stock_triggers_buy()]


def even_distribution_of_stocks_to_buy(all_stocks: [Stock], buy_padding=100.0) -> dict:
    stocks = {}
    buying_power = float(r.profiles.load_account_profile(info='buying_power'))
    spending_money = buying_power - buy_padding
    min_stock_price = min([stock.last_recorded_price for stock in all_stocks])
    stocks_to_buy = stocks_that_trigger_buy(all_stocks)
    while spending_money >= min_stock_price:
        for stock in all_stocks:
            if stock.last_recorded_price > spending_money or stock not in stocks_to_buy:
                continue
            stocks[stock.symbol] += 1
            spending_money -= stock.last_recorded_price
    return stocks


def morning_buys(all_stocks: [Stock]) -> list:
    stocks_to_buy = even_distribution_of_stocks_to_buy(all_stocks)
    orders = []
    for stock in all_stocks:
        if stock.symbol in stocks_to_buy:
            o = r.orders.order_buy_market(symbol=stock.symbol, quantity=stocks_to_buy[stock.symbol])
            stock.buy_completed(stocks_to_buy[stock.symbol])
            orders.append(o)
    return orders


def sells(all_stocks: [Stock]) -> [dict]:
    orders = []
    for stock in all_stocks:
        if stock.stock_triggers_sell():
            o = r.orders.order_sell_market(symbol=stock.symbol, quantity=stock.shares_owned)
            stock.sell_completed(quantity=stock.shares_owned)
            orders.append(o)
    return orders


def run():
    orders = []

    # import todays projections
    all_stocks = get_todays_projections()
    all_stocks.sort(key=lambda x: x.symbol)

    # TODO: Wait until 9am
    update_all_stock_prices(all_stocks)
    orders.append(morning_buys(all_stocks))

    # TODO: Wait until 10am, then loop every 15 mins
    update_all_stock_prices(all_stocks)
    orders.append(sells(all_stocks))









