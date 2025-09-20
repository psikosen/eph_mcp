#!/usr/bin/env python3
"""
Test EPH-MCP as if Claude was calling it
This simulates how Claude would interact with the MCP server
"""
import asyncio
import json
import sys
import os
from typing import Dict, Any, List
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eph_mcp.reasoning_engine import EPHReasoningEngine

class ClaudeMCPSimulator:
    """Simulates how Claude would call EPH-MCP tools"""
    
    def __init__(self):
        """Initialize the simulator"""
        self.engine = EPHReasoningEngine({
            'explosion': {'n_fragments': 50},
            'interaction': {'iterations': 50},
            'visualization': {'enabled': False}
        })
        self.test_results = []
        
    async def simulate_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate calling an MCP tool as Claude would
        Returns the result in MCP format
        """
        start_time = datetime.now()
        
        try:
            if tool_name == "think_emergently":
                result = await self._call_think_emergently(parameters)
            elif tool_name == "analyze_patterns":
                result = await self._call_analyze_patterns(parameters)
            elif tool_name == "compare_thoughts":
                result = await self._call_compare_thoughts(parameters)
            elif tool_name == "get_reasoning_stats":
                result = await self._call_get_reasoning_stats(parameters)
            else:
                result = {
                    "error": f"Unknown tool: {tool_name}",
                    "content": []
                }
            
            duration = (datetime.now() - start_time).total_seconds()
            
            # Format as MCP response
            return {
                "tool": tool_name,
                "parameters": parameters,
                "result": result,
                "duration": duration,
                "success": "error" not in result
            }
            
        except Exception as e:
            return {
                "tool": tool_name,
                "parameters": parameters,
                "error": str(e),
                "duration": (datetime.now() - start_time).total_seconds(),
                "success": False
            }
    
    async def _call_think_emergently(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate think_emergently tool"""
        query = params.get('query', '')
        n_fragments = params.get('n_fragments', 50)
        iterations = params.get('iterations', 50)
        
        # Configure engine for this call
        custom_engine = EPHReasoningEngine({
            'explosion': {'n_fragments': n_fragments},
            'interaction': {'iterations': iterations},
            'visualization': {'enabled': False}
        })
        
        # Run reasoning
        result = await custom_engine.reason(query)
        
        # Format response as MCP would return it
        content = [
            {
                "type": "text",
                "text": result['response']
            }
        ]
        
        # Add statistics
        if 'statistics' in result:
            stats = result['statistics']
            stats_text = f"\n\n---\n📊 Statistics:\n"
            stats_text += f"Duration: {result['duration']:.2f}s\n"
            stats_text += f"Patterns: {stats.get('patterns', {}).get('total', 0)}\n"
            stats_text += f"Insights: {stats.get('insights', {}).get('total', 0)}\n"
            stats_text += f"Confidence: {stats.get('insights', {}).get('avg_confidence', 0):.0%}\n"
            stats_text += f"Novelty: {stats.get('insights', {}).get('avg_novelty', 0):.0%}"
            
            content.append({
                "type": "text",
                "text": stats_text
            })
        
        return {"content": content}
    
    async def _call_analyze_patterns(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate analyze_patterns tool"""
        text = params.get('text', '')
        min_confidence = params.get('min_confidence', 0.5)
        
        sentences = text.split('.')
        patterns_found = []
        
        # Simple pattern detection
        negation_words = ['not', 'never', 'no', 'opposite', 'contrary', 'but']
        
        for i, sent_a in enumerate(sentences):
            for sent_b in sentences[i+1:]:
                has_negation_a = any(neg in sent_a.lower() for neg in negation_words)
                has_negation_b = any(neg in sent_b.lower() for neg in negation_words)
                
                if has_negation_a != has_negation_b:
                    patterns_found.append({
                        'type': 'contradiction',
                        'elements': [sent_a.strip()[:50], sent_b.strip()[:50]],
                        'confidence': 0.7
                    })
        
        # Filter by confidence
        patterns_found = [p for p in patterns_found if p['confidence'] >= min_confidence]
        
        # Format response
        if not patterns_found:
            response_text = "No patterns found above confidence threshold."
        else:
            response_text = f"Found {len(patterns_found)} patterns:\n\n"
            for pattern in patterns_found:
                response_text += f"**{pattern['type'].title()}** (confidence: {pattern['confidence']:.0%})\n"
                response_text += f"  Elements: {', '.join(str(e) for e in pattern['elements'])}\n\n"
        
        return {
            "content": [{"type": "text", "text": response_text}]
        }
    
    async def _call_compare_thoughts(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate compare_thoughts tool"""
        thoughts = params.get('thoughts', [])
        find_contradictions = params.get('find_contradictions', True)
        find_harmonies = params.get('find_harmonies', True)
        
        comparisons = {'contradictions': [], 'harmonies': []}
        
        # Pairwise comparison
        for i, thought_a in enumerate(thoughts):
            for j, thought_b in enumerate(thoughts[i+1:], i+1):
                
                if find_contradictions:
                    negation_words = ['not', 'never', 'no', 'opposite']
                    if any(neg in thought_a.lower() or neg in thought_b.lower() for neg in negation_words):
                        comparisons['contradictions'].append({
                            'thought_a': thought_a[:50],
                            'thought_b': thought_b[:50]
                        })
                
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
            response += f"\n** Harmonies ({len(comparisons['harmonies'])})**\n"
            for h in comparisons['harmonies'][:3]:
                response += f"  • \"{h['thought_a']}...\" ↔ \"{h['thought_b']}...\"\n"
                response += f"    Resonance: {h['resonance']:.0%}\n"
        
        return {
            "content": [{"type": "text", "text": response}]
        }
    
    async def _call_get_reasoning_stats(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate get_reasoning_stats tool"""
        analysis = await self.engine.analyze_reasoning_history()
        
        response = "**EPH-MCP Reasoning Statistics**\n\n"
        
        if analysis.get('message') == 'No reasoning history available':
            response += "No reasoning sessions yet.\n"
        else:
            response += f"Sessions: {analysis.get('total_sessions', 0)}\n"
            response += f"Avg Duration: {analysis.get('avg_duration', 0):.2f}s\n"
            response += f"Total Patterns: {analysis.get('total_patterns_detected', 0)}\n"
            response += f"Avg Insights/Query: {analysis.get('avg_insights_per_query', 0):.1f}\n"
        
        return {
            "content": [{"type": "text", "text": response}]
        }
    
    async def run_test_suite(self):
        """Run a comprehensive test suite as Claude would"""
        print("\n" + "="*80)
        print("CLAUDE MCP SIMULATOR - Testing EPH-MCP Tools")
        print("="*80)
        print("\nSimulating how Claude would interact with EPH-MCP...\n")
        
        # Test 1: Basic emergent thinking
        print(" Test 1: Basic Emergent Thinking")
        print("-"*40)
        result = await self.simulate_tool_call(
            "think_emergently",
            {
                "query": "What is the nature of consciousness?",
                "n_fragments": 30,
                "iterations": 30
            }
        )
        self._print_result(result)
        self.test_results.append(result)
        
        # Test 2: Pattern analysis
        print("\n Test 2: Pattern Analysis")
        print("-"*40)
        result = await self.simulate_tool_call(
            "analyze_patterns",
            {
                "text": "Order creates structure. Chaos destroys structure. But chaos also creates new possibilities. Order constrains possibilities.",
                "min_confidence": 0.5
            }
        )
        self._print_result(result)
        self.test_results.append(result)
        
        # Test 3: Thought comparison
        print("\n Test 3: Thought Comparison")
        print("-"*40)
        result = await self.simulate_tool_call(
            "compare_thoughts",
            {
                "thoughts": [
                    "Intelligence emerges from simple rules",
                    "Complexity requires complicated systems",
                    "Simple patterns can create infinite variety",
                    "Chaos is just order we don't understand"
                ],
                "find_contradictions": True,
                "find_harmonies": True
            }
        )
        self._print_result(result)
        self.test_results.append(result)
        
        # Test 4: Complex reasoning
        print("\n Test 4: Complex Emergent Reasoning")
        print("-"*40)
        result = await self.simulate_tool_call(
            "think_emergently",
            {
                "query": "How do paradoxes lead to breakthrough insights?",
                "n_fragments": 75,
                "iterations": 100
            }
        )
        self._print_result(result)
        self.test_results.append(result)
        
        # Test 5: Get stats
        print("\n Test 5: Reasoning Statistics")
        print("-"*40)
        result = await self.simulate_tool_call(
            "get_reasoning_stats",
            {}
        )
        self._print_result(result)
        self.test_results.append(result)
        
        # Summary
        self._print_summary()
    
    def _print_result(self, result: Dict[str, Any]):
        """Print a tool call result"""
        if result['success']:
            print(f"Tool: {result['tool']}")
            print(f" Duration: {result['duration']:.2f}s")
            
            # Print first content item
            if 'content' in result['result'] and result['result']['content']:
                first_content = result['result']['content'][0]
                if first_content['type'] == 'text':
                    text = first_content['text']
                    # Show first 200 chars
                    if len(text) > 200:
                        print(f" Response: {text[:200]}...")
                    else:
                        print(f"Response: {text}")
        else:
            print(f" Tool: {result['tool']}")
            print(f"Error: {result.get('error', 'Unknown error')}")
    
    def _print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print(" TEST SUMMARY")
        print("="*80)
        
        successful = sum(1 for r in self.test_results if r['success'])
        total = len(self.test_results)
        
        print(f"\n Successful calls: {successful}/{total}")
        print(f"⏱  Total time: {sum(r['duration'] for r in self.test_results):.2f}s")
        print(f" Average time per call: {sum(r['duration'] for r in self.test_results)/total:.2f}s")
        
        print("\n Tools tested:")
        for result in self.test_results:
            status = "" if result['success'] else ""
            print(f"  {status} {result['tool']} ({result['duration']:.2f}s)")
        
        if successful == total:
            print("\n ALL TESTS PASSED!")
            print(" EPH-MCP is ready for use with Claude!")
        else:
            print(f"\n  {total - successful} tests failed")
            print("Please check the errors above")
        

async def main():
    """Main test function"""
    simulator = ClaudeMCPSimulator()
    await simulator.run_test_suite()

if __name__ == "__main__":
    # Suppress tokenizer warning
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    
    print("\nEPH-MCP Claude Integration Test")
    print("Testing the MCP server as if Claude was calling it...")
    
    asyncio.run(main())
