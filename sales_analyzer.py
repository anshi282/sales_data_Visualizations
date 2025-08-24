import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
import os
from config import COLORS, PLOTLY_CONFIG, CHARTS_DIR
warnings.filterwarnings('ignore')

class SalesVisualizationTool:
    def __init__(self):
        """Initialize the Sales Visualization Tool"""
        self.data = None
        self.processed_data = None
        
        # Set plotting styles
        plt.style.use('default')
        sns.set_palette(COLORS['palette'])
        
    def generate_sample_data(self, num_records=1000):
        """Generate sample sales data for demonstration"""
        np.random.seed(42)
        
        # Date range
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2024, 12, 31)
        date_range = pd.date_range(start_date, end_date, freq='D')
        
        # Sample data generation
        data = []
        products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Mouse', 'Keyboard', 'Monitor']
        regions = ['North', 'South', 'East', 'West', 'Central']
        sales_reps = [f'Rep_{i}' for i in range(1, 21)]
        
        for _ in range(num_records):
            record = {
                'Date': np.random.choice(date_range),
                'Product': np.random.choice(products),
                'Region': np.random.choice(regions),
                'Sales_Rep': np.random.choice(sales_reps),
                'Quantity': np.random.randint(1, 50),
                'Unit_Price': np.random.uniform(50, 2000),
                'Customer_ID': f'CUST_{np.random.randint(1000, 9999)}'
            }
            record['Total_Sales'] = record['Quantity'] * record['Unit_Price']
            data.append(record)
        
        self.data = pd.DataFrame(data)
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data['Month'] = self.data['Date'].dt.to_period('M')
        self.data['Quarter'] = self.data['Date'].dt.to_period('Q')
        
        print(f"Generated {len(self.data)} sales records")
        
        # Save sample data
        os.makedirs('data', exist_ok=True)
        self.data.to_csv(os.path.join('data', 'sample_sales_data.csv'), index=False)
        
        return self.data
    
    def load_data(self, file_path):
        """Load sales data from CSV file"""
        try:
            self.data = pd.read_csv(file_path)
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            print(f"Loaded {len(self.data)} records from {file_path}")
            return self.data
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
    
    def data_summary(self):
        """Display data summary and statistics"""
        if self.data is None:
            print("No data loaded. Please load data first.")
            return
        
        print("=== DATA SUMMARY ===")
        print(f"Shape: {self.data.shape}")
        print(f"Date Range: {self.data['Date'].min()} to {self.data['Date'].max()}")
        print(f"Total Sales: ${self.data['Total_Sales'].sum():,.2f}")
        print(f"Average Sale: ${self.data['Total_Sales'].mean():.2f}")
        print("\n=== TOP PRODUCTS ===")
        print(self.data.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False).head())
        print("\n=== SALES BY REGION ===")
        print(self.data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False))
    
    def save_chart(self, fig, filename, chart_type='plotly'):
        """Save chart to file"""
        os.makedirs(CHARTS_DIR, exist_ok=True)
        filepath = os.path.join(CHARTS_DIR, filename)
        
        try:
            if chart_type == 'plotly':
                fig.write_html(f"{filepath}.html")
                fig.write_image(f"{filepath}.png")
            else:
                fig.savefig(f"{filepath}.png", dpi=300, bbox_inches='tight')
            print(f"Chart saved: {filepath}")
        except Exception as e:
            print(f"Error saving chart: {e}")
    
    def create_time_series_plot(self, interactive=True):
        """Create time series plot of sales over time"""
        if self.data is None:
            print("No data available")
            return
        
        daily_sales = self.data.groupby('Date')['Total_Sales'].sum().reset_index()
        
        if interactive:
            fig = px.line(daily_sales, x='Date', y='Total_Sales',
                         title='Daily Sales Trend',
                         labels={'Total_Sales': 'Sales ($)', 'Date': 'Date'},
                         color_discrete_sequence=[COLORS['primary']])
            fig.update_layout(hovermode='x unified')
            fig.show(config=PLOTLY_CONFIG)
            self.save_chart(fig, 'time_series_plot')
        else:
            plt.figure(figsize=(12, 6))
            plt.plot(daily_sales['Date'], daily_sales['Total_Sales'], 
                    color=COLORS['primary'], linewidth=2)
            plt.title('Daily Sales Trend', fontsize=16, fontweight='bold')
            plt.xlabel('Date', fontsize=12)
            plt.ylabel('Sales ($)', fontsize=12)
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            self.save_chart(plt, 'time_series_plot_static', 'matplotlib')
            plt.show()
    
    def create_product_analysis(self, interactive=True):
        """Create product performance analysis"""
        if self.data is None:
            print("No data available")
            return
        
        product_sales = self.data.groupby('Product').agg({
            'Total_Sales': 'sum',
            'Quantity': 'sum',
            'Customer_ID': 'nunique'
        }).reset_index()
        
        if interactive:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Sales by Product', 'Quantity Sold', 
                               'Customers per Product', 'Average Sale per Product'),
                specs=[[{"type": "bar"}, {"type": "bar"}],
                       [{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Sales by product
            fig.add_trace(go.Bar(x=product_sales['Product'], y=product_sales['Total_Sales'],
                               name='Total Sales', marker_color=COLORS['primary']), row=1, col=1)
            
            # Quantity sold
            fig.add_trace(go.Bar(x=product_sales['Product'], y=product_sales['Quantity'],
                               name='Quantity', marker_color=COLORS['secondary']), row=1, col=2)
            
            # Unique customers
            fig.add_trace(go.Bar(x=product_sales['Product'], y=product_sales['Customer_ID'],
                               name='Customers', marker_color=COLORS['success']), row=2, col=1)
            
            # Average sale per product
            avg_sales = self.data.groupby('Product')['Total_Sales'].mean()
            fig.add_trace(go.Bar(x=avg_sales.index, y=avg_sales.values,
                               name='Avg Sale', marker_color=COLORS['warning']), row=2, col=2)
            
            fig.update_layout(height=800, title_text="Product Analysis Dashboard", showlegend=False)
            fig.show(config=PLOTLY_CONFIG)
            self.save_chart(fig, 'product_analysis')
        else:
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
            
            # Sales by product
            product_sales.plot(x='Product', y='Total_Sales', kind='bar', ax=ax1, color=COLORS['primary'])
            ax1.set_title('Sales by Product', fontweight='bold')
            ax1.set_ylabel('Total Sales ($)')
            ax1.tick_params(axis='x', rotation=45)
            
            # Quantity sold
            product_sales.plot(x='Product', y='Quantity', kind='bar', ax=ax2, color=COLORS['secondary'])
            ax2.set_title('Quantity Sold by Product', fontweight='bold')
            ax2.set_ylabel('Quantity')
            ax2.tick_params(axis='x', rotation=45)
            
            # Customers per product
            product_sales.plot(x='Product', y='Customer_ID', kind='bar', ax=ax3, color=COLORS['success'])
            ax3.set_title('Unique Customers per Product', fontweight='bold')
            ax3.set_ylabel('Number of Customers')
            ax3.tick_params(axis='x', rotation=45)
            
            # Average sale per product
            avg_sales = self.data.groupby('Product')['Total_Sales'].mean()
            avg_sales.plot(kind='bar', ax=ax4, color=COLORS['warning'])
            ax4.set_title('Average Sale per Product', fontweight='bold')
            ax4.set_ylabel('Average Sale ($)')
            ax4.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            self.save_chart(plt, 'product_analysis_static', 'matplotlib')
            plt.show()
    
    def create_regional_analysis(self, interactive=True):
        """Create regional sales analysis"""
        if self.data is None:
            print("No data available")
            return
        
        regional_data = self.data.groupby('Region').agg({
            'Total_Sales': 'sum',
            'Quantity': 'sum',
            'Customer_ID': 'nunique'
        }).reset_index()
        
        if interactive:
            fig = px.pie(regional_data, values='Total_Sales', names='Region',
                        title='Sales Distribution by Region',
                        hover_data=['Quantity', 'Customer_ID'],
                        color_discrete_sequence=COLORS['palette'])
            fig.show(config=PLOTLY_CONFIG)
            self.save_chart(fig, 'regional_analysis')
        else:
            plt.figure(figsize=(10, 8))
            colors = COLORS['palette'][:len(regional_data)]
            plt.pie(regional_data['Total_Sales'], labels=regional_data['Region'], 
                   autopct='%1.1f%%', colors=colors)
            plt.title('Sales Distribution by Region', fontsize=16, fontweight='bold')
            plt.axis('equal')
            self.save_chart(plt, 'regional_analysis_static', 'matplotlib')
            plt.show()
    
    def create_sales_rep_performance(self, top_n=10, interactive=True):
        """Analyze sales representative performance"""
        if self.data is None:
            print("No data available")
            return
        
        rep_performance = self.data.groupby('Sales_Rep').agg({
            'Total_Sales': 'sum',
            'Customer_ID': 'nunique',
            'Date': 'count'
        }).rename(columns={'Date': 'Transactions'}).reset_index()
        
        rep_performance['Avg_Sale'] = rep_performance['Total_Sales'] / rep_performance['Transactions']
        top_reps = rep_performance.nlargest(top_n, 'Total_Sales')
        
        if interactive:
            fig = px.bar(top_reps, x='Sales_Rep', y='Total_Sales',
                        title=f'Top {top_n} Sales Representatives',
                        hover_data=['Customer_ID', 'Transactions', 'Avg_Sale'],
                        color='Total_Sales',
                        color_continuous_scale='blues')
            fig.update_xaxes(tickangle=45)
            fig.show(config=PLOTLY_CONFIG)
            self.save_chart(fig, 'sales_rep_performance')
        else:
            plt.figure(figsize=(12, 6))
            plt.bar(top_reps['Sales_Rep'], top_reps['Total_Sales'], color=COLORS['primary'])
            plt.title(f'Top {top_n} Sales Representatives', fontsize=16, fontweight='bold')
            plt.xlabel('Sales Representative')
            plt.ylabel('Total Sales ($)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            self.save_chart(plt, 'sales_rep_performance_static', 'matplotlib')
            plt.show()
    
    def create_monthly_trends(self, interactive=True):
        """Create monthly sales trends analysis"""
        if self.data is None:
            print("No data available")
            return
        
        monthly_data = self.data.groupby(['Month', 'Product'])['Total_Sales'].sum().reset_index()
        monthly_data['Month_str'] = monthly_data['Month'].astype(str)
        
        if interactive:
            fig = px.line(monthly_data, x='Month_str', y='Total_Sales', color='Product',
                         title='Monthly Sales Trends by Product',
                         labels={'Month_str': 'Month', 'Total_Sales': 'Sales ($)'},
                         color_discrete_sequence=COLORS['palette'])
            fig.update_xaxes(tickangle=45)
            fig.show(config=PLOTLY_CONFIG)
            self.save_chart(fig, 'monthly_trends')
        else:
            plt.figure(figsize=(14, 8))
            for i, product in enumerate(monthly_data['Product'].unique()):
                product_data = monthly_data[monthly_data['Product'] == product]
                plt.plot(product_data['Month_str'], product_data['Total_Sales'], 
                        marker='o', label=product, color=COLORS['palette'][i % len(COLORS['palette'])])
            
            plt.title('Monthly Sales Trends by Product', fontsize=16, fontweight='bold')
            plt.xlabel('Month')
            plt.ylabel('Sales ($)')
            plt.legend()
            plt.xticks(rotation=45)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            self.save_chart(plt, 'monthly_trends_static', 'matplotlib')
            plt.show()
    
    def create_correlation_heatmap(self):
        """Create correlation heatmap of numerical variables"""
        if self.data is None:
            print("No data available")
            return
        
        # Select numerical columns
        numerical_cols = ['Quantity', 'Unit_Price', 'Total_Sales']
        if all(col in self.data.columns for col in numerical_cols):
            corr_matrix = self.data[numerical_cols].corr()
            
            plt.figure(figsize=(8, 6))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, fmt='.2f', cbar_kws={'label': 'Correlation'})
            plt.title('Correlation Heatmap of Sales Metrics', fontsize=16, fontweight='bold')
            plt.tight_layout()
            self.save_chart(plt, 'correlation_heatmap', 'matplotlib')
            plt.show()
        else:
            print("Required numerical columns not found")
    
    def create_comprehensive_dashboard(self):
        """Create a comprehensive interactive dashboard"""
        if self.data is None:
            print("No data available")
            return
        
        # Prepare data
        daily_sales = self.data.groupby('Date')['Total_Sales'].sum()
        monthly_sales = self.data.groupby(self.data['Date'].dt.to_period('M'))['Total_Sales'].sum()
        product_sales = self.data.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)
        regional_sales = self.data.groupby('Region')['Total_Sales'].sum()
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Daily Sales Trend', 'Sales by Region', 
                          'Monthly Sales', 'Top Products',
                          'Sales Rep Performance', 'Sales Distribution'),
            specs=[[{"colspan": 2}, None],
                   [{"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "histogram"}]]
        )
        
        # Daily sales trend
        fig.add_trace(go.Scatter(x=daily_sales.index, y=daily_sales.values,
                               mode='lines', name='Daily Sales', 
                               line=dict(color=COLORS['primary'])), row=1, col=1)
        
        # Monthly sales
        fig.add_trace(go.Bar(x=[str(x) for x in monthly_sales.index], y=monthly_sales.values,
                           name='Monthly Sales', marker_color=COLORS['secondary']), row=2, col=1)
        
        # Regional pie chart
        fig.add_trace(go.Pie(labels=regional_sales.index, values=regional_sales.values,
                           name='Regional Sales'), row=2, col=2)
        
        # Top products
        top_products = product_sales.head(10)
        fig.add_trace(go.Bar(x=top_products.values, y=top_products.index,
                           orientation='h', name='Top Products',
                           marker_color=COLORS['success']), row=3, col=1)
        
        # Sales distribution histogram
        fig.add_trace(go.Histogram(x=self.data['Total_Sales'], nbinsx=30,
                                 name='Sales Distribution',
                                 marker_color=COLORS['warning']), row=3, col=2)
        
        fig.update_layout(height=1200, title_text="Sales Analytics Dashboard",
                         showlegend=False)
        fig.show(config=PLOTLY_CONFIG)
        self.save_chart(fig, 'comprehensive_dashboard')
    
    def export_summary_report(self, filename=None):
        """Export a summary report to HTML"""
        if self.data is None:
            print("No data available")
            return
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sales_report_{timestamp}.html"
        
        # Generate summary statistics
        total_sales = self.data['Total_Sales'].sum()
        avg_sale = self.data['Total_Sales'].mean()
        total_transactions = len(self.data)
        date_range = f"{self.data['Date'].min().strftime('%Y-%m-%d')} to {self.data['Date'].max().strftime('%Y-%m-%d')}"
        
        top_products = self.data.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False).head()
        top_regions = self.data.groupby('Region')['Total_Sales'].sum().sort_values(ascending=False).head()
        top_reps = self.data.groupby('Sales_Rep')['Total_Sales'].sum().sort_values(ascending=False).head()
        
        # Create HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Sales Analysis Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 40px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; }}
                .summary {{ background-color: #f5f5f5; padding: 20px; margin: 20px 0; }}
                .metric {{ display: inline-block; margin: 10px 20px; }}
                table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Sales Analysis Report</h1>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            
            <div class="summary">
                <h2>Executive Summary</h2>
                <div class="metric"><strong>Total Sales:</strong> ${total_sales:,.2f}</div>
                <div class="metric"><strong>Average Sale:</strong> ${avg_sale:.2f}</div>
                <div class="metric"><strong>Total Transactions:</strong> {total_transactions:,}</div>
                <div class="metric"><strong>Date Range:</strong> {date_range}</div>
            </div>
            
            <h2>Top Products by Sales</h2>
            <table>
                <tr><th>Product</th><th>Total Sales</th></tr>
                {''.join([f"<tr><td>{prod}</td><td>${sales:,.2f}</td></tr>" for prod, sales in top_products.items()])}
            </table>
            
            <h2>Top Regions by Sales</h2>
            <table>
                <tr><th>Region</th><th>Total Sales</th></tr>
                {''.join([f"<tr><td>{region}</td><td>${sales:,.2f}</td></tr>" for region, sales in top_regions.items()])}
            </table>
            
            <h2>Top Sales Representatives</h2>
            <table>
                <tr><th>Sales Rep</th><th>Total Sales</th></tr>
                {''.join([f"<tr><td>{rep}</td><td>${sales:,.2f}</td></tr>" for rep, sales in top_reps.items()])}
            </table>
        </body>
        </html>
        """
        
        # Save report
        report_path = os.path.join('output', 'reports', filename)
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        print(f"Summary report exported to: {report_path}")
        return report_path