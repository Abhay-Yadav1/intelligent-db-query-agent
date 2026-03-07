import sqlite3

def test_db_conn():
    try:
        conn=sqlite3.connect('my_database.db')
        print("Database connection successful!")
        cur=conn.cursor()
        cur.execute("SELECT * FROM orders")
        orders=cur.fetchall()
        print("Orders in the database:")
        for order in orders:
            print(order)
    except sqlite3.Error as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    test_db_conn()
