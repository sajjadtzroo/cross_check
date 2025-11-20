# Cross Check - Data Management System

A comprehensive desktop application for managing and analyzing customer, order, and financial data from Excel files.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20|%20macOS%20|%20Linux-lightgrey.svg)

## 🎯 Features

- **Modern GUI** - Built with Tkinter for easy data visualization
- **CLI Version** - Terminal-based interface for headless environments
- **SQLite Database** - Persistent storage with SQLAlchemy ORM
- **Excel Import** - Read and validate data from multiple Excel files
- **Data Analysis** - Statistics, reports, and search functionality
- **Multi-threaded** - Non-blocking operations during data import

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cross_check.git
cd cross_check

# Install dependencies
pip install sqlalchemy pandas openpyxl xlrd

# Test installation
python test_import.py
```

### Run the Application

**GUI Version (with display):**
```bash
python app.py
```

**CLI Version (terminal/headless):**
```bash
python app_cli.py
```

**Automated Demo:**
```bash
python demo.py
```

## 📊 What It Does

The application imports data from three Excel files:

1. **excel1.xls** - Customer/User information
2. **excel2.xls** - Orders/Invoices
3. **excel3.xls** - Financial transactions

All data is validated, imported into a SQLite database, and made available for:
- Viewing and searching
- Statistical analysis
- Top customers reports
- Direct SQL queries

## 📁 Project Structure

```
cross_check/
├── app.py              # Main GUI application (Tkinter)
├── app_cli.py          # CLI application (Terminal)
├── demo.py             # Automated demo
├── models.py           # Database models (SQLAlchemy)
├── data_processor.py   # Data import and validation
├── test_import.py      # Installation test script
│
├── excel1.xls          # Users data (sample)
├── excel2.xls          # Orders data (sample)
├── excel3 .xls         # Financials data (sample)
│
├── README.md           # This file
├── README_APP.md       # Detailed application guide
├── QUICK_START.md      # Quick reference
├── PROJECT_SUMMARY.md  # Technical overview
└── HOW_TO_RUN.md       # Running instructions
```

## 🗄️ Database Schema

```
Users (subscription_code PK)
  ├─ name, surname, national_id
  ├─ mobile, phone, email
  └─ address, postal_code, province, city

Orders (id PK, subscription_code FK)
  ├─ invoice_id, product_code
  ├─ quantity, price, total_value
  └─ dates, warehouse info

Financials (id PK, subscription_code FK)
  ├─ loan_code, amount
  └─ description
```

## 💻 Requirements

- Python 3.8 or higher
- SQLAlchemy 2.0+
- Pandas 2.0+
- OpenPyXL
- xlrd
- Tkinter (usually included with Python)

## 📚 Documentation

- **[README_APP.md](README_APP.md)** - Complete application guide
- **[QUICK_START.md](QUICK_START.md)** - Quick reference
- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - Running instructions
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Technical details

## 🔧 Usage Examples

### Import Data
```python
from data_processor import DataProcessor

processor = DataProcessor('data.db')
stats = processor.import_all_data(
    'excel1.xls',
    'excel2.xls',
    'excel3.xls'
)
```

### Query Database
```python
from models import Database, User, Order

db = Database('data.db')
session = db.get_session()

# Get all users
users = session.query(User).all()

# Search users
users = session.query(User).filter(
    User.name.like('%John%')
).all()
```

### Direct SQL
```bash
sqlite3 data.db "SELECT * FROM users LIMIT 10;"
```

## 🐛 Troubleshooting

### GUI won't start
If you get "no display name" error, use the CLI version:
```bash
python app_cli.py
```

### Missing dependencies
```bash
pip install sqlalchemy pandas openpyxl xlrd
```

## 📝 License

This project is provided as-is for educational and commercial use.

## 👨‍💻 Author

Built with Python, Tkinter, SQLAlchemy, and Pandas.

---

**For detailed usage instructions, see [README_APP.md](README_APP.md)**

**For quick start, see [QUICK_START.md](QUICK_START.md)**
