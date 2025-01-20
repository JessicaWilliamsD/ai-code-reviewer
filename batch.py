"""
Batch analysis module for processing multiple files
"""

import os
import glob
from typing import List, Dict
from analyzer import CodeAnalyzer, CodeIssue
from report import ReportGenerator

class BatchAnalyzer:
    def __init__(self, config_path: str = '.aireviewer.json'):
        self.analyzer = CodeAnalyzer(config_path)
        self.report_gen = ReportGenerator()
        
    def analyze_directory(self, directory: str, pattern: str = "**/*", recursive: bool = True) -> Dict[str, List[CodeIssue]]:
        """Analyze all matching files in a directory"""
        if not os.path.isdir(directory):
            raise ValueError(f"Directory not found: {directory}")
        
        results = {}
        search_pattern = os.path.join(directory, pattern)
        
        # Get all matching files
        files = glob.glob(search_pattern, recursive=recursive)
        
        # Filter for supported file types
        supported_files = []
        for file_path in files:
            if os.path.isfile(file_path):
                ext = os.path.splitext(file_path)[1].lower()
                if ext in self.analyzer.supported_extensions:
                    supported_files.append(file_path)
        
        # Analyze each file
        for file_path in supported_files:
            try:
                issues = self.analyzer.analyze_file(file_path)
                results[file_path] = issues
            except Exception as e:
                print(f"Warning: Failed to analyze {file_path}: {e}")
                
        return results
    
    def analyze_files(self, file_paths: List[str]) -> Dict[str, List[CodeIssue]]:
        """Analyze a list of specific files"""
        results = {}
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue
                
            try:
                issues = self.analyzer.analyze_file(file_path)
                results[file_path] = issues
            except Exception as e:
                print(f"Warning: Failed to analyze {file_path}: {e}")
                
        return results
    
    def generate_summary_report(self, results: Dict[str, List[CodeIssue]], format_type: str = 'text') -> str:
        """Generate a summary report for batch analysis results"""
        total_files = len(results)
        total_issues = sum(len(issues) for issues in results.values())
        
        if format_type == 'json':
            import json
            from datetime import datetime
            
            summary_data = {
                'analysis_summary': {
                    'total_files': total_files,
                    'total_issues': total_issues,
                    'generated_at': datetime.now().isoformat()
                },
                'files': {}
            }
            
            for file_path, issues in results.items():
                summary_data['files'][file_path] = {
                    'issue_count': len(issues),
                    'issues': [
                        {
                            'line': issue.line,
                            'type': issue.issue_type,
                            'message': issue.message,
                            'severity': issue.severity
                        } for issue in issues
                    ]
                }
            
            return json.dumps(summary_data, indent=2)
        
        # Text format
        lines = []
        lines.append("AI Code Review - Batch Analysis Summary")
        lines.append("=" * 50)
        lines.append(f"Files analyzed: {total_files}")
        lines.append(f"Total issues found: {total_issues}")
        lines.append("")
        
        # Files with issues
        files_with_issues = {f: issues for f, issues in results.items() if issues}
        
        if not files_with_issues:
            lines.append("✅ No issues found in any files!")
            return '\n'.join(lines)
        
        lines.append(f"Files with issues: {len(files_with_issues)}")
        lines.append("")
        
        # Sort files by issue count (descending)
        sorted_files = sorted(files_with_issues.items(), key=lambda x: len(x[1]), reverse=True)
        
        for file_path, issues in sorted_files:
            lines.append(f"📄 {file_path}")
            lines.append(f"   Issues: {len(issues)}")
            
            # Group by severity
            severity_counts = {}
            for issue in issues:
                if issue.severity not in severity_counts:
                    severity_counts[issue.severity] = 0
                severity_counts[issue.severity] += 1
            
            severity_info = []
            for severity in ['error', 'warning', 'info']:
                if severity in severity_counts:
                    count = severity_counts[severity]
                    icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[severity]
                    severity_info.append(f"{icon} {count}")
            
            if severity_info:
                lines.append(f"   {' '.join(severity_info)}")
            lines.append("")
        
        return '\n'.join(lines)