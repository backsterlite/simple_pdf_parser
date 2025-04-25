# 🧾 simple_pdf_parser

**simple_pdf_parser** is a lightweight tool to extract and structure table data from PDF invoices.  
It uses **pdfplumber** and **pandas** to convert semi-structured PDF content into machine-readable format.

---

## 📦 Features

- Extracts tabular data from invoices (using pdfplumber)
- Parses and cleans currency and quantity fields
- Calculates totals (net, VAT, gross)
- Detects and filters transaction rows
- Converts result to CSV

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/backsterlite/simple_pdf_parser.git
cd simple_pdf_parser
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the parser

```bash
python main.py --path sample-invoice.pdf
```

Or with `--all` to parse multiple PDFs from `./invoices` folder.

---

## 📁 Example Output

Extracted CSV includes:

- `Service Description`
- `Quantity`
- `Unit Price`
- `Total Amount`
- `VAT`
- `Gross Total`

See `output/invoice_info.csv` for an example.

---

## 🧰 Technologies

- Python 3.12+
- pdfplumber
- pandas
- argparse
- logging

---

## 📚 License

MIT © 2025 [Your Name]

---

## 🤝 Contributing

Pull requests are welcome. Ideas for improving table detection and format compatibility are appreciated!
