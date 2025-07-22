# 📊 Benchmarks Folder

This folder contains the KPI benchmark targets used by the `hopify_db_v1_gen.py` script during database generation.

### 🧩 File Included

- `hopify-benchmarks-seg-table.csv`  
  Contains simulated target values for key SaaS KPIs across customer segments (`SMB`, `Mid-Market`, `Enterprise`).

### 📌 Key Metrics Tracked

Benchmarks include:
- Monthly Churn Rate %
- Gross Revenue Retention (GRR)
- Net Revenue Retention (NRR)
- CAC Payback Period
- Avg Resolution Time (Support)
- ARPU Targets

### ⚙️ How It's Used

The Python script directly loads this CSV to:
- Assign realistic performance goals per segment
- Enable KPI comparisons in downstream analysis
- Drive segment-aware logic in churn, pricing, and support modeling

> 📎 Do not rename or restructure the CSV without updating the script accordingly.
