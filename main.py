#!/usr/bin/env python3
"""
AI Code Reviewer - Main application entry point
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)