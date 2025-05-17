from graphviz import Digraph

dot = Digraph(comment="Hopify v1 ERD")

# Define tables and columns
tables = {
    "customers": ["customer_id (PK)", "name", "signup_date", "customer_segment", "location_id"],
    "subscriptions": ["subscription_id (PK)", "customer_id (FK)", "start_date", "end_date", "plan_name"],
    "orders": ["order_id (PK)", "customer_id (FK)", "order_date", "product_id", "quantity"],
    "products": ["product_id (PK)", "product_name", "price", "category"],
    "churn_events": ["churn_id (PK)", "customer_id (FK)", "churn_date", "reason"],
    "benchmarks": ["metric_category", "segment", "metric_name", "target_value", "description"]
}

# Add nodes (tables)
for table, columns in tables.items():
    dot.node(table, label=f"<<TABLE BORDER='1' CELLBORDER='0' CELLSPACING='0'>"
                          f"<TR><TD BGCOLOR='lightgray'><B>{table}</B></TD></TR>" +
                          ''.join(f"<TR><TD>{col}</TD></TR>" for col in columns) +
                          "</TABLE>>", shape='plain')

# Add relationships
dot.edge("customers", "subscriptions", label="customer_id")
dot.edge("customers", "orders", label="customer_id")
dot.edge("customers", "churn_events", label="customer_id")
dot.edge("orders", "products", label="product_id")

# Render as PNG
dot.render("visuals/hopify_v1_erd", format="png", cleanup=True)

print("[INFO] ERD generated: visuals/hopify_v1_erd.png")
