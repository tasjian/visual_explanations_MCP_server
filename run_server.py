#!/usr/bin/env python3
"""
Visual Explanation MCP Server Startup Script
"""

import os
import sys
import asyncio
from pathlib import Path

def check_requirements():
    """Check if all required dependencies are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pydantic'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n💡 Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True

def check_environment():
    """Check environment variables and configuration"""
    print("\n🔧 Environment Configuration:")
    
    # Check for API keys (optional)
    api_keys = {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY')
    }
    
    for key, value in api_keys.items():
        if value:
            print(f"✅ {key}: configured")
        else:
            print(f"⚠️  {key}: not set (will use mock responses)")
    
    if not any(api_keys.values()):
        print("\n💡 To use real LLM responses, set one of the API keys:")
        print("   export OPENAI_API_KEY='your-key-here'")
        print("   export ANTHROPIC_API_KEY='your-key-here'")

def print_banner():
    """Print startup banner"""
    banner = """
    🎬 Visual Explanation MCP Server 🎬
    =====================================
    
    An MCP server that generates animated visual explanations
    for scientific and educational concepts using AI.
    
    Features:
    • Text explanations from AI models  
    • Structured animation instructions
    • Interactive 3D/2D visualizations
    • Multiple animation templates
    """
    print(banner)

def main():
    """Main startup function"""
    print_banner()
    
    if not check_requirements():
        sys.exit(1)
    
    check_environment()
    
    print(f"\n🚀 Starting server...")
    print(f"📁 Working directory: {Path.cwd()}")
    print(f"🌐 Server URL: http://localhost:8000")
    print(f"📺 Demo page: http://localhost:8000/demo")
    print(f"📚 API docs: http://localhost:8000/docs")
    print(f"\n📝 Try asking: 'Why does the Earth have seasons?'")
    print("=" * 50)
    
    # Import and run the server
    try:
        import uvicorn
        from mcp_server import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down server...")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()