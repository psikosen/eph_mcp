#!/usr/bin/env python3
"""
EPH-MCP Server using FastMCP for simplicity
"""
import asyncio
from typing import Dict, List, Any, Optional
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from eph_mcp.reasoning_engine import EPHReasoningEngine

# Initialize FastMCP server
mcp = FastMCP("eph-mcp")

# Global engine instance
engine: Optional[EPHReasoningEngine] = None

def get_engine() -> EPHReasoningEngine:
    """Get or create the reasoning engine"""
    global engine
    if engine is None:
        engine = EPHReasoningEngine({
            'explosion': {'n_fragments': 50},
            'interaction': {'iterations': 50},
            'visualization': {'enabled': False}
        })
    return engine

@mcp.tool()
async def think_emergently(
    query: str = Field(..., description="The question or topic to explore"),
    n_fragments: int = Field(50, description="Number of thought fragments to generate"),
    iterations: int = Field(50, description="Number of interaction iterations")
) -> str:
    """
    Apply emergent pattern thinking to explore a question or topic.
    This tool explodes thoughts into fragments, simulates their interactions,
    detects emergent patterns, crystallizes insights, and weaves them into
    a coherent response.
    """
    try:
        # Get or create engine with custom config
        custom_engine = EPHReasoningEngine({
            'explosion': {'n_fragments': n_fragments},
            'interaction': {'iterations': iterations},
            'visualization': {'enabled': False}
        })
        
        # Run reasoning
        result = await custom_engine.reason(query)
        
        # Format response with statistics
        response = result['response']
        
        stats = result.get('statistics', {})
        if stats:
            response += f"\n\n---\nStatistics:\n"
            response += f"Duration: {result['duration']:.2f}s\n"
            response += f"Patterns: {stats.get('patterns', {}).get('total', 0)}\n"
            response += f"Insights: {stats.get('insights', {}).get('total', 0)}\n"
            
            if 'insights' in stats:
                response += f"Confidence: {stats['insights'].get('avg_confidence', 0):.0%}\n"
                response += f"Novelty: {stats['insights'].get('avg_novelty', 0):.0%}"
        
        return response
        
    except Exception as e:
        return f" Error in emergent thinking: {str(e)}"

@mcp.tool()
async def analyze_patterns(
    text: str = Field(..., description="Text to analyze for emergent patterns"),
    min_confidence: float = Field(0.5, description="Minimum confidence threshold")
) -> str:
    """
    Analyze text for emergent patterns without full reasoning process.
    Finds contradictions, repetitions, and other patterns in the text.
    """
    try:
        sentences = text.split('.')
        patterns_found = []
        
        # Look for contradictions
        negation_words = ['not', 'never', 'no', 'opposite', 'contrary', 'but']
        for i, sent_a in enumerate(sentences):
            for sent_b in sentences[i+1:]:
                # Check for contradictions
                has_negation_a = any(neg in sent_a.lower() for neg in negation_words)
                has_negation_b = any(neg in sent_b.lower() for neg in negation_words)
                
                if has_negation_a != has_negation_b:
                    patterns_found.append({
                        'type': 'contradiction',
                        'elements': [sent_a.strip()[:50], sent_b.strip()[:50]],
                        'confidence': 0.7
                    })
        
        # Look for repetitions
        word_freq = {}
        for sentence in sentences:
            for word in sentence.lower().split():
                if len(word) > 4:
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        repetitions = [(w, f) for w, f in word_freq.items() if f >= 3]
        if repetitions:
            patterns_found.append({
                'type': 'repetition',
                'elements': [w for w, f in repetitions[:5]],
                'confidence': 0.8
            })
        
        # Filter by confidence
        patterns_found = [p for p in patterns_found 
                        if p['confidence'] >= min_confidence]
        
        # Format response
        if not patterns_found:
            return "No patterns found above confidence threshold."
        
        response = f"Found {len(patterns_found)} patterns:\n\n"
        for pattern in patterns_found:
            response += f"**{pattern['type'].title()}** (confidence: {pattern['confidence']:.0%})\n"
            response += f"  Elements: {', '.join(str(e) for e in pattern['elements'])}\n\n"
        
        return response
        
    except Exception as e:
        return f" Error analyzing patterns: {str(e)}"

