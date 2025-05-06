# Data Merge & Insight Tool

A lightweight web app to upload, merge, and explore multiple datasets interactively.

## Features

- Upload multiple CSV or Excel files at once
- Select any two datasets to merge on a user-specified column
- View summary insights and key metrics:
  - Total/unique/duplicate keys in each dataset
  - Matched/unmatched rows and match rate
  - Top values in the join column
  - Distribution of numeric columns
  - Missing value counts
- Explore merged data with filtering by any column
- Global search across all columns and rows
- Quick, interactive visualizations

## Getting Started

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Upload two or more datasets (CSV or Excel).
2. Enter the name of the common column to join on.
3. Select which two datasets to merge.
4. Explore summary insights, filter data, or search globally.

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies (Streamlit, pandas, etc.)
