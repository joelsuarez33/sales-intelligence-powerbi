import pandas as pd
import numpy as np
from datetime import datetime

# ==========================================
# PROJECT: Sales Intelligence Automation
# AUTHOR: Joel Suarez
# DESCRIPTION: Scalability Layer - Alternative ETL script designed to 
# pre-process high-volume datasets (1M+ rows) before Power BI ingestion.
# ==========================================

def clean_sales_data(file_path):
    # 1. Data Ingestion
    print("Loading dataset...")
    # Supports Excel or CSV. For Big Data, we would switch to parquet/arrow.
    df = pd.read_excel(file_path) 

    # 2. Date Standardization
    # Converting the date column to datetime objects to prevent regional format errors
    # during the import process (crucial for accurate Time Intelligence in DAX).
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # 3. Text Normalization
    # Cleaning whitespace and standardizing capitalization for categorical columns
    # to ensure the "Region" and "Product" filters work correctly in the dashboard.
    text_cols = ['Product Name', 'Customer Name', 'Region']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    # 4. Business Logic & Pre-calculation
    # Calculating Gross Margin at the ETL level reduces the processing load 
    # on the Power BI engine (VertiPaq) during runtime rendering.
    if 'Sales' in df.columns and 'Cost' in df.columns:
        df['Gross_Margin'] = df['Sales'] - df['Cost']
        # Handling potential division by zero is handled by Pandas/NumPy automatically (inf)
        # but rounding ensures clean data for the UI.
        df['Margin_Percentage'] = (df['Gross_Margin'] / df['Sales']).round(2)

    # 5. Handling Missing Values (Null Handling)
    # Filling nulls with 0 for numerical columns to allow aggregation functions (SUM/AVG).
    df.fillna({'Cost': 0, 'Sales': 0}, inplace=True)

    # 6. Export for Visualization
    output_name = 'Clean_Sales_Data_Processed.csv'
    df.to_csv(output_name, index=False)
    print(f"Data successfully processed and exported to: {output_name}")

# Execution Entry Point
if __name__ == "__main__":
    # Context: This script simulates the backend processing.
    # Replace 'Sales_Dataset_Raw.xlsx' with your actual source file name.
    try:
        clean_sales_data('Sales_Dataset_Raw.xlsx')
    except Exception as e:
        print(f"Error: Input file not found. Details: {e}")