"""
Sales Dataset Generator for EDA Practice
=========================================
This script creates a sample sales dataset with realistic features including:
- 100,000 transaction records
- Multiple product categories and regions
- Missing values (5% in price, 2% in region)
- Date range from 2023 to 2024
- Reproducible results using numpy seed 42

Author: Data Science Team
Date: 2024
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys

# Set random seed for reproducibility
np.random.seed(42)


def generate_sales_data(n_rows=100000):
    """
    Generate synthetic sales transaction data.
    
    Parameters:
    -----------
    n_rows : int
        Number of transaction records to generate (default: 100,000)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing transaction data with columns:
        transaction_id, customer_id, product, category, quantity, 
        price, revenue, date, region
    """
    
    try:
        print("=" * 60)
        print("Sales Dataset Generator - Starting")
        print("=" * 60)
        print(f"Generating {n_rows:,} transaction records...\n")
        
        # Define data parameters
        categories = ['Electronics', 'Clothing', 'Home & Garden', 'Sports', 'Books']
        products = {
            'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones'],
            'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes'],
            'Home & Garden': ['Lamp', 'Chair', 'Plant', 'Rug'],
            'Sports': ['Running Shoes', 'Yoga Mat', 'Dumbbell', 'Bicycle'],
            'Books': ['Fiction Novel', 'Self-Help', 'Biography', 'Cookbook']
        }
        regions = ['North', 'South', 'East', 'West', 'Central']
        
        # Generate transaction IDs (unique)
        transaction_ids = np.arange(1, n_rows + 1)
        
        # Generate customer IDs (not unique - customers can have multiple purchases)
        customer_ids = np.random.randint(1000, 5000, n_rows)
        
        # Generate categories
        selected_categories = np.random.choice(categories, n_rows)
        
        # Generate products based on selected categories
        selected_products = [
            np.random.choice(products[cat]) for cat in selected_categories
        ]
        
        # Generate quantities (between 1 and 10)
        quantities = np.random.randint(1, 11, n_rows)
        
        # Generate prices (between $10 and $500)
        prices = np.random.uniform(10, 500, n_rows).round(2)
        
        # Introduce missing values in price column (5%)
        missing_price_indices = np.random.choice(
            n_rows, size=int(0.05 * n_rows), replace=False
        )
        prices[missing_price_indices] = np.nan
        
        # Calculate revenue (quantity * price)
        revenues = (quantities * prices).round(2)
        
        # Generate dates (between 2023-01-01 and 2024-12-31)
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 12, 31)
        date_range = (end_date - start_date).days
        random_days = np.random.randint(0, date_range + 1, n_rows)
        dates = [start_date + timedelta(days=int(d)) for d in random_days]
        
        # Generate regions
        selected_regions = np.random.choice(regions, n_rows)
        
        # Introduce missing values in region column (2%)
        missing_region_indices = np.random.choice(
            n_rows, size=int(0.02 * n_rows), replace=False
        )
        selected_regions = selected_regions.astype('object')
        selected_regions[missing_region_indices] = np.nan
        
        # Create DataFrame
        df = pd.DataFrame({
            'transaction_id': transaction_ids,
            'customer_id': customer_ids,
            'product': selected_products,
            'category': selected_categories,
            'quantity': quantities,
            'price': prices,
            'revenue': revenues,
            'date': dates,
            'region': selected_regions
        })
        
        print("✓ Data generation completed successfully")
        print(f"  Rows generated: {len(df):,}")
        print(f"  Columns: {list(df.columns)}\n")
        
        return df
    
    except Exception as e:
        print(f"✗ Error during data generation: {str(e)}", file=sys.stderr)
        raise


def validate_data(df):
    """
    Validate the generated dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Generated sales data
    
    Returns:
    --------
    bool
        True if validation passes
    """
    
    print("Validating dataset...")
    
    # Check shape
    assert df.shape[0] == 100000, f"Expected 100,000 rows, got {df.shape[0]}"
    print(f"✓ Row count: {df.shape[0]:,}")
    
    # Check columns
    expected_cols = [
        'transaction_id', 'customer_id', 'product', 'category', 
        'quantity', 'price', 'revenue', 'date', 'region'
    ]
    assert list(df.columns) == expected_cols, "Columns don't match expected schema"
    print(f"✓ All {len(expected_cols)} columns present")
    
    # Check missing values
    missing_price = df['price'].isna().sum()
    missing_region = df['region'].isna().sum()
    print(f"✓ Missing values - Price: {missing_price} (~5%), Region: {missing_region} (~2%)")
    
    # Check data types
    assert pd.api.types.is_integer_dtype(df['transaction_id']), "transaction_id should be integer"
    assert pd.api.types.is_integer_dtype(df['customer_id']), "customer_id should be integer"
    assert pd.api.types.is_datetime64_any_dtype(df['date']), "date should be datetime"
    print("✓ Data types are correct")
    
    # Check date range
    min_date = df['date'].min()
    max_date = df['date'].max()
    assert min_date.year == 2023 or min_date.year == 2024, "Dates outside expected range"
    assert max_date.year == 2024, "Dates outside expected range"
    print(f"✓ Date range: {min_date.date()} to {max_date.date()}")
    
    print()
    return True


def save_dataset(df, filepath='sales_data.csv'):
    """
    Save the dataset to a CSV file.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales dataset
    filepath : str
        Path where to save the CSV file (default: 'sales_data.csv')
    
    Returns:
    --------
    None
    """
    
    try:
        df.to_csv(filepath, index=False)
        file_size_mb = np.ceil(df.memory_usage(deep=True).sum() / 1024**2)
        print(f"✓ Dataset saved to: {filepath}")
        print(f"  File size: ~{file_size_mb} MB")
        print()
    
    except Exception as e:
        print(f"✗ Error saving dataset: {str(e)}", file=sys.stderr)
        raise


def display_sample(df, n_samples=5):
    """
    Display sample rows from the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales dataset
    n_samples : int
        Number of sample rows to display (default: 5)
    
    Returns:
    --------
    None
    """
    
    print("Sample data (first 5 rows):")
    print("-" * 60)
    print(df.head(n_samples).to_string(index=False))
    print()
    
    print("Dataset summary statistics:")
    print("-" * 60)
    print(df[['quantity', 'price', 'revenue']].describe().to_string())
    print()


def main():
    """
    Main function to orchestrate dataset generation.
    """
    
    try:
        # Generate dataset
        df = generate_sales_data(n_rows=100000)
        
        # Validate data
        validate_data(df)
        
        # Save to CSV
        save_dataset(df, filepath='sales_data.csv')
        
        # Display samples and statistics
        display_sample(df)
        
        print("=" * 60)
        print("✓ All tasks completed successfully!")
        print("=" * 60)
        print("\nNext steps for EDA:")
        print("  - Load the data: df = pd.read_csv('sales_data.csv')")
        print("  - Check info: df.info()")
        print("  - Explore missing values: df.isnull().sum()")
        print("  - Analyze distributions and correlations")
        print()
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("✗ EXECUTION FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
