# Sales Data Visualization Tool

A comprehensive Python tool for analyzing and visualizing sales data with interactive charts, dashboards, and detailed reports.

## 🚀 Features

- **Multiple Visualization Types**: Time series plots, product analysis, regional breakdowns, sales rep performance
- **Interactive Charts**: Built with Plotly for interactive exploration
- **Static Charts**: High-quality matplotlib/seaborn charts for reports
- **Comprehensive Dashboard**: All-in-one view of key metrics
- **Data Loading**: Support for CSV and Excel files
- **Sample Data Generation**: Built-in sample data for testing
- **Export Capabilities**: Save charts and generate HTML reports
- **Easy Configuration**: Customizable colors, themes, and settings

## 📁 Project Structure

```
sales_visualization_tool/
├── requirements.txt          # Python dependencies
├── main.py                  # Main application entry point
├── sales_analyzer.py        # Core visualization tool
├── config.py               # Configuration settings
├── README.md               # This file
├── data/                   # Data files
│   ├── sample_sales_data.csv
│   └── README.md
├── output/                 # Generated charts and reports
│   ├── charts/
│   └── reports/
├── src/                    # Source modules
│   ├── __init__.py
│   ├── data_loader.py      # Data loading utilities
│   ├── visualizations.py  # Visualization components
│   └── utils.py           # Helper functions
└── examples/               # Usage examples
    ├── basic_usage.py
    ├── advanced_analysis.py
    └── custom_dashboard.py
```

## 🛠️ Installation

### Step 1: Clone or Download the Project
```bash
# Create the project directory
mkdir sales_visualization_tool
cd sales_visualization_tool
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

If you don't have the requirements.txt file, install manually:
```bash
pip install pandas matplotlib seaborn plotly numpy openpyxl jupyter kaleido
```

### Step 4: Create Directory Structure
```bash
mkdir data output src examples
mkdir output/charts output/reports
```

## 🎯 Quick Start

### Option 1: Run the Main Application
```bash
python main.py
```

This will start an interactive menu where you can:
- Generate sample data
- Load your own CSV files
- Create various visualizations
- Generate comprehensive reports

### Option 2: Use in Python Script
```python
from sales_analyzer import SalesVisualizationTool

# Initialize the tool
sales_tool = SalesVisualizationTool()

# Generate sample data
sales_tool.generate_sample_data(1000)

# Create visualizations
sales_tool.create_time_series_plot()
sales_tool.create_product_analysis()
sales_tool.create_comprehensive_dashboard()
```

### Option 3: Load Your Own Data
```python
from sales_analyzer import SalesVisualizationTool

sales_tool = SalesVisualizationTool()

# Load your CSV file
sales_tool.load_data('your_sales_data.csv')

# Analyze the data
sales_tool.data_summary()
sales_tool.create_comprehensive_dashboard()
```

## 📊 Data Format

Your CSV file should have the following columns (minimum required):

| Column | Description | Example |
|--------|-------------|---------|
| Date | Transaction date | 2024-01-15 |
| Product | Product name | Laptop |
| Region | Sales region | North America |
| Total_Sales | Sales amount | 1250.50 |

Additional optional columns:
- `Sales_Rep`: Sales representative name
- `Quantity`: Number of items sold
- `Unit_Price`: Price per unit
- `Customer_ID`: Customer identifier

## 🎨 Visualizations Available

1. **Time Series Analysis**
   - Daily, monthly, quarterly sales trends
   - Interactive line charts with zoom and hover

2. **Product Performance**
   - Sales by product comparison
   - Quantity analysis
   - Customer segmentation by product

3. **Regional Analysis**
   - Geographic sales distribution
   - Regional performance comparison
   - Market share analysis

4. **Sales Representative Performance**
   - Top performers ranking
   - Individual rep analysis
   - Performance metrics

5. **Comprehensive Dashboard**
   - All-in-one interactive dashboard
   - Multiple chart types in single view
   - Drill-down capabilities

## 🔧 Configuration

Edit `config.py` to customize:
- File paths and directories
- Chart themes and colors
- Default settings
- Export options

Example customization:
```python
# Change chart theme
CHART_THEME = 'plotly_dark'  # or 'plotly_white', 'ggplot2', etc.

# Customize colors
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'success': '#F18F01',
    # ... more colors
}
```

## 📈 Advanced Usage

### Creating Custom Visualizations
```python
# Advanced filtering and analysis
filtered_data = sales_tool.data[sales_tool.data['Product'] == 'Laptop']
custom_analysis = filtered_data.groupby('Region')['Total_Sales'].sum()

# Create custom plotly chart
import plotly.express as px
fig = px.bar(x=custom_analysis.index, y=custom_analysis.values)
fig.show()
```

### Generating Reports
```python
# Export comprehensive HTML report
sales_tool.export_summary_report('monthly_report.html')

# Save all charts
sales_tool.create_time_series_plot()
sales_tool.create_product_analysis()
# Charts are automatically saved to output/charts/
```

## 🐛 Troubleshooting

### Common Issues:

1. **ImportError for plotly/matplotlib**
   ```bash
   pip install --upgrade plotly matplotlib seaborn
   ```

2. **Charts not displaying**
   - For Jupyter notebooks: `pip install jupyter`
   - For static images: `pip install kaleido`

3. **Data loading errors**
   - Check CSV format and encoding
   - Ensure required columns exist
   - Try different date formats

4. **Permission errors on save**
   - Check write permissions for output directories
   - Run with appropriate user permissions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open-source and available under the MIT License.

## 📞 Support

For questions or issues:
1. Check the examples in the `examples/` directory
2. Review the troubleshooting section
3. Create an issue with your specific problem

## 🎉 Example Screenshots

The tool generates professional-looking visualizations like:
- Interactive time series with hover details
- Colorful pie charts for regional analysis
- Professional bar charts for product comparison
- Comprehensive dashboards with multiple views

Start exploring your sales data today! 🚀