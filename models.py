"""
Database models using SQLAlchemy ORM
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class User(Base):
    """User/Customer table"""
    __tablename__ = 'users'

    subscription_code = Column(BigInteger, primary_key=True, comment='کد اشتراک')
    name = Column(String(100), comment='نام')
    surname = Column(String(100), comment='نام خانوادگی')
    father_name = Column(String(100), nullable=True, comment='نام پدر')
    certificate_number = Column(String(50), nullable=True, comment='شماره شناسنامه')
    national_id = Column(String(10), comment='کد ملی/شناسه ملی')
    second_name = Column(String(100), nullable=True, comment='نام دوم (چاپی)')
    phone1 = Column(String(20), comment='تلفن 1')
    phone2 = Column(String(20), nullable=True, comment='تلفن 2')
    phone3 = Column(String(20), nullable=True, comment='تلفن 3')
    mobile = Column(String(20), comment='موبایل')
    fax = Column(String(20), nullable=True, comment='نمابر')
    economic_code = Column(String(50), nullable=True, comment='کد اقتصادی')
    address = Column(String(500), comment='آدرس')
    postal_code = Column(String(10), comment='کد پستی')
    email = Column(String(100), nullable=True, comment='ایمیل')
    province = Column(String(100), comment='استان')
    city = Column(String(100), comment='شهرستان')

    # Relationships
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')
    financials = relationship('Financial', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<User(code={self.subscription_code}, name={self.name} {self.surname})>"


class Order(Base):
    """Order/Invoice table"""
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(String(50), comment='شناسه فاکتور')
    invoice_date = Column(String(20), comment='تاریخ فاکتور')
    subscription_code = Column(BigInteger, ForeignKey('users.subscription_code'), comment='کد اشتراک')
    person_name = Column(String(200), nullable=True, comment='نام شخص')
    description = Column(String(500), nullable=True, comment='توضیحات')
    settlement_type = Column(String(50), nullable=True, comment='نوع تسویه')
    settlement_date = Column(String(20), comment='تاریخ تسویه')
    expiry_date = Column(String(20), comment='تاریخ انقضا')
    person_subject_code = Column(String(50), nullable=True, comment='کدبابت شخص')
    operation_subject_code = Column(String(50), nullable=True, comment='کد بابت عملیات')
    invoice_nature_code = Column(String(50), nullable=True, comment='کد ماهیت فاکتور')
    marketer_code = Column(String(50), nullable=True, comment='کد بازاریاب')
    amount_discount = Column(Float, nullable=True, comment='تخفیف مبلغی')
    total_tax_percent = Column(Float, nullable=True, comment='درصد مالیات کل')
    total_toll_percent = Column(Float, nullable=True, comment='درصد عوارض کل')
    warehouse_code = Column(String(50), comment='کد انبار')
    warehouse_name = Column(String(200), nullable=True, comment='نام انبار')
    product_code = Column(String(50), comment='کد کالا')
    product_name = Column(String(300), nullable=True, comment='نام کالا')
    item_description = Column(String(500), nullable=True, comment='توضیحات کالا')
    special_coef1 = Column(Float, nullable=True, comment='ضریب ویژه 1')
    special_coef2 = Column(Float, nullable=True, comment='ضریب ویژه 2')
    special_coef3 = Column(Float, nullable=True, comment='ضریب ویژه 3')
    quantity = Column(Integer, comment='تعداد (واحد اصلی)')
    secondary_quantity = Column(Float, nullable=True, comment='مقدار (واحد فرعی)')
    price = Column(Float, comment='فی')
    price_foreign = Column(Float, nullable=True, comment='فی (ارزی)')
    discount_percent = Column(Float, nullable=True, comment='درصد/مبلغ تخفیف')
    tax_percent = Column(Float, nullable=True, comment='درصد مالیات')
    toll_percent = Column(Float, nullable=True, comment='درصد عوارض')
    sending_nature_code = Column(String(50), comment='کد ماهیت ارسال')
    sending_date = Column(String(20), comment='تاریخ ارسال')
    total_value = Column(Float, comment='ارزش کل (فی × تعداد)')

    # Relationships
    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order(id={self.id}, invoice={self.invoice_id}, subscription={self.subscription_code})>"


class Financial(Base):
    """Financial/Loan table"""
    __tablename__ = 'financials'

    id = Column(Integer, primary_key=True, autoincrement=True)
    subscription_code = Column(BigInteger, ForeignKey('users.subscription_code'), comment='کد اشتراک')
    amount = Column(Float, comment='مبلغ')
    loan_code = Column(String(50), comment='کد وام')
    description = Column(String(500), nullable=True, comment='توضیحات')

    # Relationships
    user = relationship('User', back_populates='financials')

    def __repr__(self):
        return f"<Financial(id={self.id}, subscription={self.subscription_code}, amount={self.amount})>"


class Database:
    """Database manager class"""

    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """Drop all tables"""
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        """Get a new session"""
        return self.Session()

    def recreate_database(self):
        """Drop and recreate all tables"""
        self.drop_tables()
        self.create_tables()
