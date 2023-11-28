import ccxt
from colorama import init, Fore
import time
from datetime import datetime

exchange = ccxt.binance({
'apiKey': 'y9ZZxXpHnEXXFsMHzoDZAvonb5A8BpSxV8XD2E9eYP5ifreb1CXfHLMBLpeDicJV',
'secret': 'kYn13lJCWszMlhU4HkJuDu87hxFiuotllKo42ZDZiHP7VRXmaEH4B9BPEBeMhlRH'
})

init()

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
                        pair1_buy_price = exchange.fetch_ticker(pair1_market)['bid']
                        pair2_buy_price = exchange.fetch_ticker(pair2_market)['bid']
                        pair3_sell_price = exchange.fetch_ticker(pair3_market)['ask']
                        
                        if pair1_buy_price is not None and pair2_buy_price is not None and pair3_sell_price is not None:
                            profit_percentage = ((pair1_buy_price * pair2_buy_price * pair3_sell_price) - 1) * 100
                            profit_percentage = round(profit_percentage, 2)

                            if profit_percentage > 0: # Исправлено: проверка на прибыльность
                                pair1_url = f"https://www.binance.com/ru/trade/{pair1_market.replace('/', '_')}?_from=markets"
                                pair2_url = f"https://www.binance.com/ru/trade/{pair2_market.replace('/', '_')}?_from=markets"
                                pair3_url = f"https://www.binance.com/ru/trade/{pair3_market.replace('/', '_')}?_from=markets"

                                print(f"Pair 1: {Fore.BLUE} {pair1_market} {Fore.RESET},    Buy Price:  {Fore.GREEN}{pair1_buy_price}{Fore.RESET}\n{pair1_url}")
                                print(f"Pair 2: {Fore.BLUE} {pair2_market} {Fore.RESET},     Buy Price:  {Fore.GREEN}{pair2_buy_price}{Fore.RESET}\n{pair2_url}")
                                print(f"Pair 3: {Fore.BLUE} {pair3_market} {Fore.RESET},    Sell Price:  {Fore.RED}{pair3_sell_price}{Fore.RESET}\n{pair3_url}")
                                print(f"Profit:  {profit_percentage}%")
                                print("-------------------")
                                linked_pairs.append((pair1_market, pair2_market, pair3_market))

    return linked_pairs



def main():
    server_time = exchange.fetch_time()
    local_time = datetime.now().timestamp() * 1000
    time_diff = int(local_time - server_time)
    exchange.options = {
        'adjustForTimeDifference': True,
        'timestamp': time_diff
    }

    result = find_arbitrage_pairs(markets)
    for pair in result:
        print(pair)

if __name__ == "__main__":
    main()

