import sys
import os

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connections import DatabaseManager
from config import DATABASE_URL

def test_database_manager():
    print("=== Testing DatabaseManager ===\n")
    
    # Initialize
    db_manager = DatabaseManager('sqlite:///my_database.db')
    
    # Test 1: Get table names
    print("1. All Tables:")
    tables = db_manager.get_table_names()
    print(tables)
    print()
    
    # Test 2: Get customers schema
    print("2. Customers Schema:")
    schema = db_manager.get_table_schema('customers')
    print(schema)
    print()
    
    # Test 3: Execute SELECT query
    print("3. Query Results (SELECT * FROM customers):")
    results = db_manager.execute_query("SELECT * FROM customers")
    for row in results:
        print(row)
    print()
    
    # Test 4: Get orders schema
    print("4. Orders Schema:")
    schema = db_manager.get_table_schema('orders')
    print(schema)
    
    # Close
    db_manager.close()
    print("\n=== Tests Completed ===")

if __name__ == "__main__":
    test_database_manager()