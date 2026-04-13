"""
Custom HTML Profile Report Generator
=====================================
Generates a professional HTML report with visualizations and statistics
without YData Profiling dependencies.

Requirements:
- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.5.0

Author: Data Science Team
Date: 2024
"""

import sys
import pandas as pd
import numpy as np
import base64
from io import BytesIO
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend


def load_dataset(filepath='sales_data.csv'):
    """Load the sales dataset."""
    
    print("Loading dataset...")
    try:
        if not Path(filepath).exists():
            raise FileNotFoundError(f"Dataset not found: {filepath}")
        
        df = pd.read_csv(filepath)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        print(f"✓ Dataset loaded: {df.shape[0]:,} rows × {df.shape[1]} columns\n")
        return df
    
    except Exception as e:
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


def fig_to_base64(fig):
    """Convert matplotlib figure to base64 string for embedding in HTML."""
    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)
    return image_base64


def create_distribution_chart(df):
    """Create distribution charts for numeric columns."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Distribution of Numeric Features', fontsize=14, fontweight='bold')
    axes = axes.flatten()
    
    for idx, col in enumerate(numeric_cols[:4]):
        axes[idx].hist(df[col].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
        axes[idx].set_title(f'{col}')
        axes[idx].set_xlabel('Value')
        axes[idx].set_ylabel('Frequency')
        axes[idx].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig_to_base64(fig)


def create_correlation_heatmap(df):
    """Create correlation heatmap for numeric columns."""
    numeric_df = df.select_dtypes(include=[np.number])
    
    fig, ax = plt.subplots(figsize=(10, 8))
    corr = numeric_df.corr()
    
    im = ax.imshow(corr, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(corr.columns)))
    ax.set_yticks(np.arange(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha='right')
    ax.set_yticklabels(corr.columns)
    
    # Add correlation values
    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            text = ax.text(j, i, f'{corr.iloc[i, j]:.2f}',
                          ha="center", va="center", color="black", fontsize=9)
    
    ax.set_title('Correlation Heatmap', fontweight='bold', fontsize=12)
    fig.colorbar(im, ax=ax)
    plt.tight_layout()
    
    return fig_to_base64(fig)


def create_missing_values_chart(df):
    """Create missing values visualization."""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    missing_data = missing_pct[missing_pct > 0].sort_values(ascending=False)
    
    if len(missing_data) == 0:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 4))
    missing_data.plot(kind='barh', ax=ax, color='coral', edgecolor='black')
    ax.set_xlabel('Missing Percentage (%)')
    ax.set_title('Missing Values by Column', fontweight='bold', fontsize=12)
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    return fig_to_base64(fig)


def create_categorical_bars(df):
    """Create bar charts for categorical columns."""
    categorical_cols = df.select_dtypes(include=['object']).columns[:2]
    
    if len(categorical_cols) == 0:
        return None
    
    fig, axes = plt.subplots(1, len(categorical_cols), figsize=(12, 4))
    if len(categorical_cols) == 1:
        axes = [axes]
    
    fig.suptitle('Top Categories', fontsize=14, fontweight='bold')
    
    for idx, col in enumerate(categorical_cols):
        value_counts = df[col].value_counts().head(10)
        axes[idx].bar(range(len(value_counts)), value_counts.values, color='skyblue', edgecolor='black')
        axes[idx].set_xticks(range(len(value_counts)))
        axes[idx].set_xticklabels(value_counts.index, rotation=45, ha='right')
        axes[idx].set_title(f'{col}')
        axes[idx].set_ylabel('Count')
        axes[idx].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig_to_base64(fig)


def generate_html_report(df, output_filepath='ydata_report.html'):
    """Generate comprehensive HTML report."""
    
    print("Generating HTML report...")
    print("  Creating distribution chart...")
    
    try:
        # Generate charts
        dist_chart = create_distribution_chart(df)
        print("  ✓ Distribution chart created")
    except Exception as e:
        print(f"  ✗ Distribution chart failed: {e}")
        dist_chart = None
    
    try:
        print("  Creating correlation heatmap...")
        corr_chart = create_correlation_heatmap(df)
        print("  ✓ Correlation heatmap created")
    except Exception as e:
        print(f"  ✗ Correlation heatmap failed: {e}")
        corr_chart = None
    
    try:
        print("  Creating missing values chart...")
        missing_chart = create_missing_values_chart(df)
        if missing_chart:
            print("  ✓ Missing values chart created")
    except Exception as e:
        print(f"  ✗ Missing values chart failed: {e}")
        missing_chart = None
    
    try:
        print("  Creating categorical chart...")
        cat_chart = create_categorical_bars(df)
        if cat_chart:
            print("  ✓ Categorical chart created")
    except Exception as e:
        print(f"  ✗ Categorical chart failed: {e}")
        cat_chart = None
    
    # Calculate statistics
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['object']).columns
    
    missing = df.isnull().sum()
    missing_pct = (missing / len(df) * 100).round(2)
    
    # Build HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sales Dataset - Profile Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #333;
                padding: 20px;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                background: white;
                border-radius: 10px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            section {{
                margin-bottom: 50px;
            }}
            
            h2 {{
                color: #667eea;
                font-size: 1.8em;
                margin-bottom: 20px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-card {{
                background: #f8f9fa;
                border: 2px solid #667eea;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
            }}
            
            .stat-value {{
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
                margin: 10px 0;
            }}
            
            .stat-label {{
                color: #666;
                font-size: 0.9em;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            
            th {{
                background: #667eea;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            
            td {{
                padding: 10px 12px;
                border-bottom: 1px solid #eee;
            }}
            
            tr:hover {{
                background: #f8f9fa;
            }}
            
            .chart-container {{
                margin: 30px 0;
                text-align: center;
            }}
            
            .chart-container img {{
                max-width: 100%;
                height: auto;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }}
            
            .missing-value {{
                color: #e74c3c;
                font-weight: bold;
            }}
            
            footer {{
                background: #f8f9fa;
                padding: 20px;
                text-align: center;
                color: #666;
                border-top: 1px solid #eee;
                margin-top: 40px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>📊 Sales Dataset Profile Report</h1>
                <p>Comprehensive Exploratory Data Analysis</p>
            </header>
            
            <div class="content">
                <!-- OVERVIEW SECTION -->
                <section>
                    <h2>Dataset Overview</h2>
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-label">Total Rows</div>
                            <div class="stat-value">{len(df):,}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Total Columns</div>
                            <div class="stat-value">{len(df.columns)}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Numeric Columns</div>
                            <div class="stat-value">{len(numeric_cols)}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Categorical Columns</div>
                            <div class="stat-value">{len(categorical_cols)}</div>
                        </div>
                    </div>
                </section>
                
                <!-- MISSING VALUES SECTION -->
                <section>
                    <h2>Missing Values Analysis</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Column</th>
                                <th>Missing Count</th>
                                <th>Missing %</th>
                            </tr>
                        </thead>
                        <tbody>
    """
    
    for col in df.columns:
        if missing[col] > 0:
            html_content += f"""
                            <tr>
                                <td>{col}</td>
                                <td class="missing-value">{missing[col]:,}</td>
                                <td class="missing-value">{missing_pct[col]:.2f}%</td>
                            </tr>
            """
    
    if missing.sum() == 0:
        html_content += """
                            <tr>
                                <td colspan="3"><strong>No missing values found!</strong></td>
                            </tr>
        """
    
    html_content += """
                        </tbody>
                    </table>
                </section>
                
                <!-- STATISTICS SECTION -->
                <section>
                    <h2>Statistical Summary</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Statistic</th>
    """
    
    for col in numeric_cols:
        html_content += f"<th>{col}</th>"
    
    html_content += """
                            </tr>
                        </thead>
                        <tbody>
    """
    
    stats = ['Count', 'Mean', 'Median', 'Std Dev', 'Min', 'Max']
    for stat in stats:
        html_content += f"<tr><td><strong>{stat}</strong></td>"
        for col in numeric_cols:
            if stat == 'Count':
                val = df[col].notna().sum()
            elif stat == 'Mean':
                val = f"{df[col].mean():.2f}"
            elif stat == 'Median':
                val = f"{df[col].median():.2f}"
            elif stat == 'Std Dev':
                val = f"{df[col].std():.2f}"
            elif stat == 'Min':
                val = f"{df[col].min():.2f}"
            elif stat == 'Max':
                val = f"{df[col].max():.2f}"
            html_content += f"<td>{val}</td>"
        html_content += "</tr>"
    
    html_content += """
                        </tbody>
                    </table>
                </section>
    """
    
    # Add charts
    if dist_chart:
        html_content += f"""
                <section>
                    <h2>Feature Distributions</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{dist_chart}" alt="Distribution Charts">
                    </div>
                </section>
        """
    
    if corr_chart:
        html_content += f"""
                <section>
                    <h2>Correlation Heatmap</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{corr_chart}" alt="Correlation Heatmap">
                    </div>
                </section>
        """
    
    if missing_chart:
        html_content += f"""
                <section>
                    <h2>Missing Values Visualization</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{missing_chart}" alt="Missing Values">
                    </div>
                </section>
        """
    
    if cat_chart:
        html_content += f"""
                <section>
                    <h2>Categorical Analysis</h2>
                    <div class="chart-container">
                        <img src="data:image/png;base64,{cat_chart}" alt="Categorical Analysis">
                    </div>
                </section>
        """
    
    html_content += """
            </div>
            
            <footer>
                <p>Report generated by Custom HTML Profile Report Generator</p>
                <p>© 2024 Data Science Team</p>
            </footer>
        </div>
    </body>
    </html>
    """
    
    # Save HTML with UTF-8 encoding
    with open(output_filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    file_size_mb = Path(output_filepath).stat().st_size / 1024**2
    print(f"✓ HTML report saved: {output_filepath} ({file_size_mb:.2f} MB)\n")


def main():
    """Main function."""
    print("=" * 70)
    print("CUSTOM HTML PROFILE REPORT GENERATOR")
    print("=" * 70)
    print()
    
    try:
        df = load_dataset('sales_data.csv')
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print()
        
        generate_html_report(df, output_filepath='ydata_report.html')
        
        print("=" * 70)
        print("✓ REPORT GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print("\nOpen 'ydata_report.html' in your web browser to view the report.")
        print()
        
    except Exception as e:
        import traceback
        print(f"✗ Error: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
