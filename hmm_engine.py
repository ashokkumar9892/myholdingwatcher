"""
HMM Engine Module
Implements Hidden Markov Model for market regime detection using 7 components
"""

import numpy as np
import pandas as pd
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')


class RegimeDetector:
    """
    Hidden Markov Model for market regime detection
    Uses 7 hidden states to identify market regimes:
    - Bull Run state (highest positive return)
    - Bear/Crash state (lowest return)
    - Other intermediate regimes
    """
    
    def __init__(self, n_components=7, covariance_type='diag', n_iter=1000):
        """
        Initialize the HMM model
        
        Args:
            n_components (int): Number of hidden states (default: 7)
            covariance_type (str): Type of covariance matrix ('diag' for diagonal)
            n_iter (int): Number of iterations for training
        """
        self.n_components = n_components
        self.model = GaussianHMM(n_components=n_components, 
                                 covariance_type=covariance_type,
                                 n_iter=n_iter,
                                 random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        self.bull_state = None
        self.bear_state = None
        self.means = None
        
    def train(self, features, min_samples=100):
        """
        Train the HMM model on features
        
        Features required:
        1. Returns (log returns)
        2. Range (High - Low) / Close
        3. Volume Volatility (rolling std of returns)
        
        Args:
            features (np.ndarray): Training features of shape (n_samples, 3)
            min_samples (int): Minimum samples required for training
        
        Returns:
            bool: True if training successful, False otherwise
        """
        if len(features) < min_samples:
            print(f"Error: Need at least {min_samples} samples for training, got {len(features)}")
            return False
        
        # Handle any remaining NaN values
        features = features[~np.isnan(features).any(axis=1)]
        
        # Standardize features
        features_scaled = self.scaler.fit_transform(features)
        
        try:
            # Train the model
            self.model.fit(features_scaled)
            self.is_trained = True
            self.means = self.model.means_
            
            # Identify Bull and Bear states
            self._identify_states(features_scaled)
            
            return True
        
        except Exception as e:
            print(f"Error training HMM model: {str(e)}")
            return False
    
    def _identify_states(self, features_scaled):
        """
        Identify Bull (top states) and Bear (bottom states) states
        With 7 states, we'll classify:
        - Top 2 states as Bull
        - Bottom 2 states as Bear
        - Middle 3 as Neutral
        
        Args:
            features_scaled (np.ndarray): Scaled features
        """
        # Get means for each state (first feature is returns)
        returns_by_state = self.means[:, 0]
        
        # Sort states by return
        sorted_indices = np.argsort(returns_by_state)
        
        # Top 2 states = Bull
        self.bull_states = sorted_indices[-2:].tolist()
        
        # Bottom 2 states = Bear  
        self.bear_states = sorted_indices[:2].tolist()
        
        # Keep original single state IDs for backwards compatibility
        self.bull_state = sorted_indices[-1]
        self.bear_state = sorted_indices[0]
        
        bull_returns = [returns_by_state[i] for i in self.bull_states]
        bear_returns = [returns_by_state[i] for i in self.bear_states]
        print(f"Bull states: {self.bull_states} (returns: {[f'{r:.4f}' for r in bull_returns]})")
        print(f"Bear states: {self.bear_states} (returns: {[f'{r:.4f}' for r in bear_returns]})")
    
    def predict_regime(self, features):
        """
        Predict the regime for given features
        
        Args:
            features (np.ndarray): Features of shape (n_samples, 3)
        
        Returns:
            np.ndarray: Array of predicted states for each sample
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Handle NaN values
        if np.isnan(features).any():
            features = features[~np.isnan(features).any(axis=1)]
        
        # Standardize features
        features_scaled = self.scaler.transform(features)
        
        # Predict hidden states
        hidden_states = self.model.predict(features_scaled)
        
        return hidden_states
    
    def predict_proba(self, features):
        """
        Get probability distribution over states
        
        Args:
            features (np.ndarray): Features of shape (n_samples, 3)
        
        Returns:
            np.ndarray: Probability distribution over states
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        # Handle NaN values
        if np.isnan(features).any():
            features = features[~np.isnan(features).any(axis=1)]
        
        # Standardize features
        features_scaled = self.scaler.transform(features)
        
        # Get posterior probabilities
        posteriors = self.model.predict_proba(features_scaled)
        
        return posteriors
    
    def get_current_regime(self, features):
        """
        Get the current market regime
        
        Args:
            features (np.ndarray): Most recent features (last row)
        
        Returns:
            str: 'Bull', 'Bear', or 'Neutral'
        """
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
        
        current_state = self.predict_regime(features[-1:].reshape(1, -1))[0]
        
        if current_state in self.bull_states:
            return 'Bull'
        elif current_state in self.bear_states:
            return 'Bear'
        else:
            return 'Neutral'
    
    def get_regime_label(self, state):
        """
        Get regime label for a given state
        
        Args:
            state (int): Hidden state number
        
        Returns:
            str: Regime label ('Bull', 'Bear', or 'Neutral')
        """
        if state in self.bull_states:
            return 'Bull'
        elif state in self.bear_states:
            return 'Bear'
        else:
            return 'Neutral'
    
    def get_all_regime_timeseries(self, features):
        """
        Get the complete time series of regimes
        
        Args:
            features (np.ndarray): All historical features
        
        Returns:
            np.ndarray: Array of regime labels for each timestamp
        """
        states = self.predict_regime(features)
        regimes = np.array([self.get_regime_label(state) for state in states])
        return regimes


if __name__ == "__main__":
    print("HMM Engine module loaded successfully")
