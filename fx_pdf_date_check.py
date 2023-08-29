# python fx_pdf_date_check.py --pdfs fx_pdfs/*.pdf

import argparse
from enum import Enum
import fitz  # pymupdf
from tqdm import tqdm
import pandas as pd


def pdf_date_check(pdf: str) -> str:
    class Mode(Enum):
        NONE = -1
        DATE = 0

    doc = fitz.open(pdf)
    page = doc.load_page(0)
    text = page.get_text("text")
    lines = text.split("\n")

    mode = Mode.NONE
    date = None

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
            # モード使用
            elif mode == Mode.DATE:
                date = line.replace("/", "-")
                mode = Mode.NONE
                break
    doc.close()

    assert date is not None
    return date


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdfs", nargs="+", default=["取引報告書兼取引残高報告書（日次）.pdf"])
    args = parser.parse_args()

    print(args.pdfs)

    df = pd.DataFrame(
        {"date": sorted([pdf_date_check(pdf) for pdf in tqdm(args.pdfs)])}
    )
    df["date"] = pd.to_datetime(df["date"])
    df["weekday"] = df["date"].dt.weekday
    df["date_diff_days"] = df["date"].diff().dt.days
    missing_end = df[
        df["date_diff_days"].notnull()
        & (
            ((df["weekday"] != 0) & (df["date_diff_days"] != 1))  # 月曜以外
            | ((df["weekday"] == 0) & (df["date_diff_days"] != 3))  # 月曜
        )
    ]
    # print(missing_end)

    miss_dates = []
    for i, row in missing_end.iterrows():
        miss = pd.date_range(
            row["date"] - pd.DateOffset(days=row["date_diff_days"] - 1),
            row["date"] - pd.DateOffset(days=1),
        ).to_series()
        miss_dates.append(miss[miss.dt.weekday <= 4])
    print(pd.concat(miss_dates, ignore_index=True))
