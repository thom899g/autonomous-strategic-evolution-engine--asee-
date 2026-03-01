"""
Robust logging utility for ASEE system
Provides structured logging with file and stdout handlers
"""
import logging
import sys
from datetime import datetime
import os
from config.config import config

class ASEELogger:
    """Custom logger for ASEE system"""
    
    @staticmethod
    def setup_logger(name: str = "ASEE") -> logging.Logger:
        """
        Set up and configure logger
        
        Args:
            name: Logger name
            
        Returns:
            Configured logger instance
        """
        logger = logging.getLogger(name)
        
        # Avoid duplicate handlers
        if logger.hasHandlers():
            return logger
            
        logger.setLevel(getattr(logging, config.log_level))
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, config.log_level))
        console_handler.setFormatter(console_formatter)
        
        # File handler
        log_dir = os.path.join(config.data_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file