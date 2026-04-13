"""
D-Tale Interactive EDA Launcher
================================
This script loads the sales dataset and launches D-Tale GUI,
providing an interactive exploratory data analysis interface.

Requirements:
- pandas>=2.0.0
- dtale>=3.0.0

Installation:
pip install dtale

Author: Data Science Team
Date: 2024
"""

import sys
import pandas as pd
from pathlib import Path
import time


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
        print(f"  Columns: {list(df.columns)}")
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


def launch_dtale(df):
    """
    Launch D-Tale GUI for interactive EDA.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Sales dataset to analyze
    
    Returns:
    --------
    str
        URL to access the D-Tale interface
    
    Raises:
    -------
    ImportError
        If dtale is not installed
    Exception
        If D-Tale launch fails
    """
    
    print("=" * 70)
    print("LAUNCHING D-TALE INTERACTIVE EDA")
    print("=" * 70)
    
    try:
        # Import D-Tale
        import dtale
        
        print("Initializing D-Tale...")
        
        # Create D-Tale instance
        d = dtale.show(df, open_browser=False)
        
        # Get the URL - try different attributes
        try:
            url = d.url
        except AttributeError:
            # Try alternative attribute names
            try:
                url = d._url
            except AttributeError:
                # Build URL manually
                port = d.port if hasattr(d, 'port') else 40000
                url = f"http://127.0.0.1:{port}"
        
        print(f"✓ D-Tale launched successfully!")
        print()
        print("=" * 70)
        print("D-TALE INTERFACE READY")
        print("=" * 70)
        print(f"✓ Server is running on: {url}")
        print()
        print("Features available in D-Tale:")
        print("  • View and filter data")
        print("  • Sort columns")
        print("  • Generate statistics")
        print("  • Create visualizations")
        print("  • Export data")
        print("  • Analyze correlations")
        print()
        print("IMPORTANT INSTRUCTIONS:")
        print("-" * 70)
        print("1. Open your web browser")
        print(f"2. Navigate to: {url}")
        print("3. Explore the data interactively")
        print("4. When finished, press Ctrl+C in this terminal to close D-Tale")
        print("-" * 70)
        print()
        
        return url
    
    except ImportError:
        print("✗ Error: D-Tale is not installed", file=sys.stderr)
        print("\nInstall D-Tale with:")
        print("  pip install dtale")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error launching D-Tale: {str(e)}", file=sys.stderr)
        sys.exit(1)


def keep_alive():
    """
    Keep the server running until user interrupts (Ctrl+C).
    """
    
    try:
        print("D-Tale server is running...")
        print("Press Ctrl+C to stop the server and exit.")
        print()
        
        # Keep the script running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n")
        print("=" * 70)
        print("✓ D-Tale server stopped")
        print("=" * 70)
        print("Thank you for using D-Tale EDA!")
        print()
        sys.exit(0)


def main():
    """
    Main function to orchestrate D-Tale launch.
    """
    
    try:
        # Load dataset
        df = load_dataset('sales_data.csv')
        
        # Launch D-Tale
        url = launch_dtale(df)
        
        # Keep server alive
        keep_alive()
        
    except Exception as e:
        print("\n" + "=" * 70)
        print("✗ EXECUTION FAILED")
        print("=" * 70)
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
