#!/usr/bin/env python3
"""
AI Code Reviewer - Main application entry point
"""

import os
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from analyzer import CodeAnalyzer

app = FastAPI(
    title="AI Code Reviewer",
    description="AI-powered code review and analysis tool",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Code Reviewer API", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/analyze")
async def analyze_code(file: UploadFile = File(...)):
    """Analyze uploaded code file"""
    if not file.filename:
        return {"error": "No file provided"}
    
    # Save uploaded file temporarily
    temp_path = f"/tmp/{file.filename}"
    
    try:
        content = await file.read()
        with open(temp_path, "wb") as f:
            f.write(content)
        
        # Analyze the file
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_file(temp_path)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return {
            "filename": file.filename,
            "issues_count": len(issues),
            "issues": [
                {
                    "line": issue.line,
                    "type": issue.issue_type,
                    "message": issue.message,
                    "severity": issue.severity
                } for issue in issues
            ]
        }
        
    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)