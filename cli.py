#!/usr/bin/env python3
"""
CLI interface for AI Code Reviewer
"""

import argparse
import sys
import os
from analyzer import CodeAnalyzer
from report import ReportGenerator
from batch import BatchAnalyzer

def main():
    parser = argparse.ArgumentParser(description='AI Code Reviewer - Analyze code files for issues')
    parser.add_argument('path', help='Path to file or directory to analyze')
    parser.add_argument('--format', choices=['text', 'json', 'html'], default='text', 
                       help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Output file path (optional)')
    parser.add_argument('--batch', action='store_true', help='Batch mode for directory analysis')
    parser.add_argument('--pattern', default='**/*', help='File pattern for batch mode (default: **/*)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Determine analysis mode
    if args.batch or os.path.isdir(args.path):
        # Batch analysis mode
        batch_analyzer = BatchAnalyzer()
        
        if os.path.isdir(args.path):
            results = batch_analyzer.analyze_directory(args.path, args.pattern)
        else:
            print("Error: Batch mode requires a directory path", file=sys.stderr)
            sys.exit(1)
        
        # Generate batch report
        report_content = batch_analyzer.generate_summary_report(results, args.format)
        
    else:
        # Single file analysis mode
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_file(args.path)
        
        # Generate single file report
        report_gen = ReportGenerator()
        report_content = report_gen.generate_report(args.path, issues, args.format)
    
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