#!/usr/bin/env python
"""
AdsenseAI Campaign Risk Analyzer - Quick Start Script
Runs the FastAPI server with proper configuration
"""

import os
import sys
from dotenv import load_dotenv

def check_env():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("⚠️  Warning: .env file not found!")
        print("   Copy .env.example to .env and add your Gemini API key")
        print("   The server will start but image analysis will not work without the API key.\n")
        return False
    return True

def main():
    """Start the FastAPI server"""
    print("=" * 60)
    print("AdsenseAI Campaign Risk Analyzer")
    print("=" * 60)
    
    # Load environment variables
    load_dotenv()
    
    # Check environment
    check_env()
    
    # Get configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    print(f"\n🚀 Starting server on http://{host}:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"🔍 Alternative Docs: http://localhost:{port}/redoc")
    print(f"❤️  Health Check: http://localhost:{port}/api/health")
    print("\nPress CTRL+C to stop the server\n")
    
    # Import and run
    import uvicorn
    
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
