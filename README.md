# 🏗️ Hopify SaaS DB Generator

> **Version:** `v1.0`  
> 🗓️ Released: May 2025

This project generates a realistic, benchmark-aware **SaaS customer lifecycle database** for Hopify — a simulated B2B subscription software platform.

Built in Python using `Faker`, `SQLite`, and scalable logic, this generator produces a clean dataset to support business analysis across churn, retention, revenue, marketing, and customer lifecycle KPIs.

---

## 📦 What It Does

- ✅ Generates a **fully normalized SQLite database** (`hopify_saas_v1.db`)
- ✅ Simulates customer acquisition, product subscriptions, support, churn, and retention behavior
- ✅ Models **monthly acquisition spikes/dips** to reflect campaigns
- ✅ Embeds **segment-specific benchmarks** for KPI tracking
- ✅ Supports multi-year simulation with decay logic for churn, revenue, and LTV

---

## 📁 Project Structure

hopify-saas-db-generator/
├── hopify_db_v1_gen.py ✅ Main generator script
├── benchmarks/
│ └── hopify_kpi_benchmarks.csv ✅ Embedded benchmark KPIs
├── data/
│ └── hopify_saas_v1.db ✅ SQLite database output
├── visuals/
│ ├── hopify_v1_erd.png     ✅ ERD from DBeaver
│ ├── hopify_cust_lifecycle_flow.png
│ ├── hopify_cust_lifecycle_flow.svg
│ └── hopify_benchmark_kpi_matrix.png
├── python/
│ ├── hopify_cust_lifecycle_flow_gen.py
│ └── hopify_benchmark_kpi_matrix_gen.py
├── README.md
├── LICENSE
└── .gitignore


---

## 🧠 Key Features

| Feature | Description |
|--------|-------------|
| **Segment-aware modeling** | Customers are tagged as `SMB`, `Mid-Market`, or `Enterprise` and behave differently |
| **Retention & churn simulation** | Behavior decays based on segment and time since signup |
| **Benchmarks table** | KPI targets (e.g., churn %, NRR, ARPU) are embedded for downstream SQL analysis |
| **Monthly scaling logic** | Each cohort and behavior scales over time and seasonality |

---

## 🛠️ Requirements

- Python 3.8+
- Dependencies:

```bash
pip install faker python-dateutil

---

## 🚀 Usage
Run the generator from the project root:

bash
Copy code
python hopify_db_v1_gen.py
This creates:

data/hopify_saas_v1.db → A ready-to-query SQLite database

Tables: customers, subscriptions, orders, products, churn_events, benchmarks

---

## 📎 Related Projects
📊 Hopify SQL Analysis
Scenario-based SQL queries for churn, NRR, LTV, CAC, MRR, and benchmark tracking using this dataset.

---

## 📄 License
This project is licensed under the Apache License 2.0.
You are free to use, modify, and distribute this project under the terms of the license.

See the LICENSE file for full details.

---

