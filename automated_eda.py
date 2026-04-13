"""
Automated Exploratory Data Analysis (EDA) Script
=================================================
This script performs comprehensive EDA on the sales dataset using:
- YData Profiling: Automated statistical analysis and report generation
- Sweetviz: Interactive data visualization and analysis reports

Requirements:
- pandas>=2.0.0
- numpy>=1.24.0
- ydata-profiling>=4.0.0
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
        'ydata-profiling': '4.0.0',
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
                # Try alternate package names
                alt_names = {'ydata-profiling': 'ydata_profiling', 'sweetviz': 'sweetviz'}
                if lib in alt_names:
                    installed_version = get_version(alt_names[lib])
                else:
                    raise
            
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
        print("  pip install pandas>=2.0.0 numpy>=1.24.0 ydata-profiling>=4.0.0 sweetviz>=2.1.0")
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


def generate_ydata_report(df, output_filepath='ydata_report.html'):
    """
    Generate YData Profiling report with minimal=True for faster execution.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales dataset
    output_filepath : str
        Path where to save the HTML report (default: 'ydata_report.html')
    
    Returns:
    --------
    None
    
    Raises:
    -------
    Exception
        If report generation fails
    """
    
    print("=" * 70)
    print("GENERATING YDATA PROFILING REPORT")
    print("=" * 70)
    
    try:
        print("This may take a minute... Generating minimal profile report")
        
        from ydata_profiling import ProfileReport
        
        # Create profile with minimal=True for faster execution
        profile = ProfileReport(
            df,
            title="Sales Dataset - YData Profiling Report",
            minimal=True,
            progress_bar=True,
            explorative=False
        )
        
        print(f"✓ Report generated successfully")
        print(f"  Saving to: {output_filepath}")
        
        # Save to HTML
        profile.to_file(output_filepath)
        
        # Get file size
        file_size_mb = Path(output_filepath).stat().st_size / 1024**2
        print(f"✓ YData report saved")
        print(f"  File: {output_filepath}")
        print(f"  Size: {file_size_mb:.2f} MB")
        print()
        
    except Exception as e:
        print(f"✗ Error generating YData report: {str(e)}", file=sys.stderr)
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
        
        print(f"Generating Sweetviz report with target: '{target_variable}'")
        print("This may take a minute... Processing data visualizations")
        
        # Create Sweetviz analysis with target variable
        analysis = sv.analyze(
            df,
            target_variable=target_variable,
            pairwise_analysis='on'
        )
        
        print(f"✓ Report generated successfully")
        print(f"  Saving to: {output_filepath}")
        
        # Save to HTML
        analysis.show_html(
            filepath=output_filepath,
            open_browser=False,
            verbose=False
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


def display_dataset_info(df):
    """
    Display basic information about the dataset.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales dataset
    
    Returns:
    --------
    None
    """
    
    print("=" * 70)
    print("DATASET INFORMATION")
    print("=" * 70)
    print(f"\nData Types:")
    print(df.dtypes.to_string())
    
    print(f"\n\nMissing Values:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Count': missing,
        'Percentage': missing_pct
    })
    print(missing_df[missing_df['Count'] > 0].to_string())
    
    print(f"\n\nBasic Statistics:")
    print(df[['quantity', 'price', 'revenue']].describe().to_string())
    print()


def main():
    """
    Main function to orchestrate automated EDA generation.
    """
    
    try:
        # Step 1: Verify library versions
        verify_library_versions()
        
        # Step 2: Load dataset
        df = load_dataset('sales_data.csv')
        
        # Step 3: Display dataset information
        display_dataset_info(df)
        
        # Step 4: Generate YData Profiling report
        generate_ydata_report(df, output_filepath='ydata_report.html')
        
        # Step 5: Generate Sweetviz report
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
        print("  1. ydata_report.html - Statistical analysis and distributions")
        print("     (Open in browser: ydata_report.html)")
        print("  2. sweetviz_report.html - Interactive visualizations and correlations")
        print("     (Open in browser: sweetviz_report.html)")
        print("\nNext Steps:")
        print("  - Open the HTML reports in your web browser")
        print("  - Review missing value patterns and distributions")
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
