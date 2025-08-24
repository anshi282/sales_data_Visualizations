# Complete Setup Guide - Sales Visualization Tool

## 🚀 Quick Start (Automated Setup)

### Option 1: Automated Setup (Recommended)
```bash
# 1. Download and save the setup.py file
# 2. Run the automated setup
python setup.py

# 3. Start using the tool
python main.py
```

## 📁 Manual Setup Instructions

### Step 1: Create Project Directory
```bash
mkdir sales_visualization_tool
cd sales_visualization_tool
```

### Step 2: Create Directory Structure
```bash
# Create all required directories
mkdir data output src examples tests
mkdir output/charts output/reports

# Create __init__.py files
touch src/__init__.py
touch tests/__init__.py
```

### Step 3: Install Python Dependencies
```bash
# Option A: Using pip
pip install pandas matplotlib seaborn plotly numpy openpyxl jupyter kaleido scikit-learn statsmodels dash dash-bootstrap-components

# Option B: Using conda (if you have it)
conda create -n sales-viz-tool python=3.9
conda activate sales-viz-tool
conda install -c conda-forge pandas matplotlib seaborn numpy jupyter scikit-learn
pip install plotly openpyxl kaleido statsmodels dash dash-bootstrap-components
```

### Step 4: Create All Files
Create these files in your project directory with the content from the artifacts:

#### Core Files:
- `requirements.txt` - Python dependencies
- `main.py` - Main application entry point
- `sales_analyzer.py` - Core visualization tool
- `config.py` - Configuration settings
- `README.md` - Project documentation

#### Source Files (src/ directory):
- `src/__init__.py` - Package initialization
- `src/data_loader.py` - Data loading utilities
- `src/visualizations.py` - Advanced visualization components
- `src/utils.py` - Utility functions and data processing

#### Example Files (examples/ directory):
- `examples/basic_usage.py` - Basic usage examples
- `examples/advanced_analysis.py` - Advanced analytics examples
- `examples/custom_dashboard.py` - Custom dashboard creation

#### Data Files (data/ directory):
- `data/README.md` - Data format instructions
- `data/sample_sales_data.csv` - Sample data for testing

## 📋 Complete File List

Here's the complete list of files you need to create:

### Root Directory Files:
```
sales_visualization_tool/
├── requirements.txt
├── main.py
├── sales_analyzer.py
├── config.py
├── README.md
├── setup.py
└── COMPLETE_SETUP_GUIDE.md
```

### Directory Structure:
```
├── data/
│   ├── README.md
│   └── sample_sales_data.csv
├── output/
│   ├── charts/          # Generated charts saved here
│   └── reports/         # HTML/Excel reports saved here
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── visualizations.py
│   └── utils.py
└── examples/
    ├── basic_usage.py
    ├── advanced_analysis.py
    └── custom_dashboard.py
```

## 🎯 Step-by-Step File Creation

### 1. Core Application Files

**Copy these from the artifacts provided:**
- `requirements.txt`
- `main.py` 
- `sales_analyzer.py`
- `config.py`
- `README.md`

### 2. Source Module Files

**In the `src/` directory, create:**
- `__init__.py` (can be empty or use the provided content)
- `data_loader.py` (from artifact)
- `visualizations.py` (from artifact)  
- `utils.py` (from artifact)

### 3. Example Files

**In the `examples/` directory, create:**
- `basic_usage.py` (from artifact)
- `advanced_analysis.py` (from artifact)
- `custom_dashboard.py` (from artifact)

### 4. Data Files

**In the `data/` directory, create:**
- `README.md` (from artifact)
- `sample_sales_data.csv` (from artifact, or will be generated automatically)

## 🔧 Configuration Steps

### 1. Virtual Environment Setup (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install from requirements.txt
pip install -r requirements.txt

# OR install individually:
pip install pandas matplotlib seaborn plotly numpy openpyxl jupyter kaleido
```

### 3. Verify Installation
```python
# Test import of key packages
python -c "import pandas, matplotlib, seaborn, plotly, numpy; print('All packages imported successfully!')"
```

## 🚦 Testing Your Setup

### 1. Run Basic Test
```bash
python main.py
```
Choose option 1 to generate sample data and run a demo.

### 2. Run Example Scripts
```bash
# Basic usage example
python examples/basic_usage.py

# Advanced analysis example
python examples/advanced_analysis.py

