# python fx_pdf_parser.py --pdfs fx_pdfs/*.pdf

import argparse
from collections import defaultdict
from enum import Enum
import pandas as pd
import fitz  # pymupdf
from tqdm import tqdm
from typing import Tuple


def to_int(string: str) -> int:
    num = None
    try:
        num = int(string)
    except:
        pass
    return num


def pdf_to_record(pdf: str) -> Tuple[dict, dict]:
    class Mode(Enum):
        NONE = -1
        DATE = 0
        ACCOUNT_STATE = 1
        DETAIL = 2
        INOUT = 3
        INOUT_SUM = 4

    doc = fitz.open(pdf)
    page = doc.load_page(0)
    text = page.get_text("text")
    lines = text.split("\n")

    mode = Mode.NONE
    currency_pair = None

    date = None
    account_columns = [
        "預託証拠金",
        "(内)ポジション",
        "評価損益",
        "(内)スワップ",
        "受渡前損益",
        "有効証拠金",
        "総必要証拠金",
        "(内)必要証拠金",
        "出金予約額",
        "出金可能額",
    ]
    account_values = []
    inout_columns = ["入出金", "売買損益", "スワップ損益", "その他", "総合計", "スワップ振替"]
    inout_values = []
    currency_pair_sum = defaultdict(int)

    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text")
        lines = text.split("\n")

        # print(lines)
        for line in lines:
            # モード切り替え
            if "【取引日】" == line:
                if date is None:
                    mode = Mode.DATE
            elif "【口座状況】" == line:
                mode = Mode.ACCOUNT_STATE
            elif "未決済金額" == line:
                mode = Mode.NONE
            elif "新規決済区分" == line:
                mode = Mode.DETAIL
            elif "入出金" == line:
                mode = Mode.INOUT
            elif mode == Mode.INOUT and "合計" == line:
                mode = Mode.INOUT_SUM
            # モード使用
            elif mode == Mode.DATE:
                date = line.replace("/", "-")
                mode = Mode.NONE
            elif mode == Mode.ACCOUNT_STATE:
                num = to_int(line.replace(",", ""))
                if num is not None:
                    account_values.append(num)
                if len(account_values) >= len(account_columns):
                    mode = Mode.NONE
            elif mode == Mode.DETAIL:
                if len(line.split("/")) == 2:
                    currency_pair = line.replace(" ", "")
                elif currency_pair is not None and line.startswith("￥"):
                    currency_pair_sum[currency_pair] += int(line[1:].replace(",", ""))
                    currency_pair = None
            elif mode == Mode.INOUT_SUM:
                num = to_int(line.replace(",", ""))
                if num is not None:
                    inout_values.append(num)
                if len(inout_values) >= len(inout_columns):
                    mode = Mode.NONE

    if len(inout_values) == 0:
        inout_values = [0] * len(inout_columns)

    assert date is not None
    assert len(account_columns) == len(account_values)
    assert len(inout_columns) == len(inout_values)

    columns = ["日付"] + account_columns + inout_columns
    values = [date] + account_values + inout_values
    record = dict(zip(columns, values))

    currency_pair_sum["日付"] = date
    return record, currency_pair_sum


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdfs", nargs="+", default=["取引報告書兼取引残高報告書（日次）.pdf"])
    args = parser.parse_args()

    print(args.pdfs)

    records = [pdf_to_record(pdf) for pdf in tqdm(args.pdfs)]

    summary_df = pd.DataFrame([r for r, c in records])
    summary_df = summary_df.sort_values("日付")
    currency_df = pd.DataFrame([c for r, c in records])
    currency_df = currency_df.sort_values("日付")

    order = [
        "日付",
        "預託証拠金",
        "評価損益",
        "(内)ポジション",
        "(内)スワップ",
        "受渡前損益",
        "有効証拠金",
        "総必要証拠金",
        "(内)必要証拠金",
        "出金予約額",
        "出金可能額",
        "入出金",
        "売買損益",
        "スワップ損益",
        "スワップ振替",
        "その他",
        "総合計",
    ]
    summary_df = summary_df[order]

    print(summary_df)
    summary_df.to_csv("fx_summary.csv", index=False, encoding="shift_jis")

    print(currency_df)
    currency_df.to_csv("fx_currency.csv", index=False, encoding="shift_jis")
