# 🏗️ Hopify SaaS DB Generator

This project generates a realistic, benchmark-aware **SaaS customer lifecycle database** for Hopify — a simulated B2B subscription software platform.

Built entirely in Python using `Faker`, `SQLite`, and dynamic logic, it powers downstream SQL analysis modules across churn, retention, acquisition, and revenue metrics.

---

## 📦 What It Does

- ✅ Generates a **fully normalized SQLite database** (`hopify_v15.db`)
- ✅ Simulates customers, products, orders, subscriptions, and churn events
- ✅ Includes **monthly acquisition spikes/dips** to reflect marketing campaigns
- ✅ Integrates **benchmarks** for key SaaS KPIs (e.g., churn, NRR, LTV)
- ✅ Supports **multi-year data modeling** with scaling and decay factors
- ✅ Outputs clean database ready for analysis in SQL, Power BI, or Python

---

## 📁 Project Structure

hopify-saas-db-generator/
├── generate_hopify_v15.py # Main Python script to create database
├── data/
│ └── hopify_v15.db # Output SQLite database
├── benchmarks/
│ └── benchmarks.csv # Target metrics used in SQL analysis
├── visuals/ # Optional ERDs, flowcharts, etc.
├── .gitignore
└── README.md

---

## 🧠 Key Features

| Feature | Description |
|--------|-------------|
| **Segment-aware logic** | Customers are tagged as `SMB`, `Mid-Market`, or `Enterprise` and behave differently |
| **Churn simulation** | Retention decays differently across segments, mirroring SaaS patterns |
| **Marketing effects** | Spikes in acquisition and retention driven by pseudo campaign months |
| **Benchmarks** | A `benchmarks` table aligns SQL KPIs to target metrics for dashboard overlays |

---

## 🛠️ Requirements

- Python 3.8+
- Install dependencies:

```bash
pip install faker python-dateutil

---

## 🚀 Usage
Run the generator script:

bash
Copy code
python generate_hopify_v1.py
This creates:

data/hopify_v1.db → A ready-to-query SQLite database

All schema and table definitions inline with ERD

---

📎 Related Projects
📊 Hopify SQL Analysis
Scenario-based SQL queries for churn, NRR, LTV, CAC, MRR, and benchmark tracking using this dataset.

---

## 📄 License

This project is licensed under the Apache License 2.0.  
You are free to use, modify, and distribute this project under the terms of the license.

See the [LICENSE](LICENSE) file for full details.


