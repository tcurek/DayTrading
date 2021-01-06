class Stock:
    def __init__(self, symbol: str, buy_prediction: float,  buy_std_dev: float):
        self.symbol = symbol
        self.buy_prediction = buy_prediction
        self.buy_std_dev = buy_std_dev
        self.shares_owned = 0
        self.orders_made_today = 0
        self.last_recorded_price = 0
        self.highest_price_since_buy = 0

    def set_stock_price(self, current_price: float) -> None:
        self.last_recorded_price = current_price
        self.highest_price_since_buy = current_price if current_price > self.highest_price_since_buy \
            else self.highest_price_since_buy

    def stock_triggers_buy(self, current_price: float) -> bool:
        return current_price < self.buy_prediction - (1.05 * self.buy_std_dev) and self.orders_made_today <= 3

    def stock_triggers_sell(self, current_price: float) -> bool:
        return current_price < (.99 * self.highest_price_since_buy) and self.shares_owned > 0

    def buy_completed(self, quantity: int) -> None:
        self.shares_owned += quantity
        self.orders_made_today += 1

    def sell_completed(self, quantity: int) -> None:
        self.shares_owned -= quantity
