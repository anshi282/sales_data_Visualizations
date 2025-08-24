"""
Utility functions for data processing and analysis
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import warnings

class DataProcessor:
    """Data processing utilities"""
    
    @staticmethod
    def clean_column_names(df):
        """Clean and standardize column names"""
        df = df.copy()
        
        # Remove special characters and spaces
        df.columns = df.columns.str.replace(r'[^\w\s]', '', regex=True)
        df.columns = df.columns.str.replace(r'\s+', '_', regex=True)
        df.columns = df.columns.str.strip()
        
        # Convert to title case
        df.columns = df.columns.str.title()
        
        return df
    
    @staticmethod
    def detect_date_columns(df):
        """Automatically detect date columns in dataframe"""
        date_columns = []
        
        for col in df.columns:
            # Check column name for date-like patterns
            if any(keyword in col.lower() for keyword in ['date', 'time', 'day', 'month', 'year']):
                date_columns.append(col)
                continue
            
            # Check data content for date-like patterns
            sample_data = df[col].dropna().astype(str).head(10)
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
                r'\d{4}/\d{2}/\d{2}',  # YYYY/MM/DD
            ]
            
            for pattern in date_patterns:
                if any(re.match(pattern, str(val)) for val in sample_data):
                    date_columns.append(col)
                    break
        
        return list(set(date_columns))
    
    @staticmethod
    def convert_to_numeric(df, columns=None):
        """Convert columns to numeric, handling common formatting issues"""
        df = df.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=['object']).columns
        
        for col in columns:
            if col in df.columns:
                # Remove common currency symbols and separators
                df[col] = df[col].astype(str).str.replace(r'[$,€£¥]', '', regex=True)
                df[col] = df[col].str.replace(r'[()]', '', regex=True)  # Remove parentheses
                df[col] = df[col].str.strip()
                
                # Convert to numeric
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    @staticmethod
    def handle_missing_values(df, strategy='auto'):
        """Handle missing values with different strategies"""
        df = df.copy()
        
        if strategy == 'auto':
            for col in df.columns:
                if df[col].dtype in ['int64', 'float64']:
                    # Numeric columns: fill with median
                    df[col].fillna(df[col].median(), inplace=True)
                else:
                    # Categorical columns: fill with mode or 'Unknown'
                    mode_val = df[col].mode()
                    if len(mode_val) > 0:
                        df[col].fillna(mode_val[0], inplace=True)
                    else:
                        df[col].fillna('Unknown', inplace=True)
        
        elif strategy == 'drop':
            df.dropna(inplace=True)
        
        elif strategy == 'forward_fill':
            df.fillna(method='ffill', inplace=True)
        
        return df
    
    @staticmethod
    def detect_outliers(df, columns=None, method='iqr', threshold=1.5):
        """Detect outliers in numeric columns"""
        outliers = {}
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        for col in columns:
            if col in df.columns:
                if method == 'iqr':
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    
                    lower_bound = Q1 - threshold * IQR
                    upper_bound = Q3 + threshold * IQR
                    
                    outliers[col] = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()
                
                elif method == 'zscore':
                    z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                    outliers[col] = df[z_scores > threshold].index.tolist()
        
        return outliers
    
    @staticmethod
    def create_time_features(df, date_col):
        """Create additional time-based features from date column"""
        df = df.copy()
        
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col])
            
            # Extract time components
            df[f'{date_col}_Year'] = df[date_col].dt.year
            df[f'{date_col}_Month'] = df[date_col].dt.month
            df[f'{date_col}_Quarter'] = df[date_col].dt.quarter
            df[f'{date_col}_DayOfWeek'] = df[date_col].dt.dayofweek
            df[f'{date_col}_DayOfYear'] = df[date_col].dt.dayofyear
            df[f'{date_col}_WeekOfYear'] = df[date_col].dt.isocalendar().week
            df[f'{date_col}_IsWeekend'] = df[date_col].dt.dayofweek.isin([5, 6])
            
            # Create readable day names
            df[f'{date_col}_DayName'] = df[date_col].dt.day_name()
            df[f'{date_col}_MonthName'] = df[date_col].dt.month_name()
        
        return df
    
    @staticmethod
    def calculate_moving_averages(df, value_col, windows=[7, 30, 90]):
        """Calculate moving averages for a value column"""
        df = df.copy()
        
        for window in windows:
            df[f'{value_col}_MA_{window}'] = df[value_col].rolling(window=window, min_periods=1).mean()
        
        return df
    
    @staticmethod
    def create_categorical_features(df, columns, encoding='label'):
        """Create categorical features with different encoding methods"""
        df = df.copy()
        
        for col in columns:
            if col in df.columns:
                if encoding == 'label':
                    from sklearn.preprocessing import LabelEncoder
                    le = LabelEncoder()
                    df[f'{col}_encoded'] = le.fit_transform(df[col].astype(str))
                
                elif encoding == 'onehot':
                    # Create dummy variables
                    dummies = pd.get_dummies(df[col], prefix=col)
                    df = pd.concat([df, dummies], axis=1)
        
        return df

class ReportGenerator:
    """Generate various types of reports"""
    
    def __init__(self, data):
        self.data = data
    
    def generate_executive_summary(self):
        """Generate executive summary statistics"""
        if self.data is None:
            return "No data available"
        
        summary = {}
        
        # Basic metrics
        if 'Total_Sales' in self.data.columns:
            summary['total_sales'] = self.data['Total_Sales'].sum()
            summary['avg_sale'] = self.data['Total_Sales'].mean()
            summary['median_sale'] = self.data['Total_Sales'].median()
            summary['max_sale'] = self.data['Total_Sales'].max()
            summary['min_sale'] = self.data['Total_Sales'].min()
        
        summary['total_transactions'] = len(self.data)
        summary['unique_customers'] = self.data['Customer_ID'].nunique() if 'Customer_ID' in self.data.columns else 'N/A'
        summary['unique_products'] = self.data['Product'].nunique() if 'Product' in self.data.columns else 'N/A'
        
        # Date range
        if 'Date' in self.data.columns:
            summary['date_range'] = {
                'start': self.data['Date'].min(),
                'end': self.data['Date'].max(),
                'days': (self.data['Date'].max() - self.data['Date'].min()).days
            }
        
        return summary
    
    def generate_performance_metrics(self):
        """Generate performance metrics by different dimensions"""
        metrics = {}
        
        # Product performance
        if 'Product' in self.data.columns and 'Total_Sales' in self.data.columns:
            metrics['product_performance'] = self.data.groupby('Product').agg({
                'Total_Sales': ['sum', 'mean', 'count'],
                'Customer_ID': 'nunique' if 'Customer_ID' in self.data.columns else lambda x: len(x)
            }).round(2)
        
        # Regional performance
        if 'Region' in self.data.columns and 'Total_Sales' in self.data.columns:
            metrics['regional_performance'] = self.data.groupby('Region').agg({
                'Total_Sales': ['sum', 'mean', 'count']
            }).round(2)
        
        # Sales rep performance
        if 'Sales_Rep' in self.data.columns and 'Total_Sales' in self.data.columns:
            metrics['sales_rep_performance'] = self.data.groupby('Sales_Rep').agg({
                'Total_Sales': ['sum', 'mean', 'count'],
                'Customer_ID': 'nunique' if 'Customer_ID' in self.data.columns else lambda x: len(x)
            }).round(2).sort_values(('Total_Sales', 'sum'), ascending=False)
        
        return metrics
    
    def export_to_excel(self, filename, include_charts=False):
        """Export analysis results to Excel file"""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # Raw data
                self.data.to_excel(writer, sheet_name='Raw_Data', index=False)
                
                # Summary metrics
                summary = self.generate_executive_summary()
                summary_df = pd.DataFrame(list(summary.items()), columns=['Metric', 'Value'])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Performance metrics
                metrics = self.generate_performance_metrics()
                
                for sheet_name, data in metrics.items():
                    if isinstance(data, pd.DataFrame):
                        data.to_excel(writer, sheet_name=sheet_name.replace('_', ' ').title())
                
                print(f"Excel report exported to: {filename}")
                
        except Exception as e:
            print(f"Error exporting to Excel: {e}")

class ValidationUtils:
    """Data validation utilities"""
    
    @staticmethod
    def validate_sales_data(df, required_columns=None):
        """Validate sales data for common issues"""
        if required_columns is None:
            required_columns = ['Date', 'Product', 'Total_Sales']
        
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'suggestions': []
        }
        
        # Check required columns
        missing_cols = [col for col in required_columns if col not in df.columns]
        if missing_cols:
            validation_results['errors'].append(f"Missing required columns: {missing_cols}")
            validation_results['is_valid'] = False
        
        # Check for empty dataset
        if len(df) == 0:
            validation_results['errors'].append("Dataset is empty")
            validation_results['is_valid'] = False
            return validation_results
        
        # Date validation
        if 'Date' in df.columns:
            try:
                pd.to_datetime(df['Date'])
            except:
                validation_results['warnings'].append("Date column contains invalid dates")
            
            # Check for future dates
            future_dates = pd.to_datetime(df['Date']) > datetime.now()
            if future_dates.any():
                validation_results['warnings'].append(f"{future_dates.sum()} records have future dates")
        
        # Sales amount validation
        if 'Total_Sales' in df.columns:
            negative_sales = (df['Total_Sales'] < 0).sum()
            if negative_sales > 0:
                validation_results['warnings'].append(f"{negative_sales} records have negative sales")
            
            zero_sales = (df['Total_Sales'] == 0).sum()
            if zero_sales > 0:
                validation_results['warnings'].append(f"{zero_sales} records have zero sales")
        
        # Duplicates check
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            validation_results['warnings'].append(f"{duplicates} duplicate records found")
            validation_results['suggestions