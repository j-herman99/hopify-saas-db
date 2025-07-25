# 🧪 Hopify SaaS DB Generator

![Built With: Python](https://img.shields.io/badge/Built%20With-Python-06b6d4?style=flat&labelColor=333&logo=python&logoColor=white)
![Status: Stable](https://img.shields.io/badge/Status-Stable-facc15?style=flat&labelColor=333)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-f59e0b?style=flat&labelColor=333)
![Use Case: SaaS KPI Analysis](https://img.shields.io/badge/Use%20Case-SaaS%20KPI%20Analysis-14b8a6?style=flat&labelColor=333)
![Data Type: Synthetic B2B SaaS](https://img.shields.io/badge/Data%20Type-Synthetic%20B2B%20SaaS-7dd3fc?style=flat&labelColor=333)
![Benchmarked: Industry Metrics](https://img.shields.io/badge/Benchmarked-Industry%20Metrics-6366f1?style=flat&labelColor=333)
![Schema: ERD Included](https://img.shields.io/badge/Schema-ERD%20Included-9333ea?style=flat&labelColor=333)


_This project simulates a realistic B2B SaaS company dataset inspired by platforms like Shopify. It generates synthetic customer, revenue, churn, and support data to support KPI analysis across customer lifecycle stages._

The database is designed to reflect real-world SaaS performance metrics (e.g., CAC, LTV, GRR, NRR, Churn Rate), supporting financial analysis, customer segmentation, and lifecycle modeling.

---

## 📂 Project Structure

| Folder | Description |
|--------|-------------|
| [`01_project_artifacts`](./01_project_artifacts) | Benchmarks and ERD diagrams used to guide database structure and performance assumptions. |
| └── [`01_benchmarks`](./01_project_artifacts/01_benchmarks) | Industry metrics used for segmentation and KPI calibration. |
| └── [`02_hopify_erd_source_files`](./01_project_artifacts/02_erd_source_files) | ERD (.png and DBeaver .sql/.pdf) for data schema visualization. |
| [`02_documentation`](./02_documentation) | Dataset overview and annotated Python section notes. |
| [`03_data`](./03_data) | Final generated SQLite database (`.zip`) for use in Tableau, Power BI, or SQL analysis. |
| [`04_code`](./04_code) | Python script to generate the full multi-year Hopify dataset. |
| Files | `requirements.txt`, `.gitignore`, `LICENSE` |

---

## 📘 Key Documentation

- 📄 [Dataset Overview](./02_documentation/hopify_db_dataset_overview.md)  
- 🧠 [Code Block Annotations](./02_documentation/hopify_db_gen_section_notes.md)  
- 🧮 [Benchmarks Reference Table](./01_project_artifacts/01_benchmarks/hopify_benchmarks_seg_table.csv)  
- 🗺️ [ERD Diagram](./01_project_artifacts/02_erd_source_files/hopify_v1_erd_dbeaver.png)

---

## 🔧 How to Use

1. Clone this repo and install dependencies:
   ```bash
   pip install -r requirements.txt


---

## 📘 Key Documentation

- 📄 [Dataset Overview](./02_documentation/hopify_db_dataset_overview.md)  
- 🧠 [Code Block Annotations](./02_documentation/hopify_db_gen_section_notes.md)  
- 🧮 [Benchmarks Reference Table](./01_project_artifacts/benchmarks/hopify-benchmarks-seg-table.csv)  
- 🗺️ [ERD Diagram](./01_project_artifacts/erd/hopify_v1_erd_dbeaver.png)

---

## 🔧 How to Use

1. Clone this repo and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the generator:
   ```bash
   python 04_code/hopify_db_v1_gen.py
   ```

3. The generated SQLite database will be available under `03_data/`.

---

## 🚀 Future Plans

- Add support for Postgres and BigQuery export
- Generate dashboard-ready views with KPI aggregations
- Publish on Kaggle with SQL challenge prompts

---
