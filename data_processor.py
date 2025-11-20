"""
Data processing module for reading Excel files and importing to database
"""
import pandas as pd
from models import Database, User, Order, Financial


class DataProcessor:
    """Handles data import from Excel files to database"""

    def __init__(self, db_path='data.db'):
        self.db = Database(db_path)
        self.stats = {
            'users_imported': 0,
            'orders_imported': 0,
            'financials_imported': 0,
            'errors': []
        }

    def import_users_from_excel(self, file_path, log_callback=None):
        """Import users from excel1.xls"""
        if log_callback:
            log_callback(f"Reading users from: {file_path}")

        try:
            # Read Excel file
            df = pd.read_excel(file_path, engine='xlrd')

            if log_callback:
                log_callback(f"Found {len(df)} rows in users file")

            session = self.db.get_session()
            imported_count = 0

            for index, row in df.iterrows():
                try:
                    # Create user object
                    user = User(
                        subscription_code=int(row.get('کد اشتراک', 0)) if pd.notna(row.get('کد اشتراک')) else None,
                        name=str(row.get('نام', '')).strip() if pd.notna(row.get('نام')) else None,
                        surname=str(row.get('نام خانوادگی', '')).strip() if pd.notna(row.get('نام خانوادگی')) else None,
                        father_name=str(row.get('نام پدر', '')).strip() if pd.notna(row.get('نام پدر')) else None,
                        certificate_number=str(row.get('شماره شناسنامه', '')).strip() if pd.notna(row.get('شماره شناسنامه')) else None,
                        national_id=str(row.get('کد ملی/شناسه ملی', '')).strip() if pd.notna(row.get('کد ملی/شناسه ملی')) else None,
                        second_name=str(row.get('نام دوم (چاپی)', '')).strip() if pd.notna(row.get('نام دوم (چاپی)')) else None,
                        phone1=str(row.get('تلفن 1', '')).strip() if pd.notna(row.get('تلفن 1')) else None,
                        phone2=str(row.get('تلفن 2', '')).strip() if pd.notna(row.get('تلفن 2')) else None,
                        phone3=str(row.get('تلفن 3', '')).strip() if pd.notna(row.get('تلفن 3')) else None,
                        mobile=str(row.get('موبایل', '')).strip() if pd.notna(row.get('موبایل')) else None,
                        fax=str(row.get('نمابر', '')).strip() if pd.notna(row.get('نمابر')) else None,
                        economic_code=str(row.get('کد اقتصادی', '')).strip() if pd.notna(row.get('کد اقتصادی')) else None,
                        address=str(row.get('آدرس', '')).strip() if pd.notna(row.get('آدرس')) else None,
                        postal_code=str(row.get('کد پستی', '')).strip() if pd.notna(row.get('کد پستی')) else None,
                        email=str(row.get('ایمیل', '')).strip() if pd.notna(row.get('ایمیل')) else None,
                        province=str(row.get('استان', '')).strip() if pd.notna(row.get('استان')) else None,
                        city=str(row.get('شهرستان', '')).strip() if pd.notna(row.get('شهرستان')) else None
                    )

                    if user.subscription_code:
                        session.merge(user)  # Use merge to handle duplicates
                        imported_count += 1

                except Exception as e:
                    error_msg = f"Error importing user at row {index + 2}: {str(e)}"
                    self.stats['errors'].append(error_msg)
                    if log_callback:
                        log_callback(f"⚠️ {error_msg}")

            session.commit()
            session.close()

            self.stats['users_imported'] = imported_count
            if log_callback:
                log_callback(f"✅ Successfully imported {imported_count} users")

            return imported_count

        except Exception as e:
            error_msg = f"Error reading users file: {str(e)}"
            self.stats['errors'].append(error_msg)
            if log_callback:
                log_callback(f"❌ {error_msg}")
            return 0

    def import_orders_from_excel(self, file_path, log_callback=None):
        """Import orders from excel2.xls"""
        if log_callback:
            log_callback(f"Reading orders from: {file_path}")

        try:
            df = pd.read_excel(file_path, engine='xlrd')

            if log_callback:
                log_callback(f"Found {len(df)} rows in orders file")

            session = self.db.get_session()
            imported_count = 0

            for index, row in df.iterrows():
                try:
                    # Calculate total value
                    quantity = int(row.get('تعداد (واحد اصلی)', 0)) if pd.notna(row.get('تعداد (واحد اصلی)')) else 0
                    price = float(row.get('فی', 0)) if pd.notna(row.get('فی')) else 0.0
                    total_value = quantity * price

                    order = Order(
                        invoice_id=str(row.get('شناسه فاکتور', '')).strip() if pd.notna(row.get('شناسه فاکتور')) else None,
                        invoice_date=str(row.get('تاریخ فاکتور', '')).strip() if pd.notna(row.get('تاریخ فاکتور')) else None,
                        subscription_code=int(row.get('کد اشتراک', 0)) if pd.notna(row.get('کد اشتراک')) else None,
                        person_name=str(row.get('نام شخص', '')).strip() if pd.notna(row.get('نام شخص')) else None,
                        description=str(row.get('توضیحات', '')).strip() if pd.notna(row.get('توضیحات')) else None,
                        settlement_type=str(row.get('نوع تسویه', '')).strip() if pd.notna(row.get('نوع تسویه')) else None,
                        settlement_date=str(row.get('تاریخ تسویه', '')).strip() if pd.notna(row.get('تاریخ تسویه')) else None,
                        expiry_date=str(row.get('تاریخ انقضا', '')).strip() if pd.notna(row.get('تاریخ انقضا')) else None,
                        person_subject_code=str(row.get('کدبابت شخص', '')).strip() if pd.notna(row.get('کدبابت شخص')) else None,
                        operation_subject_code=str(row.get('کد بابت عملیات', '')).strip() if pd.notna(row.get('کد بابت عملیات')) else None,
                        invoice_nature_code=str(row.get('کد ماهیت فاکتور', '')).strip() if pd.notna(row.get('کد ماهیت فاکتور')) else None,
                        marketer_code=str(row.get('کد بازاریاب', '')).strip() if pd.notna(row.get('کد بازاریاب')) else None,
                        amount_discount=float(row.get('تخفیف مبلغی', 0)) if pd.notna(row.get('تخفیف مبلغی')) else None,
                        total_tax_percent=float(row.get('درصد مالیات کل', 0)) if pd.notna(row.get('درصد مالیات کل')) else None,
                        total_toll_percent=float(row.get('درصد عوارض کل', 0)) if pd.notna(row.get('درصد عوارض کل')) else None,
                        warehouse_code=str(row.get('کد انبار', '')).strip() if pd.notna(row.get('کد انبار')) else None,
                        warehouse_name=str(row.get('نام انبار', '')).strip() if pd.notna(row.get('نام انبار')) else None,
                        product_code=str(row.get('کد کالا', '')).strip() if pd.notna(row.get('کد کالا')) else None,
                        product_name=str(row.get('نام کالا', '')).strip() if pd.notna(row.get('نام کالا')) else None,
                        item_description=str(row.get('توضیحات', '')).strip() if pd.notna(row.get('توضیحات')) else None,
                        special_coef1=float(row.get('ضریب ویژه 1', 0)) if pd.notna(row.get('ضریب ویژه 1')) else None,
                        special_coef2=float(row.get('ضریب ویژه 2', 0)) if pd.notna(row.get('ضریب ویژه 2')) else None,
                        special_coef3=float(row.get('ضریب ویژه 3', 0)) if pd.notna(row.get('ضریب ویژه 3')) else None,
                        quantity=quantity,
                        secondary_quantity=float(row.get('مقدار (واحد فرعی)', 0)) if pd.notna(row.get('مقدار (واحد فرعی)')) else None,
                        price=price,
                        price_foreign=float(row.get('فی (ارزی)', 0)) if pd.notna(row.get('فی (ارزی)')) else None,
                        discount_percent=float(row.get('درصد/مبلغ تخفیف', 0)) if pd.notna(row.get('درصد/مبلغ تخفیف')) else None,
                        tax_percent=float(row.get('درصد مالیات', 0)) if pd.notna(row.get('درصد مالیات')) else None,
                        toll_percent=float(row.get('درصد عوارض', 0)) if pd.notna(row.get('درصد عوارض')) else None,
                        sending_nature_code=str(row.get('کد ماهیت ارسال', '')).strip() if pd.notna(row.get('کد ماهیت ارسال')) else None,
                        sending_date=str(row.get('تاریخ ارسال', '')).strip() if pd.notna(row.get('تاریخ ارسال')) else None,
                        total_value=total_value
                    )

                    if order.subscription_code:
                        session.add(order)
                        imported_count += 1

                except Exception as e:
                    error_msg = f"Error importing order at row {index + 2}: {str(e)}"
                    self.stats['errors'].append(error_msg)
                    if log_callback:
                        log_callback(f"⚠️ {error_msg}")

            session.commit()
            session.close()

            self.stats['orders_imported'] = imported_count
            if log_callback:
                log_callback(f"✅ Successfully imported {imported_count} orders")

            return imported_count

        except Exception as e:
            error_msg = f"Error reading orders file: {str(e)}"
            self.stats['errors'].append(error_msg)
            if log_callback:
                log_callback(f"❌ {error_msg}")
            return 0

    def import_financials_from_excel(self, file_path, log_callback=None):
        """Import financial records from excel3.xls"""
        if log_callback:
            log_callback(f"Reading financials from: {file_path}")

        try:
            df = pd.read_excel(file_path, sheet_name='Sheet1', engine='xlrd')

            if log_callback:
                log_callback(f"Found {len(df)} rows in financials file")

            session = self.db.get_session()
            imported_count = 0

            for index, row in df.iterrows():
                try:
                    financial = Financial(
                        subscription_code=int(row.get('کد اشتراک ', 0)) if pd.notna(row.get('کد اشتراک ')) else None,
                        amount=float(row.get('مبلغ ', 0)) if pd.notna(row.get('مبلغ ')) else 0.0,
                        loan_code=str(row.get('کد وام ', '')).strip() if pd.notna(row.get('کد وام ')) else None,
                        description=str(row.get('توضیحات ', '')).strip() if pd.notna(row.get('توضیحات ')) else None
                    )

                    if financial.subscription_code:
                        session.add(financial)
                        imported_count += 1

                except Exception as e:
                    error_msg = f"Error importing financial at row {index + 2}: {str(e)}"
                    self.stats['errors'].append(error_msg)
                    if log_callback:
                        log_callback(f"⚠️ {error_msg}")

            session.commit()
            session.close()

            self.stats['financials_imported'] = imported_count
            if log_callback:
                log_callback(f"✅ Successfully imported {imported_count} financial records")

            return imported_count

        except Exception as e:
            error_msg = f"Error reading financials file: {str(e)}"
            self.stats['errors'].append(error_msg)
            if log_callback:
                log_callback(f"❌ {error_msg}")
            return 0

    def import_all_data(self, excel1_path, excel2_path, excel3_path, log_callback=None):
        """Import all data from three Excel files"""
        if log_callback:
            log_callback("=" * 80)
            log_callback("Starting data import process...")
            log_callback("=" * 80)

        # Recreate database
        if log_callback:
            log_callback("Creating database tables...")
        self.db.recreate_database()

        # Import users
        self.import_users_from_excel(excel1_path, log_callback)

        # Import orders
        self.import_orders_from_excel(excel2_path, log_callback)

        # Import financials
        self.import_financials_from_excel(excel3_path, log_callback)

        if log_callback:
            log_callback("=" * 80)
            log_callback("Import Summary:")
            log_callback(f"  Users imported: {self.stats['users_imported']}")
            log_callback(f"  Orders imported: {self.stats['orders_imported']}")
            log_callback(f"  Financials imported: {self.stats['financials_imported']}")
            log_callback(f"  Errors: {len(self.stats['errors'])}")
            log_callback("=" * 80)

        return self.stats

    def get_statistics(self):
        """Get database statistics"""
        from sqlalchemy import func
        session = self.db.get_session()

        try:
            users_count = session.query(User).count()
            orders_count = session.query(Order).count()
            financials_count = session.query(Financial).count()

            # Total amounts
            total_orders_value = session.query(func.sum(Order.total_value)).scalar() or 0
            total_financial_amount = session.query(func.sum(Financial.amount)).scalar() or 0

            return {
                'users_count': users_count,
                'orders_count': orders_count,
                'financials_count': financials_count,
                'total_orders_value': total_orders_value,
                'total_financial_amount': total_financial_amount
            }
        finally:
            session.close()
