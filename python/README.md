
# 🐍 Visual Generation Scripts

This folder contains Python scripts that generate structural and analytical visuals for the Hopify DB Generator project. All scripts should be run from the project root (`hopify-saas-db-generator/`).

---

## 📜 Scripts & Outputs

| Script                               | Description / Output Visual                                |
|--------------------------------------|-------------------------------------------------------------|
| `hopify_cust_lifecycle_flow_gen.py`  | Customer lifecycle flowchart (Graphviz PNG/SVG)            |
| `hopify_benchmark_kpi_matrix_gen.py` | Heatmap of benchmark KPI coverage (Matplotlib PNG)         |
| `hopify_generate_erd_svg.py`         | Full ERD with all 15 entities rendered as SVG              |

---

## 🛠️ Requirements

These scripts require:

- Python 3.x  
- `graphviz` for ERD and flow diagrams  
- `matplotlib` for benchmark matrix visual

Install dependencies using:

```bash
pip install graphviz matplotlib
```

Make sure you also have [Graphviz](https://graphviz.org/download/) installed on your system for rendering visuals.

---

## 📁 Output Directory

All generated visuals are saved to the `/visuals/` directory. These assets are referenced in the main project `README.md`.

---
