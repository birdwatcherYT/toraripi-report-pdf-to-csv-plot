# python fx_pdf_rename.py --pdfs fx_pdfs/*.pdf

import argparse
from enum import Enum
import fitz  # pymupdf
from tqdm import tqdm
from pathlib import Path


def pdf_rename(pdf: str):
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
                date = line.replace("/", "")
                mode = Mode.NONE
                break
    doc.close()

    assert date is not None
    pdf_before_path = Path(pdf)
    pdf_after_path = pdf_before_path.parent / f"{date}.pdf"
    pdf_before_path.rename(pdf_after_path)
    print(f"{pdf_before_path} -> {pdf_after_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdfs", nargs="+", default=["取引報告書兼取引残高報告書（日次）.pdf"])
    args = parser.parse_args()

    print(args.pdfs)

    for pdf in tqdm(args.pdfs):
        pdf_rename(pdf)
