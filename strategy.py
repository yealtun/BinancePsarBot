import ccxt, config
import pandas as pd
from ta.trend import PSARIndicator
from smtplib import SMTP



symbolName = input("Sembol adı girin (BTC, ETH, LTC...vb): ")
leverage = input("Kaldıraç büyüklüğü: ")
zamanAraligi = input("Zaman aralığı (1m,3m,5m,15m,30m,45m,1h,2h,4h,6h,8h,12h,1d): ")
symbol = str(symbolName) + "/USDT"
alinacak_miktar = 1

# SAR parameters
sar_af = 0.02
sar_max_af = 0.2

stop_loss_percentage = 0.4
take_profit_percentage = 1.0

longPozisyonda = False
shortPozisyonda = False
pozisyondami = False

# API CONNECT
exchange = ccxt.binance({
    "apiKey": config.apiKey,
    "secret": config.secretKey,
    'options': {'defaultType': 'future'},
    'enableRateLimit': True
})

while True:
    try:
        balance = exchange.fetch_balance()
        free_balance = exchange.fetch_free_balance()
        positions = balance['info']['positions']
        newSymbol = symbolName + "USDT"
        current_positions = [position for position in positions if
                              float(position['positionAmt']) != 0 and position['symbol'] == newSymbol]
        position_bilgi = pd.DataFrame(current_positions,
                                      columns=["symbol", "entryPrice", "unrealizedProfit", "isolatedWallet",
                                               "positionAmt", "positionSide"])

        # Pozisyonda olup olmadığını kontrol etme
        if not position_bilgi.empty and position_bilgi["positionAmt"][len(position_bilgi.index) - 1] != 0:
            pozisyondami = True
        else:
            pozisyondami = False
            shortPozisyonda = False
            longPozisyonda = False

        # Long pozisyonda mı?
        if pozisyondami and float(position_bilgi["positionAmt"][len(position_bilgi.index) - 1]) > 0:
            longPozisyonda = True
            shortPozisyonda = False
        # Short pozisyonda mı?
        if pozisyondami and float(position_bilgi["positionAmt"][len(position_bilgi.index) - 1]) < 0:
            shortPozisyonda = True
            longPozisyonda = False

        # LOAD BARS
        bars = exchange.fetch_ohlcv(symbol, timeframe=zamanAraligi, since=None, limit=1500)
        df = pd.DataFrame(bars, columns=["timestamp", "open", "high", "low", "close", "volume"])

        # LOAD PARABOLIC SAR
        psar_indicator = PSARIndicator(high=df["high"], low=df["low"], close=df["close"], step=sar_af, max_step=sar_max_af)
        df["PSAR"] = psar_indicator.psar()

        # SAR Crossover
        sar_crossover = df["close"] > df["PSAR"]
        sar_crossunder = df["close"] < df["PSAR"]

        # LONG ENTER
        def longEnter(alinacak_miktar, limit_price):
            order = exchange.create_limit_buy_order(symbol, alinacak_miktar, limit_price)
            winsound.Beep(freq, duration)

        # LONG EXIT
        def longExit(limit_price):
            order = exchange.create_limit_sell_order(symbol, float(position_bilgi["positionAmt"].iloc[-1]), limit_price, {"reduceOnly": True})
            winsound.Beep(freq, duration)

        # SHORT ENTER
        def shortEnter(alincak_miktar, limit_price):
            order = exchange.create_limit_sell_order(symbol, alincak_miktar, limit_price)
            winsound.Beep(freq, duration)

        # SHORT EXIT
        def shortExit(limit_price):
            order = exchange.create_limit_buy_order(symbol, (float(position_bilgi["positionAmt"].iloc[-1]) * -1), limit_price, {"reduceOnly": True})
            winsound.Beep(freq, duration)

        # BULL EVENT
        if sar_crossover.iloc[-1] and not sar_crossover.iloc[-2] and not longPozisyonda:
            if shortPozisyonda:
                print("SHORT İŞLEMDEN ÇIKILIYOR...")
                limit_sell_price = df["close"].iloc[-1]
                shortExit(limit_sell_price)

            alinacak_miktar = (((float(free_balance["USDT"]) / 100) * 100) * float(leverage)) / float(df["close"].iloc[-1])
            print("LONG İŞLEME GİRİLİYOR...")
            limit_buy_price = df["close"].iloc[-1]
            longEnter(alinacak_miktar, limit_buy_price)
            baslik = symbol
            message = "LONG ENTER\n" + "Toplam Para: " + str(balance['total']["USDT"])
            content = f"Subject: {baslik}\n\n{message}"
            print(message)

        # BEAR EVENT
        if sar_crossunder.iloc[-1] and not sar_crossunder.iloc[-2] and not shortPozisyonda:
            if longPozisyonda:
                print("LONG İŞLEMDEN ÇIKILIYOR...")
                limit_buy_price = df["close"].iloc[-1]
                longExit(limit_buy_price)

            alinacak_miktar = (((float(free_balance["USDT"]) / 100) * 100) * float(leverage)) / float(df["close"].iloc[-1])
            print("SHORT İŞLEME GİRİLİYOR...")
            limit_sell_price = df["close"].iloc[-1]
            shortEnter(alinacak_miktar, limit_sell_price)
            baslik = symbol
            message = "SHORT ENTER\n" + "Toplam Para: " + str(balance['total']["USDT"])
            print(message)


        # Check for stop-loss and take-profit
        if pozisyondami:
            entry_price = float(position_bilgi["entryPrice"].iloc[-1])
            current_price = df["close"].iloc[-1]

            if shortPozisyonda:
                stop_loss_price = entry_price + (entry_price * stop_loss_percentage / 100)
                take_profit_price = entry_price - (entry_price * take_profit_percentage / 100)

                # Dynamic adjustment for take-profit
                if current_price <= take_profit_price:
                    take_profit_percentage = 1.0  # Set take-profit to 1% gain
                    take_profit_price = entry_price - (entry_price * take_profit_percentage / 100)
                elif current_price > entry_price * (1 + take_profit_percentage / 100):
                    take_profit_percentage += 1.0  # Increase take-profit by 1% if price increased

                if current_price >= stop_loss_price:
                    print("STOP LOSS HIT - SHORT İŞLEMDEN ÇIKILIYOR...")
                    shortExit(current_price)
                elif current_price <= take_profit_price:
                    print("TAKE PROFIT HIT - SHORT İŞLEMDEN ÇIKILIYOR...")
                    shortExit(current_price)

            elif longPozisyonda:
                stop_loss_price = entry_price - (entry_price * stop_loss_percentage / 100)
                take_profit_price = entry_price + (entry_price * take_profit_percentage / 100)

                # Dynamic adjustment for take-profit
                if current_price >= take_profit_price:
                    take_profit_percentage = 1.0  # Set take-profit to 1% gain
                    take_profit_price = entry_price + (entry_price * take_profit_percentage / 100)
                elif current_price < entry_price * (1 - take_profit_percentage / 100):
                    take_profit_percentage += 1.0  # Increase take-profit by 1% if price decreased

                if current_price <= stop_loss_price:
                    print("STOP LOSS HIT - LONG İŞLEMDEN ÇIKILIYOR...")
                    longExit(current_price)
                elif current_price >= take_profit_price:
                    print("TAKE PROFIT HIT - LONG İŞLEMDEN ÇIKILIYOR...")
                    longExit(current_price)
                    
        if not pozisyondami:
            print("POZİSYON ARANIYOR...")
            current_price = df["close"].iloc[-1]
            sar_value = df["PSAR"].iloc[-1]
            print(f"Şu Anki Fiyat: {current_price}")
            print(f"SAR Değeri: {sar_value}")

        if shortPozisyonda:
            print("SHORT POZİSYONDA BEKLİYOR")
            print(f"{'-'*30}")
            print(f"|{'Entry Price':<15}| {entry_price:<15.2f}|")
            print(f"|{'Stop Loss Price':<15}| {stop_loss_price:<15.2f}|")
            print(f"|{'Take Profit Price':<15}| {take_profit_price:<15.2f}|")
            unrealized_profit = float(position_bilgi["unrealizedProfit"].iloc[-1])
            print(f"|{'Unrealized Profit':<15}| {unrealized_profit:<15.2f}|")
            print(f"{'-'*30}")

        elif longPozisyonda:
            print("LONG POZİSYONDA BEKLİYOR")
            print(f"{'-'*30}")
            print(f"|{'Entry Price':<15}| {entry_price:<15.2f}|")
            print(f"|{'Stop Loss Price':<15}| {stop_loss_price:<15.2f}|")
            print(f"|{'Take Profit Price':<15}| {take_profit_price:<15.2f}|")
            unrealized_profit = float(position_bilgi["unrealizedProfit"].iloc[-1])
            print(f"|{'Unrealized Profit':<15}| {unrealized_profit:<15.2f}|")
            print(f"{'-'*30}")

    except ccxt.BaseError as Error:
        print("[ERROR] ", Error)
        continue
