"""
Setup script for Sales Visualization Tool
Run this to set up the complete project structure and install dependencies
"""
import os
import subprocess
import sys
from pathlib import Path

def create_directory_structure():
    """Create the complete directory structure"""
    directories = [
        'data',
        'output',
        'output/charts',
        'output/reports',
        'src',
        'examples',
        'tests'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")
    
    # Create __init__.py files
    init_files = [
        'src/__init__.py',
        'tests/__init__.py'
    ]
    
    for init_file in init_files:
        Path(init_file).touch(exist_ok=True)
        print(f"✓ Created file: {init_file}")

def install_dependencies():
    """Install required Python packages"""
    packages = [
        'pandas>=1.5.0',
        'matplotlib>=3.6.0',
        'seaborn>=0.12.0',
        'plotly>=5.15.0',
        'numpy>=1.24.0',
        'openpyxl>=3.1.0',
        'jupyter>=1.0.0',
        'kaleido>=0.2.1',
        'scikit-learn>=1.3.0',
        'statsmodels>=0.14.0',
        'dash>=2.14.0',
        'dash-bootstrap-components>=1.4.0'
    ]
    
    print("Installing Python packages...")
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✓ Installed: {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {package}: {e}")

def create_configuration_files():
    """Create additional configuration files"""
    
    # Create .gitignore
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
output/charts/*.png
output/charts/*.html
output/reports/*.html
output/reports/*.xlsx
data/large_files/
*.log

# Jupyter Notebooks
.ipynb_checkpoints/
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")
    
    # Create environment.yml for conda users
    conda_env = """
name: sales-viz-tool
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.9
  - pandas>=1.5.0
  - matplotlib>=3.6.0
  - seaborn>=0.12.0
  - numpy>=1.24.0
  - jupyter
  - scikit-learn
  - pip
  - pip:
    - plotly>=5.15.0
    - openpyxl>=3.1.0
    - kaleido>=0.2.1
    - statsmodels>=0.14.0
    - dash>=2.14.0
    - dash-bootstrap-components>=1.4.0
"""
    
    with open('environment.yml', 'w') as f:
        f.write(conda_env)
    print("✓ Created environment.yml")

def create_batch_scripts():
    """Create batch scripts for easy execution"""
    
    # Windows batch script
    windows_script = """@echo off
echo Starting Sales Visualization Tool...
python main.py
pause
"""
    
    with open('run_tool.bat', 'w') as f:
        f.write(windows_script)
    print("✓ Created run_tool.bat (Windows)")
    
    # Linux/Mac shell script
    shell_script = """#!/bin/bash
echo "Starting Sales Visualization Tool..."
python main.py
read -p "Press enter to continue..."
"""
    
    with open('run_tool.sh', 'w') as f:
        f.write(shell_script)
    
    # Make shell script executable
    try:
        os.chmod('run_tool.sh', 0o755)
        print("✓ Created run_tool.sh (Linux/Mac)")
    except:
        print("✓ Created run_tool.sh (permissions may need to be set manually)")

def verify_installation():
    """Verify that all components are properly installed"""
    print("\n" + "="*50)
    print("VERIFYING INSTALLATION")
    print("="*50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major == 3 and python_version.minor >= 8:
        print(f"✓ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"⚠ Python version {python_version.major}.{python_version.minor} may not be optimal (recommended: 3.8+)")
    
    # Check required packages
    required_packages = ['pandas', 'matplotlib', 'seaborn', 'plotly', 'numpy', 'openpyxl']
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            print(f"✗ {package} is NOT available")
    
    # Check directory structure
    required_dirs = ['data', 'output', 'src', 'examples']
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✓ Directory exists: {directory}")
        else:
            print(f"✗ Directory missing: {directory}")
    
    print("\n" + "="*50)
    print("INSTALLATION COMPLETE!")
    print("="*50)
    print("To get started:")
    print("1. Run: python main.py")
    print("2. Or check examples: python examples/basic_usage.py")
    print("3. Windows users can double-click: run_tool.bat")
    print("4. Linux/Mac users can run: ./run_tool.sh")

def main():
    """Main setup function"""
    print("🚀 Sales Visualization Tool Setup")
    print("="*50)
    
    try:
        # Create directory structure
        print("1. Creating directory structure...")
        create_directory_structure()
        
        # Install dependencies
        print("\n2. Installing dependencies...")
        install_dependencies()
        
        # Create configuration files
        print("\n3. Creating configuration files...")
        create_configuration_files()
        
        # Create batch scripts
        print("\n4. Creating execution scripts...")
        create_batch_scripts()
        
        # Verify installation
        verify_installation()
        
        print(f"\n🎉 Setup completed successfully!")
        print(f"Project ready in: {os.getcwd()}")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())