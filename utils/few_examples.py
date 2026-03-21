"""
Few-shot examples for SQL generation
These help the LLM learn the pattern
"""

FEW_SHOT_EXAMPLES = [
    {
        "question": "Show all customers",
        "schema": "customers(id, name, email, city)",
        "sql": "SELECT * FROM customers;"
    },
    {
        "question": "Get customers from Mumbai",
        "schema": "customers(id, name, email, city)",
        "sql": "SELECT * FROM customers WHERE city = 'Mumbai';"
    },
    {
        "question": "Count total orders",
        "schema": "orders(id, customer_id, amount, order_date)",
        "sql": "SELECT COUNT(*) FROM orders;"
    },
    {
        "question": "Show customer names with their total order amount",
        "schema": "customers(id, name, email, city), orders(id, customer_id, amount, order_date)",
        "sql": """SELECT c.name, SUM(o.amount) as total_amount 
FROM customers c 
JOIN orders o ON c.id = o.customer_id 
GROUP BY c.id, c.name;"""
    },
    {
        "question": "Get orders from last month",
        "schema": "orders(id, customer_id, amount, order_date)",
        "sql": "SELECT * FROM orders WHERE order_date >= DATE('now', '-1 month');"
    }
]

def format_examples_for_prompt():
    """Format examples for inclusion in prompt"""
    formatted = []
    for example in FEW_SHOT_EXAMPLES:
        formatted.append(f"""
Question: {example['question']}
Schema: {example['schema']}
SQL: {example['sql']}
""")
    return "\n".join(formatted)