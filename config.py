"""
Configuration management for AI Code Reviewer
"""

import json
import os
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

@dataclass 
class AnalysisConfig:
    max_line_length: int = 120
    max_function_lines: int = 50
    enabled_checks: List[str] = None
    severity_levels: Dict[str, str] = None
    
    def __post_init__(self):
        if self.enabled_checks is None:
            self.enabled_checks = ['complexity', 'style', 'syntax']
        if self.severity_levels is None:
            self.severity_levels = {
                'syntax': 'error',
                'complexity': 'warning', 
                'style': 'info'
            }

class ConfigManager:
    def __init__(self, config_path: str = '.aireviewer.json'):
        self.config_path = config_path
        self.config = AnalysisConfig()
        self.load_config()
    
    def load_config(self):
        """Load configuration from file if it exists"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                
                self.config = AnalysisConfig(
                    max_line_length=data.get('max_line_length', 120),
                    max_function_lines=data.get('max_function_lines', 50),
                    enabled_checks=data.get('enabled_checks', ['complexity', 'style', 'syntax']),
                    severity_levels=data.get('severity_levels', {
                        'syntax': 'error',
                        'complexity': 'warning', 
                        'style': 'info'
                    })
                )
            except Exception as e:
                print(f"Warning: Failed to load config: {e}")
                self.config = AnalysisConfig()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(asdict(self.config), f, indent=2)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def create_default_config(self):
        """Create a default configuration file"""
        self.config = AnalysisConfig()
        self.save_config()
        print(f"Created default configuration file: {self.config_path}")