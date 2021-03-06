# python fx_currency_plot.py --save

import argparse
import pandas as pd
import japanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

UNITS = {"円": 1, "千円": 1000, "万円": 10000}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="fx_currency.csv", help="fx_currency.csv")
    parser.add_argument("--save", action="store_true", help="保存するかどうか")
    parser.add_argument("--unit", default="万円", type=str, help="万円/千円/円")
    args = parser.parse_args()

    unit_value = UNITS[args.unit]

    df = pd.read_csv(args.file, encoding="shift_jis")
    df = df.set_index("日付")
    df = df.fillna(0).cumsum()

    ax = df.plot(
        kind="bar",
        stacked=True,
        grid=True,
        legend=True,
        title="通貨ごとの確定損益",
        rot=20,
        figsize=(8, 5),
    )
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.yaxis.set_major_formatter(
        ticker.FuncFormatter(lambda v, p: f"{v/unit_value:,.0f}{args.unit}")
    )

    if args.save:
        plt.savefig("fx_currency.png")
    else:
        plt.show()
