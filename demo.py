#!/usr/bin/env python3
"""
Automated demo of Cross Check application
"""
import time
from models import Database
from data_processor import DataProcessor
from sqlalchemy import func


def print_header(title, char="="):
    print("\n" + char * 80)
    print(f"  {title}")
    print(char * 80)


def demo():
    """Run automated demo"""
    print("\n" + "╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "🎬 CROSS CHECK - AUTOMATED DEMO" + " " * 32 + "║")
    print("╚" + "═" * 78 + "╝")

    print_header("STEP 1: Initialize Database", "-")
    print("Creating database and tables...")
    db = Database('data.db')
    db.create_tables()
    print("✅ Database initialized!")
    time.sleep(1)

    print_header("STEP 2: Import Data from Excel Files", "-")
    print("\n📁 Importing from:")
    print("  • excel1.xls (Users)")
    print("  • excel2.xls (Orders)")
    print("  • excel3 .xls (Financials)")
    print()

    processor = DataProcessor('data.db')

    def log_callback(msg):
        print(f"  {msg}")

    stats = processor.import_all_data(
        'excel1.xls',
        'excel2.xls',
        'excel3 .xls',
        log_callback=log_callback
    )

    print("\n✅ Import Summary:")
    print(f"  • Users imported: {stats['users_imported']}")
    print(f"  • Orders imported: {stats['orders_imported']}")
    print(f"  • Financials imported: {stats['financials_imported']}")
    time.sleep(2)

    print_header("STEP 3: View Users Data", "-")
    session = db.get_session()

    from models import User, Order, Financial

    users = session.query(User).limit(10).all()
    print(f"\n👥 First 10 users (out of {session.query(User).count()}):\n")
    print(f"{'Code':<12} {'Name':<20} {'Surname':<20} {'Mobile':<15}")
    print("-" * 80)
    for user in users:
        print(f"{user.subscription_code:<12} "
              f"{(user.name or '')[:19]:<20} "
              f"{(user.surname or '')[:19]:<20} "
              f"{(user.mobile or '')[:14]:<15}")
    time.sleep(2)

    print_header("STEP 4: View Orders Data", "-")
    orders = session.query(Order).limit(10).all()
    print(f"\n📦 First 10 orders (out of {session.query(Order).count()}):\n")
    print(f"{'Invoice':<15} {'SubCode':<12} {'Qty':<6} {'Price':<18} {'Total':<18}")
    print("-" * 80)
    for order in orders:
        print(f"{(order.invoice_id or '')[:14]:<15} "
              f"{order.subscription_code:<12} "
              f"{order.quantity:<6} "
              f"{order.price:>17,.0f} "
              f"{order.total_value:>17,.0f}")
    time.sleep(2)

    print_header("STEP 5: View Financial Data", "-")
    financials = session.query(Financial).limit(10).all()
    print(f"\n💰 First 10 financial records (out of {session.query(Financial).count()}):\n")
    print(f"{'SubCode':<12} {'Loan Code':<12} {'Amount':<20}")
    print("-" * 80)
    for fin in financials:
        print(f"{fin.subscription_code:<12} "
              f"{(fin.loan_code or ''):<12} "
              f"{fin.amount:>19,.0f}")
    time.sleep(2)

    print_header("STEP 6: Database Statistics", "-")

    users_count = session.query(User).count()
    orders_count = session.query(Order).count()
    financials_count = session.query(Financial).count()

    total_orders_value = session.query(func.sum(Order.total_value)).scalar() or 0
    total_financial_amount = session.query(func.sum(Financial.amount)).scalar() or 0

    print("\n📊 Statistics:\n")
    print(f"  Record Counts:")
    print(f"    • Total Users:              {users_count:>10,}")
    print(f"    • Total Orders:             {orders_count:>10,}")
    print(f"    • Total Financial Records:  {financials_count:>10,}")
    print(f"\n  Financial Totals:")
    print(f"    • Total Order Value:        {total_orders_value:>18,.0f} Rials")
    print(f"    • Total Financial Amount:   {total_financial_amount:>18,.0f} Rials")
    time.sleep(2)

    print_header("STEP 7: Top 5 Customers by Order Value", "-")

    top_users = session.query(
        User.subscription_code,
        User.name,
        User.surname,
        func.sum(Order.total_value).label('total')
    ).join(Order).group_by(
        User.subscription_code
    ).order_by(
        func.sum(Order.total_value).desc()
    ).limit(5).all()

    print("\n🏆 Top 5 Customers:\n")
    print(f"{'Rank':<6} {'Code':<12} {'Name':<35} {'Total Value':<20}")
    print("-" * 80)

    for i, (code, name, surname, total) in enumerate(top_users, 1):
        full_name = f"{name} {surname}"
        print(f"{i:<6} {code:<12} {full_name[:34]:<35} {total:>19,.0f}")

    session.close()
    time.sleep(2)

    print_header("✅ DEMO COMPLETED!", "=")
    print("\n🎉 All features demonstrated successfully!\n")
    print("📋 What you've seen:")
    print("  ✓ Database initialization")
    print("  ✓ Excel data import with validation")
    print("  ✓ Users management")
    print("  ✓ Orders tracking")
    print("  ✓ Financial records")
    print("  ✓ Statistics and analytics")
    print("  ✓ Top customers report")

    print("\n💡 Next steps:")
    print("  • Run CLI version: python app_cli.py")
    print("  • Run GUI version on your local machine: python app.py")
    print("  • Query database directly: sqlite3 data.db")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
