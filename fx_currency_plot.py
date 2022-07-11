# python fx_plot.py --save

import argparse
import pandas as pd
import japanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates

UNITS = {"円": 1, "千円": 1000, "万円": 10000}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csvs", default=["成立履歴.csv"], nargs="+", help="成立履歴.csv")
    parser.add_argument("--save", action="store_true", help="保存するかどうか")
    parser.add_argument("--unit", default="万円", type=str, help="万円/千円/円")
    args = parser.parse_args()

    unit_value = UNITS[args.unit]

    print(args.csvs)

    df = pd.concat(
        [pd.read_csv(csv, encoding="shift_jis", dtype="str") for csv in args.csvs],
        ignore_index=True,
    )

    df = df.loc[df["区分"] == "決済"]
    df["成立日時"] = pd.to_datetime(df["成立日時"])
    df["日付"] = df["成立日時"].dt.date
    df["確定損益"] = df["確定損益"].str.replace(",", "").astype(int)

    df_group = df.groupby(["通貨ペア", "日付"])["確定損益"].sum().reset_index()
    df_pivot = pd.pivot_table(df_group, values="確定損益", index="日付", columns="通貨ペア")
    df_pivot = df_pivot.fillna(0).cumsum()

    ax = df_pivot.plot(
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
