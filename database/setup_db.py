import sqlite3

def setup_database():
    conn=sqlite3.connect('my_database.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT,city TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer_id INTEGER, product TEXT, amount REAL, FOREIGN KEY(customer_id) REFERENCES customers(id))")
    cur.execute("INSERT INTO customers (name, email, city) VALUES ('John Doe', 'john.doe@example.com', 'New York'), ('Jane Smith', 'jane.smith@example.com', 'Los Angeles'), ('Alice Johnson', 'alice.johnson@example.com', 'Chicago'), ('Bob Brown', 'bob.brown@example.com', 'Houston')")
    cur.execute("INSERT INTO orders (customer_id, product, amount) VALUES (1, 'Laptop', 999.99), (1, 'Mouse', 25.50), (2, 'Smartphone', 499.99), (3, 'Headphones', 199.99), (4, 'Monitor', 299.99)")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
    print("Sample database created!")    