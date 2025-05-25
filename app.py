"""
Simple FastAPI app to handle health checks and route to Streamlit.
"""
from fastapi import FastAPI, Response
from fastapi.responses import RedirectResponse
import uvicorn
import os
import sys
from pathlib import Path

app = FastAPI()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/")
async def root():
    return RedirectResponse(url="/_stcore/")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8501))
    uvicorn.run(app, host="0.0.0.0", port=port)
