"""
Custom dashboard creation example
This shows how to create specialized dashboards for different use cases
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from sales_analyzer import SalesVisualizationTool
from visualizations import ChartGenerator
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class ExecutiveDashboard:
    """Executive-level dashboard with KPIs and high-level metrics"""
    
    def __init__(self, data):
        self.data = data
        self.chart_gen = ChartGenerator(data)
    
    def create_kpi_cards(self):
        """Create KPI cards for key metrics"""
        kpis = {
            'Total Revenue': self.data['Total_Sales'].sum(),
            'Average Order Value': self.data['Total_Sales'].mean(),
            'Total Orders': len(self.data),
            'Unique Customers': self.data['Customer_ID'].nunique() if 'Customer_ID' in self.data.columns else 'N/A'
        }
        
        # Create gauge charts for each KPI
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=list(kpis.keys()),
            specs=[[{"type": "indicator"}, {"type": "indicator"}],
                   [{"type": "indicator"}, {"type": "indicator"}]]
        )
        
        positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        
        for i, (title, value) in enumerate(kpis.items()):
            if isinstance(value, (int, float)):
                max_val = value * 1.2 if value > 0 else 100
                
                fig.add_trace(go.Indicator(
                    mode="number+gauge",
                    value=value,
                    title={"text": title},
                    gauge={
                        'axis': {'range': [0, max_val]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, max_val * 0.6], 'color': "lightgray"},
                            {'range': [max_val * 0.6, max_val * 0.9], 'color': "gray"}
                        ]
                    }
                ), row=positions[i][0], col=positions[i][1])
        
        fig.update_layout(height=600, title_text="Executive KPI Dashboard")
        return fig
    
    def create_executive_summary(self):
        """Create comprehensive executive dashboard"""
        fig = make_subplots(
            rows=3, cols=3,
            subplot_titles=['Revenue Trend', 'Top Products', 'Regional Performance',
                          'Monthly Growth', 'Sales Funnel', 'Customer Segments',
                          'Performance Score', 'Market Share', 'Forecast'],
            specs=[[{"type": "scatter"}, {"type": "bar"}, {"type": "pie"}],
                   [{"type": "bar"}, {"type": "funnel"}, {"type": "bar"}],
                   [{"type": "indicator"}, {"type": "pie"}, {"type": "scatter"}]]
        )
        
        # Revenue trend
        daily_revenue = self.data.groupby('Date')['Total_Sales'].sum()
        fig.add_trace(go.Scatter(x=daily_revenue.index, y=daily_revenue.values,
                               mode='lines', name='Revenue'), row=1, col=1)
        
        # Top products
        top_products = self.data.groupby('Product')['Total_Sales'].sum().nlargest(5)
        fig.add_trace(go.Bar(x=top_products.index, y=top_products.values,
                           name='Top Products'), row=1, col=2)
        
        # Regional performance
        regional_sales = self.data.groupby('Region')['Total_Sales'].sum()
        fig.add_trace(go.Pie(labels=regional_sales.index, values=regional_sales.values,
                           name='Regional Sales'), row=1, col=3)
        
        # Monthly growth
        monthly_data = self.data.groupby(pd.Grouper(key='Date', freq='M'))['Total_Sales'].sum()
        fig.add_trace(go.Bar(x=[str(x) for x in monthly_data.index], y=monthly_data.values,
                           name='Monthly Sales'), row=2, col=1)
        
        # Performance indicator
        total_sales = self.data['Total_Sales'].sum()
        target_sales = total_sales * 1.1  # 10% above current
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=total_sales,
            delta={'reference': target_sales},
            title={'text': "Sales vs Target"},
            gauge={'axis': {'range': [0, target_sales * 1.2]}}
        ), row=3, col=1)
        
        fig.update_layout(height=1000, title_text="Executive Dashboard")
        return fig

class SalesTeamDashboard:
    """Dashboard focused on sales team performance"""
    
    def __init__(self, data):
        self.data = data
        self.chart_gen = ChartGenerator(data)
    
    def create_sales_performance_dashboard(self):
        """Create sales team performance dashboard"""
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=['Top Performers', 'Sales by Region', 'Monthly Targets',
                          'Activity Levels', 'Conversion Rates', 'Team Leaderboard'],
            specs=[[{"type": "bar"}, {"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "bar"}, {"type": "table"}]]
        )
        
        # Top performers
        rep_performance = self.data.groupby('Sales_Rep')['Total_Sales'].sum().nlargest(10)
        fig.add_trace(go.Bar(x=rep_performance.values, y=rep_performance.index,
                           orientation='h', name='Sales Rep Performance'), row=1, col=1)
        
        # Sales by region
        regional_sales = self.data.groupby('Region')['Total_Sales'].sum()
        fig.add_trace(go.Bar(x=regional_sales.index, y=regional_sales.values,
                           name='Regional Sales'), row=1, col=2)
        
        # Activity levels (transactions per rep)
        activity_levels = self.data.groupby('Sales_Rep').size()
        sales_amounts = self.data.groupby('Sales_Rep')['Total_Sales'].sum()
        fig.add_trace(go.Scatter(x=activity_levels.values, y=sales_amounts.values,
                               mode='markers', name='Activity vs Sales'), row=2, col=1)
        
        # Team leaderboard
        leaderboard = self.data.groupby('Sales_Rep').agg({
            'Total_Sales': 'sum',
            'Customer_ID': 'nunique' if 'Customer_ID' in self.data.columns else 'count',
            'Date': 'count'
        }).round(2).sort_values('Total_Sales', ascending=False).head(10)
        
        fig.add_trace(go.Table(
            header=dict(values=['Sales Rep', 'Total Sales', 'Customers', 'Transactions']),
            cells=dict(values=[leaderboard.index,
                             leaderboard['Total_Sales'],
                             leaderboard['Customer_ID'],
                             leaderboard['Date']])
        ), row=2, col=3)
        
        fig.update_layout(height=800, title_text="Sales Team Performance Dashboard")
        return fig

class ProductAnalyticsDashboard:
    """Dashboard focused on product performance and analytics"""
    
    def __init__(self, data):
        self.data = data
        self.chart_gen = ChartGenerator(data)
    
    def create_product_analytics_dashboard(self):
        """Create comprehensive product analytics dashboard"""
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=['Product Sales Distribution', 'Product Trends Over Time',
                          'Price vs Quantity Analysis', 'Product Performance Matrix',
                          'Market Share Evolution', 'Product Profitability'],
            specs=[[{"type": "treemap"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "scatter"}],
                   [{"type": "scatter"}, {"type": "bar"}]]
        )
        
        # Product trends over time
        product_trends = self.data.groupby(['Date', 'Product'])['Total_Sales'].sum().reset_index()
        for product in product_trends['Product'].unique()[:5]:  # Top 5 products
            product_data = product_trends[product_trends['Product'] == product]
            fig.add_trace(go.Scatter(x=product_data['Date'], y=product_data['Total_Sales'],
                                   mode='lines', name=product), row=1, col=2)
        
        # Price vs Quantity analysis
        if 'Unit_Price' in self.data.columns and 'Quantity' in self.data.columns:
            fig.add_trace(go.Scatter(
                x=self.data['Unit_Price'], 
                y=self.data['Quantity'],
                mode='markers',
                text=self.data['Product'],
                name='Price vs Quantity'
            ), row=2, col=1)
        
        # Product performance matrix (Sales vs Customers)
        product_metrics = self.data.groupby('Product').agg({
            'Total_Sales': 'sum',
            'Customer_ID': 'nunique' if 'Customer_ID' in self.data.columns else 'count'
        })
        
        fig.add_trace(go.Scatter(
            x=product_metrics['Total_Sales'],
            y=product_metrics['Customer_ID'],
            mode='markers+text',
            text=product_metrics.index,
            textposition='top center',
            name='Performance Matrix'
        ), row=2, col=2)
        
        # Product profitability (if we have cost data, simulate it)
        product_sales = self.data.groupby('Product')['Total_Sales'].sum().sort_values(ascending=True)
        fig.add_trace(go.Bar(x=product_sales.values, y=product_sales.index,
                           orientation='h', name='Product Sales'), row=3, col=2)
        
        fig.update_layout(height=1200, title_text="Product Analytics Dashboard")
        return fig

class FinancialDashboard:
    """Financial performance dashboard"""
    
    def __init__(self, data):
        self.data = data
        self.chart_gen = ChartGenerator(data)
    
    def create_financial_dashboard(self):
        """Create financial performance dashboard"""
        fig = make_subplots(
            rows=2, cols=3,
            subplot_titles=['Revenue Waterfall', 'Profit Margins', 'Cash Flow Trend',
                          'Revenue Breakdown', 'Financial Ratios', 'Budget vs Actual'],
            specs=[[{"type": "waterfall"}, {"type": "bar"}, {"type": "scatter"}],
                   [{"type": "pie"}, {"type": "indicator"}, {"type": "bar"}]]
        )
        
        # Revenue waterfall
        monthly_revenue = self.data.groupby(pd.Grouper(key='Date', freq='M'))['Total_Sales'].sum()
        monthly_changes = monthly_revenue.diff().fillna(monthly_revenue.iloc[0])
        
        fig.add_trace(go.Waterfall(
            name="Revenue",
            orientation="v",
            measure=["absolute"] + ["relative"] * (len(monthly_changes) - 1),
            x=[str(x)[:7] for x in monthly_revenue.index],
            y=monthly_changes.values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "red"}},
            increasing={"marker": {"color": "green"}},
        ), row=1, col=1)
        
        # Cash flow trend
        daily_revenue = self.data.groupby('Date')['Total_Sales'].sum()
        cumulative_revenue = daily_revenue.cumsum()
        fig.add_trace(go.Scatter(x=cumulative_revenue.index, y=cumulative_revenue.values,
                               mode='lines', name='Cumulative Revenue'), row=1, col=3)
        
        # Revenue breakdown
        revenue_by_product = self.data.groupby('Product')['Total_Sales'].sum()
        fig.add_trace(go.Pie(labels=revenue_by_product.index, values=revenue_by_product.values,
                           name='Revenue Breakdown'), row=2, col=1)
        
        # Financial KPI
        total_revenue = self.data['Total_Sales'].sum()
        fig.add_trace(go.Indicator(
            mode="number+gauge",
            value=total_revenue,
            title={"text": "Total Revenue"},
            gauge={'axis': {'range': [0, total_revenue * 1.5]}}
        ), row=2, col=2)
        
        fig.update_layout(height=800, title_text="Financial Performance Dashboard")
        return fig

def create_