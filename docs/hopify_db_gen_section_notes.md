# 🧪 Hopify DB Generator – Section Purpose & Role Notes

This document, located in the `/docs/` folder, outlines each major section of the `hopify_db_v1_gen.py` script, explaining its role in building a realistic, segment-aware SaaS dataset for analysis.

---

## 🐍 Import Python Libraries – Purpose & Role

This section loads all essential Python libraries used to build the Hopify v15 synthetic SaaS database:

- **`Faker`**: Generates realistic synthetic data including names, emails, addresses, and product descriptions.
- **`sqlite3`**: Manages creation and population of the local SQLite database, handling schema setup and inserts.
- **`random`**: Introduces controlled randomness to simulate real-world variability in customer behavior, purchases, and support events.
- **`datetime`, `timedelta`**: Used for timestamping events, simulating historical activity, and calculating durations.
- **`relativedelta`** (from `dateutil`): Allows for clean monthly offsets (e.g., 36 months back) when generating time-based trends.
- **`defaultdict`** (from `collections`): Enables dynamic construction of the Monthly Acquisition Plan without requiring manual initialization for each month.

---

## ⚙️ Constants and Lookups – Purpose & Role

Defines fixed reference values used throughout the dataset generation process:

- Customer volumes, product counts
- Plan pricing (`PLAN_TYPES`) and segments (`CUSTOMER_SEGMENTS`)
- Support categories, payment methods, churn reasons
- Global office locations for regional modeling

---

## 📈 Dynamic Monthly Acquisition Plan – Purpose & Role

Generates a month-by-month acquisition plan over 3 years:

- Includes seasonal spikes (holiday campaigns), dips (summer), and random campaign boosts
- Stored in a `defaultdict` for ease of access during customer generation
- Drives customer volume and acquisition source attribution

---

## 🗂️ Connect and Create Schema – Purpose & Role

Initializes the SQLite database and defines all tables:

- Drops old tables to ensure clean rebuild
- Creates all core, join, and reference tables with foreign key relationships
- Foundation for structured relational dataset

---

## 🛒 Products (Static and Dynamic) – Purpose & Role

Populates the `products` table with realistic offerings:

- Mix of static labeled and dynamically generated names
- Varies categories and revenue types (One-Time vs. Subscription)
- Supports segment-driven purchasing patterns

---

## 🏢 Office Locations – Purpose & Role

Creates `locations` table using predefined global office hubs:

- Includes city, region, and country info
- Anchors app install activity to real-world geographies

---

## 👥 Customers Based on Plan

Generates customer records monthly based on the acquisition plan:

- Assigns realistic signup dates and acquisition sources
- Segments customers by plan type (SMB, Mid-Market, Enterprise)
- Stored in `customers_list` for use in later stages

---

## 📄 Subscriptions (including history)

Builds subscription histories for each customer:

- Includes multiple plan changes (upgrades/reactivations)
- Uses segment-based plan sequences and churn probabilities
- Captures lifecycle states: active or cancelled

---

## 💳 Orders, Order Items, and Payments

Simulates transactions tied to customers:

- Orders linked to product categories by segment
- Payments include method and success/failure rates
- Supports ARPU, revenue, and monetization analysis

---

## 🎟️ Support Tickets

Models customer support volume and resolution:

- Ticket counts, categories, and resolution time vary by segment
- Resolution speed and volume used later in churn scoring
- Reflects support load and SLA quality

---

## 🔻 Churn Events

Scores customers for churn using behavioral logic:

- Baseline churn by segment + decay adjustments by tenure
- SQL pre-aggregation of support metrics
- Adds churn dates and categorized reasons

---

## 🧩 App Installs per Location

Simulates product deployments across office locations:

- Links products to locations and tracks install dates
- Enables geographic product usage insights

---

## 💸 Discounts and Order Discounts

Adds promotional behavior to revenue model:

- Generates unique discount codes and date ranges
- Applies to random orders through join table
- Enables discount impact analysis

---

## 📢 Marketing Campaigns

Populates major campaign events:

- Includes spend, duration, channel, and type
- Aligns with acquisition source logic and traffic spikes

---

## 🌐 Web Traffic Data

Generates monthly traffic volume per channel:

- Tracks visitors → leads → MQLs over 24 months
- Aligns with paid and organic campaigns
- Foundation for funnel analysis

---

## 🎯 Benchmarks

Loads KPI benchmark values from a CSV file:

- Includes Revenue, Customer, Support, and Marketing metrics
- Fields include `segment`, `metric_name`, `target_value`, and `target_period` (monthly, annual, or lifetime)
- Enables comparisons of actual vs. target across segments using predefined targets for each KPI and time period
- Enhances executive reporting and dashboards

---

## ✅ Finalize and Close Connection

Commits and closes the SQLite connection:

- Ensures all data is written to disk
- Prints success summary of dataset scope
- Marks successful completion of the Hopify v15 database generation process

---
