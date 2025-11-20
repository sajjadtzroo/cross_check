#!/usr/bin/env python3
"""
Cross Check - Data Management System
GUI Application using Tkinter with SQLAlchemy and Pandas
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import threading
import os
from models import Database, User, Order, Financial
from data_processor import DataProcessor


class CrossCheckApp:
    """Main application window"""

    def __init__(self, root):
        self.root = root
        self.root.title("Cross Check - مدیریت اطلاعات")
        self.root.geometry("1200x700")

        # Database and processor
        self.db_path = 'data.db'
        self.db = Database(self.db_path)
        self.processor = DataProcessor(self.db_path)

        # Create database tables if not exist
        self.db.create_tables()

        # Initialize UI
        self.create_menu()
        self.create_tabs()
        self.create_status_bar()

        # Load initial data
        self.refresh_all_views()

    def create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Import Data", command=self.show_import_tab)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh All", command=self.refresh_all_views)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_tabs(self):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs
        self.create_import_tab()
        self.create_users_tab()
        self.create_orders_tab()
        self.create_financials_tab()
        self.create_statistics_tab()

    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = tk.Label(self.status_frame, text="Ready", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    # ==================== IMPORT TAB ====================

    def create_import_tab(self):
        """Create data import tab"""
        self.import_frame = tk.Frame(self.notebook)
        self.notebook.add(self.import_frame, text="📥 Import Data")

        # Title
        title = tk.Label(self.import_frame, text="Import Data from Excel Files",
                        font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # File selection frame
        file_frame = tk.LabelFrame(self.import_frame, text="Select Excel Files", padx=20, pady=20)
        file_frame.pack(padx=20, pady=10, fill="x")

        self.excel1_path = tk.StringVar(value="excel1.xls")
        self.excel2_path = tk.StringVar(value="excel2.xls")
        self.excel3_path = tk.StringVar(value="excel3 .xls")

        # Excel 1
        tk.Label(file_frame, text="Users File (excel1.xls):").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(file_frame, textvariable=self.excel1_path, width=50).grid(row=0, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=lambda: self.browse_file(self.excel1_path)).grid(row=0, column=2)

        # Excel 2
        tk.Label(file_frame, text="Orders File (excel2.xls):").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(file_frame, textvariable=self.excel2_path, width=50).grid(row=1, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=lambda: self.browse_file(self.excel2_path)).grid(row=1, column=2)

        # Excel 3
        tk.Label(file_frame, text="Financials File (excel3.xls):").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(file_frame, textvariable=self.excel3_path, width=50).grid(row=2, column=1, padx=5)
        tk.Button(file_frame, text="Browse", command=lambda: self.browse_file(self.excel3_path)).grid(row=2, column=2)

        # Import button
        self.import_button = tk.Button(self.import_frame, text="🚀 Start Import",
                                      command=self.start_import,
                                      bg="#4CAF50", fg="white",
                                      font=("Arial", 12, "bold"),
                                      padx=20, pady=10)
        self.import_button.pack(pady=20)

        # Log area
        log_frame = tk.LabelFrame(self.import_frame, text="Import Log", padx=10, pady=10)
        log_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.import_log = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.import_log.pack(fill="both", expand=True)

    def browse_file(self, var):
        """Browse for file"""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xls *.xlsx"), ("All files", "*.*")]
        )
        if filename:
            var.set(filename)

    def log_message(self, message):
        """Add message to import log"""
        self.import_log.insert(tk.END, message + "\n")
        self.import_log.see(tk.END)
        self.root.update_idletasks()

    def start_import(self):
        """Start data import in separate thread"""
        # Validate files
        if not all([
            os.path.exists(self.excel1_path.get()),
            os.path.exists(self.excel2_path.get()),
            os.path.exists(self.excel3_path.get())
        ]):
            messagebox.showerror("Error", "Please select all three Excel files!")
            return

        # Disable button
        self.import_button.config(state=tk.DISABLED, text="⏳ Importing...")
        self.import_log.delete(1.0, tk.END)

        # Run in thread
        thread = threading.Thread(target=self.do_import, daemon=True)
        thread.start()

    def do_import(self):
        """Perform data import"""
        try:
            self.processor = DataProcessor(self.db_path)
            stats = self.processor.import_all_data(
                self.excel1_path.get(),
                self.excel2_path.get(),
                self.excel3_path.get(),
                log_callback=self.log_message
            )

            # Refresh all views
            self.root.after(0, self.refresh_all_views)

            # Show completion message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Import completed!\n\n"
                f"Users: {stats['users_imported']}\n"
                f"Orders: {stats['orders_imported']}\n"
                f"Financials: {stats['financials_imported']}\n"
                f"Errors: {len(stats['errors'])}"
            ))

        except Exception as e:
            self.log_message(f"❌ Fatal error: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", str(e)))

        finally:
            self.root.after(0, lambda: self.import_button.config(
                state=tk.NORMAL,
                text="🚀 Start Import"
            ))

    # ==================== USERS TAB ====================

    def create_users_tab(self):
        """Create users view tab"""
        self.users_frame = tk.Frame(self.notebook)
        self.notebook.add(self.users_frame, text="👥 Users")

        # Search frame
        search_frame = tk.Frame(self.users_frame)
        search_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.users_search = tk.Entry(search_frame, width=30)
        self.users_search.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="🔍 Search", command=self.search_users).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="🔄 Refresh", command=self.load_users).pack(side=tk.LEFT, padx=5)

        # Treeview
        tree_frame = tk.Frame(self.users_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Scrollbars
        v_scroll = tk.Scrollbar(tree_frame, orient="vertical")
        h_scroll = tk.Scrollbar(tree_frame, orient="horizontal")

        self.users_tree = ttk.Treeview(
            tree_frame,
            columns=("code", "name", "surname", "national_id", "mobile", "postal_code", "province", "city"),
            show="headings",
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )

        v_scroll.config(command=self.users_tree.yview)
        h_scroll.config(command=self.users_tree.xview)

        # Column headers
        self.users_tree.heading("code", text="Subscription Code")
        self.users_tree.heading("name", text="Name")
        self.users_tree.heading("surname", text="Surname")
        self.users_tree.heading("national_id", text="National ID")
        self.users_tree.heading("mobile", text="Mobile")
        self.users_tree.heading("postal_code", text="Postal Code")
        self.users_tree.heading("province", text="Province")
        self.users_tree.heading("city", text="City")

        # Column widths
        self.users_tree.column("code", width=120)
        self.users_tree.column("name", width=100)
        self.users_tree.column("surname", width=100)
        self.users_tree.column("national_id", width=100)
        self.users_tree.column("mobile", width=120)
        self.users_tree.column("postal_code", width=100)
        self.users_tree.column("province", width=100)
        self.users_tree.column("city", width=100)

        # Pack
        self.users_tree.pack(side=tk.LEFT, fill="both", expand=True)
        v_scroll.pack(side=tk.RIGHT, fill="y")
        h_scroll.pack(side=tk.BOTTOM, fill="x")

        # Count label
        self.users_count_label = tk.Label(self.users_frame, text="Total: 0 users")
        self.users_count_label.pack(pady=5)

    def load_users(self):
        """Load users into treeview"""
        self.update_status("Loading users...")

        # Clear existing
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        session = self.db.get_session()
        try:
            users = session.query(User).all()

            for user in users:
                self.users_tree.insert("", "end", values=(
                    user.subscription_code or "",
                    user.name or "",
                    user.surname or "",
                    user.national_id or "",
                    user.mobile or "",
                    user.postal_code or "",
                    user.province or "",
                    user.city or ""
                ))

            self.users_count_label.config(text=f"Total: {len(users)} users")
            self.update_status(f"Loaded {len(users)} users")

        finally:
            session.close()

    def search_users(self):
        """Search users"""
        search_term = self.users_search.get().strip()
        if not search_term:
            self.load_users()
            return

        self.update_status(f"Searching for: {search_term}")

        # Clear existing
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)

        session = self.db.get_session()
        try:
            users = session.query(User).filter(
                (User.name.like(f"%{search_term}%")) |
                (User.surname.like(f"%{search_term}%")) |
                (User.mobile.like(f"%{search_term}%")) |
                (User.national_id.like(f"%{search_term}%"))
            ).all()

            for user in users:
                self.users_tree.insert("", "end", values=(
                    user.subscription_code or "",
                    user.name or "",
                    user.surname or "",
                    user.national_id or "",
                    user.mobile or "",
                    user.postal_code or "",
                    user.province or "",
                    user.city or ""
                ))

            self.users_count_label.config(text=f"Found: {len(users)} users")
            self.update_status(f"Found {len(users)} users")

        finally:
            session.close()

    # ==================== ORDERS TAB ====================

    def create_orders_tab(self):
        """Create orders view tab"""
        self.orders_frame = tk.Frame(self.notebook)
        self.notebook.add(self.orders_frame, text="📦 Orders")

        # Toolbar
        toolbar = tk.Frame(self.orders_frame)
        toolbar.pack(fill="x", padx=5, pady=5)

        tk.Button(toolbar, text="🔄 Refresh", command=self.load_orders).pack(side=tk.LEFT, padx=5)

        # Treeview
        tree_frame = tk.Frame(self.orders_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        v_scroll = tk.Scrollbar(tree_frame, orient="vertical")
        h_scroll = tk.Scrollbar(tree_frame, orient="horizontal")

        self.orders_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "invoice_id", "subscription_code", "product_code", "quantity", "price", "total", "sending_date"),
            show="headings",
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )

        v_scroll.config(command=self.orders_tree.yview)
        h_scroll.config(command=self.orders_tree.xview)

        # Headers
        self.orders_tree.heading("id", text="ID")
        self.orders_tree.heading("invoice_id", text="Invoice ID")
        self.orders_tree.heading("subscription_code", text="Subscription Code")
        self.orders_tree.heading("product_code", text="Product Code")
        self.orders_tree.heading("quantity", text="Quantity")
        self.orders_tree.heading("price", text="Price")
        self.orders_tree.heading("total", text="Total Value")
        self.orders_tree.heading("sending_date", text="Sending Date")

        # Widths
        self.orders_tree.column("id", width=50)
        self.orders_tree.column("invoice_id", width=100)
        self.orders_tree.column("subscription_code", width=120)
        self.orders_tree.column("product_code", width=120)
        self.orders_tree.column("quantity", width=80)
        self.orders_tree.column("price", width=120)
        self.orders_tree.column("total", width=120)
        self.orders_tree.column("sending_date", width=100)

        self.orders_tree.pack(side=tk.LEFT, fill="both", expand=True)
        v_scroll.pack(side=tk.RIGHT, fill="y")
        h_scroll.pack(side=tk.BOTTOM, fill="x")

        self.orders_count_label = tk.Label(self.orders_frame, text="Total: 0 orders")
        self.orders_count_label.pack(pady=5)

    def load_orders(self):
        """Load orders into treeview"""
        self.update_status("Loading orders...")

        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)

        session = self.db.get_session()
        try:
            orders = session.query(Order).all()

            for order in orders:
                self.orders_tree.insert("", "end", values=(
                    order.id,
                    order.invoice_id or "",
                    order.subscription_code or "",
                    order.product_code or "",
                    order.quantity or 0,
                    f"{order.price:,.0f}" if order.price else "0",
                    f"{order.total_value:,.0f}" if order.total_value else "0",
                    order.sending_date or ""
                ))

            self.orders_count_label.config(text=f"Total: {len(orders)} orders")
            self.update_status(f"Loaded {len(orders)} orders")

        finally:
            session.close()

    # ==================== FINANCIALS TAB ====================

    def create_financials_tab(self):
        """Create financials view tab"""
        self.financials_frame = tk.Frame(self.notebook)
        self.notebook.add(self.financials_frame, text="💰 Financials")

        # Toolbar
        toolbar = tk.Frame(self.financials_frame)
        toolbar.pack(fill="x", padx=5, pady=5)

        tk.Button(toolbar, text="🔄 Refresh", command=self.load_financials).pack(side=tk.LEFT, padx=5)

        # Treeview
        tree_frame = tk.Frame(self.financials_frame)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)

        v_scroll = tk.Scrollbar(tree_frame, orient="vertical")
        h_scroll = tk.Scrollbar(tree_frame, orient="horizontal")

        self.financials_tree = ttk.Treeview(
            tree_frame,
            columns=("id", "subscription_code", "loan_code", "amount", "description"),
            show="headings",
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set
        )

        v_scroll.config(command=self.financials_tree.yview)
        h_scroll.config(command=self.financials_tree.xview)

        # Headers
        self.financials_tree.heading("id", text="ID")
        self.financials_tree.heading("subscription_code", text="Subscription Code")
        self.financials_tree.heading("loan_code", text="Loan Code")
        self.financials_tree.heading("amount", text="Amount")
        self.financials_tree.heading("description", text="Description")

        # Widths
        self.financials_tree.column("id", width=50)
        self.financials_tree.column("subscription_code", width=120)
        self.financials_tree.column("loan_code", width=100)
        self.financials_tree.column("amount", width=150)
        self.financials_tree.column("description", width=300)

        self.financials_tree.pack(side=tk.LEFT, fill="both", expand=True)
        v_scroll.pack(side=tk.RIGHT, fill="y")
        h_scroll.pack(side=tk.BOTTOM, fill="x")

        self.financials_count_label = tk.Label(self.financials_frame, text="Total: 0 records")
        self.financials_count_label.pack(pady=5)

    def load_financials(self):
        """Load financial records into treeview"""
        self.update_status("Loading financials...")

        for item in self.financials_tree.get_children():
            self.financials_tree.delete(item)

        session = self.db.get_session()
        try:
            financials = session.query(Financial).all()

            for fin in financials:
                self.financials_tree.insert("", "end", values=(
                    fin.id,
                    fin.subscription_code or "",
                    fin.loan_code or "",
                    f"{fin.amount:,.0f}" if fin.amount else "0",
                    fin.description or ""
                ))

            self.financials_count_label.config(text=f"Total: {len(financials)} records")
            self.update_status(f"Loaded {len(financials)} financial records")

        finally:
            session.close()

    # ==================== STATISTICS TAB ====================

    def create_statistics_tab(self):
        """Create statistics tab"""
        self.stats_frame = tk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="📊 Statistics")

        # Title
        title = tk.Label(self.stats_frame, text="Database Statistics",
                        font=("Arial", 16, "bold"))
        title.pack(pady=20)

        # Stats display
        self.stats_text = scrolledtext.ScrolledText(
            self.stats_frame,
            height=25,
            width=80,
            font=("Courier", 10)
        )
        self.stats_text.pack(padx=20, pady=10, fill="both", expand=True)

        # Refresh button
        tk.Button(self.stats_frame, text="🔄 Refresh Statistics",
                 command=self.load_statistics,
                 font=("Arial", 12)).pack(pady=10)

    def load_statistics(self):
        """Load and display statistics"""
        self.update_status("Loading statistics...")
        self.stats_text.delete(1.0, tk.END)

        session = self.db.get_session()
        try:
            # Count records
            users_count = session.query(User).count()
            orders_count = session.query(Order).count()
            financials_count = session.query(Financial).count()

            # Get top users by order value
            from sqlalchemy import func
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

            # Display stats
            stats = f"""
{'='*80}
                          DATABASE STATISTICS
{'='*80}

