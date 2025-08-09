#!/usr/bin/env python3
"""
Quick test script for the Visual Explanation MCP Server
"""

import asyncio
import json
from llm_integration import generate_llm_response, LLMProvider

async def test_llm_integration():
    """Test the LLM integration with a simple query"""
    print("🧪 Testing LLM integration...")
    
    try:
        # Test with a simple query
        query = "Why does the Earth have seasons?"
        response = await generate_llm_response(query, LLMProvider.ANTHROPIC)
        
        print("✅ LLM Response received:")
        print(f"   Text: {response['text'][:100]}...")
        
        if 'animation_instructions' in response:
            instructions = response['animation_instructions']
            print(f"   Scene type: {instructions.get('scene_type', 'unknown')}")
            print(f"   Actors: {instructions.get('actors', [])}")
            print("✅ Animation instructions generated")
        else:
            print("ℹ️  No animation instructions (using mock response)")
            
        return True
        
    except Exception as e:
        print(f"❌ LLM integration error: {e}")
        return False

async def main():
    """Run all tests"""
    print("🎬 Visual Explanation MCP Server Tests")
    print("=" * 40)
    
    # Test LLM integration
    llm_success = await test_llm_integration()
    
    print("\n" + "=" * 40)
    if llm_success:
        print("✅ All tests passed! Server should work correctly.")
        print("🚀 Run: python run_server.py")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())