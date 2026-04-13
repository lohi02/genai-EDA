# GenAI EDA - Exploratory Data Analysis Toolkit

A comprehensive Python toolkit for automated exploratory data analysis (EDA) with multiple visualization and reporting approaches. Perfect for data scientists and analysts who need quick insights into their datasets.

## 🎯 Project Overview

This project generates a realistic sales dataset and provides three powerful ways to explore it:

1. **Automated Report Generation** - Text & HTML analysis reports
2. **Interactive Visualizations** - Sweetviz & custom HTML dashboards
3. **Live Exploration** - D-Tale GUI for real-time data discovery

## 📦 Features

### Data Generation
- **100,000 synthetic transaction records** with realistic patterns
- Multiple product categories and regions
- Missing values (5% in price, 2% in region)
- Date range: 2023-2024
- Reproducible results with numpy seed 42

### Analysis Tools
- **Custom EDA Analysis** - Statistical summaries, correlations, outlier detection
- **HTML Profile Report** - Professional dashboard with charts and statistics
- **Sweetviz Report** - Interactive visualizations with target analysis
- **D-Tale Interactive GUI** - Live data exploration in browser

### Generated Artifacts
```
genai-EDA/
├── sales_data.csv              # Generated dataset (100k rows)
├── eda_analysis.txt            # Statistical analysis report
├── ydata_report.html           # Interactive profile report
├── sweetviz_report.html        # Sweetviz visualizations
├── generate_sales_data.py      # Data generator
├── automated_eda_lite.py       # Report automation
├── create_html_report.py       # HTML report creator
├── dtale_launch.py             # D-Tale launcher
└── README.md                   # Documentation
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python -m venv eda_env

# Activate (Windows PowerShell)
eda_env\Scripts\Activate.ps1

# Activate (Linux/Mac)
source eda_env/bin/activate
```

### 2. Install Dependencies

```bash
pip install pandas>=2.0.0 numpy>=1.24.0 matplotlib>=3.5.0 sweetviz>=2.1.0 dtale>=3.0.0
```

### 3. Generate Sales Dataset

```bash
python generate_sales_data.py
```

**Output:** `sales_data.csv` (100,000 rows)

### 4. Run Automated EDA

```bash
python automated_eda_lite.py
```

**Outputs:**
- `eda_analysis.txt` - Text-based statistical report
- `sweetviz_report.html` - Interactive Sweetviz dashboard

### 5. Generate HTML Profile Report

```bash
python create_html_report.py
```

**Output:** `ydata_report.html` - Beautiful HTML dashboard with charts

### 6. Launch Interactive D-Tale GUI

```bash
python dtale_launch.py
```

Navigate to the URL displayed in terminal (e.g., `http://127.0.0.1:40000`)

## 📊 Dataset Schema

| Column | Type | Description |
|--------|------|-------------|
| transaction_id | int | Unique transaction identifier |
| customer_id | int | Customer identifier |
| product | str | Product name |
| category | str | Product category |
| quantity | int | Items purchased (1-10) |
| price | float | Unit price ($10-$500) |
| revenue | float | Quantity × Price |
| date | datetime | Transaction date (2023-2024) |
| region | str | Geographic region |

**Data Quality:**
- Missing values: 5% in `price`, 2% in `region`
- 5 product categories with 4 products each
- 5 regions: North, South, East, West, Central
- 3,000+ unique customers

## 🛠️ Technologies Used

- **Python 3.10+**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Chart generation
- **sweetviz** - Interactive EDA reports
- **dtale** - Interactive GUI exploration

## 📝 Code Quality

✓ **Best Practices:**
- Comprehensive error handling
- Type hints and docstrings
- Modular function design
- Logging and print statements
- Professional comments

✓ **Reproducibility:**
- Fixed random seed (42)
- Documented dependencies
- Configuration parameters
- Virtual environment setup

## 🎓 Learning Outcomes

This project demonstrates:
- Data generation and validation
- Automated report generation
- Interactive data visualization
- Error handling and logging
- Project organization
- Documentation best practices

## 📄 License

MIT License - Free to use for personal and commercial projects

## 👨‍💻 Author

Data Science Team - April 2026
