"""
ASEE Configuration Manager
Centralized configuration with environment variable support and validation
"""
import os
from dataclasses import dataclass
from typing import Dict, Any
import logging
from dotenv import load_dotenv

load_dotenv()

@dataclass
class FirebaseConfig:
    """Firebase configuration"""
    project_id: str = os.getenv("FIREBASE_PROJECT_ID", "asee-trading")
    credentials_path: str = os.getenv("FIREBASE_CREDENTIALS_PATH", "./config/firebase-credentials.json")
    collection_strategies: str = "strategies"
    collection_performance: str = "performance_metrics"
    collection_knowledge: str = "shared_knowledge"
    
    def validate(self) -> bool:
        """Validate Firebase configuration"""
        if not os.path.exists(self.credentials_path):
            logging.warning(f"Firebase credentials not found at {self.credentials_path}")
            return False
        return True

@dataclass
class TradingConfig:
    """Trading system configuration"""
    simulation_mode: bool = os.getenv("SIMULATION_MODE", "True").lower() == "true"
    initial_capital: float = float(os.getenv("INITIAL_CAPITAL", "100000.0"))
    max_drawdown: float = float(os.getenv("MAX_DRAWDOWN", "0.25"))
    risk_per_trade: float = float(os.getenv("RISK_PER_TRADE", "0.02"))
    
    def validate(self) -> bool:
        """Validate trading configuration"""
        if self.initial_capital <= 0:
            raise ValueError("Initial capital must be positive")
        if not 0 < self.max_drawdown <= 1:
            raise ValueError("Max drawdown must be between 0 and 1")
        return True

@dataclass  
class NeuralNetConfig:
    """Neural network configuration"""
    hidden_layers: tuple = (64, 32, 16)
    learning_rate: float = 0.001
    dropout_rate: float = 0.2
    batch_size: int = 32
    epochs: int = 50
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "hidden_layers": self.hidden_layers,
            "learning_rate": self.learning_rate,
            "dropout_rate": self.dropout_rate,
            "batch_size": self.batch_size,
            "epochs": self.epochs
        }

class ASEEConfig:
    """Main configuration manager"""
    
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.trading = TradingConfig()
        self.neural_net = NeuralNetConfig()
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.data_dir = os.getenv("DATA_DIR", "./data")
        
    def validate_all(self) -> bool:
        """Validate all configurations"""
        try:
            self.firebase.validate()
            self.trading.validate()
            return True
        except Exception as e:
            logging.error(f"Configuration validation failed: {e}")
            return False
    
    def ensure_data_dir(self):
        """Ensure data directory exists"""
        os.makedirs(self.data_dir, exist_ok=True)

config = ASEEConfig()