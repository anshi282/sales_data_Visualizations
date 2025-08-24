"""
Main entry point for Sales Visualization Tool
Run this file to start the application
"""
import os
import sys
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from sales_analyzer import SalesVisualizationTool
from config import DATA_DIR, OUTPUT_DIR, CHARTS_DIR, REPORTS_DIR

def ensure_directories():
    """Create necessary directories if they don't exist"""
    directories = [DATA_DIR, OUTPUT_DIR, CHARTS_DIR, REPORTS_DIR]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    print("✓ Directory structure verified")

def main():
    """Main function to run the sales visualization tool"""
    print("=" * 50)
    print("Sales Data Visualization Tool")
    print("=" * 50)
    
    # Ensure directories exist
    ensure_directories()
    
    # Initialize the tool
    sales_tool = SalesVisualizationTool()
    
    # Menu system
    while True:
        print("\nWhat would you like to do?")
        print("1. Generate sample data and run demo")
        print("2. Load data from CSV file")
        print("3. View data summary")
        print("4. Create time series plot")
        print("5. Create product analysis")
        print("6. Create regional analysis")
        print("7. Create sales rep performance")
        print("8. Create monthly trends")
        print("9. Create correlation heatmap")
        print("10. Create comprehensive dashboard")
        print("11. Generate full report")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-11): ").strip()
        
        if choice == "0":
            print("Thank you for using Sales Visualization Tool!")
            break
        
        elif choice == "1":
            print("\nGenerating sample data...")
            sales_tool.generate_sample_data(1500)
            sales_tool.data_summary()
            
            print("\nRunning demo with all visualizations...")
            run_demo(sales_tool)
            
        elif choice == "2":
            file_path = input("Enter the path to your CSV file: ").strip()
            if os.path.exists(file_path):
                sales_tool.load_data(file_path)
            else:
                print(f"File not found: {file_path}")
        
        elif choice == "3":
            sales_tool.data_summary()
        
        elif choice == "4":
            if sales_tool.data is not None:
                sales_tool.create_time_series_plot(interactive=True)
            else:
                print("Please load data first (option 1 or 2)")
        
        elif choice == "5":
            if sales_tool.data is not None:
                sales_tool.create_product_analysis(interactive=True)
            else:
                print("Please load data first (option 1 or 2)")
        
        elif choice == "6":
            if sales_tool.data is not None:
                sales_tool.create_regional_analysis(interactive=True)
            else:
                print("Please load data first (option 1 or 2)")
        
        elif choice == "7":
            if sales_tool.data is not None:
                sales_tool.create_sales_rep_performance(interactive=True)
            else:
                print("Please load data first (option 1 or 2)")
        
        elif choice == "8":
            if sales_tool.data is not None:
                sales_tool.create_monthly_trends(interactive=True)
            else:
                print("Please load data first (option 1 or 2)")
        
        elif choice == "9":
            if sales_tool.data is not None:
                sales_tool.create_correlation_heatmap()
            else:
                print("Please load data first (option 1 or 2)")
        
        elif choice == "10":
            if sales_tool.data is not None:
                sales_tool.create_comprehensive_dashboard()
            else:
                print("Please load data first (option 1 or 2)")
        
        elif choice == "11":
            if sales_tool.data is not None:
                generate_full_report(sales_tool)
            else:
                print("Please load data first (option 1 or 2)")
        
        else:
            print("Invalid choice. Please try again.")

def run_demo(sales_tool):
    """Run a complete demo of all visualizations"""
    try:
        print("Creating time series plot...")
        sales_tool.create_time_series_plot(interactive=True)
        
        print("Creating product analysis...")
        sales_tool.create_product_analysis(interactive=True)
        
        print("Creating regional analysis...")
        sales_tool.create_regional_analysis(interactive=True)
        
        print("Creating sales rep performance...")
        sales_tool.create_sales_rep_performance(interactive=True)
        
        print("Creating monthly trends...")
        sales_tool.create_monthly_trends(interactive=True)
        
        print("Creating correlation heatmap...")
        sales_tool.create_correlation_heatmap()
        
        print("Creating comprehensive dashboard...")
        sales_tool.create_comprehensive_dashboard()
        
        print("✓ Demo completed successfully!")
        
    except Exception as e:
        print(f"Error during demo: {e}")

def generate_full_report(sales_tool):
    """Generate a comprehensive report with all analyses"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(REPORTS_DIR, f"sales_report_{timestamp}.html")
        
        print(f"Generating comprehensive report...")
        print(f"Report will be saved to: {report_file}")
        
        # Generate all static plots for the report
        sales_tool.create_time_series_plot(interactive=False)
        sales_tool.create_product_analysis(interactive=False)
        sales_tool.create_regional_analysis(interactive=False)
        sales_tool.create_sales_rep_performance(interactive=False)
        sales_tool.create_monthly_trends(interactive=False)
        sales_tool.create_correlation_heatmap()
        
        print(f"✓ Report generated successfully!")
        print(f"Check the {REPORTS_DIR} directory for output files")
        
    except Exception as e:
        print(f"Error generating report: {e}")

if __name__ == "__main__":
    main()