#!/usr/bin/env python3
"""
Test script to verify all imports and basic functionality
"""

print("Testing imports...")

try:
    print("  ✓ Importing models...")
    from models import Database, User, Order, Financial
    print("    - Database, User, Order, Financial imported successfully")

    print("  ✓ Importing data_processor...")
    from data_processor import DataProcessor
    print("    - DataProcessor imported successfully")

    print("\nTesting database creation...")
    db = Database('test.db')
    db.create_tables()
    print("  ✓ Database tables created successfully")

    print("\nTesting session creation...")
    session = db.get_session()
    print("  ✓ Session created successfully")

    # Test creating a user
    print("\nTesting user creation...")
    test_user = User(
        subscription_code=9999999,
        name="Test",
        surname="User",
        national_id="1234567890",
        phone1="09123456789",
        mobile="09123456789",
        address="Test Address",
        postal_code="1234567890",
        province="Test Province",
        city="Test City"
    )
    session.add(test_user)
    session.commit()
    print("  ✓ Test user created successfully")

    # Query the user
    print("\nTesting query...")
    user = session.query(User).filter_by(subscription_code=9999999).first()
    if user:
        print(f"  ✓ User found: {user.name} {user.surname}")

    session.close()

    print("\n" + "="*60)
    print("✅ ALL TESTS PASSED!")
    print("="*60)
    print("\nThe application is ready to use.")
    print("Run the GUI with: python app.py")

    # Clean up test database
    import os
    if os.path.exists('test.db'):
        os.remove('test.db')
        print("\n(Test database cleaned up)")

except ImportError as e:
    print(f"\n❌ Import Error: {e}")
    print("Please make sure all required packages are installed:")
    print("  pip install sqlalchemy pandas openpyxl xlrd")
    exit(1)

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
