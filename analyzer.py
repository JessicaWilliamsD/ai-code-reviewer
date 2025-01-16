"""
Code analysis module for AI Code Reviewer
"""

import ast
import os
from typing import List, Dict, Any
from dataclasses import dataclass
from config import ConfigManager

@dataclass
class CodeIssue:
    line: int
    issue_type: str
    message: str
    severity: str

class CodeAnalyzer:
    def __init__(self, config_path: str = '.aireviewer.json'):
        self.supported_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c']
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.config
    
    def analyze_file(self, file_path: str) -> List[CodeIssue]:
        """Analyze a single file and return list of issues"""
        if not os.path.exists(file_path):
            return []
        
        extension = os.path.splitext(file_path)[1].lower()
        
        if extension == '.py':
            return self._analyze_python_file(file_path)
        else:
            return self._basic_analysis(file_path)
    
    def _analyze_python_file(self, file_path: str) -> List[CodeIssue]:
        """Analyze Python file for common issues"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                tree = ast.parse(content)
                
            # Check for long functions and other complexity issues
            if 'complexity' in self.config.enabled_checks:
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_lines = node.end_lineno - node.lineno
                        if func_lines > self.config.max_function_lines:
                            issues.append(CodeIssue(
                                line=node.lineno,
                                issue_type="complexity",
                                message=f"Function '{node.name}' is too long ({func_lines} lines)",
                                severity=self.config.severity_levels.get('complexity', 'warning')
                            ))
                        
                        # Check for too many parameters
                        param_count = len(node.args.args)
                        if param_count > 5:
                            issues.append(CodeIssue(
                                line=node.lineno,
                                issue_type="complexity",
                                message=f"Function '{node.name}' has too many parameters ({param_count})",
                                severity=self.config.severity_levels.get('complexity', 'warning')
                            ))
                    
                    # Check for deep nesting
                    if isinstance(node, (ast.If, ast.For, ast.While)):
                        nesting_depth = self._calculate_nesting_depth(node)
                        if nesting_depth > 3:
                            issues.append(CodeIssue(
                                line=node.lineno,
                                issue_type="complexity",
                                message=f"Code block has deep nesting (depth: {nesting_depth})",
                                severity=self.config.severity_levels.get('complexity', 'warning')
                            ))
                        
        except Exception as e:
            issues.append(CodeIssue(
                line=1,
                issue_type="syntax",
                message=f"Failed to parse file: {str(e)}",
                severity="error"
            ))
        
        return issues
    
    def _calculate_nesting_depth(self, node):
        """Calculate the nesting depth of a code block"""
        def count_nested_blocks(n, depth=0):
            max_depth = depth
            for child in ast.iter_child_nodes(n):
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
                    child_depth = count_nested_blocks(child, depth + 1)
                    max_depth = max(max_depth, child_depth)
                else:
                    child_depth = count_nested_blocks(child, depth)
                    max_depth = max(max_depth, child_depth)
            return max_depth
        
        return count_nested_blocks(node, 1)
    
    def _basic_analysis(self, file_path: str) -> List[CodeIssue]:
        """Basic analysis for non-Python files"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            if 'style' in self.config.enabled_checks:
                for i, line in enumerate(lines, 1):
                    if len(line.strip()) > self.config.max_line_length:
                        issues.append(CodeIssue(
                            line=i,
                            issue_type="style",
                            message=f"Line too long (>{self.config.max_line_length} characters)",
                            severity=self.config.severity_levels.get('style', 'info')
                        ))
                        
        except Exception as e:
            issues.append(CodeIssue(
                line=1,
                issue_type="error",
                message=f"Failed to read file: {str(e)}",
                severity="error"
            ))
        
        return issues