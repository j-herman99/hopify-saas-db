
# Standard library
import os
import sqlite3
import random
import csv
import re
from datetime import datetime, timedelta
from collections import defaultdict

# Third-party libraries
from faker import Faker
from dateutil.relativedelta import relativedelta

random.seed(42)
fake = Faker()
fake.seed_instance(42)


# ------------------------------
# Constants and Lookups
# ------------------------------
NUM_CUSTOMERS = 50000
NUM_PRODUCTS_STATIC = 30
NUM_PRODUCTS_DYNAMIC = 50
NUM_PRODUCTS_TOTAL = NUM_PRODUCTS_STATIC + NUM_PRODUCTS_DYNAMIC

PLAN_TYPES = {
    "Starter": 29,
    "Basic": 79,
    "Hopify Standard": 299,
    "Advanced": 399,
    "Plus": 2000
}
CUSTOMER_SEGMENTS = ["SMB", "Mid-Market", "Enterprise"]
TICKET_CATEGORIES = ["Billing", "Technical", "Onboarding", "Account Access", "General Inquiry"]
PAYMENT_METHODS = ["Card", "ACH", "PayPal", "Hop Pay"]
CHURN_REASONS = ["Too expensive", "Switched provider", "Lack of features", "Poor support", "Other"]

OFFICE_LOCATIONS = [
    ("Hopify NYC HQ", "150 Elgin St", "New York City", "NY", "10001", "United States"),
    ("Hopify Canada Hub", "123 King St", "Toronto", "ON", "M5H 1J9", "Canada"),
    ("Hopify Brazil Hub", "50 Paulista Ave", "Sao Paulo", "SP", "01310-100", "Brazil"),
    ("Hopify Germany Hub", "Unter den Linden 1", "Berlin", "BE", "10117", "Germany"),
    ("Hopify Singapore Hub", "1 Raffles Place", "Singapore", "Singapore", "048616", "Singapore")
]

print("[INFO] Database structure and constants initialized.")

# ------------------------------
# B2B Name & Domain Helpers
# ------------------------------
def generate_customer_name(segment):
    if segment == "SMB":
        return fake.name()
    elif segment == "Mid-Market":
        return random.choice([
            f"{fake.first_name()}'s {random.choice(['Studio', 'Shop', 'Solutions'])}",
            fake.company()
        ])
    elif segment == "Enterprise":
        return f"{fake.company()} {random.choice(['Inc.', 'LLC', 'Group', 'Solutions', 'Systems'])}"

def slugify(text):
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")

def generate_store_metadata(name):
    slug = slugify(name)
    domain = f"{slug}.hopify.com"
    return slug, domain

# ------------------------------
# Dynamic Monthly Acquisition Plan (with dips, spikes, and marketing campaigns)
# ------------------------------

acquisition_plan = defaultdict(int)
start_month = datetime.now() - relativedelta(months=36)  # Extend to 3 years for v15
current_month = datetime.now() - relativedelta(months=1)
month_cursor = start_month

while month_cursor <= current_month:
    year_month = month_cursor.strftime('%Y-%m')
    if month_cursor.month in [6, 7, 8]:
        target_customers = random.randint(1200, 1800)
    elif month_cursor.month in [11, 12, 1]:
        target_customers = random.randint(2200, 3000)
    elif month_cursor.month == 4 and random.random() < 0.3:
        target_customers = random.randint(3000, 4000)
    else:
        target_customers = random.randint(1800, 2300)
    acquisition_plan[year_month] = target_customers
    month_cursor += relativedelta(months=1)

print(f"[INFO] Acquisition plan generated for {len(acquisition_plan)} months.")

# ------------------------------
# Connect and Create Schema
# ------------------------------

db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hopify_saas_v1.db')
conn = sqlite3.connect(os.path.abspath(db_path))
cursor = conn.cursor()


