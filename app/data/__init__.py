# AdsenseAI Campaign Risk Analyzer - Data Package
# Contains data loading and synthetic data generation modules

from .synthetic_data_generator import (
    SyntheticDataGenerator,
    generate_synthetic_data
)

__all__ = [
    'SyntheticDataGenerator',
    'generate_synthetic_data'
]
