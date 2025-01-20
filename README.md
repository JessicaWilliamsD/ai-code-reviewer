# AI Code Reviewer

A simple AI-powered code review tool that helps analyze code quality and suggest improvements.

## Features

- Automated code analysis
- Support for multiple programming languages
- Generate detailed review reports
- Easy to use CLI interface
- RESTful API for integration

## Getting Started

### Installation

```bash
pip install -r requirements.txt
```

### CLI Usage

Single file analysis:
```bash
python cli.py path/to/your/file.py
python cli.py --format json path/to/your/file.py
python cli.py --format html --output report.html path/to/your/file.py
```

Batch analysis for directories:
```bash
python cli.py --batch src/
python cli.py --batch --pattern "**/*.py" src/
python cli.py --batch --format json --output batch_report.json src/
```

### API Usage

Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`