cursor.executescript("""
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS subscriptions;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS churn_events;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS app_installs;
DROP TABLE IF EXISTS discounts;
DROP TABLE IF EXISTS order_discounts;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS locations;
DROP TABLE IF EXISTS marketing_campaigns;
DROP TABLE IF EXISTS web_traffic;
DROP TABLE IF EXISTS benchmarks;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    billing_address TEXT,
    shipping_address TEXT,
    signup_date TEXT,
    customer_segment TEXT,
    acquisition_source TEXT,
    store_slug TEXT,
    store_domain TEXT
);

CREATE TABLE subscriptions (
    subscription_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    plan_type TEXT,
    subscription_price REAL,
    start_date TEXT,
    end_date TEXT,
    status TEXT,
    change_type TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    subtotal REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE payments (
    payment_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    payment_amount REAL,
    payment_date TEXT,
    payment_method TEXT,
    success INTEGER,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE marketing_spend (
    segment TEXT,
    month TEXT,
    monthly_budget REAL
);                     

CREATE TABLE churn_events (
    churn_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    churn_date TEXT,
    churn_reason TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE support_tickets (
    ticket_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    ticket_category TEXT,
    created_at TEXT,
    resolved_at TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE app_installs (
    install_id INTEGER PRIMARY KEY,
    location_id INTEGER,
    product_id INTEGER,
    install_date TEXT,
    FOREIGN KEY (location_id) REFERENCES locations(location_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

CREATE TABLE discounts (
    discount_id INTEGER PRIMARY KEY,
    discount_code TEXT,
    discount_percent INTEGER,
    start_date TEXT,
    end_date TEXT
);

CREATE TABLE order_discounts (
    order_id INTEGER,
    discount_id INTEGER,
    PRIMARY KEY (order_id, discount_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (discount_id) REFERENCES discounts(discount_id)
);

CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    name TEXT,
    category TEXT,
    price REAL,
    revenue_type TEXT
);

CREATE TABLE locations (
    location_id INTEGER PRIMARY KEY,
    name TEXT,
    address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    country TEXT
);

CREATE TABLE web_traffic (
    traffic_id INTEGER PRIMARY KEY AUTOINCREMENT,
    traffic_date TEXT,
    source_channel TEXT,
    visitors INTEGER,
    leads INTEGER,
    mqls INTEGER
);

CREATE TABLE benchmarks (
    benchmark_id TEXT PRIMARY KEY,
    metric_category TEXT NOT NULL,
    segment TEXT NOT NULL,
    metric_name TEXT NOT NULL,
    target_value REAL,
    description TEXT,
    target_period TEXT
);

""")

print("[INFO] Database schema created.")


# ------------------------------
# Products (Static and Dynamic)
# ------------------------------
product_id = 1
categories = ['POS Hardware & Software', 'Payments & Finance', 'Financial Services', 'Apps & Integrations',
              'Storefront Tools', 'Marketing & Growth', 'Logistics & Shipping']

# Static products
for i in range(NUM_PRODUCTS_STATIC):
    cursor.execute("""
        INSERT INTO products VALUES (?, ?, ?, ?, ?)
    """, (
        product_id,
        f"Static Product {i+1}",
        random.choice(categories),
        round(random.uniform(20, 500), 2),
        random.choice(["One-Time", "Subscription"])
    ))
    product_id += 1

# Dynamic products
for i in range(NUM_PRODUCTS_DYNAMIC):
    cursor.execute("""
        INSERT INTO products VALUES (?, ?, ?, ?, ?)
    """, (
        product_id,
        fake.catch_phrase(),
        random.choice(categories),
        round(random.uniform(20, 500), 2),
        random.choice(["One-Time", "Subscription"])
    ))
    product_id += 1

print("[INFO] Inserted products.")

