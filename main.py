import pandas as pd
import matplotlib.pyplot as plt

file_path = "C:/Users/USER/Desktop/SPX.csv"

df = pd.read_csv(file_path)

df["Open"] = df["Open"].fillna("unknown")
df["High"] = df["High"].fillna("unknown")
df["Low"] = df["Low"].fillna("unknown")
df["Close"] = df["Close"].fillna("unknown")

open_list = df["Open"].tolist()
high_list = df["High"].tolist()
low_list = df["Low"].tolist()
close_list = df["Close"].tolist()

all_price_list = open_list + high_list + low_list + close_list

# all_price_list = [1, 3, 2, 3, 2, 3, 1, 3]
# print(all_price_list)
polished_price_list = []
ratio_drop = 0.9
ratio_increase = 1.1

def list_polishing_function():
    count = 0
    for q in all_price_list:
        polished_price_list.append(q)
        count += 1
        if count < len(all_price_list):
            if all_price_list[count] > all_price_list[count - 1]:
                while q < all_price_list[count]:
                    q += ratio_increase - 1
                    if q < all_price_list[count]:
                        polished_price_list.append(q)

            elif all_price_list[count] < all_price_list[count - 1]:
                while q > all_price_list[count]:
                    q -= ratio_increase - 1
                    if q > all_price_list[count]:
                        polished_price_list.append(q)


list_polishing_function()
print("polished_price_list: ", polished_price_list)
stock_price_g = []
inv_g = []
Bankroll = 100
volatility_strategy_bankroll_g = [100]
buy_and_hold_strategy_bankroll_g = []

def profitability_testing_function(Bankroll: int):
    for i in polished_price_list:
        if len(inv_g) == 0:
            inv_g.append(1)
            stock_price_g.append(i)
            Bankroll -= 1
            print("111iii: ", i)
            print("111Bankroll: ", Bankroll)
            volatility_strategy_bankroll_g.append(Bankroll)
            print("")
        elif len(inv_g) > 0:
            if i <= stock_price_g[- 1] * ratio_drop:
                inv_g.append(inv_g[- 1] * ratio_drop)
                Bankroll -= inv_g[- 1] * ratio_drop
                stock_price_g.append(stock_price_g[- 1] * ratio_drop)
                print("2222iii: ", i)
                print("222Bankroll: ", Bankroll)
                volatility_strategy_bankroll_g.append(Bankroll)
                print("")
            elif i >= stock_price_g[- 1] * ratio_increase:
                print("3333iii: ", i)
                print("333111inv_g: ", inv_g)
                Bankroll += inv_g[- 1] * ratio_increase
                stock_price_g.append(stock_price_g[- 1] * ratio_increase)
                del stock_price_g[- 1]
                del inv_g[- 1]
                print("333Bankroll: ", Bankroll)
                volatility_strategy_bankroll_g.append(Bankroll)
                print("333inv_g: ", inv_g)
                if len(inv_g) == 0:
                    inv_g.append(1)
                    stock_price_g.append(i)
                    Bankroll -= 1
                print("3fff33Bankroll: ", Bankroll)
                volatility_strategy_bankroll_g.append(Bankroll)
                print("3fff33inv_g: ", inv_g)
                print("")

    return Bankroll


Bankroll = profitability_testing_function(Bankroll)
print("Bankroll: ", Bankroll)

def graph_plotting_function():
    print("plotting begins")
    plt.figure(figsize=(10, 5), dpi=350)  # High DPI is used for sharpness
    plt.figure(figsize=(10, 5))
    plt.plot(list(range(1, len(volatility_strategy_bankroll_g) + 1)), volatility_strategy_bankroll_g, marker='o', linestyle='-', color='red', label='Bankroll', linewidth=1, alpha=1, antialiased=False)
    #plt.plot(list(range(1, len(polished_price_list) + 1)), polished_price_list, marker='o', linestyle='-', color='blue', label='Bankroll', linewidth=1, alpha=1, antialiased=False)
    #plt.plot(list(range(1, len(buy_and_hold_strategy_bankroll_g) + 1)), buy_and_hold_strategy_bankroll_g, marker='o', linestyle='-', color='blue', label='Bankroll', linewidth=1, alpha=1, antialiased=False)

    plt.title('Bankroll vs. Number of Games')
    plt.xlabel('Number of Games')
    plt.ylabel('Bankroll ($)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
    print("plotting complete")


graph_plotting_function()
