def order(symbol, quantity, side, order_type, time_in, API_KEY, SECRET_KEY):
    import alpaca_trade_api as tradeapi

    order = tradeapi.REST(API_KEY, SECRET_KEY, base_url='https://paper-api.alpaca.markets')
    order.submit_order(
        symbol=symbol,
        qty=quantity,
        side=side,  # 'buy' for buying or 'sell' for selling
        type=order_type,  # 'market', 'limit', 'stop', or 'stop_limit'
        time_in_force=time_in  # 'gtc', 'day', or 'opg'
    )

    print('========== Order Sent ==========')