# ------------------------------
# Office Locations
# ------------------------------
for i, (name, address, city, state, postal_code, country) in enumerate(OFFICE_LOCATIONS, 1):
    cursor.execute("""
        INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (i, name, address, city, state, postal_code, country))

print("[INFO] Inserted office locations.")

# ------------------------------
# Customer Generation
# ------------------------------
customer_id = 1
customer_list = []
batch_data = []
batch_size = 1000

for year_month, target in acquisition_plan.items():
    month_start = datetime.strptime(year_month + "-01", "%Y-%m-%d")
    month_end = month_start + relativedelta(months=1) - timedelta(days=1)

    for _ in range(target):
        signup_date = fake.date_time_between_dates(month_start, month_end)
        segment = random.choices(CUSTOMER_SEGMENTS, weights=[0.6, 0.3, 0.1])[0]

        # Segment-aware acquisition channel
        if segment == "SMB":
            source = random.choices(
                ["Organic", "Social", "Paid Search", "Referral", "Direct"],
                weights=[0.45, 0.25, 0.20, 0.05, 0.05]
            )[0]
        elif segment == "Mid-Market":
            source = random.choices(
                ["Paid Search", "Referral", "Organic", "Social", "Direct"],
                weights=[0.30, 0.25, 0.20, 0.15, 0.10]
            )[0]
        else:  # Enterprise
            source = random.choices(
                ["Referral", "Paid Search", "Direct", "Organic", "Social"],
                weights=[0.35, 0.30, 0.20, 0.10, 0.05]
            )[0]

        # Generate B2B-style name and domain
        name = generate_customer_name(segment)
        slug, domain = generate_store_metadata(name)

        batch_data.append((
            customer_id,
            name,
            fake.email(),
            fake.address(),
            fake.address(),
            signup_date.strftime("%Y-%m-%d %H:%M:%S"),
            segment,
            source,
            slug,
            domain
        ))

        customer_list.append((customer_id, segment))
        customer_id += 1

        if len(batch_data) >= batch_size:
            cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", batch_data)
            conn.commit()
            batch_data = []

if batch_data:
    cursor.executemany("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", batch_data)
    conn.commit()

print(f"[INFO] Inserted {len(customer_list)} customers.")

# ------------------------------
# Orders, Order Items, Payments
# ------------------------------
order_id = 1
item_id = 1
payment_id = 1

for customer_id, segment in customer_list:
    num_orders = random.randint(1, 3) if segment == 'SMB' else random.randint(2, 4) if segment == 'Mid-Market' else random.randint(3, 6)

    for _ in range(num_orders):
        order_date = fake.date_time_between(start_date='-2y', end_date=datetime.today())
        total = 0.0

        cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", (
            order_id, customer_id, order_date.strftime("%Y-%m-%d %H:%M:%S"), 0.0
        ))

        # Segment-based category preferences
        if segment == 'Enterprise':
            categories = ['POS Hardware & Software', 'Payments & Finance', 'Financial Services', 'Apps & Integrations']
            weights = [0.4, 0.3, 0.2, 0.1]
        elif segment == 'Mid-Market':
            categories = ['Apps & Integrations', 'Storefront Tools', 'Marketing & Growth']
            weights = [0.4, 0.4, 0.2]
        else:
            categories = ['Storefront Tools', 'Marketing & Growth', 'Logistics & Shipping']
            weights = [0.5, 0.3, 0.2]

        for _ in range(random.randint(1, 5)):
            category = random.choices(categories, weights=weights)[0]
            cursor.execute("SELECT product_id, price FROM products WHERE category = ? ORDER BY RANDOM() LIMIT 1", (category,))
            result = cursor.fetchone()
            if result:
                pid, price = result
                qty = random.randint(1, 3)
                subtotal = round(price * qty, 2)
                total += subtotal
                cursor.execute("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", (item_id, order_id, pid, qty, subtotal))
                item_id += 1

        # Update total
        cursor.execute("UPDATE orders SET total_amount = ? WHERE order_id = ?", (round(total, 2), order_id))

        # Payment
        pay_date = fake.date_time_between(start_date=order_date, end_date=datetime.today())
        method = random.choice(PAYMENT_METHODS)
        success = 1 if random.random() > 0.03 else 0
        cursor.execute("INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?)", (
            payment_id, customer_id, round(total, 2), pay_date.strftime("%Y-%m-%d %H:%M:%S"), method, success
        ))

        order_id += 1
        payment_id += 1

print("[INFO] Inserted base orders, items, and payments.")

# ------------------------------
# Expansion Revenue Events
# ------------------------------
segment_expansion_params = {
    "SMB": {"rate": 0.03, "factor_range": (0.05, 0.1)},
    "Mid-Market": {"rate": 0.1, "factor_range": (0.08, 0.15)},
    "Enterprise": {"rate": 0.15, "factor_range": (0.1, 0.2)}
}

exp_order_id = 900000
exp_payment_id = 900000
expansion_count = 0

for customer_id, segment in customer_list:
    params = segment_expansion_params[segment]
    if random.random() < params["rate"]:
        # Select a random base order date
        cursor.execute("SELECT order_date FROM orders WHERE customer_id = ? ORDER BY RANDOM() LIMIT 1", (customer_id,))
        result = cursor.fetchone()
        if not result:
            continue
        base_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")

        # Generate 1–4 monthly expansions
        months = random.randint(1, 4)
        for i in range(months):
            expansion_date = base_date + relativedelta(months=i+1)
            factor = random.uniform(*params["factor_range"])
            revenue = round(random.uniform(100, 1000) * factor, 2)

            cursor.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", (
                exp_order_id, customer_id, expansion_date.strftime("%Y-%m-%d %H:%M:%S"), revenue
            ))
            cursor.execute("INSERT INTO payments VALUES (?, ?, ?, ?, ?, ?)", (
                exp_payment_id, customer_id, revenue, expansion_date.strftime("%Y-%m-%d %H:%M:%S"), "Card", 1
            ))

            exp_order_id += 1
            exp_payment_id += 1
            expansion_count += 1

print(f"[INFO] Simulated {expansion_count} expansion revenue events.")

# ------------------------------
# Subscriptions with Signups and Upgrades
# ------------------------------

cursor.execute("SELECT MAX(subscription_id) FROM subscriptions")
existing_sub_id = cursor.fetchone()[0]
sub_id = existing_sub_id + 1 if existing_sub_id is not None else 1

subscription_data = []

for customer_id, segment in customer_list:
    cursor.execute("SELECT signup_date FROM customers WHERE customer_id = ?", (customer_id,))
    signup_date_str = cursor.fetchone()[0]
    signup_date = datetime.strptime(signup_date_str, "%Y-%m-%d %H:%M:%S")
    
    start_date = fake.date_time_between(start_date=signup_date, end_date=signup_date + relativedelta(months=3))
    duration_months = random.randint(6, 24)
    end_date = start_date + relativedelta(months=duration_months)

    if segment == 'Enterprise':
        plan_type = random.choice(['Pro', 'Enterprise'])
        price = round(random.uniform(300, 800), 2)
    elif segment == 'Mid-Market':
        plan_type = random.choice(['Standard', 'Pro'])
        price = round(random.uniform(100, 300), 2)
    else:
        plan_type = random.choice(['Starter', 'Standard'])
        price = round(random.uniform(30, 100), 2)

    # Insert initial signup subscription
    subscription_data.append((
        sub_id, customer_id, plan_type, price,
        start_date.strftime("%Y-%m-%d %H:%M:%S"),
        end_date.strftime("%Y-%m-%d %H:%M:%S"),
        'active', 'signup'
    ))
    sub_id += 1

    # Simulate upgrades
    upgrade_chance = {"SMB": 0.1, "Mid-Market": 0.2, "Enterprise": 0.3}
    if random.random() < upgrade_chance[segment]:
        upgrade_date = start_date + timedelta(days=random.randint(90, 365))
        if upgrade_date < datetime.today():
            upgrade_price = round(price * random.uniform(1.2, 1.6), 2)
            subscription_data.append((
                sub_id, customer_id, plan_type, upgrade_price,
                upgrade_date.strftime("%Y-%m-%d %H:%M:%S"),
                None, 'active', 'upgrade'
            ))
            sub_id += 1

cursor.executemany("INSERT INTO subscriptions VALUES (?, ?, ?, ?, ?, ?, ?, ?)", subscription_data)
conn.commit()

print(f"[INFO] Inserted {len(subscription_data)} subscriptions including signups and upgrades.")


# ------------------------------
# Support Tickets (Segment-Aware with defensive handling)
# ------------------------------
ticket_id = 1
sample_size = min(20000, len(customer_list))
sampled_customers = random.sample(customer_list, sample_size)

for customer_id, segment in sampled_customers:
    if segment == 'Enterprise':
        num_tickets = random.choices([5, 6, 7, 8, 9, 10], weights=[20, 30, 25, 15, 7, 3])[0]
        resolution_range = (6, 36)
    elif segment == 'Mid-Market':
        num_tickets = random.choices([2, 3, 4, 5, 6], weights=[30, 30, 20, 15, 5])[0]
        resolution_range = (12, 72)
    else:
        num_tickets = random.choices([0, 1, 2, 3], weights=[50, 30, 15, 5])[0]
        resolution_range = (24, 120)

    for _ in range(num_tickets):
        created = fake.date_time_between(start_date='-1y', end_date='-7d')
        resolution_hours = random.randint(*resolution_range)
        resolved = created + timedelta(hours=resolution_hours)

        if resolved <= created:
            resolved = created + timedelta(hours=1)

        category = random.choice(TICKET_CATEGORIES)

        cursor.execute("""
            INSERT INTO support_tickets VALUES (?, ?, ?, ?, ?)
        """, (
            ticket_id,
            customer_id,
            category,
            created.strftime("%Y-%m-%d %H:%M:%S"),
            resolved.strftime("%Y-%m-%d %H:%M:%S")
        ))

        ticket_id += 1

print("[INFO] Inserted support tickets.")

# ------------------------------
# Churn Events (Segment-aware with support friction and decay adjustments)
# ------------------------------
churn_id = 1
cursor.execute("""
    SELECT 
        c.customer_id,
        c.customer_segment,
        c.signup_date,
        COUNT(st.ticket_id) AS total_tickets,
        MIN(st.created_at) AS first_ticket_date,
        AVG(JULIANDAY(st.resolved_at) - JULIANDAY(st.created_at)) AS avg_resolution_days,
        SUM(CASE WHEN st.ticket_category = 'Billing' THEN 1 ELSE 0 END) AS billing_tickets
    FROM customers c
    LEFT JOIN support_tickets st
    ON c.customer_id = st.customer_id
    GROUP BY c.customer_id
""")

churn_candidates = 0
churn_inserted = 0

for row in cursor.fetchall():
    customer_id, segment, signup_date_str, total_tickets, first_ticket_date, avg_resolution_days, billing_tickets = row
    signup_date = datetime.strptime(signup_date_str, "%Y-%m-%d %H:%M:%S")
    days_since_signup = (datetime.today() - signup_date).days

    churn_prob = 0.02 if segment == 'Enterprise' else 0.05 if segment == 'Mid-Market' else 0.12

    if days_since_signup < 90:
        churn_prob *= 0.2
    elif days_since_signup < 180:
        churn_prob *= 0.5

    if total_tickets >= 5:
        churn_prob += 0.15 if segment == 'SMB' else 0.1
    elif 1 <= total_tickets <= 4:
        churn_prob -= 0.05

    if avg_resolution_days and avg_resolution_days > 3:
        churn_prob += 0.05 if segment == 'Enterprise' else 0.1

    if billing_tickets and billing_tickets >= 2:
        churn_prob += 0.15 if segment == 'Enterprise' else 0.1

    if not first_ticket_date:
        first_ticket_delay_days = 999
    else:
        first_ticket_date_obj = datetime.strptime(first_ticket_date, "%Y-%m-%d %H:%M:%S")
        first_ticket_delay_days = (first_ticket_date_obj - signup_date).days

    if first_ticket_delay_days > 90:
        churn_prob += 0.1 if segment == 'SMB' else 0.05

    churn_prob = min(churn_prob, 0.9)

    if random.random() < churn_prob:
        min_lifetime_days = 30 if segment == 'SMB' else 60 if segment == 'Mid-Market' else 120
        if datetime.today() >= signup_date + timedelta(days=min_lifetime_days):
            churn_candidates += 1
            churn_date = fake.date_time_between(
                start_date=signup_date + timedelta(days=min_lifetime_days),
                end_date=datetime.today()
            ).strftime("%Y-%m-%d %H:%M:%S")

            cursor.execute("INSERT INTO churn_events VALUES (?, ?, ?, ?)", (
                churn_id, customer_id, churn_date, random.choice(["Too expensive", "Switched provider", "Lack of features", "Poor support", "Other"])
            ))
            churn_inserted += 1
            churn_id += 1

        if random.random() < 0.1:  # 10% chance to reactivate
            reactivation_date = datetime.strptime(churn_date, "%Y-%m-%d %H:%M:%S") + timedelta(days=random.randint(30, 120))
            cursor.execute("""
                INSERT INTO subscriptions (subscription_id, customer_id, plan_type, subscription_price, start_date, end_date, status, change_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sub_id, customer_id, "Hopify Standard", 299,
                reactivation_date.strftime("%Y-%m-%d %H:%M:%S"), None, "Active", "Reactivation"
            ))
            sub_id += 1

