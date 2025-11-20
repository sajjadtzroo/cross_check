#!/usr/bin/env python3
"""
Cross Check - Command Line Interface
Run this version in terminal/headless environments
"""
import sys
from models import Database, User, Order, Financial
from data_processor import DataProcessor
from sqlalchemy import func


class CrossCheckCLI:
    """Command-line interface for Cross Check"""

    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.db = Database(db_path)
        self.processor = DataProcessor(db_path)
        self.db.create_tables()

    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "=" * 80)
        print(f"  {title}")
        print("=" * 80)

    def print_menu(self):
        """Display main menu"""
        self.print_header("CROSS CHECK - DATA MANAGEMENT SYSTEM")
        print("\n📋 Main Menu:")
        print("  1. Import Data from Excel files")
        print("  2. View Users")
        print("  3. View Orders")
        print("  4. View Financials")
        print("  5. Show Statistics")
        print("  6. Search Users")
        print("  7. Exit")
        print("\n" + "-" * 80)

    def import_data(self):
        """Import data from Excel files"""
        self.print_header("IMPORT DATA")

        print("\n📁 Excel files to import:")
        print("  • excel1.xls (Users)")
        print("  • excel2.xls (Orders)")
        print("  • excel3 .xls (Financials)")

        confirm = input("\n⚠️  This will recreate the database. Continue? (y/n): ").lower()
        if confirm != 'y':
            print("❌ Import cancelled.")
            return

        print("\n🚀 Starting import...\n")

        def log_callback(msg):
            print(f"  {msg}")

        stats = self.processor.import_all_data(
            'excel1.xls',
            'excel2.xls',
            'excel3 .xls',
            log_callback=log_callback
        )

        print("\n✅ Import completed!")
        print(f"\n📊 Summary:")
        print(f"  • Users imported: {stats['users_imported']}")
        print(f"  • Orders imported: {stats['orders_imported']}")
        print(f"  • Financials imported: {stats['financials_imported']}")
        print(f"  • Errors: {len(stats['errors'])}")

        if stats['errors']:
            show_errors = input("\nShow errors? (y/n): ").lower()
            if show_errors == 'y':
                for error in stats['errors'][:10]:  # Show first 10
                    print(f"  ⚠️  {error}")

    def view_users(self, limit=20):
        """View users"""
        self.print_header("USERS")

        session = self.db.get_session()
        try:
            total = session.query(User).count()
            users = session.query(User).limit(limit).all()

            if not users:
                print("\n❌ No users found. Please import data first.")
                return

            print(f"\nShowing {len(users)} of {total} users:\n")
            print(f"{'Code':<12} {'Name':<15} {'Surname':<15} {'Mobile':<15} {'City':<15}")
            print("-" * 80)

            for user in users:
                print(f"{user.subscription_code:<12} "
                      f"{(user.name or '')[:14]:<15} "
                      f"{(user.surname or '')[:14]:<15} "
                      f"{(user.mobile or '')[:14]:<15} "
                      f"{(user.city or '')[:14]:<15}")

            print(f"\n📊 Total: {total} users")

        finally:
            session.close()

    def view_orders(self, limit=20):
        """View orders"""
        self.print_header("ORDERS")

        session = self.db.get_session()
        try:
            total = session.query(Order).count()
            orders = session.query(Order).limit(limit).all()

            if not orders:
                print("\n❌ No orders found. Please import data first.")
                return

            print(f"\nShowing {len(orders)} of {total} orders:\n")
            print(f"{'Invoice':<12} {'SubCode':<10} {'Product':<15} {'Qty':<6} {'Price':<15} {'Total':<15}")
            print("-" * 80)

            for order in orders:
                print(f"{(order.invoice_id or '')[:11]:<12} "
                      f"{order.subscription_code:<10} "
                      f"{(order.product_code or '')[:14]:<15} "
                      f"{order.quantity:<6} "
                      f"{order.price:>14,.0f} "
                      f"{order.total_value:>14,.0f}")

            print(f"\n📊 Total: {total} orders")

        finally:
            session.close()

    def view_financials(self, limit=20):
        """View financial records"""
        self.print_header("FINANCIALS")

        session = self.db.get_session()
        try:
            total = session.query(Financial).count()
            financials = session.query(Financial).limit(limit).all()

            if not financials:
                print("\n❌ No financial records found. Please import data first.")
                return

            print(f"\nShowing {len(financials)} of {total} records:\n")
            print(f"{'ID':<6} {'SubCode':<12} {'Loan Code':<12} {'Amount':<18} {'Description':<30}")
            print("-" * 80)

            for fin in financials:
                desc = (fin.description or '')[:29]
                print(f"{fin.id:<6} "
                      f"{fin.subscription_code:<12} "
                      f"{(fin.loan_code or ''):<12} "
                      f"{fin.amount:>17,.0f} "
                      f"{desc:<30}")

            print(f"\n📊 Total: {total} records")

        finally:
            session.close()

    def show_statistics(self):
        """Show database statistics"""
        self.print_header("STATISTICS")

        session = self.db.get_session()
        try:
            users_count = session.query(User).count()
            orders_count = session.query(Order).count()
            financials_count = session.query(Financial).count()

            if users_count == 0:
                print("\n❌ No data found. Please import data first.")
                return

            # Total amounts
            total_orders_value = session.query(func.sum(Order.total_value)).scalar() or 0
            total_financial_amount = session.query(func.sum(Financial.amount)).scalar() or 0

            print("\n📊 Database Statistics:\n")
            print(f"  Record Counts:")
            print(f"    • Users:              {users_count:>10,}")
            print(f"    • Orders:             {orders_count:>10,}")
            print(f"    • Financial Records:  {financials_count:>10,}")
            print(f"\n  Financial Totals:")
            print(f"    • Total Order Value:  {total_orders_value:>15,.0f} Rials")
            print(f"    • Total Financials:   {total_financial_amount:>15,.0f} Rials")

            # Top users by order value
            print("\n  📈 Top 10 Users by Order Value:\n")
            top_users = session.query(
                User.subscription_code,
                User.name,
                User.surname,
                func.sum(Order.total_value).label('total')
            ).join(Order).group_by(
                User.subscription_code
            ).order_by(
                func.sum(Order.total_value).desc()
            ).limit(10).all()

            print(f"    {'Rank':<6} {'Code':<12} {'Name':<30} {'Total Value':<20}")
            print("    " + "-" * 70)

            for i, (code, name, surname, total) in enumerate(top_users, 1):
                full_name = f"{name} {surname}"
                print(f"    {i:<6} {code:<12} {full_name[:29]:<30} {total:>19,.0f}")

        finally:
            session.close()

    def search_users(self):
        """Search users"""
        self.print_header("SEARCH USERS")

        query = input("\n🔍 Enter search term (name, mobile, or national ID): ").strip()
        if not query:
            print("❌ Search cancelled.")
            return

        session = self.db.get_session()
        try:
            users = session.query(User).filter(
                (User.name.like(f"%{query}%")) |
                (User.surname.like(f"%{query}%")) |
                (User.mobile.like(f"%{query}%")) |
                (User.national_id.like(f"%{query}%"))
            ).limit(50).all()

            if not users:
                print(f"\n❌ No users found matching '{query}'")
                return

            print(f"\n✅ Found {len(users)} user(s):\n")
            print(f"{'Code':<12} {'Name':<15} {'Surname':<15} {'Mobile':<15} {'National ID':<12}")
            print("-" * 80)

            for user in users:
                print(f"{user.subscription_code:<12} "
                      f"{(user.name or '')[:14]:<15} "
                      f"{(user.surname or '')[:14]:<15} "
                      f"{(user.mobile or '')[:14]:<15} "
                      f"{(user.national_id or '')[:11]:<12}")

        finally:
            session.close()

    def run(self):
        """Main application loop"""
        print("\n" + "╔" + "═" * 78 + "╗")
        print("║" + " " * 20 + "Welcome to Cross Check CLI" + " " * 32 + "║")
        print("╚" + "═" * 78 + "╝")

        while True:
            try:
                self.print_menu()
                choice = input("Select option (1-7): ").strip()

                if choice == '1':
                    self.import_data()
                elif choice == '2':
                    self.view_users()
                elif choice == '3':
                    self.view_orders()
                elif choice == '4':
                    self.view_financials()
                elif choice == '5':
                    self.show_statistics()
                elif choice == '6':
                    self.search_users()
                elif choice == '7':
                    print("\n👋 Goodbye!\n")
                    sys.exit(0)
                else:
                    print("❌ Invalid option. Please select 1-7.")

                input("\n⏎ Press Enter to continue...")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!\n")
                sys.exit(0)
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()
                input("\n⏎ Press Enter to continue...")


def main():
    """Main entry point"""
    app = CrossCheckCLI()
    app.run()


if __name__ == "__main__":
    main()
