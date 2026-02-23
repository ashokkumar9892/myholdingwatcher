"""
Quick Start & Setup Verification Script
Validates the installation and environment setup
"""

import sys
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is compatible"""
    print(f"\n📍 Python Version: {sys.version}")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    print("✅ Python version compatible")
    return True


def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name.lower()
    
    try:
        __import__(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - NOT INSTALLED")
        return False


def check_dependencies():
    """Check if all dependencies are installed"""
    print_header("Checking Dependencies")
    
    required = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('polygon-api-client', 'polygon'),
        ('python-dotenv', 'dotenv'),
        ('plotly', 'plotly'),
        ('hmmlearn', 'hmmlearn'),
        ('scikit-learn', 'sklearn'),
    ]
    
    optional = [
        ('TA-Lib', 'talib'),
    ]
    
    print("\nRequired Packages:")
    required_ok = all(check_package(name, imp) for name, imp in required)
    
    print("\nOptional Packages:")
    for name, imp in optional:
        check_package(name, imp)
    
    return required_ok


def check_modules():
    """Check if project modules can be imported"""
    print_header("Checking Project Modules")
    
    modules = [
        'data_loader',
        'indicators',
        'hmm_engine',
        'myPortfoliobacktester',
        'config'
    ]
    
    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"✅ {module}.py")
        except ImportError as e:
            print(f"❌ {module}.py - {str(e)}")
            all_ok = False
    
    return all_ok


def check_polygon_api():
    """Check if Polygon.io API key is configured"""
    print_header("Checking Polygon.io API Configuration")
    
    import os
    from dotenv import load_dotenv
    
    # Load .env file
    load_dotenv()
    
    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️  .env file not found")
        print("   → Copy .env.example to .env and add your API key")
        print("   → Get your free key at: https://polygon.io/")
        return False
    else:
        print("✅ .env file found")
    
    # Check if API key is set
    api_key = os.getenv('POLYGON_API_KEY', '')
    if not api_key or api_key == 'your_polygon_api_key_here':
        print("⚠️  POLYGON_API_KEY not configured")
        print("   → Edit .env and add your actual API key")
        print("   → Get your free key at: https://polygon.io/")
        return False
    else:
        # Mask the API key for security
        masked_key = api_key[:8] + '...' + api_key[-4:] if len(api_key) > 12 else '***'
        print(f"✅ POLYGON_API_KEY found: {masked_key}")
    
    # Test API connection
    try:
        from polygon import RESTClient
        print("\nTesting Polygon.io connection...")
        client = RESTClient(api_key=api_key)
        
        # Try to fetch a simple quote
        list(client.list_aggs(
            ticker="AAPL",
            multiplier=1,
            timespan="day",
            from_="2024-01-01",
            to="2024-01-02",
            limit=1
        ))
        print("✅ Successfully connected to Polygon.io API")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Polygon.io: {str(e)[:100]}")
        print("   → Check your API key")
        print("   → Verify your internet connection")
        return False


def check_files():
    """Check if all required files exist"""
    print_header("Checking Project Files")
    
    files_needed = [
        'data_loader.py',
        'indicators.py',
        'hmm_engine.py',
        'myPortfoliobacktester.py',
        'myPortfolioapp.py',
        'config.py',
        'requirements.txt',
        'README.md',
        '.env.example'
    ]
    
    current_dir = Path('.')
    all_exist = True
    
    for file in files_needed:
        filepath = current_dir / file
        if filepath.exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            all_exist = False
    
    return all_exist


def print_next_steps():
    """Print next steps for user"""
    print_header("Next Steps")
    
    print("""
1. If dependencies are missing:
   pip install -r requirements.txt

2. If Polygon API key is not configured:
   a) Copy .env.example to .env
   b) Get your FREE API key at: https://polygon.io/
   c) Edit .env and add your key
   d) See POLYGON_SETUP.md for detailed instructions

3. (Optional) Install TA-Lib for better performance:
   - Windows: pip install TA-Lib
   - macOS: brew install ta-lib && pip install TA-Lib
   - Linux: See README.md for installation instructions

4. Run the Streamlit app:
   streamlit run myPortfolioapp.py

5. The dashboard will open in your browser at:
   http://localhost:8501

6. Select a ticker and click "Run Backtest" to test the strategy

📖 Quick reference: See QUICK_START.txt
    """)


def main():
    """Main setup verification"""
    print_header("REGIME-BASED TRADING APP - SETUP VERIFICATION")
    
    results = []
    
    # Check Python version
    results.append(("Python Version", check_python_version()))
    
    # Check dependencies
    results.append(("Dependencies", check_dependencies()))
    
    # Check Polygon API
    results.append(("Polygon.io API", check_polygon_api()))
    
    # Check files
    results.append(("Project Files", check_files()))
    
    # Check modules
    results.append(("Project Modules", check_modules()))
    
    # Print summary
    print_header("Setup Summary")
    
    for check_name, status in results:
        status_icon = "✅" if status else "⚠️"
        print(f"{status_icon} {check_name}")
    
    all_ok = all(status for _, status in results)
    
    if all_ok:
        print("\n✅ All checks passed! Installation looks good.")
        print_next_steps()
    else:
        print("\n⚠️  Some issues detected. Please fix them before running the app.")
        print("\nTo install missing dependencies:")
        print("  pip install -r requirements.txt")
        print("\nFor more details, see README.md")
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
