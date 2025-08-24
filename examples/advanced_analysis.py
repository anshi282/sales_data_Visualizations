"""
Advanced analysis examples for Sales Visualization Tool
This demonstrates advanced features and custom analytics
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sales_analyzer import SalesVisualizationTool
from visualizations import ChartGenerator, AdvancedAnalytics
from utils import DataProcessor, ReportGenerator
import pandas as pd
import numpy as np

def advanced_time_series_analysis():
    """Advanced time series analysis example"""
    print("=== Advanced Time Series Analysis ===")
    
    # Initialize tools
    sales_tool = SalesVisualizationTool()
    chart_gen = ChartGenerator()
    
    # Generate sample data
    sales_tool.generate_sample_data(2000)
    chart_gen.set_data(sales_tool.data)
    
    # Create advanced time series with multiple groupings
    print("Creating advanced time series plot...")
    fig = chart_gen.create_advanced_time_series(
        date_col='Date', 
        value_col='Total_Sales', 
        group_col='Product'
    )
    fig.show()
    
    # Seasonality analysis
    analytics = AdvancedAnalytics(sales_tool.data)
    print("Calculating seasonality patterns...")
    seasonality = analytics.calculate_seasonality()
    
    if seasonality:
        print("Seasonality analysis completed!")
        print(f"Trend component range: {seasonality['trend'].min():.2f} to {seasonality['trend'].max():.2f}")

def customer_segmentation_analysis():
    """Customer segmentation using RFM analysis"""
    print("\n=== Customer Segmentation Analysis ===")
    
    sales_tool = SalesVisualizationTool()
    sales_tool.generate_sample_data(1500)
    
    analytics = AdvancedAnalytics(sales_tool.data)
    
    # Perform RFM analysis
    print("Performing RFM (Recency, Frequency, Monetary) analysis...")
    rfm_results = analytics.customer_segmentation()
    
    if rfm_results is not None:
        print(f"Analyzed {len(rfm_results)} customers")
        print("\nTop 10 customers by RFM score:")
        print(rfm_results.head(10))
        
        # Create visualization of customer segments
        chart_gen = ChartGenerator(rfm_results.reset_index())
        fig = chart_gen.create_scatter_matrix(['Recency', 'Frequency', 'Monetary'])
        fig.show()

def advanced_product_analysis():
    """Advanced product performance analysis"""
    print("\n=== Advanced Product Analysis ===")
    
    sales_tool = SalesVisualizationTool()
    sales_tool.generate_sample_data(1200)
    
    chart_gen = ChartGenerator(sales_tool.data)
    
    # Create treemap for product hierarchy
    print("Creating product treemap...")
    fig = chart_gen.create_treemap(
        data_col='Product',
        size_col='Total_Sales',
        color_col='Quantity',
        title="Product Sales Treemap"
    )
    fig.show()
    
    # Product performance radar chart
    product_metrics = sales_tool.data.groupby('Product').agg({
        'Total_Sales': 'sum',
        'Quantity': 'sum',
        'Customer_ID': 'nunique'
    }).reset_index()
    
    # Normalize metrics for radar chart
    for col in ['Total_Sales', 'Quantity', 'Customer_ID']:
        product_metrics[f'{col}_norm'] = (product_metrics[col] / product_metrics[col].max()) * 100
    
    # Create radar chart for top product
    top_product = product_metrics.loc[product_metrics['Total_Sales'].idxmax()]
    categories = ['Sales Volume', 'Quantity Sold', 'Customer Reach']
    values = [top_product['Total_Sales_norm'], top_product['Quantity_norm'], top_product['Customer_ID_norm']]
    
    fig = chart_gen.create_radar_chart(categories, values, 
                                     f"Performance Profile: {top_product['Product']}")
    fig.show()

def sales_forecasting_example():
    """Sales forecasting example"""
    print("\n=== Sales Forecasting Analysis ===")
    
    sales_tool = SalesVisualizationTool()
    sales_tool.generate_sample_data(1000)
    
    analytics = AdvancedAnalytics(sales_tool.data)
    
    # Generate forecast
    print("Generating 30-day sales forecast...")
    forecast_results = analytics.forecast_sales(periods=30)
    
    if forecast_results:
        print(f"Model R² score: {forecast_results['model_score']:.3f}")
        print(f"Forecast period: {forecast_results['forecast'].index[0]} to {forecast_results['forecast'].index[-1]}")
        
        # Create visualization combining historical and forecast data
        import plotly.graph_objects as go
        
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=forecast_results['historical'].index,
            y=forecast_results['historical'].values,
            mode='lines',
            name='Historical Sales',
            line=dict(color='blue')
        ))
        
        # Forecast data
        fig.add_trace(go.Scatter(
            x=forecast_results['forecast'].index,
            y=forecast_results['forecast'].values,
            mode='lines',
            name='Forecasted Sales',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title="Sales Forecast - 30 Days",
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            hovermode='x unified'
        )
        
        fig.show()

def growth_analysis():
    """Growth rate analysis example"""
    print("\n=== Growth Rate Analysis ===")
    
    sales_tool = SalesVisualizationTool()
    sales_tool.generate_sample_data(1800)
    
    analytics = AdvancedAnalytics(sales_tool.data)
    
    # Calculate monthly growth rates
    print("Calculating monthly growth rates...")
    growth_data = analytics.calculate_growth_rates(period='M')
    
    if growth_data:
        print(f"Average monthly growth rate: {growth_data['growth_rates'].mean():.2f}%")
        print(f"Total cumulative growth: {growth_data['cumulative_growth'].iloc[-1]:.2f}%")
        
        # Create waterfall chart for growth analysis
        chart_gen = ChartGenerator()
        
        # Prepare data for waterfall chart
        monthly_values = growth_data['values'].dropna()
        categories = [str(date) for date in monthly_values.index]
        values = monthly_values.values
        
        # Create changes for waterfall
        changes = [values[0]] + [values[i] - values[i-1] for i in range(1, len(values))]
        
        fig = chart_gen.create_waterfall_chart(
            categories[:6],  # Show first 6 months
            changes[:6],
            title="Monthly Sales Growth Waterfall"
        )
        fig.show()

def comprehensive_data_quality_report():
    """Generate comprehensive data quality report"""
    print("\n=== Data Quality Analysis ===")
    
    sales_tool = SalesVisualizationTool()
    sales_tool.generate_sample_data(1000)
    
    # Add some data quality issues for demonstration
    data = sales_tool.data.copy()
    
    # Introduce missing values
    data.loc[np.random.choice(data.index, 50), 'Product'] = np.nan
    data.loc[np.random.choice(data.index, 30), 'Total_Sales'] = np.nan
    
    # Introduce negative sales
    data.loc[np.random.choice(data.index, 20), 'Total_Sales'] = -abs(data.loc[np.random.choice(data.index, 20), 'Total_Sales'])
    
    from utils import ValidationUtils
    
    # Validate data
    validation_results = ValidationUtils.validate_sales_data(data)
    quality_score = ValidationUtils.data_quality_score(data)
    
    print(f"Data Quality Score: {quality_score:.1f}/100")
    print(f"Validation Status: {'PASSED' if validation_results['is_valid'] else 'FAILED'}")
    
    if validation_results['errors']:
        print(f"Errors: {len(validation_results['errors'])}")
        for error in validation_results['errors']:
            print(f"  - {error}")
    
    if validation_results['warnings']:
        print(f"Warnings: {len(validation_results['warnings'])}")
        for warning in validation_results['warnings']:
            print(f"  - {warning}")
    
    if validation_results['suggestions']:
        print("Suggestions:")
        for suggestion in validation_results['suggestions']:
            print(f"  - {suggestion}")

def performance_benchmarking():
    """Performance benchmarking and optimization"""
    print("\n=== Performance Benchmarking ===")
    
    sales_tool = SalesVisualizationTool()
    
    # Test with different data sizes
    sizes = [500, 1000, 2000, 5000]
    
    for size in sizes:
        print(f"\nTesting with {size} records...")
        
        import time
        start_time = time.time()
        
        # Generate data
        sales_tool.generate_sample_data(size)
        
        # Create visualizations
        sales_tool.create_time_series_plot(interactive=False)  # Use static for speed
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"Processing time: {processing_time:.2f} seconds")
        print(f"Records per second: {size/processing_time:.0f}")
        
        # Memory optimization
        from utils import PerformanceUtils
        optimized_data = PerformanceUtils.optimize_dataframe(sales_tool.data.copy())

def export_comprehensive_report():
    """Export comprehensive analysis to multiple formats"""
    print("\n=== Comprehensive Report Export ===")
    
    sales_tool = SalesVisualizationTool()
    sales_tool.generate_sample_data(1500)
    
    # Generate HTML report
    report_file = sales_tool.export_summary_report()
    print(f"HTML report generated: {report_file}")
    
    # Generate Excel report
    report_gen = ReportGenerator(sales_tool.data)
    excel_file = os.path.join('output', 'reports', 'comprehensive_analysis.xlsx')
    os.makedirs(os.path.dirname(excel_file), exist_ok=True)
    report_gen.export_to_excel(excel_file)
    
    # Save all charts
    chart_gen = ChartGenerator(sales_tool.data)
    
    # Time series
    fig = chart_gen.create_advanced_time_series()
    chart_gen.save_chart(fig, 'advanced_time_series', 'html')
    
    # Treemap
    fig = chart_gen.create_treemap('Product', 'Total_Sales')
    chart_gen.save_chart(fig, 'product_treemap', 'html')
    
    print("All reports and charts exported successfully!")

def main():
    """Run all advanced analysis examples"""
    print("🚀 Advanced Sales Analysis Examples")
    print("=" * 50)
    
    try:
        advanced_time_series_analysis()
        customer_segmentation_analysis()
        advanced_product_analysis()
        sales_forecasting_example()
        growth_analysis()
        comprehensive_data_quality_report()
        performance_benchmarking()
        export_comprehensive_report()
        
        print("\n✅ All advanced analysis examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()