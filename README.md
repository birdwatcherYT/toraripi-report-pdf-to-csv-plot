# toraripi-report-pdf-to-csv-plot
トラリピFXの取引報告書PDFをCSVに変換・プロットする

## PDF名を日付に変更する
実行例: fx_pdfsフォルダに`取引報告書兼取引残高報告書（日次）.pdf`が大量にあり, 名前を日付に変更する

```bash
python fx_pdf_rename.py --pdfs fx_pdfs/*.pdf
```

Requirements:
- pip install pymupdf
- pip install tqdm


## PDFをパースしてCSVに変換する

実行例: fx_pdfsフォルダに`取引報告書兼取引残高報告書（日次）.pdf`が大量にあり, csvに変換する

```bash
python fx_pdf_parser.py --pdfs fx_pdfs/*.pdf
```

Requirements:
- pip install pymupdf
- pip install tqdm
- pip install pandas


## 出力したcsvをプロットする

```bash
python fx_summary_plot.py --save
python fx_currency_plot.py --save
```

Requirements:
- pip install japanize_matplotlib
- pip install matplotlib
- pip install pandas


## 成立履歴のCSVをプロットする

```bash
python fx_csv_plot.py --csvs 成立履歴.csv
```

Requirements:
- pip install japanize_matplotlib
- pip install matplotlib
- pip install pandas

## PDFの日付抜け漏れチェック

実行例: fx_pdfsフォルダに`取引報告書兼取引残高報告書（日次）.pdf`が大量にあり, 日付の連続をチェックする

```bash
python fx_pdf_date_check.py --pdfs fx_pdfs/*.pdf
```

Requirements:
- pip install pymupdf
- pip install tqdm
- pip install pandas