RECORD COUNTS:
  • Total Users:              {users_count:>10}
  • Total Orders:             {orders_count:>10}
  • Total Financial Records:  {financials_count:>10}

{'='*80}

TOP 10 USERS BY ORDER VALUE:

"""
            self.stats_text.insert(tk.END, stats)

            for i, (code, name, surname, total) in enumerate(top_users, 1):
                line = f"  {i:>2}. Code: {code:<10} | {name} {surname:<20} | {total:>15,.0f} Rials\n"
                self.stats_text.insert(tk.END, line)

            self.stats_text.insert(tk.END, "\n" + "="*80)

            self.update_status("Statistics loaded")

        finally:
            session.close()

    # ==================== UTILITY METHODS ====================

    def refresh_all_views(self):
        """Refresh all data views"""
        self.load_users()
        self.load_orders()
        self.load_financials()
        self.load_statistics()
        self.update_status("All views refreshed")

    def show_import_tab(self):
        """Switch to import tab"""
        self.notebook.select(0)

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About",
            "Cross Check - Data Management System\n\n"
            "Version 1.0\n\n"
            "Built with:\n"
            "• Python\n"
            "• Tkinter (GUI)\n"
            "• SQLAlchemy (ORM)\n"
            "• Pandas (Data Processing)\n"
            "• SQLite (Database)"
        )


def main():
    """Main entry point"""
    root = tk.Tk()
    CrossCheckApp(root)  # Initialize app
    root.mainloop()


if __name__ == "__main__":
    main()
