# 🏦 Bank Statement Analyzer

A powerful and interactive Streamlit web app that lets users upload bank statements in CSV or Excel format and visualize transactions, detect anomalies, and gain insights from their financial data.

---

## ✨ Features

- 📤 Upload bank statements in `.csv` or `.xlsx` format
- 🔍 Clean and process transaction data automatically
- 📊 Interactive visualizations using Plotly:
  - Line Chart (Trends over time)
  - Bar Chart (Daily transactions)
  - Histogram (Deposit distribution)
  - Pie Chart (Deposit proportions)
- 📈 Monthly trends and summaries
- 🚨 Outlier detection for unusual deposits
- 📄 Summary insights:
  - Max/Min deposits and withdrawals
  - Dates of significant transactions
- 🔐 Secure local processing, no data leaves your machine

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/bank-statement-analyzer.git
cd bank-statement-analyzer

python -m venv .venv

# Activate it 

# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

streamlit run main.py


├── main.py                        # Streamlit frontend
├── services/
│   └── bank_statement.py          # Data processing logic
├── utils/
│   └── config_logger.py           # Logger config
├── README.md
├── requirements.txt
└── .venv/                         # Virtual environment (excluded from repo)


streamlit
pandas
plotly
openpyxl

pip install -r requirements.txt

```
