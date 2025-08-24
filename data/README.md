# Data Directory

This directory contains data files for the Sales Visualization Tool.

## File Structure

```
data/
├── README.md              # This file
├── sample_sales_data.csv  # Generated sample data
└── your_sales_data.csv    # Your custom data files
```

## Data Format Requirements

Your CSV files should follow this format for optimal compatibility:

### Required Columns
- **Date**: Transaction date (YYYY-MM-DD format recommended)
- **Product**: Product or service name
- **Region**: Geographic region or territory
- **Total_Sales**: Total sales amount (numeric)

### Optional Columns
- **Sales_Rep**: Sales representative name
- **Quantity**: Number of items sold
- **Unit_Price**: Price per unit
- **Customer_ID**: Unique customer identifier
- **Discount**: Discount percentage (0-1 format)

## Example Data Format

```csv
Date,Product,Region,Sales_Rep,Quantity,Unit_Price,Total_Sales,Customer_ID
2024-01-15,Laptop,North America,Rep_001,2,1200.00,2400.00,CUST_1001
2024-01-15,Phone,Europe,Rep_002,1,800.00,800.00,CUST_1002
2024-01-16,Tablet,Asia,Rep_003,3,500.00,1500.00,CUST_1003
```

## Data Loading Instructions

1. **Place your CSV file in this directory**
2. **Run the tool**:
   ```python
   from sales_analyzer import SalesVisualizationTool
   
   tool = SalesVisualizationTool()
   tool.load_data('data/your_sales_data.csv')
   ```

3. **Or use the interactive menu**:
   ```bash
   python main.py
   # Choose option 2: "Load data from CSV file"
   # Enter: data/your_sales_data.csv
   ```

## Sample Data

The tool can generate sample data for testing:

```python
tool = SalesVisualizationTool()
tool.generate_sample_data(1000)  # Generates 1000 records
```

This creates a file named `sample_sales_data.csv` in this directory.

## Data Tips

1. **Date Formats**: The tool accepts various date formats, but YYYY-MM-DD is recommended
2. **Missing Values**: The tool handles missing values automatically
3. **Large Files**: For files >100MB, consider preprocessing or filtering first
4. **Encoding**: UTF-8 encoding is recommended for international characters

## Troubleshooting

### Common Data Issues:

1. **Date parsing errors**:
   - Ensure consistent date format throughout the file
   - Check for empty date cells

2. **Column name issues**:
   - Remove extra spaces from column headers
   - Use consistent naming (avoid special characters)

3. **Numeric formatting**:
   - Remove currency symbols ($, €, etc.)
   - Use dots for decimal separators
   - Remove thousand separators (commas)

### Data Validation

The tool automatically validates your data and reports:
- Missing required columns
- Data type issues
- Date range problems
- Negative sales values

Place your data files here and start analyzing! 📊# Data Directory

This directory contains data files for the Sales Visualization Tool.

## File Structure

```
data/
├── README.md              # This file
├── sample_sales_data.csv  # Generated sample data
└── your_sales_data.csv    # Your custom data files
```

## Data Format Requirements

Your CSV files should follow this format for optimal compatibility:

### Required Columns
- **Date**: Transaction date (YYYY-MM-DD format recommended)
- **Product**: Product or service name
- **Region**: Geographic region or territory
- **Total_Sales**: Total sales amount (numeric)

### Optional Columns
- **Sales_Rep**: Sales representative name
- **Quantity**: Number of items sold
- **Unit_Price**: Price per unit
- **Customer_ID**: Unique customer identifier
- **Discount**: Discount percentage (0-1 format)

## Example Data Format

```csv
Date,Product,Region,Sales_Rep,Quantity,Unit_Price,Total_Sales,Customer_ID
2024-01-15,Laptop,North America,Rep_001,2,1200.00,2400.00,CUST_1001
2024-01-15,Phone,Europe,Rep_002,1,800.00,800.00,CUST_1002
2024-01-16,Tablet,Asia,Rep_003,3,500.00,1500.00,CUST_1003
```

## Data Loading Instructions

1. **Place your CSV file in this directory**
2. **Run the tool**:
   ```python
   from sales_analyzer import SalesVisualizationTool
   
   tool = SalesVisualizationTool()
   tool.load_data('data/your_sales_data.csv')
   ```

3. **Or use the interactive menu**:
   ```bash
   python main.py
   # Choose option 2: "Load data from CSV file"
   # Enter: data/your_sales_data.csv
   ```

## Sample Data

The tool can generate sample data for testing:

```python
tool = SalesVisualizationTool()
tool.generate_sample_data(1000)  # Generates 1000 records
```

This creates a file named `sample_sales_data.csv` in this directory.

## Data Tips

1. **Date Formats**: The tool accepts various date formats, but YYYY-MM-DD is recommended
2. **Missing Values**: The tool handles missing values automatically
3. **Large Files**: For files >100MB, consider preprocessing or filtering first
4. **Encoding**: UTF-8 encoding is recommended for international characters

## Troubleshooting

### Common Data Issues:

1. **Date parsing errors**:
   - Ensure consistent date format throughout the file
   - Check for empty date cells

2. **Column name issues**:
   - Remove extra spaces from column headers
   - Use consistent naming (avoid special characters)

3. **Numeric formatting**:
   - Remove currency symbols ($, €, etc.)
   - Use dots for decimal separators
   - Remove thousand separators (commas)

### Data Validation

The tool automatically validates your data and reports:
- Missing required columns
- Data type issues
- Date range problems
- Negative sales values

Place your data files here and start analyzing! 📊