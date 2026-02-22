"""
Regime-Based Trading App
A professional trading platform using Hidden Markov Models for regime detection

Version: 1.0.0
Author: EtradePorfolio Analysis
License: Proprietary
"""

__version__ = "1.0.0"
__title__ = "Regime-Based Trading App"
__description__ = "Professional HMM-based trading system with multi-factor confirmation"

# Package metadata
__all__ = [
    'data_loader',
    'hmm_engine',
    'indicators',
    'myPortfoliobacktester',
    'config',
]

try:
    from . import config
    print("✅ Regime-Based Trading App initialized")
except ImportError:
    print("ℹ️  Running modules individually (not as package)")