@mcp.tool()
async def compare_thoughts(
    thoughts: List[str] = Field(..., description="List of thoughts to compare"),
    find_contradictions: bool = Field(True, description="Look for contradictions"),
    find_harmonies: bool = Field(True, description="Look for harmonies")
) -> str:
    """
    Compare multiple thoughts or ideas to find relationships,
    contradictions, harmonies, and emergent connections.
    """
    try:
        comparisons = {
            'contradictions': [],
            'harmonies': []
        }
        
        # Pairwise comparison
        for i, thought_a in enumerate(thoughts):
            for j, thought_b in enumerate(thoughts[i+1:], i+1):
                
                # Check for contradictions
                if find_contradictions:
                    negation_words = ['not', 'never', 'no', 'opposite', 'contrary']
                    has_negation = any(neg in thought_a.lower() or neg in thought_b.lower() 
                                     for neg in negation_words)
                    
                    if has_negation:
                        comparisons['contradictions'].append({
                            'thought_a': thought_a[:50],
                            'thought_b': thought_b[:50]
                        })
                
                # Check for harmonies
                if find_harmonies:
                    words_a = set(thought_a.lower().split())
                    words_b = set(thought_b.lower().split())
                    
                    if words_a and words_b:
                        overlap = len(words_a & words_b)
                        total = len(words_a | words_b)
                        harmony = overlap / total if total > 0 else 0.0
                        
                        if harmony > 0.3:
                            comparisons['harmonies'].append({
                                'thought_a': thought_a[:50],
                                'thought_b': thought_b[:50],
                                'resonance': harmony
                            })
        
        # Format response
        response = f"Comparison of {len(thoughts)} thoughts:\n\n"
        
        if comparisons['contradictions']:
            response += f"** Contradictions ({len(comparisons['contradictions'])})**\n"
            for c in comparisons['contradictions'][:3]:
                response += f"  • \"{c['thought_a']}...\" ↔ \"{c['thought_b']}...\"\n"
        
        if comparisons['harmonies']:
            response += f"\n**🎵 Harmonies ({len(comparisons['harmonies'])})**\n"
            for h in comparisons['harmonies'][:3]:
                response += f"  • \"{h['thought_a']}...\" ↔ \"{h['thought_b']}...\"\n"
                response += f"    Resonance: {h['resonance']:.0%}\n"
        
        if not comparisons['contradictions'] and not comparisons['harmonies']:
            response += "No strong patterns detected between thoughts."
        
        return response
        
    except Exception as e:
        return f" Error comparing thoughts: {str(e)}"

@mcp.tool()
async def get_reasoning_stats() -> str:
    """
    Get statistics about the current reasoning engine state and history.
    """
    try:
        eng = get_engine()
        
        # Get history analysis
        analysis = await eng.analyze_reasoning_history()
        
        response = "**EPH-MCP Reasoning Statistics**\n\n"
        
        if analysis.get('message') == 'No reasoning history available':
            response += "No reasoning sessions yet.\n"
            response += "Use 'think_emergently' to start reasoning!"
        else:
            response += f"Sessions: {analysis.get('total_sessions', 0)}\n"
            response += f"Avg Duration: {analysis.get('avg_duration', 0):.2f}s\n"
            response += f"Total Patterns: {analysis.get('total_patterns_detected', 0)}\n"
            response += f"Avg Insights/Query: {analysis.get('avg_insights_per_query', 0):.1f}\n"
            
            if 'pattern_type_frequency' in analysis:
                response += "\n**Pattern Types:**\n"
                for ptype, count in analysis['pattern_type_frequency'].items():
                    response += f"  • {ptype}: {count}\n"
        
        return response
        
    except Exception as e:
        return f" Error getting stats: {str(e)}"

if __name__ == "__main__":
    # Run the server
    mcp.run()
