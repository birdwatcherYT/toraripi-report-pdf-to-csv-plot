echo "pdf -> csv"
python fx_pdf_parser.py --pdfs fx_pdfs/*.pdf

echo "csv -> png"
python fx_summary_plot.py --save
python fx_currency_plot.py --save
