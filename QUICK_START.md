# 🚀 Quick Start Guide

## Installation (1 minute)

```bash
# Install dependencies
pip install sqlalchemy pandas openpyxl xlrd

# Test installation
python test_import.py
```

## Run Application (instantly)

```bash
python app.py
```

## First Time Usage (3 steps)

1. **Open the app** → Go to "Import Data" tab
2. **Select files** → Click Browse for each file:
   - Users: `excel1.xls`
   - Orders: `excel2.xls`
   - Financials: `excel3 .xls`
3. **Import** → Click "🚀 Start Import"

## Features Overview

| Tab | What You Can Do |
|-----|----------------|
| 📥 Import Data | Import Excel files into database |
| 👥 Users | View/Search 990 customers |
| 📦 Orders | View 42 orders with prices |
| 💰 Financials | View 31 financial records |
| 📊 Statistics | See reports and top customers |

## Key Files

```
app.py              → Run this to start GUI
models.py           → Database structure
data_processor.py   → Import logic
data.db             → Your database (created after import)
```

## Common Tasks

### Reset Database
```bash
rm data.db
python app.py  # Then reimport
```

### Query Database Directly
```bash
sqlite3 data.db
```
```sql
SELECT COUNT(*) FROM users;
SELECT * FROM orders WHERE subscription_code = 1596564;
.quit
```

### Export to CSV
Add to your Python code:
```python
import pandas as pd
from models import Database, User

db = Database('data.db')
session = db.get_session()

# Export users to CSV
df = pd.read_sql(session.query(User).statement, session.bind)
df.to_csv('users_export.csv', index=False)
```

## Keyboard Shortcuts

- **Ctrl+C** - Copy selected text
- **Ctrl+V** - Paste
- **Ctrl+A** - Select all
- **F5** - Refresh current view (if implemented)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Import fails | Check file paths are correct |
| GUI doesn't open | Install: `sudo apt-get install python3-tk` |
| Database locked | Close other programs using data.db |
| Slow import | Normal for large files, wait for completion |

## Data Flow

```
Excel Files → Pandas → Validation → SQLAlchemy → SQLite → Tkinter Display
   (.xls)      (read)    (check)       (ORM)     (data.db)    (GUI)
```

## File Sizes
- excel1.xls: 96 KB (990 users)
- excel2.xls: 91 KB (42 orders)
- excel3.xls: 1.8 MB (31 financials)
- data.db: ~200 KB after import

---

**Need help? Check README_APP.md for detailed documentation**
