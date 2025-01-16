"""
Report generation module for AI Code Reviewer
"""

from typing import List, Dict
from analyzer import CodeIssue
import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.report_formats = ['text', 'json', 'html']
    
    def generate_report(self, file_path: str, issues: List[CodeIssue], format_type: str = 'text') -> str:
        """Generate a report in the specified format"""
        if format_type not in self.report_formats:
            raise ValueError(f"Unsupported format: {format_type}")
        
        if format_type == 'json':
            return self._generate_json_report(file_path, issues)
        elif format_type == 'html':
            return self._generate_html_report(file_path, issues)
        else:
            return self._generate_text_report(file_path, issues)
    
    def _generate_text_report(self, file_path: str, issues: List[CodeIssue]) -> str:
        """Generate a text-based report"""
        lines = []
        lines.append(f"AI Code Review Report")
        lines.append(f"=" * 50)
        lines.append(f"File: {file_path}")
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Issues: {len(issues)}\n")
        
        if not issues:
            lines.append("✅ No issues found!")
            return '\n'.join(lines)
        
        # Group by severity
        by_severity = {}
        for issue in issues:
            if issue.severity not in by_severity:
                by_severity[issue.severity] = []
            by_severity[issue.severity].append(issue)
        
        # Display summary
        lines.append("Issue Summary:")
        for severity in ['error', 'warning', 'info']:
            if severity in by_severity:
                count = len(by_severity[severity])
                icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[severity]
                lines.append(f"  {icon} {severity.title()}: {count}")
        
        lines.append("\nDetailed Issues:")
        lines.append("-" * 30)
        
        # Sort issues by line number
        sorted_issues = sorted(issues, key=lambda x: x.line)
        
        for issue in sorted_issues:
            icon = {'error': '❌', 'warning': '⚠️', 'info': 'ℹ️'}[issue.severity]
            lines.append(f"{icon} Line {issue.line}: {issue.message}")
            lines.append(f"   Type: {issue.issue_type} | Severity: {issue.severity}")
            lines.append("")
        
        return '\n'.join(lines)
    
    def _generate_json_report(self, file_path: str, issues: List[CodeIssue]) -> str:
        """Generate a JSON report"""
        report_data = {
            'file_path': file_path,
            'generated_at': datetime.now().isoformat(),
            'total_issues': len(issues),
            'summary': {},
            'issues': []
        }
        
        # Build summary
        for issue in issues:
            severity = issue.severity
            if severity not in report_data['summary']:
                report_data['summary'][severity] = 0
            report_data['summary'][severity] += 1
        
        # Build issues list
        for issue in issues:
            report_data['issues'].append({
                'line': issue.line,
                'type': issue.issue_type,
                'message': issue.message,
                'severity': issue.severity
            })
        
        return json.dumps(report_data, indent=2)
    
    def _generate_html_report(self, file_path: str, issues: List[CodeIssue]) -> str:
        """Generate an HTML report"""
        html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Code Review Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #f8f9fa; padding: 20px; border-radius: 5px; }
        .summary { margin: 20px 0; }
        .issue { margin: 10px 0; padding: 10px; border-left: 4px solid #ddd; }
        .error { border-color: #dc3545; background-color: #f8d7da; }
        .warning { border-color: #ffc107; background-color: #fff3cd; }
        .info { border-color: #17a2b8; background-color: #d1ecf1; }
        .severity { font-weight: bold; }
        .line-num { color: #666; }
    </style>
</head>
<body>
    <div class="header">
        <h1>AI Code Review Report</h1>
        <p><strong>File:</strong> {file_path}</p>
        <p><strong>Generated:</strong> {timestamp}</p>
        <p><strong>Total Issues:</strong> {total_issues}</p>
    </div>
    
    <div class="summary">
        <h2>Issue Summary</h2>
        {summary_html}
    </div>
    
    <div class="issues">
        <h2>Detailed Issues</h2>
        {issues_html}
    </div>
</body>
</html>
        """
        
        # Build summary
        summary_counts = {}
        for issue in issues:
            severity = issue.severity
            if severity not in summary_counts:
                summary_counts[severity] = 0
            summary_counts[severity] += 1
        
        summary_html = "<ul>"
        for severity in ['error', 'warning', 'info']:
            if severity in summary_counts:
                count = summary_counts[severity]
                summary_html += f"<li><span class='severity {severity}'>{severity.title()}:</span> {count}</li>"
        summary_html += "</ul>"
        
        # Build issues
        if not issues:
            issues_html = "<p>✅ No issues found!</p>"
        else:
            issues_html = ""
            sorted_issues = sorted(issues, key=lambda x: x.line)
            for issue in sorted_issues:
                issues_html += f"""
                <div class="issue {issue.severity}">
                    <strong>Line <span class="line-num">{issue.line}</span>:</strong> {issue.message}
                    <br>
                    <small>Type: {issue.issue_type} | Severity: {issue.severity}</small>
                </div>
                """
        
        return html_template.format(
            file_path=file_path,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            total_issues=len(issues),
            summary_html=summary_html,
            issues_html=issues_html
        )