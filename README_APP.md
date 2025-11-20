# Cross Check - Data Management System

A comprehensive desktop application for managing and analyzing customer, order, and financial data from Excel files using Python, Tkinter, SQLAlchemy, and Pandas.

## 🎯 Features

- **Modern GUI Interface** - Built with Tkinter for easy navigation
- **SQLite Database** - Persistent data storage with SQLAlchemy ORM
- **Excel Import** - Read and import data from multiple Excel files (.xls/.xlsx)
- **Data Viewing** - Browse and search users, orders, and financial records
- **Statistics Dashboard** - View comprehensive analytics and reports
- **Multi-threaded** - Non-blocking UI during data import operations

## 📋 Requirements

- Python 3.8 or higher
- Required packages:
  - sqlalchemy
  - pandas
  - openpyxl
  - xlrd
  - tkinter (usually comes with Python)

## 🚀 Installation

1. **Clone or download this project**

2. **Install dependencies:**
   ```bash
   pip install sqlalchemy pandas openpyxl xlrd
   ```

3. **Verify installation:**
   ```bash
   python test_import.py
   ```

## 📁 Project Structure

```
cross_check/
├── app.py                 # Main GUI application
├── models.py              # SQLAlchemy database models
├── data_processor.py      # Data import and processing logic
├── test_import.py         # Test script
├── excel1.xls            # Users data
├── excel2.xls            # Orders data
├── excel3 .xls           # Financial data
└── data.db               # SQLite database (created after import)
```

## 🎮 Usage

### Starting the Application

```bash
python app.py
```

Or make it executable:
```bash
chmod +x app.py
./app.py
```

### Application Interface

The application has 5 main tabs:

#### 1. 📥 Import Data Tab
- Select the three Excel files (excel1.xls, excel2.xls, excel3.xls)
- Click "🚀 Start Import" to import data
- Monitor the import progress in the log window
- View import statistics upon completion

#### 2. 👥 Users Tab
- View all users/customers
- Search by name, surname, mobile, or national ID
- Displays: Subscription Code, Name, Surname, National ID, Mobile, Postal Code, Province, City

#### 3. 📦 Orders Tab
- View all orders/invoices
- See order details including quantities, prices, and totals
- Displays: Invoice ID, Subscription Code, Product Code, Quantity, Price, Total Value, Sending Date

#### 4. 💰 Financials Tab
- View all financial records
- Check loan codes and amounts
- Displays: Subscription Code, Loan Code, Amount, Description

#### 5. 📊 Statistics Tab
- View database statistics
- See record counts
- View top 10 users by order value
- Click "🔄 Refresh Statistics" to update

### Menu Options

- **File Menu:**
  - Import Data - Jump to import tab
  - Exit - Close application

- **View Menu:**
  - Refresh All - Refresh all data views

- **Help Menu:**
  - About - View application information

## 📊 Database Schema

### Users Table
- **Primary Key:** subscription_code
- Fields: name, surname, national_id, mobile, postal_code, address, province, city, etc.

### Orders Table
- **Primary Key:** id (auto-increment)
- **Foreign Key:** subscription_code → users.subscription_code
- Fields: invoice_id, product_code, quantity, price, total_value, sending_date, etc.

### Financials Table
- **Primary Key:** id (auto-increment)
- **Foreign Key:** subscription_code → users.subscription_code
- Fields: loan_code, amount, description

## 🔧 Database Management

### View Database Directly

Using sqlite3 command-line:
```bash
sqlite3 data.db
```

```sql
-- View all tables
.tables

-- View users
SELECT * FROM users LIMIT 10;

-- View orders
SELECT * FROM orders LIMIT 10;

-- View financials
SELECT * FROM financials LIMIT 10;

-- Exit
.quit
```

### Reset Database

To reset the database and reimport data:
1. Delete the `data.db` file
2. Open the application
3. Go to Import Data tab
4. Import the Excel files again

Or programmatically:
```python
from models import Database

db = Database('data.db')
db.recreate_database()  # Drops and recreates all tables
```

## 🔍 Excel File Format

### excel1.xls - Users/Customers
Required columns (in Persian):
- کد اشتراک (Subscription Code)
- نام (Name)
- نام خانوادگی (Surname)
- کد ملی/شناسه ملی (National ID)
- موبایل (Mobile)
- کد پستی (Postal Code)
- آدرس (Address)
- استان (Province)
- شهرستان (City)

### excel2.xls - Orders/Invoices
Required columns (in Persian):
- شناسه فاکتور (Invoice ID)
- کد اشتراک (Subscription Code)
- کد کالا (Product Code)
- تعداد (واحد اصلی) (Quantity)
- فی (Price)
- تاریخ ارسال (Sending Date)
- And more...

### excel3.xls - Financial Records
Required columns (in Persian):
- کد اشتراک (Subscription Code - note: may have trailing space)
- مبلغ (Amount - note: may have trailing space)
- کد وام (Loan Code - note: may have trailing space)
- توضیحات (Description - note: may have trailing space)

**Note:** The column names in excel3.xls may have trailing spaces.

## 🐛 Troubleshooting

### Import Errors
- Make sure Excel files exist in the correct location
- Check that column names match exactly (including spaces)
- Verify the Excel files are not corrupted

### GUI Not Showing
- On Linux, you may need to install python3-tk:
  ```bash
  sudo apt-get install python3-tk
  ```
- On macOS, tkinter should come with Python
- On Windows, tkinter is usually included with Python

### Database Locked
- Close any other programs accessing the database
- Make sure only one instance of the application is running

## 🔒 Data Validation

The application performs the following validations during import:

- Checks for required fields
- Converts data types appropriately
- Handles missing/null values gracefully
- Logs all errors during import
- Uses database transactions for data integrity

## 🎨 Customization

### Changing Database Location
Edit the `db_path` variable in `app.py`:
```python
self.db_path = 'your_custom_path/data.db'
```

### Adding Custom Reports
You can extend the `load_statistics()` method in `app.py` to add custom SQL queries and reports.

### Modifying Import Logic
Edit `data_processor.py` to customize how data is processed and validated during import.

## 📝 License

This project is provided as-is for educational and commercial use.

## 👨‍💻 Support

For issues or questions, please check:
1. The log window during import for specific errors
2. The `test_import.py` script to verify installation
3. Ensure all dependencies are installed correctly

## 🚀 Quick Start Guide

1. Install dependencies: `pip install sqlalchemy pandas openpyxl xlrd`
2. Run test: `python test_import.py`
3. Start app: `python app.py`
4. Click "Import Data" tab
5. Select your three Excel files
6. Click "Start Import"
7. Browse your data in the other tabs!

---

**Built with ❤️ using Python, Tkinter, SQLAlchemy, and Pandas**