# Custom dashboard example
python examples/custom_dashboard.py
```

### 3. Test with Your Own Data
```bash
# Place your CSV file in the data/ directory
# Run the tool and choose option 2 to load your data
python main.py
```

## 📊 Expected Data Format

Your CSV file should have these columns (minimum):

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Date | Date | Transaction date | 2024-01-15 |
| Product | String | Product name | Laptop |
| Region | String | Sales region | North America |
| Total_Sales | Number | Sales amount | 1250.50 |

Optional columns:
- Sales_Rep (string)
- Quantity (number)  
- Unit_Price (number)
- Customer_ID (string)

## 🎨 Available Visualizations

Once set up, you can create:

1. **Time Series Analysis**
   - Daily, weekly, monthly sales trends
   - Interactive plots with zoom and hover

2. **Product Performance**
   - Sales by product comparison
   - Product performance matrix
   - Treemap visualizations

3. **Regional Analysis** 
   - Geographic sales distribution
   - Regional performance comparison

4. **Sales Team Performance**
   - Top performers ranking
   - Sales rep comparison
   - Team leaderboards

5. **Advanced Analytics**
   - Customer segmentation (RFM analysis)
   - Sales forecasting
   - Growth rate analysis
   - Seasonality detection

6. **Custom Dashboards**
   - Executive dashboards
   - Financial dashboards
   - Mobile-optimized views
   - Interactive web apps

## 🔍 Troubleshooting

### Common Issues:

1. **Import Errors**
   ```bash
   # Solution: Install missing packages
   pip install [package-name]
   ```

2. **Charts Not Displaying**
   ```bash
   # For static images
   pip install kaleido
   
   # For Jupyter notebooks
   pip install jupyter
   ```

3. **Data Loading Issues**
   - Check CSV format and encoding
   - Ensure required columns exist
   - Verify date format consistency

4. **Permission Errors**
   - Check write permissions for output directories
   - Run with appropriate user permissions

5. **Memory Issues with Large Files**
   ```python
   # Use chunk processing for large files
   from src.utils import PerformanceUtils
   PerformanceUtils.chunk_processor('large_file.csv', chunk_size=5000)
   ```

## 🚀 Getting Started Commands

### Quick Start
```bash
# 1. Generate sample data and explore
python main.py
# Choose option 1: "Generate sample data and run demo"

# 2. Load your own data
python main.py  
# Choose option 2: "Load data from CSV file"
# Enter path: data/your_file.csv

# 3. Create specific visualizations
python main.py
# Choose options 4-10 for specific chart types
```

### Advanced Usage
```bash
# Run advanced analysis examples
python examples/advanced_analysis.py

# Create custom dashboards  
python examples/custom_dashboard.py

# Interactive analysis in Jupyter
jupyter notebook
```

### Command Line Usage
```python
# Direct Python usage
from sales_analyzer import SalesVisualizationTool

tool = SalesVisualizationTool()
tool.generate_sample_data(1000)
tool.create_comprehensive_dashboard()
```

## 📈 Next Steps

After setup:

1. **Explore with Sample Data**
   - Run the demo to see all features
   - Understand the chart types available

2. **Load Your Data**
   - Prepare your CSV file according to the format
   - Use the data loading feature

3. **Customize Visualizations**
   - Modify colors and themes in `config.py`
   - Create custom chart combinations

4. **Automate Reports**
   - Schedule regular report generation
   - Export to multiple formats

5. **Extend Functionality**
   - Add new chart types in `src/visualizations.py`
   - Create custom analysis functions

## 💡 Pro Tips

1. **Data Preparation**
   - Clean your data before loading
   - Use consistent date formats
   - Remove special characters from column names

2. **Performance**
   - Use sample data for initial exploration
   - Optimize large datasets with the utility functions
   - Save static versions of interactive charts for reports

3. **Customization**
   - Modify the color palette in `config.py`
   - Adjust chart sizes and layouts
   - Create themed dashboards for different audiences

4. **Sharing Results**
   - Export charts as HTML for interactive sharing
   - Generate PDF reports for presentations
   - Save static images for documents

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the example files for usage patterns
3. Ensure all dependencies are properly installed
4. Verify your data format matches requirements

The tool is designed to be user-friendly and handle common data analysis scenarios out of the box. Happy analyzing! 🎉