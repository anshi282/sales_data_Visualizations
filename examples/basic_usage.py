"""
Basic usage example for Sales Visualization Tool
This script demonstrates how to use the tool with minimal setup
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from sales_analyzer import SalesVisualizationTool

def basic_example():
    """Basic example of using the sales visualization tool"""
    
    print("=== Basic Usage Example ===")
    
    # Initialize the tool
    sales_tool = SalesVisualizationTool()
    
    # Generate sample data for demonstration
    print("1. Generating sample data...")
    sales_tool.generate_sample_data(500)
    
    # Show data summary
    print("\n2. Data Summary:")
    sales_tool.data_summary()
    
    # Create basic visualizations
    print("\n3. Creating visualizations...")
    
    # Time series plot
    print("Creating time series plot...")
    sales_tool.create_time_series_plot(interactive=True)
    
    # Product analysis
    print("Creating product analysis...")
    sales_tool.create_product_analysis(interactive=True)
    
    # Regional analysis
    print("Creating regional analysis...")
    sales_tool.create_regional_analysis(interactive=True)
    
    print("\n4. Basic example completed!")

def load_custom_data_example():
    """Example of loading custom data"""
    
    print("\n=== Custom Data Loading Example ===")
    
    sales_tool = SalesVisualizationTool()
    
    # Example CSV file path (replace with your actual file)
    csv_file = "data/your_sales_data.csv"
    
    if os.path.exists(csv_file):
        print(f"Loading data from {csv_file}...")
        sales_tool.load_data(csv_file)
        sales_tool.data_summary()
    else:
        print(f"File {csv_file} not found. Using sample data instead.")
        sales_tool.generate_sample_data(300)
    
    # Create a simple dashboard
    sales_tool.create_comprehensive_dashboard()

if __name__ == "__main__":
    # Run basic example
    basic_example()
    
    # Run custom data example
    load_custom_data_example()