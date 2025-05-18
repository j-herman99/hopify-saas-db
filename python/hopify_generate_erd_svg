
from graphviz import Digraph

# Define the full ERD including all 15 entities with key columns
tables = {
    "customers": ["customer_id (PK)", "name", "email", "signup_date", "customer_segment", "acquisition_source"],
    "subscriptions": ["subscription_id (PK)", "customer_id (FK)", "plan_type", "subscription_price", "start_date", "end_date", "status", "change_type"],
    "orders": ["order_id (PK)", "customer_id (FK)", "order_date", "total_amount"],
    "order_items": ["order_item_id (PK)", "order_id (FK)", "product_id (FK)", "quantity", "subtotal"],
    "payments": ["payment_id (PK)", "customer_id (FK)", "payment_amount", "payment_date", "payment_method", "success"],
    "products": ["product_id (PK)", "name", "category", "price", "revenue_type"],
    "discounts": ["discount_id (PK)", "discount_code", "discount_percent", "start_date", "end_date"],
    "order_discounts": ["order_id (FK)", "discount_id (FK)", "(PK = order_id + discount_id)"],
    "churn_events": ["churn_id (PK)", "customer_id (FK)", "churn_date", "churn_reason"],
    "support_tickets": ["ticket_id (PK)", "customer_id (FK)", "ticket_category", "created_at", "resolved_at"],
    "locations": ["location_id (PK)", "name", "address", "city", "state", "postal_code", "country"],
    "app_installs": ["install_id (PK)", "location_id (FK)", "product_id (FK)", "install_date"],
    "marketing_campaigns": ["campaign_id (PK)", "campaign_name", "channel", "campaign_type", "start_date", "end_date", "total_cost"],
    "web_traffic": ["traffic_id (PK)", "traffic_date", "source_channel", "visitors", "leads", "mqls"],
    "benchmarks": ["benchmark_id (PK)", "metric_category", "segment", "metric_name", "target_value", "description"]
}

# Create a Graphviz Digraph
dot = Digraph(comment="Hopify v1 ERD", format="svg")

# Add nodes for each table
for table, columns in tables.items():
    dot.node(table, label=f"<<TABLE BORDER='1' CELLBORDER='0' CELLSPACING='0'>"
                          f"<TR><TD BGCOLOR='lightgray'><B>{table}</B></TD></TR>" +
                          ''.join(f"<TR><TD>{col}</TD></TR>" for col in columns) +
                          "</TABLE>>", shape='plain')

# Add key relationships
dot.edge("customers", "subscriptions", label="customer_id")
dot.edge("customers", "orders", label="customer_id")
dot.edge("customers", "payments", label="customer_id")
dot.edge("customers", "churn_events", label="customer_id")
dot.edge("customers", "support_tickets", label="customer_id")
dot.edge("orders", "order_items", label="order_id")
dot.edge("order_items", "products", label="product_id")
dot.edge("orders", "order_discounts", label="order_id")
dot.edge("order_discounts", "discounts", label="discount_id")
dot.edge("app_installs", "locations", label="location_id")
dot.edge("app_installs", "products", label="product_id")

# Render to SVG
dot.render("visuals/hopify_v1_erd", format="svg", cleanup=True)
print("[INFO] ERD rendered to visuals/hopify_v1_erd.svg")
