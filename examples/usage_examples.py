"""
Example usage of EPH-MCP
Demonstrates various reasoning scenarios
"""
import asyncio
import json
from eph_mcp.reasoning_engine import EPHReasoningEngine

async def example_basic_reasoning():
    """Basic reasoning example"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Emergent Reasoning")
    print("=" * 80)
    
    engine = EPHReasoningEngine()
    
    query = "What is the relationship between creativity and constraint?"
    
    result = await engine.reason(query)
    
    print(f"\nQuery: {query}")
    print(f"\nResponse:\n{result['response']}")
    print(f"\nStatistics:")
    print(f"  Duration: {result['duration']:.2f}s")
    print(f"  Total patterns: {result['statistics']['patterns']['total']}")
    print(f"  Total insights: {result['statistics']['insights']['total']}")
    
    return result

async def example_complex_reasoning():
    """Complex reasoning with intermediate results"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Complex Reasoning with Intermediate Results")
    print("=" * 80)
    
    engine = EPHReasoningEngine({
        'explosion': {'n_fragments': 100},
        'interaction': {'iterations': 150}
    })
    
    query = "How do emergent properties arise from simple rules in complex systems?"
    
    result = await engine.reason(query, return_intermediate=True)
    
    print(f"\nQuery: {query}")
    print(f"\nResponse:\n{result['response']}")
    
    if 'intermediate' in result:
        print("\n--- Intermediate Results ---")
        print(f"Fragments generated: {len(result['intermediate']['fragments'])}")
        print(f"Field entropy: {result['intermediate']['field_state']['entropy']:.2f}")
        
        print("\nPattern distribution:")
        for pattern_type, patterns in result['intermediate']['patterns'].items():
            if patterns:
                print(f"  {pattern_type}: {len(patterns)}")
        
        print("\nTop insights:")
        for i, insight in enumerate(result['intermediate']['insights'][:3], 1):
            print(f"  {i}. {insight['core_pattern'][:80]}...")
            print(f"     Confidence: {insight['confidence']:.0%}, Novelty: {insight['novelty']:.0%}")
    
    return result

async def example_contradiction_analysis():
    """Analyze contradictions in ideas"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Contradiction and Paradox Analysis")
    print("=" * 80)
    
    engine = EPHReasoningEngine()
    
    query = "Can something be both true and false simultaneously?"
    
    result = await engine.reason(query)
    
    print(f"\nQuery: {query}")
    print(f"\nResponse:\n{result['response']}")
    
    # Check for contradiction patterns
    stats = result['statistics']
    if stats['insights']['with_contradictions'] > 0:
        print(f"\n⚡ Found {stats['insights']['with_contradictions']} insights with contradictions!")
    
    return result

async def example_learning_optimization():
    """Learning strategy optimization"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Learning Strategy Optimization")
    print("=" * 80)
    
    engine = EPHReasoningEngine({
        'weaving': {'max_insights': 7}  # Allow more insights for learnming
    })
    
    query = "What's the optimal way to learn a new programming language when you already know several?"
    
    result = await engine.reason(query)
    
    print(f"\nQuery: {query}")
    print(f"\nResponse:\n{result['response']}")
    
    return result

async def example_creative_exploration():
    """Creative and open-ended exploration"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Creative Exploration")
    print("=" * 80)
    
    engine = EPHReasoningEngine({
        'explosion': {
            'n_fragments': 150,  # More fragments for creativity
            'temperature': 2.0    # Higher temperature for diversity
        }
    })
    
    query = "Imagine new forms of intelligence that don't resemble human or AI intelligence"
    
    result = await engine.reason(query)
    
    print(f"\nQuery: {query}")
    print(f"\nResponse:\n{result['response']}")
    
    # Show high-novelty insights
    print(f"\n Novelty score: {result['statistics']['insights']['avg_novelty']:.0%}")
    
    return result

async def example_meta_reasoning():
    """Reasoning about reasoning itself"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Meta-Reasoning")
    print("=" * 80)
    
    engine = EPHReasoningEngine()
    
    query = "What patterns emerge when we think about thinking?"
    
    result = await engine.reason(query, return_intermediate=True)
    
    print(f"\nQuery: {query}")
    print(f"\nResponse:\n{result['response']}")
    
    # Analyze the reasoning process itself
    if 'intermediate' in result:
        field_state = result['intermediate']['field_state']
        print("\n Meta-analysis of reasoning process:")
        print(f"  Phase transitions: {field_state['phase_transitions']}")
        print(f"  Final entropy: {field_state['entropy']:.2f}")
        print(f"  Fragment bonds: {field_state['num_bonds']}")
    
    return result

async def example_history_analysis():
    """Analyze patterns across multiple reasoning sessions"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Cross-Session Pattern Analysis")
    print("=" * 80)
    
    engine = EPHReasoningEngine()
    
    # Run multiple queries
    queries = [
        "What is consciousness?",
        "How does meaning emerge from symbols?",
        "What is the nature of understanding?"
    ]
    
    print("Running multiple reasoning sessions...")
    for query in queries:
        result = await engine.reason(query)
        print(f"  ✓ Completed: {query[:40]}...")
    
    # Analyze history
    analysis = await engine.analyze_reasoning_history()
    
    print("\n Pattern Analysis Across Sessions:")
    print(f"  Total sessions: {analysis['total_sessions']}")
    print(f"  Average duration: {analysis['avg_duration']:.2f}s")
    print(f"  Total patterns detected: {analysis['total_patterns_detected']}")
    print(f"  Average insights per query: {analysis['avg_insights_per_query']:.1f}")
    
    print("\n  Pattern type frequency:")
    for pattern_type, count in analysis['pattern_type_frequency'].items():
        print(f"    {pattern_type}: {count}")
    
    return analysis

async def main():
    """Run all examples"""
    
    print("\n EPH-MCP Examples")
    print("=" * 80)
    print("Demonstrating Emergent Pattern Hunter reasoning capabilities\n")
    
    # Run examples
    await example_basic_reasoning()
    await example_complex_reasoning()
    await example_contradiction_analysis()
    await example_learning_optimization()
    await example_creative_exploration()
    await example_meta_reasoning()
    await example_history_analysis()
    
    print("\n" + "=" * 80)
    print("✨ Examples complete! EPH reasoning demonstrates:")
    print("  • Bottom-up insight emergence")
    print("  • Pattern detection across multiple types")
    print("  • Contradiction and paradox handling")
    print("  • Creative exploration capabilities")
    print("  • Meta-reasoning awareness")
    print("  • Cross-session pattern analysis")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
