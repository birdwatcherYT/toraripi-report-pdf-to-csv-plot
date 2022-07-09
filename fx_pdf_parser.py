# python fx_pdf_parser.py --pdfs fx_pdfs/*.pdf

import argparse
import pandas as pd
import fitz  # pymupdf
from tqdm import tqdm


def to_int(string: str) -> int:
    num = None
    try:
        num = int(string)
    except:
        pass
    return num


def pdf_to_record(pdf: str) -> dict:
    doc = fitz.open(pdf)
    page = doc.load_page(0)
    text = page.get_text("text")
    lines = text.split("\n")

    next_date = False
    next_account_state = False
    next_inout = False
    next_sum = False

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

    for i in range(doc.page_count):
        page = doc.load_page(i)
        text = page.get_text("text")
        lines = text.split("\n")

        # print(lines)
        for line in lines:
            if "【取引日】" == line:
                next_date = date is None
            elif next_date:
                date = line.replace("/", "-")
                next_date = False
            elif "【口座状況】" == line:
                next_account_state = True
            elif next_account_state:
                num = to_int(line.replace(",", ""))
                if num is not None:
                    account_values.append(num)
                next_account_state = len(account_values) < len(account_columns)
            elif "【入出金明細】" == line:
                next_inout = True
            elif next_inout and "合計" == line:
                next_sum = True
            elif next_sum:
                num = to_int(line.replace(",", ""))
                if num is not None:
                    inout_values.append(num)
                next_sum = len(inout_values) < len(inout_columns)

    if len(inout_values) == 0:
        inout_values = [0] * len(inout_columns)

    assert date is not None
    assert len(account_columns) == len(account_values)
    assert len(inout_columns) == len(inout_values)

    columns = ["日付"] + account_columns + inout_columns
    values = [date] + account_values + inout_values
    record = dict(zip(columns, values))
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdfs", nargs="+", default=["取引報告書兼取引残高報告書（日次）.pdf"])
    args = parser.parse_args()

    print(args.pdfs)

    records = [pdf_to_record(pdf) for pdf in tqdm(args.pdfs)]
    df = pd.DataFrame(records)
    df = df.sort_values("日付")

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
    df = df[order]

    print(df)
    df.to_csv("fx_pdfs.csv", index=False, encoding="shift_jis")
