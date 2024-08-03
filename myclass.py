
"""
Created on Sun Jul 21 23:47:22 2024
@author: Pacifica
"""

import MetaTrader5 as mt5
import pandas as pd


class Bot:
    def __init__(self, n, symbol, volume, profit_target, proportion):
        self.n = n
        self.symbol = symbol
        self.volume = volume
        self.profit_target = profit_target
        self.proportion = proportion

    def buy_limit(self, symbol, volume, price):
        request = mt5.order_send(
            {
                'action': mt5.TRADE_ACTION_PENDING,
                'symbol': symbol,
                'volume': volume,
                'type': mt5.ORDER_TYPE_BUY_LIMIT,
                'price': price,
                'deviation': 20,
                'magic': 100,
                'comment': 'Python market order',
                'type_time': mt5.ORDER_TIME_GTC,
                'type_filling': mt5.ORDER_FILLING_IOC,
            }
        )
        print(request)

    def sell_limit(self, symbol, volume, price):
        request = mt5.order_send(
            {
                'action': mt5.TRADE_ACTION_PENDING,
                'symbol': symbol,
                'volume': volume,
                'type': mt5.ORDER_TYPE_SELL_LIMIT,
                'price': price,
                'deviation': 20,
                'magic': 100,
                'comment': 'Python market order',
                'type_time': mt5.ORDER_TIME_GTC,
                'type_filling': mt5.ORDER_FILLING_IOC,
            }
        )
        print(request)

    def cal_profit(self, symbol):
        usd_position = mt5.positions_get(symbol=symbol)
        if not usd_position:  # ตรวจสอบว่ามี position หรือไม่
            return 0.0     # ถ้าไม่มี position ให้ return 0
        df = pd.DataFrame(list(usd_position), columns=usd_position[0]._asdict().keys())
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.drop(['time_update', 'time_msc', 'time_update_msc', 'external_id'], axis=1, inplace=True)
        profit = float(df['profit'].sum())
        print(profit)
        return profit
    
    # ... (rest of the class methods are the same as your original code)

    def run(self):
        while True:
            pct_change = 1
            tick = mt5.symbol_info_tick(self.symbol)
            current_price_sell = tick.bid
            adj_sell = 1.2

            for i in range(self.n):
                price = (
                        ((pct_change / (100 * 100)) * current_price_sell) * adj_sell * self.proportion
                        + current_price_sell
                )
                self.sell_limit(self.symbol, self.volume, price)
                pct_change += 1
                adj_sell += 0.2

            pct_change_2 = -1
            tick = mt5.symbol_info_tick(self.symbol)
            current_price_buy = tick.ask
            adj_buy = 1.2

            for i in range(self.n):
                price = (
                        ((pct_change_2 / (100 * 100)) * current_price_buy) * adj_buy * self.proportion
                        + current_price_buy
                )
                self.buy_limit(self.symbol, self.volume, price)
                pct_change_2 -= 1
                adj_buy += 0.2

            while True:
                position = mt5.positions_get(symbol=self.symbol)
                if position:  # Check if position exists
                    margin_s = self.cal_sell_margin(self.symbol)
                    margin_b = self.cal_buy_margin(self.symbol)

                    if margin_s > 0:
                        try:
                            pct_sell_profit = self.cal_pct_sell_profit(self.symbol)
                            if pct_sell_profit >= self.profit_target:
                                self.close_all(self.symbol)
                        except Exception as e:
                            print(f"An error occurred: {e}") 
                            # หรือ pass เพื่อข้ามข้อผิดพลาดไป

                    if margin_b > 0:
                        try:
                            pct_buy_profit = self.cal_pct_buy_profit(self.symbol)
                            if pct_buy_profit >= self.profit_target:
                                self.close_all(self.symbol)
                        except Exception as e:
                            print(f"An error occurred: {e}")
                            # หรือ pass เพื่อข้ามข้อผิดพลาดไป
                else: 
                    self.close_limit(self.symbol) 
                    break
