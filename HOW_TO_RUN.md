# 🚀 How to Run Cross Check

## ✅ What Just Happened

The demo successfully:
- ✓ Created SQLite database (`data.db` - 20 KB)
- ✓ Imported 5 users from excel1.xls
- ✓ Imported 18 orders from excel2.xls
- ✓ Imported 5 financial records from excel3.xls
- ✓ Generated statistics and reports

---

## 🖥️ Running the GUI Application (Recommended)

The GUI version (`app.py`) requires a display server. Here's how to run it:

### **Option 1: On Your Local Machine (Windows/Mac/Linux)**

1. **Download the project files** to your local computer

2. **Install dependencies:**
   ```bash
   pip install sqlalchemy pandas openpyxl xlrd
   ```

3. **Run the GUI:**
   ```bash
   python app.py
   ```

4. **Use the application:**
   - Beautiful tabbed interface
   - Click buttons to import/view/search
   - See real-time progress logs
   - View statistics with charts

### **Option 2: In Codespaces with X11 Forwarding (Advanced)**

If you're using VS Code with Codespaces:

1. Install X server on your local machine:
   - **Windows:** Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
   - **Mac:** Install [XQuartz](https://www.xquartz.org/)
   - **Linux:** Already has X server

2. Set display variable:
   ```bash
   export DISPLAY=host.docker.internal:0
   python app.py
   ```

---

## 💻 Running the CLI Application (Works Everywhere)

The CLI version works in any terminal, including this one!

### **Interactive Mode:**
```bash
python app_cli.py
```

This gives you a menu:
```
📋 Main Menu:
  1. Import Data from Excel files
  2. View Users
  3. View Orders
  4. View Financials
  5. Show Statistics
  6. Search Users
  7. Exit
```

### **Quick Demo:**
```bash
python demo.py
```
Automatically runs through all features.

---

## 🗄️ Direct Database Access

The SQLite database (`data.db`) can be accessed directly:

### **Using sqlite3 command:**
```bash
sqlite3 data.db
```

Then run SQL queries:
```sql
-- View all users
SELECT * FROM users;

-- View orders for a specific user
SELECT * FROM orders WHERE subscription_code = 1596564;

-- Get total orders value per user
SELECT subscription_code, SUM(total_value) as total
FROM orders
GROUP BY subscription_code
ORDER BY total DESC;

-- Exit
.quit
```

### **Using Python:**
```python
import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Query users
cursor.execute("SELECT * FROM users LIMIT 5")
for row in cursor.fetchall():
    print(row)

conn.close()
```

### **Using DB Browser (GUI):**
Download [DB Browser for SQLite](https://sqlitebrowser.org/) and open `data.db`

---

## 📊 Exporting Data

### **Export to CSV:**
```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///data.db')

# Export users
df = pd.read_sql_table('users', engine)
df.to_csv('users_export.csv', index=False)

# Export orders
df = pd.read_sql_table('orders', engine)
df.to_csv('orders_export.csv', index=False)
```

### **Export to Excel:**
```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite:///data.db')

with pd.ExcelWriter('export.xlsx') as writer:
    pd.read_sql_table('users', engine).to_excel(writer, sheet_name='Users', index=False)
    pd.read_sql_table('orders', engine).to_excel(writer, sheet_name='Orders', index=False)
    pd.read_sql_table('financials', engine).to_excel(writer, sheet_name='Financials', index=False)
```

---

## 🔄 Available Commands Summary

| Command | Description |
|---------|-------------|
| `python app.py` | **GUI Application** (requires display) |
| `python app_cli.py` | **CLI Application** (interactive menu) |
| `python demo.py` | **Automated Demo** (shows all features) |
| `python test_import.py` | **Test Script** (verify installation) |
| `sqlite3 data.db` | **Direct DB Access** (SQL queries) |

---

## 📁 Project Files Overview

```
cross_check/
├── 🎨 GUI & CLI Applications
│   ├── app.py              - Tkinter GUI (23 KB) ⭐
│   ├── app_cli.py          - CLI version (15 KB)
│   └── demo.py             - Automated demo (4 KB)
│
├── 🏗️ Core Components
│   ├── models.py           - Database models (6 KB)
│   └── data_processor.py   - Import logic (15 KB)
│
├── 📊 Data Files
│   ├── excel1.xls          - Users data (96 KB)
│   ├── excel2.xls          - Orders data (91 KB)
│   ├── excel3 .xls         - Financials data (1.8 MB)
│   └── data.db             - SQLite database (20 KB) ✅
│
├── 📚 Documentation
│   ├── README_APP.md       - Complete guide (7 KB)
│   ├── QUICK_START.md      - Quick reference (2 KB)
│   ├── PROJECT_SUMMARY.md  - Technical overview (11 KB)
│   └── HOW_TO_RUN.md       - This file
│
└── 🧪 Testing
    └── test_import.py      - Installation test (2 KB)
```

---

## 🎯 Quick Start for Different Scenarios

### **Scenario 1: I want to see it working NOW**
```bash
python demo.py
```

### **Scenario 2: I want to use the terminal version**
```bash
python app_cli.py
```

### **Scenario 3: I want the beautiful GUI**
1. Copy files to local machine
2. `pip install sqlalchemy pandas openpyxl xlrd`
3. `python app.py`

### **Scenario 4: I just want to query the data**
```bash
sqlite3 data.db
```

### **Scenario 5: I want to integrate it into my project**
```python
from models import Database, User, Order, Financial

db = Database('data.db')
session = db.get_session()
users = session.query(User).all()
```

---

## 🔧 Troubleshooting

### **"No display name and no $DISPLAY" Error**
- This means you're in a headless environment
- Solution: Use `app_cli.py` instead of `app.py`
- Or: Set up X11 forwarding (advanced)

### **"Module not found" Error**
```bash
pip install sqlalchemy pandas openpyxl xlrd
```

### **"File not found" Error**
- Make sure you're in the `/workspaces/cross_check/` directory
- Check files exist: `ls -la *.xls`

### **"Database locked" Error**
- Close any other programs accessing `data.db`
- Only run one instance at a time

---

## 📈 Current Database Status

After running the demo:

| Table | Records | Description |
|-------|---------|-------------|
| **users** | 5 | Customer information |
| **orders** | 18 | Order/invoice records |
| **financials** | 5 | Financial transactions |

**Total Order Value:** 8,113,650,000 Rials
**Database Size:** 20 KB

---

## 🎓 Learning Resources

- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **Pandas Docs:** https://pandas.pydata.org/docs/
- **Tkinter Tutorial:** https://docs.python.org/3/library/tkinter.html
- **SQLite Tutorial:** https://www.sqlitetutorial.net/

---

## 💡 Pro Tips

1. **Backup your database:**
   ```bash
   cp data.db data.db.backup
   ```

2. **View table structure:**
   ```bash
   sqlite3 data.db ".schema users"
   ```

3. **Check database size:**
   ```bash
   sqlite3 data.db "SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size();"
   ```

4. **Optimize database:**
   ```bash
   sqlite3 data.db "VACUUM;"
   ```

---

## 🌟 Next Steps

1. ✅ **Demo completed** - You've seen it work!
2. 📝 **Try CLI** - Run `python app_cli.py`
3. 🖥️ **Install locally** - Get the full GUI experience
4. 🔍 **Explore data** - Use `sqlite3 data.db`
5. 🚀 **Customize** - Modify the code for your needs!

---

**For more help, check:**
- `README_APP.md` - Full documentation
- `QUICK_START.md` - Quick reference
- `PROJECT_SUMMARY.md` - Technical details

**Need support? All code is well-commented and documented!**
