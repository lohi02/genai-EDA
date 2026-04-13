"""
YData Profiling Report Generator
=================================
This script generates a YData Profiling HTML report for the sales dataset.

Requirements:
- pandas>=2.0.0
- ydata-profiling>=4.0.0
- setuptools (for pkg_resources)

Author: Data Science Team
Date: 2024
"""

import sys
import pandas as pd
from pathlib import Path


def load_dataset(filepath='sales_data.csv'):
    """Load the sales dataset from CSV file."""
    
    print("=" * 70)
    print("LOADING DATASET")
    print("=" * 70)
    
    try:
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Dataset not found: {filepath}")
        
        print(f"Loading dataset from: {filepath}")
        df = pd.read_csv(filepath)
        
        # Convert date column to datetime if it exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        print(f"✓ Dataset loaded successfully")
        print(f"  Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
        print()
        
        return df
    
    except FileNotFoundError as e:
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def generate_ydata_report(df, output_filepath='ydata_report.html'):
    """Generate YData Profiling report."""
    
    print("=" * 70)
    print("GENERATING YDATA PROFILING REPORT")
    print("=" * 70)
    
    try:
        from ydata_profiling import ProfileReport
        
        print("Generating YData Profiling report (minimal mode)...")
        print("This may take a moment...\n")
        
        # Create profile report with minimal=True for faster execution
        profile = ProfileReport(
            df,
            title="Sales Dataset - YData Profiling Report",
            minimal=True,
            progress_bar=True,
            explorative=False
        )
        
        print(f"\n✓ Report generated successfully")
        print(f"  Saving to: {output_filepath}")
        
        # Save to HTML
        profile.to_file(output_filepath)
        
        # Get file size
        file_size_mb = Path(output_filepath).stat().st_size / 1024**2
        print(f"✓ YData report saved successfully")
        print(f"  File: {output_filepath}")
        print(f"  Size: {file_size_mb:.2f} MB")
        print()
        
        return True
    
    except ImportError as e:
        print(f"✗ Import Error: {str(e)}", file=sys.stderr)
        print("\nMake sure setuptools is installed:")
        print("  pip install --upgrade setuptools")
        print("\nThen install ydata-profiling:")
        print("  pip install ydata-profiling>=4.0.0")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error generating YData report: {str(e)}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to generate YData report."""
    
    try:
        # Load dataset
        df = load_dataset('sales_data.csv')
        
        # Generate YData report
        generate_ydata_report(df, output_filepath='ydata_report.html')
        
        # Final summary
        print("=" * 70)
        print("✓ YDATA REPORT GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print("\nGenerated Report:")
        print("  ydata_report.html - Statistical analysis and distributions")
        print("  (Open in browser: ydata_report.html)")
        print()
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ EXECUTION FAILED")
        print("=" * 70)
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
