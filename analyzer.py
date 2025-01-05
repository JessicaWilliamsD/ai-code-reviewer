"""
Code analysis module for AI Code Reviewer
"""

import ast
import os
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class CodeIssue:
    line: int
    issue_type: str
    message: str
    severity: str

class CodeAnalyzer:
    def __init__(self):
        self.supported_extensions = ['.py', '.js', '.ts', '.java', '.cpp', '.c']
    
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
                
            # Check for long functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_lines = node.end_lineno - node.lineno
                    if func_lines > 50:
                        issues.append(CodeIssue(
                            line=node.lineno,
                            issue_type="complexity",
                            message=f"Function '{node.name}' is too long ({func_lines} lines)",
                            severity="warning"
                        ))
                        
        except Exception as e:
            issues.append(CodeIssue(
                line=1,
                issue_type="syntax",
                message=f"Failed to parse file: {str(e)}",
                severity="error"
            ))
        
        return issues
    
    def _basic_analysis(self, file_path: str) -> List[CodeIssue]:
        """Basic analysis for non-Python files"""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines, 1):
                if len(line.strip()) > 120:
                    issues.append(CodeIssue(
                        line=i,
                        issue_type="style",
                        message="Line too long (>120 characters)",
                        severity="info"
                    ))
                        
        except Exception as e:
            issues.append(CodeIssue(
                line=1,
                issue_type="error",
                message=f"Failed to read file: {str(e)}",
                severity="error"
            ))
        
        return issues