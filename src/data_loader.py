"""
Data loading and preprocessing utilities
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from config import DATA_REQUIRED_COLUMNS, DATE_FORMAT

class DataLoader:
    """Class to handle data loading and preprocessing"""
    
    def __init__(self):
        self.data = None
        
    def load_csv(self, file_path, encoding='utf-8'):
        """
        Load data from CSV file with error handling
        
        Args:
            file_path (str): Path to CSV file
            encoding (str): File encoding
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            # Try different separators
            separators = [',', ';', '\t', '|']
            
            for sep in separators:
                try:
                    df = pd.read_csv(file_path, sep=sep, encoding=encoding)
                    if len(df.columns) > 1:  # Valid if more than 1 column
                        break
                except:
                    continue
            
            if df is None or len(df.columns) <= 1:
                raise ValueError("Could not parse CSV file with any common separator")
            
            print(f"✓ Successfully loaded {len(df)} records from {file_path}")
            print(f"Columns found: {list(df.columns)}")
            
            return self.preprocess_data(df)
            
        except Exception as e:
            print(f"Error loading CSV file: {e}")
            return None
    
    def load_excel(self, file_path, sheet_name=None):
        """
        Load data from Excel file
        
        Args:
            file_path (str): Path to Excel file
            sheet_name (str): Name of sheet to load
            
        Returns:
            pd.DataFrame: Loaded data
        """
        try:
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            print(f"✓ Successfully loaded {len(df)} records from Excel file")
            return self.preprocess_data(df)
            
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return None
    
    def preprocess_data(self, df):
        """
        Preprocess the loaded data
        
        Args:
            df (pd.DataFrame): Raw data
            
        Returns:
            pd.DataFrame: Preprocessed data
        """
        try:
            # Make a copy to avoid modifying original
            df = df.copy()
            
            # Clean column names
            df.columns = df.columns.str.strip().str.replace(' ', '_')
            
            # Try to identify date column
            date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            if date_columns:
                date_col = date_columns[0]
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce', infer_datetime_format=True)
                if 'Date' not in df.columns:
                    df.rename(columns={date_col: 'Date'}, inplace=True)
            
            # Try to identify sales/revenue columns
            sales_columns = [col for col in df.columns if any(keyword in col.lower() 
                           for keyword in ['sales', 'revenue', 'amount', 'total', 'value'])]
            if sales_columns and 'Total_Sales' not in df.columns:
                df.rename(columns={sales_columns[0]: 'Total_Sales'}, inplace=True)
            
            # Convert numeric columns
            numeric_columns = df.select_dtypes(include=[np.number]).columns
            for col in numeric_columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Remove rows with all NaN values
            df.dropna(how='all', inplace=True)
            
            # Add derived date columns if Date exists
            if 'Date' in df.columns:
                df['Month'] = df['Date'].dt.to_period('M')
                df['Quarter'] = df['Date'].dt.to_period('Q')
                df['Year'] = df['Date'].dt.year
                df['DayOfWeek'] = df['Date'].dt.day_name()
            
            print(f"✓ Data preprocessing completed")
            print(f"Final shape: {df.shape}")
            
            self.data = df
            return df
            
        except Exception as e:
            print(f"Error preprocessing data: {e}")
            return df
    
    def generate_sample_data(self, num_records=1000, start_date='2023-01-01', end_date='2024-12-31'):
        """
        Generate sample sales data for testing
        
        Args:
            num_records (int): Number of records to generate
            start_date (str): Start date for data
            end_date (str): End date for data
            
        Returns:
            pd.DataFrame: Generated sample data
        """
        np.random.seed(42)
        
        # Date range
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        date_range = pd.date_range(start, end, freq='D')
        
        # Sample data parameters
        products = ['Laptop', 'Desktop', 'Phone', 'Tablet', 'Monitor', 
                   'Keyboard', 'Mouse', 'Headphones', 'Speaker', 'Camera']
        regions = ['North America', 'South America', 'Europe', 'Asia', 'Africa', 'Oceania']
        sales_reps = [f'Rep_{str(i).zfill(3)}' for i in range(1, 51)]
        customers = [f'CUST_{str(i).zfill(4)}' for i in range(1000, 9999)]
        
        # Price ranges for different products
        price_ranges = {
            'Laptop': (800, 3000),
            'Desktop': (500, 2500),
            'Phone': (200, 1500),
            'Tablet': (150, 1200),
            'Monitor': (150, 800),
            'Keyboard': (20, 200),
            'Mouse': (10, 150),
            'Headphones': (30, 500),
            'Speaker': (50, 1000),
            'Camera': (200, 2000)
        }
        
        data = []
        for _ in range(num_records):
            product = np.random.choice(products)
            min_price, max_price = price_ranges[product]
            
            record = {
                'Date': np.random.choice(date_range),
                'Product': product,
                'Region': np.random.choice(regions),
                'Sales_Rep': np.random.choice(sales_reps),
                'Customer_ID': np.random.choice(customers),
                'Quantity': np.random.randint(1, 20),
                'Unit_Price': np.random.uniform(min_price, max_price),
                'Discount': np.random.uniform(0, 0.2)  # 0-20% discount
            }
            
            # Calculate total sales with discount
            subtotal = record['Quantity'] * record['Unit_Price']
            record['Total_Sales'] = subtotal * (1 - record['Discount'])
            
            data.append(record)
        
        df = pd.DataFrame(data)
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Add derived columns
        df['Month'] = df['Date'].dt.to_period('M')
        df['Quarter'] = df['Date'].dt.to_period('Q')
        df['Year'] = df['Date'].dt.year
        df['DayOfWeek'] = df['Date'].dt.day_name()
        
        print(f"✓ Generated {len(df)} sample records")
        
        # Save sample data
        sample_file = os.path.join('data', 'sample_sales_data.csv')
        os.makedirs('data', exist_ok=True)
        df.to_csv(sample_file, index=False)
        print(f"✓ Sample data saved to {sample_file}")
        
        self.data = df
        return df
    
    def validate_data(self, df):
        """
        Validate the loaded data
        
        Args:
            df (pd.DataFrame): Data to validate
            
        Returns:
            dict: Validation results
        """
        validation_results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check for required columns
        missing_columns = []
        for col in DATA_REQUIRED_COLUMNS:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            validation_results['errors'].append(f"Missing required columns: {missing_columns}")
            validation_results['is_valid'] = False
        
        # Check for empty data
        if len(df) == 0:
            validation_results['errors'].append("Dataset is empty")
            validation_results['is_valid'] = False
        
        # Check for date format
        if 'Date' in df.columns:
            if df['Date'].isna().sum() > len(df) * 0.1:
                validation_results['warnings'].append("More than 10% of dates are missing")
        
        # Check for negative sales
        if 'Total_Sales' in df.columns:
            negative_sales = (df['Total_Sales'] < 0).sum()
            if negative_sales > 0:
                validation_results['warnings'].append(f"{negative_sales} records have negative sales")
        
        return validation_results
    
    def get_data_info(self):
        """
        Get information about the loaded data
        
        Returns:
            dict: Data information
        """
        if self.data is None:
            return {"error": "No data loaded"}
        
        info = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'memory_usage': self.data.memory_usage(deep=True).sum(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'data_types': self.data.dtypes.to_dict()
        }
        
        if 'Date' in self.data.columns:
            info['date_range'] = {
                'start': self.data['Date'].min(),
                'end': self.data['Date'].max(),
                'days': (self.data['Date'].max() - self.data['Date'].min()).days
            }
        
        if 'Total_Sales' in self.data.columns:
            info['sales_summary'] = {
                'total': self.data['Total_Sales'].sum(),
                'mean': self.data['Total_Sales'].mean(),
                'median': self.data['Total_Sales'].median(),
                'min': self.data['Total_Sales'].min(),
                'max': self.data['Total_Sales'].max()
            }
        
        return info