print(f"[INFO] Churn eligible: {churn_candidates}, Churn inserted: {churn_inserted}")


# ------------------------------
# Simulated Reactivations after Churn (Segment-aware)
# ------------------------------

# Continue sub_id from previous context
cursor.execute("SELECT MAX(subscription_id) FROM subscriptions")
existing_sub_id = cursor.fetchone()[0]
sub_id = existing_sub_id + 1 if existing_sub_id is not None else 1

cursor.execute("SELECT customer_id, churn_date FROM churn_events")
churned_customers = cursor.fetchall()

reactivation_count = 0

for customer_id, churn_date_str in churned_customers:
    churn_date = datetime.strptime(churn_date_str, "%Y-%m-%d %H:%M:%S")

    # 10–20% chance of reactivation depending on segment
    cursor.execute("SELECT customer_segment FROM customers WHERE customer_id = ?", (customer_id,))
    segment = cursor.fetchone()[0]
    reactivation_chance = {"SMB": 0.05, "Mid-Market": 0.1, "Enterprise": 0.2}

    if random.random() < reactivation_chance[segment]:
        reactivation_date = churn_date + timedelta(days=random.randint(30, 180))
        if reactivation_date < datetime.today():
            # Assign a reactivation plan — slightly higher pricing than original
            if segment == 'Enterprise':
                plan_type = random.choice(['Pro', 'Enterprise'])
                price = round(random.uniform(350, 900), 2)
            elif segment == 'Mid-Market':
                plan_type = random.choice(['Standard', 'Pro'])
                price = round(random.uniform(120, 350), 2)
            else:
                plan_type = random.choice(['Starter', 'Standard'])
                price = round(random.uniform(40, 120), 2)

            cursor.execute("""
                INSERT INTO subscriptions (
                    subscription_id, customer_id, plan_type,
                    subscription_price, start_date, end_date,
                    status, change_type
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                sub_id, customer_id, plan_type, price,
                reactivation_date.strftime("%Y-%m-%d %H:%M:%S"),
                None, 'active', 'reactivation'
            ))
            sub_id += 1
            reactivation_count += 1

print(f"[INFO] Reactivated {reactivation_count} churned customers.")


# ------------------------------
# App Installs per Location (Defensive Handling)
# ------------------------------

# Get current max install_id to avoid conflicts
cursor.execute("SELECT MAX(install_id) FROM app_installs")
existing_max_install_id = cursor.fetchone()[0]
install_id = existing_max_install_id + 1 if existing_max_install_id is not None else 1

for location_id in range(1, len(OFFICE_LOCATIONS) + 1):
    for _ in range(random.randint(5, 12)):
        pid = random.randint(1, NUM_PRODUCTS_TOTAL)
        install_date = fake.date_time_between(start_date='-1y', end_date=datetime.today())
        cursor.execute("INSERT INTO app_installs VALUES (?, ?, ?, ?)", (
            install_id, location_id, pid, install_date.strftime("%Y-%m-%d %H:%M:%S")
        ))
        install_id += 1

print("[INFO] Inserted app installs.")

# ------------------------------
# Discounts and Order Discounts (with defensive uniqueness)
# ------------------------------

# Ensure discount_id continues from the current max
cursor.execute("SELECT MAX(discount_id) FROM discounts")
existing_max = cursor.fetchone()[0]
start_id = existing_max + 1 if existing_max else 1

# Insert 50 new discount codes
for i in range(start_id, start_id + 50):
    code = f"SALE{i:02d}"
    percent = random.choice([5, 10, 15, 20, 25, 30])
    start = fake.date_time_between(start_date='-1y', end_date='-30d')
    end = start + timedelta(days=random.randint(7, 90))
    cursor.execute("INSERT INTO discounts VALUES (?, ?, ?, ?, ?)", (
        i, code, percent,
        start.strftime("%Y-%m-%d %H:%M:%S"),
        end.strftime("%Y-%m-%d %H:%M:%S")
    ))

# Apply discounts to unique orders, avoiding duplicate (order_id, discount_id) pairs
used_pairs = set()
cursor.execute("SELECT order_id FROM orders ORDER BY RANDOM() LIMIT 20000")
for row in cursor.fetchall():
    order_id = row[0]
    tries = 0
    while tries < 10:
        discount_id = random.randint(start_id, start_id + 49)
        if (order_id, discount_id) not in used_pairs:
            cursor.execute("INSERT INTO order_discounts VALUES (?, ?)", (order_id, discount_id))
            used_pairs.add((order_id, discount_id))
            break
        tries += 1  # Retry with a different discount

print("[INFO] Inserted discounts and applied to orders.")

# ------------------------------
# Marketing Spend Table
# ------------------------------

marketing_spend_data = []
segment_spend_ranges = {
    "SMB": (10000, 25000),
    "Mid-Market": (50000, 80000),
    "Enterprise": (100000, 150000)
}

month_cursor = datetime.now() - relativedelta(months=36)
end_month = datetime.now() - relativedelta(months=1)

while month_cursor <= end_month:
    month_str = month_cursor.strftime('%Y-%m')
    for segment in CUSTOMER_SEGMENTS:
        min_spend, max_spend = segment_spend_ranges[segment]
        variation = random.uniform(-0.1, 0.1)  # simulate 10% monthly budget fluctuation
        avg_spend = (min_spend + max_spend) / 2
        monthly_budget = round(avg_spend * (1 + variation), 2)
        marketing_spend_data.append((segment, month_str, monthly_budget))
    month_cursor += relativedelta(months=1)

cursor.executemany("""
    INSERT INTO marketing_spend (segment, month, monthly_budget)
    VALUES (?, ?, ?)
""", marketing_spend_data)

print(f"[INFO] Inserted {len(marketing_spend_data)} rows of marketing spend data with dynamic variation.")

# ------------------------------
# Web Traffic Data (Safe Refresh)
# ------------------------------

cursor.execute("DELETE FROM web_traffic")

channels = ['Paid Search', 'Social Media', 'Organic']
months = [datetime.now() - relativedelta(months=i) for i in range(0, 24)]

for month in months:
    for channel in channels:
        visitors = random.randint(10000, 30000) if channel != 'Organic' else random.randint(50000, 100000)
        leads = int(visitors * random.uniform(0.02, 0.05))
        mqls = int(leads * random.uniform(0.2, 0.4))
        cursor.execute("""
            INSERT INTO web_traffic (traffic_date, source_channel, visitors, leads, mqls)
            VALUES (?, ?, ?, ?, ?)
        """, (month.strftime("%Y-%m"), channel, visitors, leads, mqls))

print("[INFO] Sample web traffic data inserted (table cleared before insert).")

# ------------------------------
# Replace Benchmarks from CSV
# ------------------------------
benchmarks_csv_path = os.path.join(
    os.path.dirname(__file__), '..', 'benchmarks', 'hopify-benchmarks-seg-table.csv'
)
print(f"[INFO] Benchmarks CSV path set to: {benchmarks_csv_path}")

# Delete all existing benchmarks
cursor.execute("DELETE FROM benchmarks")

# Load and insert new benchmarks
rows = []
with open(benchmarks_csv_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')

    for i, row in enumerate(reader):
        try:
            # Skip rows with missing required fields
            if not row["benchmark_id"] or not row["metric_name"] or not row["target_value"]:
                print(f"[SKIP] Row {i + 1} missing required fields: {row}")
                continue

            parsed_row = (
                row["benchmark_id"].strip(),
                row["metric_category"].strip(),
                row["segment"].strip(),
                row["metric_name"].strip(),
                float(row["target_value"]),
                row["description"].strip(),
                row["target_period"].strip()
            )
            rows.append(parsed_row)

        except Exception as e:
            print(f"[ERROR] Row {i + 1} failed: {row}")
            print(f"        Error: {e}")

# Insert cleaned rows into benchmarks table
cursor.executemany("""
    INSERT INTO benchmarks (
        benchmark_id,
        metric_category,
        segment,
        metric_name,
        target_value,
        description,
        target_period
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
""", rows)

print(f"[INFO] Benchmarks replaced from CSV. Rows inserted: {len(rows)}")


# ------------------------------
# Finalize and Close Connection
# ------------------------------
conn.commit()
conn.close()

print("\n🎉 Hopify v15 (SaaS Full Lifecycle Dataset) created successfully! 🎉")
print("✅ Includes:")
print("- Dynamic multi-year historical data")
print("- Segment-aware subscriptions, churn, support, payments")
print("- Orders and product category skew by segment")
print("- Marketing campaigns, web traffic, lead conversions")
print("- Benchmarks for key SaaS and Marketing metrics")
print("- Full event timestamping and behavioral modeling")
print("- Cross-sell, upsell, support impact on churn, and more")
print("\n[INFO] All data has been committed and the connection has been closed.")