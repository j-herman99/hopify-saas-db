# 🎨 Visuals

This folder contains graphical outputs used for documentation, presentations, and data storytelling throughout the Hopify v1 project.

Visuals represent the simulated SaaS environment, including the database schema, customer lifecycle flow, and benchmark KPI matrix.

---

## 📁 Visual Descriptions

| File | Format(s) | Purpose |
|------|-----------|---------|
| `hopify_v1_erd.(pdf/png/svg)` | PDF, PNG, SVG | Entity-Relationship Diagram showing all 15 tables and foreign key relationships. SVG generated via Python; PDF/PNG exported from DBeaver. |
| `hopify_cust_lifecycle_flow.(png/svg)` | PNG, SVG | Visualizes the Hopify customer journey from acquisition to churn or retention. Built with Graphviz for integration into presentations and documentation. |
| `hopify_benchmark_kpi_matrix.png` | PNG | Heatmap of benchmark KPI coverage by segment and category. Useful for identifying analytical gaps and prioritizing metrics.

---

## ⚙️ How to Regenerate Visuals

Visuals are generated using scripts located in the [`/python/`](../python/) folder:

| Script | Output |
|--------|--------|
| `hopify_generate_erd_svg.py` | Full ERD as SVG using Graphviz (includes all 15 tables) |
| `hopify_cust_lifecycle_flow_gen.py` | Customer lifecycle flowchart (SVG/PNG) |
| `hopify_benchmark_kpi_matrix_gen.py` | Benchmark matrix heatmap (PNG)

> The ERD can also be generated visually using DBeaver (export as PDF/PNG), or code-only via `hopify_generate_erd_svg.py`.

---

**Tip:** SVGs are ideal for embedding in Notion, slide decks, or responsive documentation due to their scalability and clarity.

---
