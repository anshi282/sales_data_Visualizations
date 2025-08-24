"""
Advanced visualization components for the Sales Analysis Tool
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import os
from config import COLORS, PLOTLY_CONFIG, CHARTS_DIR

class ChartGenerator:
    """Advanced chart generation class with customization options"""
    
    def __init__(self, data=None, theme='plotly_white'):
        self.data = data
        self.theme = theme
        self.color_palette = COLORS['palette']
    
    def set_data(self, data):
        """Set the data for visualization"""
        self.data = data
    
    def create_advanced_time_series(self, date_col='Date', value_col='Total_Sales', 
                                   group_col=None, aggregate='sum'):
        """
        Create advanced time series with multiple grouping options
        
        Args:
            date_col (str): Date column name
            value_col (str): Value column name
            group_col (str): Optional grouping column
            aggregate (str): Aggregation method ('sum', 'mean', 'count')
        """
        if self.data is None:
            raise ValueError("No data provided")
        
        # Prepare data
        if group_col:
            grouped_data = self.data.groupby([pd.Grouper(key=date_col, freq='D'), group_col])[value_col].agg(aggregate).reset_index()
            
            fig = px.line(grouped_data, x=date_col, y=value_col, color=group_col,
                         title=f'{value_col} Trend by {group_col}',
                         color_discrete_sequence=self.color_palette)
        else:
            daily_data = self.data.groupby(date_col)[value_col].agg(aggregate).reset_index()
            
            fig = px.line(daily_data, x=date_col, y=value_col,
                         title=f'{value_col} Trend Over Time',
                         color_discrete_sequence=[COLORS['primary']])
        
        # Add range selector
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=7, label="7d", step="day", stepmode="backward"),
                        dict(count=30, label="30d", step="day", stepmode="backward"),
                        dict(count=90, label="3m", step="day", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        return fig
    
    def create_cohort_analysis(self, customer_col='Customer_ID', date_col='Date', value_col='Total_Sales'):
        """Create customer cohort analysis"""
        if self.data is None:
            raise ValueError("No data provided")
        
        # Prepare cohort data
        data = self.data.copy()
        data['Order_Period'] = data[date_col].dt.to_period('M')
        data['Cohort_Group'] = data.groupby(customer_col)[date_col].transform('min').dt.to_period('M')
        
        # Calculate period number
        data['Period_Number'] = (data['Order_Period'] - data['Cohort_Group']).apply(attrgetter('n'))
        
        # Create cohort table
        cohort_data = data.groupby(['Cohort_Group', 'Period_Number'])[customer_col].nunique().reset_index()
        cohort_counts = cohort_data.pivot(index='Cohort_Group', columns='Period_Number', values=customer_col)
        
        # Calculate cohort sizes
        cohort_sizes = data.groupby('Cohort_Group')[customer_col].nunique()
        cohort_table = cohort_counts.divide(cohort_sizes, axis=0)
        
        # Create heatmap
        plt.figure(figsize=(15, 8))
        sns.heatmap(cohort_table, annot=True, fmt='.1%', cmap='Blues')
        plt.title('Cohort Analysis - Customer Retention')
        plt.ylabel('Cohort Group')
        plt.xlabel('Period Number')
        
        return plt.gcf()
    
    def create_funnel_chart(self, stages, values, title="Sales Funnel"):
        """Create a funnel chart for sales process analysis"""
        fig = go.Figure(go.Funnel(
            y=stages,
            x=values,
            textinfo="value+percent initial",
            marker_color=self.color_palette[:len(stages)]
        ))
        
        fig.update_layout(
            title=title,
            font_size=12
        )
        
        return fig
    
    def create_treemap(self, data_col, size_col, color_col=None, title="Treemap Analysis"):
        """Create treemap visualization"""
        if self.data is None:
            raise ValueError("No data provided")
        
        treemap_data = self.data.groupby(data_col)[size_col].sum().reset_index()
        
        if color_col and color_col in self.data.columns:
            color_data = self.data.groupby(data_col)[color_col].mean().reset_index()
            treemap_data = treemap_data.merge(color_data, on=data_col)
            
            fig = px.treemap(treemap_data, path=[data_col], values=size_col,
                           color=color_col, color_continuous_scale='Viridis',
                           title=title)
        else:
            fig = px.treemap(treemap_data, path=[data_col], values=size_col,
                           title=title)
        
        return fig
    
    def create_waterfall_chart(self, categories, values, title="Waterfall Analysis"):
        """Create waterfall chart for analyzing changes"""
        fig = go.Figure(go.Waterfall(
            name="",
            orientation="v",
            measure=["relative"] * (len(categories) - 1) + ["total"],
            x=categories,
            textposition="outside",
            text=[f"+{v}" if v > 0 else str(v) for v in values],
            y=values,
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": COLORS['danger']}},
            increasing={"marker": {"color": COLORS['success']}},
            totals={"marker": {"color": COLORS['primary']}}
        ))
        
        fig.update_layout(title=title, showlegend=False)
        return fig
    
    def create_gauge_chart(self, value, max_value, title="Performance Gauge", target=None):
        """Create gauge chart for KPI display"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=value,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': title},
            delta={'reference': target if target else max_value * 0.8},
            gauge={
                'axis': {'range': [None, max_value]},
                'bar': {'color': COLORS['primary']},
                'steps': [
                    {'range': [0, max_value * 0.5], 'color': "lightgray"},
                    {'range': [max_value * 0.5, max_value * 0.8], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': target if target else max_value * 0.9
                }
            }
        ))
        
        return fig
    
    def create_scatter_matrix(self, columns):
        """Create scatter plot matrix for correlation analysis"""
        if self.data is None:
            raise ValueError("No data provided")
        
        # Filter numeric columns
        numeric_data = self.data[columns].select_dtypes(include=[np.number])
        
        fig = px.scatter_matrix(numeric_data, 
                               title="Scatter Plot Matrix",
                               color_discrete_sequence=self.color_palette)
        
        fig.update_traces(diagonal_visible=False)
        return fig
    
    def create_animated_bar_race(self, date_col, category_col, value_col, 
                                title="Animated Bar Chart Race"):
        """Create animated bar chart race"""
        if self.data is None:
            raise ValueError("No data provided")
        
        # Prepare data for animation
        data = self.data.copy()
        data[date_col] = pd.to_datetime(data[date_col])
        
        # Group by date and category
        anim_data = data.groupby([date_col, category_col])[value_col].sum().reset_index()
        
        # Create animated bar chart
        fig = px.bar(anim_data, x=value_col, y=category_col, 
                    animation_frame=date_col.replace(' ', '_'),
                    title=title,
                    orientation='h',
                    color=category_col,
                    color_discrete_sequence=self.color_palette)
        
        fig.layout.updatemenus[0].buttons[0].args[1]['frame']['duration'] = 1000
        fig.layout.updatemenus[0].buttons[0].args[1]['transition']['duration'] = 300
        
        return fig
    
    def create_candlestick_chart(self, date_col, open_col, high_col, low_col, close_col):
        """Create candlestick chart for financial-style analysis"""
        if self.data is None:
            raise ValueError("No data provided")
        
        fig = go.Figure(data=go.Candlestick(
            x=self.data[date_col],
            open=self.data[open_col],
            high=self.data[high_col],
            low=self.data[low_col],
            close=self.data[close_col]
        ))
        
        fig.update_layout(
            title="Sales Candlestick Analysis",
            xaxis_title="Date",
            yaxis_title="Sales Value",
            xaxis_rangeslider_visible=False
        )
        
        return fig
    
    def create_radar_chart(self, categories, values, title="Radar Chart Analysis"):
        """Create radar/spider chart"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Performance'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(values) * 1.1]
                )),
            title=title
        )
        
        return fig
    
    def save_chart(self, fig, filename, format='html'):
        """Save chart to file with multiple format support"""
        os.makedirs(CHARTS_DIR, exist_ok=True)
        filepath = os.path.join(CHARTS_DIR, f"{filename}.{format}")
        
        try:
            if hasattr(fig, 'write_html'):  # Plotly figure
                if format == 'html':
                    fig.write_html(filepath)
                elif format in ['png', 'jpg', 'pdf', 'svg']:
                    fig.write_image(filepath.replace('.html', f'.{format}'))
            else:  # Matplotlib figure
                fig.savefig(filepath.replace('.html', f'.{format}'), 
                           dpi=300, bbox_inches='tight')
            
            print(f"Chart saved: {filepath}")
        except Exception as e:
            print(f"Error saving chart: {e}")

class AdvancedAnalytics:
    """Advanced analytics and statistical analysis"""
    
    def __init__(self, data=None):
        self.data = data
    
    def calculate_seasonality(self, date_col='Date', value_col='Total_Sales', period=12):
        """Calculate seasonal patterns in sales data"""
        if self.data is None:
            return None
        
        from scipy import signal
        
        # Prepare time series data
        ts_data = self.data.groupby(date_col)[value_col].sum().sort_index()
        
        # Decompose time series
        from statsmodels.tsa.seasonal import seasonal_decompose
        decomposition = seasonal_decompose(ts_data, period=period)
        
        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'original': ts_data
        }
    
    def calculate_growth_rates(self, date_col='Date', value_col='Total_Sales', period='M'):
        """Calculate growth rates over specified periods"""
        if self.data is None:
            return None
        
        # Group by period
        period_data = self.data.groupby(pd.Grouper(key=date_col, freq=period))[value_col].sum()
        
        # Calculate growth rates
        growth_rates = period_data.pct_change() * 100
        
        return {
            'values': period_data,
            'growth_rates': growth_rates,
            'cumulative_growth': ((period_data / period_data.iloc[0]) - 1) * 100
        }
    
    def customer_segmentation(self, customer_col='Customer_ID', 
                            value_col='Total_Sales', date_col='Date'):
        """Perform RFM (Recency, Frequency, Monetary) analysis"""
        if self.data is None:
            return None
        
        # Calculate RFM metrics
        current_date = self.data[date_col].max()
        
        rfm = self.data.groupby(customer_col).agg({
            date_col: lambda x: (current_date - x.max()).days,  # Recency
            value_col: ['count', 'sum']  # Frequency, Monetary
        }).round(2)
        
        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        
        # Create RFM scores
        rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1])
        rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1,2,3,4,5])
        rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1,2,3,4,5])
        
        rfm['RFM_Score'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
        
        return rfm
    
    def forecast_sales(self, date_col='Date', value_col='Total_Sales', periods=30):
        """Simple sales forecasting using linear trend"""
        if self.data is None:
            return None
        
        try:
            from sklearn.linear_model import LinearRegression
            import numpy as np
            
            # Prepare data
            ts_data = self.data.groupby(date_col)[value_col].sum().sort_index()
            
            # Create features (days since start)
            X = np.arange(len(ts_data)).reshape(-1, 1)
            y = ts_data.values
            
            # Fit model
            model = LinearRegression()
            model.fit(X, y)
            
            # Make predictions
            future_X = np.arange(len(ts_data), len(ts_data) + periods).reshape(-1, 1)
            forecast = model.predict(future_X)
            
            # Create future dates
            last_date = ts_data.index[-1]
            future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), 
                                       periods=periods, freq='D')
            
            return {
                'historical': ts_data,
                'forecast': pd.Series(forecast, index=future_dates),
                'model_score': model.score(X, y)
            }
            
        except ImportError:
            print("scikit-learn not installed. Cannot perform forecasting.")
            return None