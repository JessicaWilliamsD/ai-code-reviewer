#!/usr/bin/env python3
"""
CLI interface for AI Code Reviewer
"""

import argparse
import sys
import os
from analyzer import CodeAnalyzer
from report import ReportGenerator

def main():
    parser = argparse.ArgumentParser(description='AI Code Reviewer - Analyze code files for issues')
    parser.add_argument('file', help='Path to the file to analyze')
    parser.add_argument('--format', choices=['text', 'json', 'html'], default='text', 
                       help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)
    
    analyzer = CodeAnalyzer()
    issues = analyzer.analyze_file(args.file)
    
    # Generate report
    report_gen = ReportGenerator()
    report_content = report_gen.generate_report(args.file, issues, args.format)
    
    # Output report
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(report_content)
            print(f"Report saved to: {args.output}")
        except Exception as e:
            print(f"Error saving report: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(report_content)

if __name__ == '__main__':
    main()