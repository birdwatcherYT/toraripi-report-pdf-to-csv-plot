# toraripi-report-pdf-to-csv-plot
トラリピFXの取引報告書PDFをCSVに変換・プロットする


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
python fx_plot.py --save
```

Requirements:
- pip install japanize_matplotlib
- pip install matplotlib
- pip install pandas


## 成立履歴のCSVをプロットする

```bash
python fx_currency_plot.py --csvs 成立履歴.csv
```

Requirements:
- pip install japanize_matplotlib
- pip install matplotlib
- pip install pandas
