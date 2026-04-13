"""
Automated Exploratory Data Analysis (EDA) Script - Lite Version
================================================================
This script performs comprehensive EDA on the sales dataset using:
- Custom pandas-based analysis (no external dependencies)
- Sweetviz: Interactive data visualization and analysis reports

Requirements:
- pandas>=2.0.0
- numpy>=1.24.0
- sweetviz>=2.1.0

Author: Data Science Team
Date: 2024
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from importlib.metadata import version as get_version


def verify_library_versions():
    """
    Verify that all required libraries are installed with compatible versions.
    
    Raises:
    -------
    ImportError
        If required libraries are not installed or version requirements not met
    """
    
    print("=" * 70)
    print("LIBRARY VERSION VERIFICATION")
    print("=" * 70)
    
    required_libs = {
        'pandas': '2.0.0',
        'numpy': '1.24.0',
        'sweetviz': '2.1.0'
    }
    
    def parse_version(version_string):
        """Convert version string to tuple for comparison."""
        return tuple(int(x) for x in version_string.split('.')[:3])
    
    try:
        for lib, min_version in required_libs.items():
            try:
                installed_version = get_version(lib)
            except Exception:
                raise ImportError(f"Package '{lib}' is not installed")
            
            if parse_version(installed_version) >= parse_version(min_version):
                print(f"✓ {lib:25} v{installed_version} (required: >={min_version})")
            else:
                raise ImportError(
                    f"{lib} v{installed_version} does not meet minimum "
                    f"requirement (>={min_version})"
                )
        
        print()
        return True
    
    except ImportError as e:
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        print("\nInstall missing packages with:")
        print("  pip install pandas>=2.0.0 numpy>=1.24.0 sweetviz>=2.1.0")
        sys.exit(1)


def load_dataset(filepath='sales_data.csv'):
    """
    Load the sales dataset from CSV file with error handling.
    
    Parameters:
    -----------
    filepath : str
        Path to the CSV file (default: 'sales_data.csv')
    
    Returns:
    --------
    pd.DataFrame
        Loaded dataset
    
    Raises:
    -------
    FileNotFoundError
        If the CSV file does not exist
    pd.errors.ParserError
        If the CSV file is malformed
    """
    
    print("=" * 70)
    print("LOADING DATASET")
    print("=" * 70)
    
    try:
        # Check if file exists
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Dataset not found: {filepath}")
        
        print(f"Loading dataset from: {filepath}")
        df = pd.read_csv(filepath)
        
        # Convert date column to datetime if it exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        print(f"✓ Dataset loaded successfully")
        print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print(f"  Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print()
        
        return df
    
    except FileNotFoundError as e:
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except pd.errors.ParserError as e:
        print(f"✗ Error parsing CSV: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error loading dataset: {str(e)}", file=sys.stderr)
        sys.exit(1)


def generate_custom_analysis(df, output_filepath='eda_analysis.txt'):
    """
    Generate custom EDA analysis report using pandas.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales dataset
    output_filepath : str
        Path where to save the text report (default: 'eda_analysis.txt')
    
    Returns:
    --------
    None
    """
    
    print("=" * 70)
    print("GENERATING CUSTOM EDA ANALYSIS REPORT")
    print("=" * 70)
    
    try:
        report = []
        report.append("=" * 80)
        report.append("EXPLORATORY DATA ANALYSIS REPORT - SALES DATASET")
        report.append("=" * 80)
        
        # Dataset Overview
        report.append("\n1. DATASET OVERVIEW")
        report.append("-" * 80)
        report.append(f"Total Rows: {len(df):,}")
        report.append(f"Total Columns: {len(df.columns)}")
        report.append(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        # Data Types
        report.append("\n2. DATA TYPES")
        report.append("-" * 80)
        for col, dtype in df.dtypes.items():
            report.append(f"  {col:20} : {dtype}")
        
        # Missing Values Analysis
        report.append("\n3. MISSING VALUES ANALYSIS")
        report.append("-" * 80)
        missing = df.isnull().sum()
        missing_pct = (missing / len(df) * 100).round(2)
        
        for col in df.columns:
            if missing[col] > 0:
                report.append(f"  {col:20} : {missing[col]:6,} rows ({missing_pct[col]:5.2f}%)")
        
        if missing.sum() == 0:
            report.append("  No missing values found!")
        
        # Statistical Summary
        report.append("\n4. STATISTICAL SUMMARY")
        report.append("-" * 80)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            report.append(f"\n  {col.upper()}:")
            report.append(f"    Count:  {df[col].notna().sum():,}")
            report.append(f"    Mean:   {df[col].mean():.2f}")
            report.append(f"    Median: {df[col].median():.2f}")
            report.append(f"    Std:    {df[col].std():.2f}")
            report.append(f"    Min:    {df[col].min():.2f}")
            report.append(f"    Max:    {df[col].max():.2f}")
        
        # Categorical Analysis
        report.append("\n5. CATEGORICAL ANALYSIS")
        report.append("-" * 80)
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        for col in categorical_cols:
            report.append(f"\n  {col.upper()}:")
            value_counts = df[col].value_counts(dropna=False)
            report.append(f"    Unique values: {df[col].nunique()}")
            report.append(f"    Top 5 values:")
            for val, count in value_counts.head(5).items():
                pct = (count / len(df) * 100)
                report.append(f"      {str(val):20} : {count:6,} ({pct:5.2f}%)")
        
        # Date Range Analysis
        if 'date' in df.columns:
            report.append("\n6. DATE RANGE ANALYSIS")
            report.append("-" * 80)
            report.append(f"  Earliest Date: {df['date'].min()}")
            report.append(f"  Latest Date:   {df['date'].max()}")
            report.append(f"  Date Span:     {(df['date'].max() - df['date'].min()).days} days")
        
        # Correlation Analysis
        report.append("\n7. CORRELATION ANALYSIS (Numeric Columns)")
        report.append("-" * 80)
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    corr_val = corr_matrix.loc[col1, col2]
                    report.append(f"  {col1} vs {col2}: {corr_val:.4f}")
        
        # Outlier Detection
        report.append("\n8. OUTLIER DETECTION (IQR Method)")
        report.append("-" * 80)
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            outlier_pct = (outliers / len(df) * 100)
            
            report.append(f"  {col:20} : {outliers:6,} outliers ({outlier_pct:5.2f}%)")
        
        report.append("\n" + "=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)
        
        # Save report
        report_text = "\n".join(report)
        with open(output_filepath, 'w') as f:
            f.write(report_text)
        
        # Print to console
        print(report_text)
        
        # Confirm save
        file_size_kb = Path(output_filepath).stat().st_size / 1024
        print(f"\n✓ Analysis report saved")
        print(f"  File: {output_filepath}")
        print(f"  Size: {file_size_kb:.2f} KB")
        print()
        
    except Exception as e:
        print(f"✗ Error generating analysis report: {str(e)}", file=sys.stderr)
        raise


def generate_sweetviz_report(df, target_variable='revenue', output_filepath='sweetviz_report.html'):
    """
    Generate Sweetviz report with specified target variable.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales dataset
    target_variable : str
        Column name to use as target variable (default: 'revenue')
    output_filepath : str
        Path where to save the HTML report (default: 'sweetviz_report.html')
    
    Returns:
    --------
    None
    
    Raises:
    -------
    Exception
        If report generation fails
    """
    
    print("=" * 70)
    print("GENERATING SWEETVIZ REPORT")
    print("=" * 70)
    
    try:
        import sweetviz as sv
        
        # Verify target variable exists
        if target_variable not in df.columns:
            raise ValueError(
                f"Target variable '{target_variable}' not found in dataset. "
                f"Available columns: {list(df.columns)}"
            )
        
        # Create a copy for Sweetviz analysis without NaN values in target
        df_clean = df.dropna(subset=[target_variable])
        
        print(f"Generating Sweetviz report with target: '{target_variable}'")
        print(f"  Original rows: {len(df):,}")
        print(f"  Rows without NaN in target: {len(df_clean):,}")
        print("This may take a minute... Processing data visualizations")
        
        # Create Sweetviz analysis with target variable
        analysis = sv.analyze(
            df_clean,
            target_feat=target_variable,
            pairwise_analysis='on'
        )
        
        print(f"✓ Report generated successfully")
        print(f"  Saving to: {output_filepath}")
        
        # Save to HTML
        analysis.show_html(
            filepath=output_filepath,
            open_browser=False
        )
        
        # Get file size
        file_size_mb = Path(output_filepath).stat().st_size / 1024**2
        print(f"✓ Sweetviz report saved")
        print(f"  File: {output_filepath}")
        print(f"  Size: {file_size_mb:.2f} MB")
        print()
        
    except ValueError as e:
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        raise
    except Exception as e:
        print(f"✗ Error generating Sweetviz report: {str(e)}", file=sys.stderr)
        raise


def main():
    """
    Main function to orchestrate automated EDA generation.
    """
    
    try:
        # Step 1: Verify library versions
        verify_library_versions()
        
        # Step 2: Load dataset
        df = load_dataset('sales_data.csv')
        
        # Step 3: Generate custom analysis
        generate_custom_analysis(df, output_filepath='eda_analysis.txt')
        
        # Step 4: Generate Sweetviz report
        generate_sweetviz_report(
            df,
            target_variable='revenue',
            output_filepath='sweetviz_report.html'
        )
        
        # Final summary
        print("=" * 70)
        print("✓ AUTOMATED EDA COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("\nGenerated Reports:")
        print("  1. eda_analysis.txt - Comprehensive statistical analysis")
        print("     (View in text editor)")
        print("  2. sweetviz_report.html - Interactive visualizations and correlations")
        print("     (Open in browser: sweetviz_report.html)")
        print("\nNext Steps:")
        print("  - Review eda_analysis.txt for detailed statistics")
        print("  - Open sweetviz_report.html in your web browser")
        print("  - Analyze correlations with revenue")
        print("  - Identify data quality issues and outliers")
        print()
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ EXECUTION FAILED")
        print("=" * 70)
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
