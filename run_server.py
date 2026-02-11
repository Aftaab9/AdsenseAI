"""
AdsenseAI Server Launcher
Simple script to start the FastAPI server
"""

import uvicorn
import sys
from pathlib import Path

def main():
    """Launch the AdsenseAI server"""
    print("\n" + "=" * 70)
    print("🚀 Starting AdsenseAI Campaign Risk Analyzer Server")
    print("=" * 70 + "\n")
    
    # Check if .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("   Image analysis will not be available without GEMINI_API_KEY")
        print("   Text-only analysis will still work.\n")
    
    print("Server Configuration:")
    print("  • Host: http://localhost:8000")
    print("  • API Docs: http://localhost:8000/docs")
    print("  • Interface: http://localhost:8000")
    print("\n" + "=" * 70)
    print("Press CTRL+C to stop the server")
    print("=" * 70 + "\n")
    
    try:
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,  # Auto-reload on code changes
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\n" + "=" * 70)
        print("✅ Server stopped successfully")
        print("=" * 70 + "\n")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
