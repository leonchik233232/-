import ccxt
import datetime
import time
import requests

def sync_time_with_ntp():
    ntp_server = 'http://worldtimeapi.org/api/timezone/UTC'
    response = requests.get(ntp_server)
    server_time = response.json()['unixtime']
    current_time = time.time()
    time_difference = server_time - current_time
    time_offset = datetime.timedelta(seconds=time_difference)
    datetime.datetime.now() + time_offset

# Вызов функции для синхронизации времени
    return sync_time_with_ntp()


exchange = ccxt.binance({
    'apiKey': 'y9ZZxXpHnEXXFsMHzoDZAvonb5A8BpSxV8XD2E9eYP5ifreb1CXfHLMBLpeDicJV',
    'secret': 'kYn13lJCWszMlhU4HkJuDu87hxFiuotllKo42ZDZiHP7VRXmaEH4B9BPEBeMhlRH',
})

markets = exchange.fetch_markets()


def find_arbitrage_pairs(markets):
    linked_pairs = []

    for market1 in markets:
        pair1_market = market1['symbol']
        base1, quote1 = pair1_market.split('/')

        if quote1 != 'USDT':
            continue

        for market2 in markets:
            pair2_market = market2['symbol']
            quote2, base2 = pair2_market.split('/')

            if quote2 == base1 and base2 != 'USDT':
                for market3 in markets:
                    pair3_market = market3['symbol']
                    quote3, base3 = pair3_market.split('/')

                    if base3 == base2 and quote3 == 'USDT':
                        ticker1 = exchange.fetch_ticker(pair1_market)
                        ticker2 = exchange.fetch_ticker(pair2_market)
                        ticker3 = exchange.fetch_ticker(pair3_market)

                        pair1_ask_price = ticker1['ask']
                        pair2_ask_price = ticker2['ask']
                        pair3_bid_price = ticker3['bid']

                        

                        profit_percentage_1 = (pair3_bid_price - pair1_ask_price) / pair1_ask_price * 100
                        profit_percentage = profit_percentage_1 + 100
                        print(f"Pair 1: {pair1_market} \nPair 2: {pair2_market} \nPair 3: {pair3_market} \nProfit: {profit_percentage}%")
                        print("-------------------")

                        linked_pairs.append((pair1_market, pair2_market, pair3_market))

    return linked_pairs
# Вызов функции find_arbitrage_pairs и вывод результатов
result = find_arbitrage_pairs(markets)
for pair in result:
    print(pair)
