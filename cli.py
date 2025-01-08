#!/usr/bin/env python3
"""
CLI interface for AI Code Reviewer
"""

import argparse
import sys
import os
from analyzer import CodeAnalyzer

def main():
    parser = argparse.ArgumentParser(description='AI Code Reviewer - Analyze code files for issues')
    parser.add_argument('file', help='Path to the file to analyze')
    parser.add_argument('--format', choices=['text', 'json'], default='text', 
                       help='Output format (default: text)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)
    
    analyzer = CodeAnalyzer()
    issues = analyzer.analyze_file(args.file)
    
    if args.format == 'json':
        import json
        result = {
            'file': args.file,
            'issues_count': len(issues),
            'issues': [
                {
                    'line': issue.line,
                    'type': issue.issue_type,
                    'message': issue.message,
                    'severity': issue.severity
                } for issue in issues
            ]
        }
        print(json.dumps(result, indent=2))
    else:
        print(f"Analyzing: {args.file}")
        print(f"Found {len(issues)} issues:\n")
        
        for issue in issues:
            severity_symbol = {
                'error': '❌',
                'warning': '⚠️', 
                'info': 'ℹ️'
            }.get(issue.severity, '•')
            
            print(f"{severity_symbol} Line {issue.line}: {issue.message} ({issue.issue_type})")

if __name__ == '__main__':
    main()