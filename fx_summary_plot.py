# python fx_summary_plot.py --save

import argparse
import pandas as pd
import japanize_matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

UNITS = {"円": 1, "千円": 1000, "万円": 10000}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--file", default="fx_summary.csv", help="fx_summary.csv", type=str
    )
    parser.add_argument("--save", action="store_true", help="保存するかどうか")
    parser.add_argument("--settlement", action="store_true", help="決済成立タイミングで月集計")
    parser.add_argument("--width", default=2, type=int, help="棒グラフの幅")
    parser.add_argument("--base", default=0, type=int, help="データに含まれない初期資金")
    parser.add_argument("--ymin", default=None, type=int, help="資産推移の最小値")
    parser.add_argument("--unit", default="万円", type=str, help="万円/千円/円")
    args = parser.parse_args()

    unit_value = UNITS[args.unit]

    df = pd.read_csv(args.file, encoding="shift_jis")

    if "累計入出金" not in df.columns:
        df["累計入出金"] = df["入出金"].cumsum() + args.base
    if "累計確定損益" not in df.columns:
        df["累計確定損益"] = df["預託証拠金"] - df["累計入出金"] + df["受渡前損益"]

    df["日付"] = pd.to_datetime(df["日付"])

    plt.figure(figsize=(8, 5))
    plt.bar(df["日付"], df["累計確定損益"], label="累計確定損益", color="red", width=args.width)
    plt.plot(df["日付"], df["評価損益"], label="評価損益", color="blue")
    plt.grid()
    plt.legend()
    plt.title("損益推移")
    plt.gca().get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda v, p: f"{v/unit_value:,.0f}{args.unit}")
    )

    if args.save:
        plt.savefig("fx_profit.png")
    else:
        plt.show()

    df["年月"] = df["日付"].dt.strftime("%Y-%m")
    df["確定損益"] = df["累計確定損益"].diff().fillna(0)
    data_month = df.groupby(["年月"])[["総合計", "入出金", "確定損益"]].sum()

    plt.figure(figsize=(8, 5))
    plt.bar(
        data_month.index,
        data_month["確定損益"]
        if args.settlement
        else data_month["総合計"] - data_month["入出金"],
        label="確定損益",
        color="red",
    )
    plt.grid()
    plt.legend()
    plt.title("毎月の確定損益 " + ("(決済成立タイミング)" if args.settlement else "(口座反映タイミング)"))
    plt.gca().get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda v, p: f"{v/unit_value:,.0f}{args.unit}")
    )
    plt.xticks(rotation=30)

    if args.save:
        plt.savefig("fx_month_profit.png")
    else:
        plt.show()

    plt.figure(figsize=(8, 5))
    plt.plot(df["日付"], df["預託証拠金"], "b", label="預託証拠金")
    plt.plot(df["日付"], df["有効証拠金"], "r--", label="有効証拠金")
    plt.plot(df["日付"], df["累計入出金"], "g:", label="累計入出金")
    plt.grid()
    plt.legend()
    plt.title("資産推移")
    plt.gca().get_yaxis().set_major_formatter(
        ticker.FuncFormatter(lambda v, p: f"{v/unit_value:,.0f}{args.unit}")
    )
    plt.ylim([args.ymin, None])

    if args.save:
        plt.savefig("fx_total.png")
    else:
        plt.show()
