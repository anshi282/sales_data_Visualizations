"""
Configuration file for Sales Visualization Tool
"""
import os

# Project paths
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'output')
CHARTS_DIR = os.path.join(OUTPUT_DIR, 'charts')
REPORTS_DIR = os.path.join(OUTPUT_DIR, 'reports')

# Data file settings
SAMPLE_DATA_FILE = os.path.join(DATA_DIR, 'sample_sales_data.csv')
DEFAULT_DATA_FILE = os.path.join(DATA_DIR, 'sales_data.csv')

# Chart settings
CHART_THEME = 'plotly_white'  # plotly themes: plotly, plotly_white, plotly_dark, ggplot2, seaborn, simple_white
DEFAULT_CHART_SIZE = (1200, 600)
CHART_DPI = 300

# Color palettes
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17a2b8',
    'palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
}

# Default chart configurations
PLOTLY_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'sales_chart',
        'height': 600,
        'width': 1200,
        'scale': 1
    }
}

# Data validation rules
DATA_REQUIRED_COLUMNS = ['Date', 'Product', 'Region', 'Total_Sales']
DATE_FORMAT = '%Y-%m-%d'

# Report settings
REPORT_TITLE = "Sales Analysis Report"
REPORT_AUTHOR = "Sales Analytics Team"