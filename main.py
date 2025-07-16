# The code below is meant to test the profitability of the volatility trading strategy in the long run over the hold and buy strategy
# The data was obtained from
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

# print(all_price_list)
polished_price_list = []
ratio_drop = 0.9
ratio_increase = 1.1


def list_polishing_function():
    count = 0
    for q in all_price_list:
        if q != "unknown":
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


def profitability_testing_function(Bankroll: int):
    total_count = 0
    buy_and_hold_bankroll = 100
    buy_and_hold_inv_ratio = polished_price_list[0] / buy_and_hold_bankroll
    buy_and_hold_strategy_bankroll_g = [100]
    for i in polished_price_list:
        buy_and_hold_strategy_bankroll_g.append(i/ buy_and_hold_inv_ratio)
        total_count += 1
        if len(inv_g) == 0:
            inv_g.append(1)
            stock_price_g.append(i)
            Bankroll -= 1
            volatility_strategy_bankroll_g.append(Bankroll)
            print("")
        elif len(inv_g) > 0:
            if i <= stock_price_g[- 1] * ratio_drop:
                inv_g.append(inv_g[- 1] * ratio_drop)
                Bankroll -= inv_g[- 1] * ratio_drop
                stock_price_g.append(stock_price_g[- 1] * ratio_drop)
                volatility_strategy_bankroll_g.append(Bankroll)
                print("")
                if i < stock_price_g[- 1] * ratio_drop and total_count < len(polished_price_list):
                    polished_price_list[total_count] = i

            elif i >= stock_price_g[- 1] * ratio_increase:
                Bankroll += inv_g[- 1] * ratio_increase
                stock_price_g.append(stock_price_g[- 1] * ratio_increase)
                del stock_price_g[- 1]
                del inv_g[- 1]
                volatility_strategy_bankroll_g.append(Bankroll)
                if len(inv_g) == 0:
                    inv_g.append(1)
                    stock_price_g.append(i)
                    Bankroll -= 1
                    volatility_strategy_bankroll_g.append(Bankroll)
                print("")
                if i > stock_price_g[- 1] * ratio_drop and total_count < len(polished_price_list):
                    polished_price_list[total_count] = i

    return [Bankroll, buy_and_hold_strategy_bankroll_g]


func_list = profitability_testing_function(Bankroll)
Bankroll = func_list[0]
buy_and_hold_strategy_bankroll_g = func_list[1]
print("len(buy_and_hold_strategy_bankroll_g): ", len(buy_and_hold_strategy_bankroll_g))
print("len(volatility_strategy_bankroll_g): ", len(volatility_strategy_bankroll_g))

def graph_plotting_function():
    print("plotting begins")
    plt.figure(figsize=(10, 5), dpi=350)  # High DPI is used for sharpness
    plt.figure(figsize=(10, 5))
    plt.plot(list(range(1, len(volatility_strategy_bankroll_g) + 1)), volatility_strategy_bankroll_g, marker='o',
             linestyle='-', color='red', label='volatility strategy bankroll', linewidth=1, alpha=1, antialiased=False)
    plt.plot(list(range(1, len(polished_price_list) + 1)), polished_price_list, marker='o', linestyle='-', color='green', label='Bankroll', linewidth=1, alpha=1, antialiased=False)
    plt.plot(list(range(1, len(buy_and_hold_strategy_bankroll_g) + 1)), buy_and_hold_strategy_bankroll_g, marker='o', linestyle='-', color='blue', label='buy and hold strategy bankroll', linewidth=1, alpha=1, antialiased=False)

    plt.title('Bankroll vs. Number of Games')
    plt.xlabel('Number of Games')
    plt.ylabel('Bankroll ($)')
    plt.grid(True)
    plt.legend(loc="upper left")
    plt.tight_layout()
    plt.show()
    print("plotting complete")

graph_plotting_function()
