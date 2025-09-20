#!/usr/bin/env python3
"""
Quick start script for EPH-MCP
Run this to test the system immediately
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

async def quick_demo():
    """Quick demonstration of EPH reasoning"""
    
    print("🌟 EPH-MCP Quick Start Demo")
    print("=" * 60)
    
    # Minimal imports to avoid dependency issues
    try:
        from eph_mcp.reasoning_engine import EPHReasoningEngine
        print("✓ EPH-MCP loaded successfully")
    except ImportError as e:
        print(f" Failed to load EPH-MCP: {e}")
        print("\nPlease install dependencies:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm")
        return False
    
    print("\n Running quick reasoning test...")
    print("-" * 60)
    
    # Create engine with minimal config for speed
    engine = EPHReasoningEngine({
        'explosion': {'n_fragments': 20},
        'interaction': {'iterations': 10},
        'visualization': {'enabled': False}
    })
    
    # Test query
    query = "What emerges when order meets chaos?"
    print(f"\n Query: {query}")
    print("\n⚡ Processing (this may take 10-30 seconds)...")
    
    try:
        # Run reasoning
        result = await engine.reason(query)
        
        print("\n Response:")
        print("-" * 60)
        print(result['response'])
        print("-" * 60)
        
        # Show statistics
        stats = result['statistics']
        print(f"\n Statistics:")
        print(f"  • Duration: {result['duration']:.2f} seconds")
        print(f"  • Fragments: {stats['fragments']['total']}")
        print(f"  • Patterns detected: {stats['patterns']['total']}")
        print(f"  • Insights generated: {stats['insights']['total']}")
        print(f"  • Average confidence: {stats['insights']['avg_confidence']:.0%}")
        print(f"  • Average novelty: {stats['insights']['avg_novelty']:.0%}")
        
        # Show pattern distribution
        if stats['patterns']['by_type']:
            print("\n Pattern types found:")
            for ptype, count in stats['patterns']['by_type'].items():
                if count > 0:
                    print(f"  • {ptype}: {count}")
        
        print("\n" + "=" * 60)
        print(" Quick demo completed successfully!")
        print("\n Next steps:")
        print("  1. Start the MCP server: python -m eph_mcp.server")
        print("  2. Run examples: python examples/usage_examples.py")
        print("  3. Run tests: python tests/test_basic.py")
        print("  4. Read the README.md for full documentation")
        
        return True
        
    except Exception as e:
        print(f"\n Error during reasoning: {e}")
        print("\nThis might be due to missing dependencies.")
        print("Make sure you have installed:")
        print("  • sentence-transformers")
        print("  • spacy (with en_core_web_sm model)")
        print("  • torch")
        return False

def main():
    """Main entry point"""
    print("\n" + "=" * 60)
    print("     EMERGENT PATTERN HUNTER - QUICK START")
    print("=" * 60)
    print("\nInitializing EPH reasoning engine...")
    
    
    # Run demo
    success = asyncio.run(quick_demo())
    
    if success:
        print("\n EPH-MCP is ready to use!")
    else: 
        print("\n Please resolve the issues above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
