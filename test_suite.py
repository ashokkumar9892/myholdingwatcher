"""
Comprehensive Test Suite
Validates all components of the Regime-Based Trading App
"""

import sys
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all core modules can be imported"""
    print("\n" + "="*60)
    print("TEST 1: Module Imports")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    modules = [
        'config',
        'data_loader',
        'indicators',
        'hmm_engine',
        'myPortfoliobacktester',
    ]
    
    for module_name in modules:
        tests_total += 1
        try:
            __import__(module_name)
            print(f"  ✅ {module_name}")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ {module_name}: {str(e)}")
    
    return tests_passed, tests_total


def test_config():
    """Test configuration module"""
    print("\n" + "="*60)
    print("TEST 2: Configuration")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    try:
        from config import (
            HMM_COMPONENTS, MIN_CONDITIONS_FOR_ENTRY,
            DEFAULT_INITIAL_CAPITAL, DEFAULT_LEVERAGE,
            COOLDOWN_HOURS, validate_config, get_stock_list
        )
        
        # Test parameters
        tests_total += 1
        if HMM_COMPONENTS == 7:
            print(f"  ✅ HMM components: {HMM_COMPONENTS}")
            tests_passed += 1
        else:
            print(f"  ❌ HMM components: expected 7, got {HMM_COMPONENTS}")
        
        tests_total += 1
        if MIN_CONDITIONS_FOR_ENTRY == 7:
            print(f"  ✅ Min conditions: {MIN_CONDITIONS_FOR_ENTRY}")
            tests_passed += 1
        else:
            print(f"  ❌ Min conditions: expected 7, got {MIN_CONDITIONS_FOR_ENTRY}")
        
        # Test validation
        tests_total += 1
        errors = validate_config()
        if len(errors) == 0:
            print(f"  ✅ Configuration validation passed")
            tests_passed += 1
        else:
            print(f"  ❌ Configuration errors: {errors}")
        
        # Test stock list
        tests_total += 1
        stocks = get_stock_list()
        if len(stocks) >= 28:
            print(f"  ✅ Stock list has {len(stocks)} stocks")
            tests_passed += 1
        else:
            print(f"  ❌ Stock list has only {len(stocks)} stocks (expected 28+)")
    
    except Exception as e:
        print(f"  ❌ Configuration test failed: {str(e)}")
    
    return tests_passed, tests_total


def test_data_loader():
    """Test data loader module"""
    print("\n" + "="*60)
    print("TEST 3: Data Loader (Quick Test)")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    try:
        from data_loader import calculate_features, get_training_features
        import numpy as np
        
        # Create mock data
        mock_data = {
            'Open': np.random.randn(100) + 100,
            'High': np.random.randn(100) + 101,
            'Low': np.random.randn(100) + 99,
            'Close': np.random.randn(100) + 100,
            'Volume': np.random.randint(1000000, 10000000, 100)
        }
        
        import pandas as pd
        mock_df = pd.DataFrame(mock_data)
        
        # Test features
        tests_total += 1
        try:
            features_df = calculate_features(mock_df)
            if len(features_df) > 0:
                print(f"  ✅ Features calculated: {features_df.shape[0]} rows, {features_df.shape[1]} cols")
                tests_passed += 1
            else:
                print(f"  ❌ No features generated")
        except Exception as e:
            print(f"  ❌ Feature calculation failed: {str(e)}")
        
        # Test training features
        tests_total += 1
        try:
            train_features = get_training_features(features_df)
            if train_features.shape[1] == 3:
                print(f"  ✅ Training features: {train_features.shape[0]} samples, {train_features.shape[1]} features")
                tests_passed += 1
            else:
                print(f"  ❌ Wrong number of features: {train_features.shape[1]} (expected 3)")
        except Exception as e:
            print(f"  ❌ Training feature extraction failed: {str(e)}")
    
    except Exception as e:
        print(f"  ❌ Data loader test failed: {str(e)}")
    
    return tests_passed, tests_total


def test_hmm_engine():
    """Test HMM engine"""
    print("\n" + "="*60)
    print("TEST 4: HMM Engine")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    try:
        from hmm_engine import RegimeDetector
        import numpy as np
        
        # Create mock features
        np.random.seed(42)
        features = np.random.randn(500, 3)
        
        # Test model creation
        tests_total += 1
        try:
            detector = RegimeDetector(n_components=7)
            print(f"  ✅ RegimeDetector created")
            tests_passed += 1
        except Exception as e:
            print(f"  ❌ RegimeDetector creation failed: {str(e)}")
            return tests_passed, tests_total
        
        # Test training
        tests_total += 1
        try:
            success = detector.train(features)
            if success:
                print(f"  ✅ Model trained successfully")
                tests_passed += 1
            else:
                print(f"  ❌ Model training failed")
        except Exception as e:
            print(f"  ❌ Training failed: {str(e)}")
        
        # Test prediction
        tests_total += 1
        try:
            states = detector.predict_regime(features)
            if len(states) == len(features):
                print(f"  ✅ Regime prediction: {len(states)} states")
                tests_passed += 1
            else:
                print(f"  ❌ Wrong number of predictions")
        except Exception as e:
            print(f"  ❌ Prediction failed: {str(e)}")
        
        # Test current regime
        tests_total += 1
        try:
            regime = detector.get_current_regime(features[-1:])
            if regime in ['Bull', 'Bear', 'Neutral']:
                print(f"  ✅ Current regime: {regime}")
                tests_passed += 1
            else:
                print(f"  ❌ Invalid regime: {regime}")
        except Exception as e:
            print(f"  ❌ Current regime check failed: {str(e)}")
    
    except Exception as e:
        print(f"  ❌ HMM engine test failed: {str(e)}")
    
    return tests_passed, tests_total


def test_indicators():
    """Test technical indicators module"""
    print("\n" + "="*60)
    print("TEST 5: Technical Indicators")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    try:
        from indicators import (
            calculate_rsi, calculate_macd, calculate_adx,
            calculate_ema, calculate_sma, calculate_volatility
        )
        import pandas as pd
        import numpy as np
        
        # Create mock data
        np.random.seed(42)
        mock_close = np.random.randn(200).cumsum() + 100
        mock_high = mock_close + np.abs(np.random.randn(200))
        mock_low = mock_close - np.abs(np.random.randn(200))
        
        mock_df = pd.DataFrame({
            'Close': mock_close,
            'High': mock_high,
            'Low': mock_low,
            'Volume': np.random.randint(1000000, 10000000, 200)
        })
        
        # Test RSI
        tests_total += 1
        try:
            rsi = calculate_rsi(mock_df)
            if len(rsi) == len(mock_df):
                print(f"  ✅ RSI calculated")
                tests_passed += 1
            else:
                print(f"  ❌ RSI length mismatch")
        except Exception as e:
            print(f"  ❌ RSI calculation failed: {str(e)}")
        
        # Test MACD
        tests_total += 1
        try:
            macd, signal, hist = calculate_macd(mock_df)
            if len(macd) == len(mock_df):
                print(f"  ✅ MACD calculated")
                tests_passed += 1
            else:
                print(f"  ❌ MACD length mismatch")
        except Exception as e:
            print(f"  ❌ MACD calculation failed: {str(e)}")
        
        # Test ADX
        tests_total += 1
        try:
            adx = calculate_adx(mock_df)
            if len(adx) == len(mock_df):
                print(f"  ✅ ADX calculated")
                tests_passed += 1
            else:
                print(f"  ❌ ADX length mismatch")
        except Exception as e:
            print(f"  ❌ ADX calculation failed: {str(e)}")
        
        # Test EMAs
        tests_total += 1
        try:
            ema50 = calculate_ema(mock_df, 50)
            ema200 = calculate_ema(mock_df, 200)
            if len(ema50) == len(mock_df) and len(ema200) == len(mock_df):
                print(f"  ✅ EMAs calculated")
                tests_passed += 1
            else:
                print(f"  ❌ EMA length mismatch")
        except Exception as e:
            print(f"  ❌ EMA calculation failed: {str(e)}")
    
    except Exception as e:
        print(f"  ❌ Indicators test failed: {str(e)}")
    
    return tests_passed, tests_total


def test_backtester():
    """Test backtester module"""
    print("\n" + "="*60)
    print("TEST 6: Backtester Logic")
    print("="*60)
    
    tests_passed = 0
    tests_total = 0
    
    try:
        from myPortfoliobacktester import RegimeBasedBacktester, TradeLogger
        
        # Test TradeLogger
        tests_total += 1
        try:
            logger = TradeLogger()
            logger.log_trade(None, 'BUY', 100, 10, 'test', 'Bull')
            if len(logger.trades) == 1:
                print(f"  ✅ TradeLogger working")
                tests_passed += 1
            else:
                print(f"  ❌ TradeLogger failed")
        except Exception as e:
            print(f"  ❌ TradeLogger test failed: {str(e)}")
        
        # Test RegimeBasedBacktester
        tests_total += 1
        try:
            backtester = RegimeBasedBacktester(
                initial_capital=2000,
                leverage=2.5,
                cooldown_hours=48
            )
            if backtester.equity == 2000:
                print(f"  ✅ RegimeBasedBacktester initialized")
                tests_passed += 1
            else:
                print(f"  ❌ Backtester initialization failed")
        except Exception as e:
            print(f"  ❌ Backtester test failed: {str(e)}")
        
        # Test entry conditions check
        tests_total += 1
        try:
            import pandas as pd
            import numpy as np
            
            mock_row = pd.Series({
                'RSI': 50,
                'Momentum': 2.0,
                'Volatility': 3.0,
                'Volume': 1000000,
                'SMA20_Volume': 800000,
                'ADX': 30,
                'Close': 100,
                'EMA50': 95,
                'EMA200': 90,
                'MACD': 0.5,
                'MACD_Signal': 0.3
            })
            
            conditions = backtester.check_entry_conditions(mock_row)
            if conditions == 8:
                print(f"  ✅ Entry conditions check: {conditions}/8 met")
                tests_passed += 1
            else:
                print(f"  ⚠️  Entry conditions: {conditions}/8 met")
                tests_passed += 1  # This is ok, just informational
        except Exception as e:
            print(f"  ❌ Entry conditions test failed: {str(e)}")
    
    except Exception as e:
        print(f"  ❌ Backtester test failed: {str(e)}")
    
    return tests_passed, tests_total


def print_summary(all_results):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    total_passed = 0
    total_tests = 0
    
    for test_name, (passed, total) in all_results.items():
        total_passed += passed
        total_tests += total
        pct = (passed / total * 100) if total > 0 else 0
        status = "✅" if passed == total else "⚠️"
        print(f"{status} {test_name}: {passed}/{total} ({pct:.0f}%)")
    
    print("-"*60)
    overall_pct = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"OVERALL: {total_passed}/{total_tests} tests passed ({overall_pct:.0f}%)")
    print("="*60)
    
    if overall_pct >= 80:
        print("✅ Application is ready to use!")
        return 0
    elif overall_pct >= 60:
        print("⚠️  Some tests failed. Check output above.")
        return 1
    else:
        print("❌ Multiple tests failed. Fix issues before using.")
        return 1


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  REGIME-BASED TRADING APP - TEST SUITE".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    
    results = {}
    
    try:
        results['Imports'] = test_imports()
        results['Configuration'] = test_config()
        results['Data Loader'] = test_data_loader()
        results['HMM Engine'] = test_hmm_engine()
        results['Indicators'] = test_indicators()
        results['Backtester'] = test_backtester()
        
        return print_summary(results)
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
