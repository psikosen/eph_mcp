"""
EPH-MCP Server
Main server implementation for the Emergent Pattern Hunter MCP
"""
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

from mcp.server import Server
from mcp import Tool
from mcp.types import TextContent, ImageContent, EmbeddedResource
from pydantic import BaseModel, Field

from .reasoning_engine import EPHReasoningEngine
from .visualization import FieldVisualizer

# Tool input models
class ThinkEmergentlyInput(BaseModel):
    """Input for emergent thinking"""
    query: str = Field(..., description="The question or topic to explore through emergent pattern thinking")
    config: Optional[Dict[str, Any]] = Field(None, description="Optional configuration overrides")
    return_intermediate: bool = Field(False, description="Whether to return intermediate reasoning artifacts")
    visualize: bool = Field(True, description="Whether to generate visualizations")

class AnalyzePatternInput(BaseModel):
    """Input for pattern analysis"""
    text: str = Field(..., description="Text to analyze for emergent patterns")
    pattern_types: Optional[List[str]] = Field(None, description="Specific pattern types to look for")
    min_confidence: float = Field(0.5, description="Minimum confidence threshold for patterns")

class CompareThoughtsInput(BaseModel):
    """Input for comparing multiple thoughts"""
    thoughts: List[str] = Field(..., description="List of thoughts/ideas to compare for patterns")
    find_contradictions: bool = Field(True, description="Whether to specifically look for contradictions")
    find_harmonies: bool = Field(True, description="Whether to look for harmonic resonances")

class ReasoningHistoryInput(BaseModel):
    """Input for accessing reasoning history"""
    session_id: Optional[str] = Field(None, description="Specific session ID to retrieve")
    last_n: int = Field(5, description="Number of recent sessions to retrieve")
    analyze: bool = Field(False, description="Whether to analyze patterns across history")

class EPHMCPServer:
    """Main EPH-MCP Server"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize EPH-MCP server"""
        
        # Initialize MCP server
        self.server = Server("eph-mcp")
        
        # Initialize reasoning engine
        self.engine = EPHReasoningEngine(config)
        
        # Track active sessions
        self.active_sessions = {}
        
        # Register tools
        self._register_tools()
        
        print("🌟 EPH-MCP Server initialized")
    
    def _register_tools(self):
        """Register all EPH tools with the MCP server"""
        
        # Main reasoning tool
        self.server.add_tool(Tool(
            name="think_emergently",
            description=(
                "Apply emergent pattern thinking to explore a question or topic. "
                "This tool explodes thoughts into fragments, simulates their interactions, "
                "detects emergent patterns, crystallizes insights, and weaves them into "
                "a coherent response. Unlike sequential thinking, this discovers insights "
                "through bottom-up emergence."
            ),
            input_schema=ThinkEmergentlyInput.schema(),
            handler=self.think_emergently
        ))
        
        # Pattern analysis tool
        self.server.add_tool(Tool(
            name="analyze_patterns",
            description=(
                "Analyze text for emergent patterns without full reasoning process. "
                "Useful for finding patterns in existing content."
            ),
            input_schema=AnalyzePatternInput.schema(),
            handler=self.analyze_patterns
        ))
        
        # Thought comparison tool
        self.server.add_tool(Tool(
            name="compare_thoughts",
            description=(
                "Compare multiple thoughts or ideas to find relationships, "
                "contradictions, harmonies, and emergent connections."
            ),
            input_schema=CompareThoughtsInput.schema(),
            handler=self.compare_thoughts
        ))
        
        # History analysis tool
        self.server.add_tool(Tool(
            name="reasoning_history",
            description=(
                "Access and analyze the history of reasoning sessions to find "
                "meta-patterns across multiple queries."
            ),
            input_schema=ReasoningHistoryInput.schema(),
            handler=self.reasoning_history
        ))
    
    async def think_emergently(self, input: ThinkEmergentlyInput) -> List[Any]:
        """Main emergent thinking handler"""
        
        try:
            # Run reasoning engine
            result = await self.engine.reason(
                query=input.query,
                return_intermediate=input.return_intermediate
            )
            
            # Store session
            session_id = result.get('session_id')
            if session_id:
                self.active_sessions[session_id] = {
                    'query': input.query,
                    'timestamp': datetime.now().isoformat(),
                    'result': result
                }
            
            # Prepare response content
            content = [
                TextContent(
                    type="text",
                    text=result['response']
                )
            ]
            
            # Add statistics if available
            if 'statistics' in result:
                stats_text = self._format_statistics(result['statistics'])
                content.append(TextContent(
                    type="text",
                    text=f"\n\n---\n📊 Reasoning Statistics:\n{stats_text}"
                ))
            
            # Add intermediate results if requested
            if input.return_intermediate and 'intermediate' in result:
                intermediate_json = json.dumps(result['intermediate'], indent=2)
                content.append(EmbeddedResource(
                    type="embedded",
                    resource_type="application/json",
                    title="Intermediate Reasoning Artifacts",
                    content=intermediate_json
                ))
            
            # Add visualization links if generated
            if input.visualize:
                session = self.engine.get_session_details(session_id)
                if session and 'visualizations' in session:
                    viz_text = "\n\n🎨 Visualizations generated:\n"
                    for viz_type, filepath in session['visualizations'].items():
                        viz_text += f"  • {viz_type}: {filepath}\n"
                    content.append(TextContent(
                        type="text",
                        text=viz_text
                    ))
            
            return content
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error in emergent thinking: {str(e)}"
            )]
    
    async def analyze_patterns(self, input: AnalyzePatternInput) -> List[Any]:
        """Analyze text for patterns without full reasoning"""
        
        try:
            # Create minimal fragments from text
            from .phases.explosion import ThoughtExplosion
            
            explosion = ThoughtExplosion()
            
            # Generate fragments from text chunks
            sentences = input.text.split('.')
            fragments = []
            
            for sentence in sentences[:20]:  # Limit to 20 sentences
                if sentence.strip():
                    fragment = await explosion._generate_fragment(
                        sentence.strip(), 
                        'decompose_mechanically',
                        None
                    )
                    if fragment[0]:
                        fragments.append(fragment[0])
            
            # Quick pattern detection
            patterns_found = []
            
            # Look for contradictions
            for i, sent_a in enumerate(sentences):
                for sent_b in sentences[i+1:]:
                    if self._detect_contradiction(sent_a, sent_b):
                        patterns_found.append({
                            'type': 'contradiction',
                            'elements': [sent_a[:50], sent_b[:50]],
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
                            if p['confidence'] >= input.min_confidence]
            
            # Format response
            response = f"Found {len(patterns_found)} patterns in text:\n\n"
            
            for pattern in patterns_found:
                response += f"**{pattern['type'].title()} Pattern** (confidence: {pattern['confidence']:.0%})\n"
                response += f"  Elements: {', '.join(pattern['elements'])}\n\n"
            
            return [TextContent(type="text", text=response)]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error analyzing patterns: {str(e)}"
            )]
    
    async def compare_thoughts(self, input: CompareThoughtsInput) -> List[Any]:
        """Compare multiple thoughts for patterns"""
        
        try:
            # Quick comparison without full reasoning
            comparisons = {
                'contradictions': [],
                'harmonies': [],
                'bridges': [],
                'clusters': []
            }
            
            # Pairwise comparison
            for i, thought_a in enumerate(input.thoughts):
                for j, thought_b in enumerate(input.thoughts[i+1:], i+1):
                    
                    # Check for contradictions
                    if input.find_contradictions:
                        if self._detect_contradiction(thought_a, thought_b):
                            comparisons['contradictions'].append({
                                'thought_a': thought_a[:50],
                                'thought_b': thought_b[:50],
                                'tension': 'opposing concepts detected'
                            })
                    
                    # Check for harmonies
                    if input.find_harmonies:
                        harmony = self._detect_harmony(thought_a, thought_b)
                        if harmony > 0.5:
                            comparisons['harmonies'].append({
                                'thought_a': thought_a[:50],
                                'thought_b': thought_b[:50],
                                'resonance': harmony
                            })
            
            # Format response
            response = f"Comparison of {len(input.thoughts)} thoughts:\n\n"
            
            if comparisons['contradictions']:
                response += f"**🔥 Contradictions Found ({len(comparisons['contradictions'])})**\n"
                for c in comparisons['contradictions'][:3]:
                    response += f"  • \"{c['thought_a']}...\" ↔ \"{c['thought_b']}...\"\n"
                    response += f"    Tension: {c['tension']}\n"
                response += "\n"
            
            if comparisons['harmonies']:
                response += f"**🎵 Harmonies Found ({len(comparisons['harmonies'])})**\n"
                for h in comparisons['harmonies'][:3]:
                    response += f"  • \"{h['thought_a']}...\" ↔ \"{h['thought_b']}...\"\n"
                    response += f"    Resonance: {h['resonance']:.0%}\n"
                response += "\n"
            
            if not comparisons['contradictions'] and not comparisons['harmonies']:
                response += "No strong patterns detected between thoughts.\n"
            
            return [TextContent(type="text", text=response)]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error comparing thoughts: {str(e)}"
            )]
    
    async def reasoning_history(self, input: ReasoningHistoryInput) -> List[Any]:
        """Access and analyze reasoning history"""
        
        try:
            response = ""
            
            if input.session_id:
                # Get specific session
                session = self.engine.get_session_details(input.session_id)
                if session:
                    response = f"**Session: {input.session_id}**\n"
                    response += f"Query: {session['query']}\n"
                    response += f"Duration: {session['duration']:.2f}s\n\n"
                    
                    # Add phase details
                    for phase, data in session['phases'].items():
                        response += f"{phase.title()}: {data.get('duration', 0):.3f}s\n"
                else:
                    response = f"Session {input.session_id} not found."
            
            elif input.analyze:
                # Analyze patterns across history
                analysis = await self.engine.analyze_reasoning_history()
                
                response = "**Reasoning History Analysis**\n\n"
                response += f"Total sessions: {analysis['total_sessions']}\n"
                response += f"Average duration: {analysis['avg_duration']:.2f}s\n"
                response += f"Total patterns detected: {analysis['total_patterns_detected']}\n"
                response += f"Average insights per query: {analysis['avg_insights_per_query']:.1f}\n\n"
                
                if analysis['pattern_type_frequency']:
                    response += "**Pattern Type Distribution:**\n"
                    for ptype, count in analysis['pattern_type_frequency'].items():
                        response += f"  • {ptype}: {count}\n"
            
            else:
                # Get recent sessions
                history = self.engine.reasoning_history[-input.last_n:]
                
                response = f"**Last {len(history)} Reasoning Sessions**\n\n"
                for session in history:
                    response += f"• {session['id']}\n"
                    response += f"  Query: {session['query'][:50]}...\n"
                    response += f"  Duration: {session['duration']:.2f}s\n"
                    response += f"  Patterns: {session['phases']['detection']['total_patterns']}\n"
                    response += f"  Insights: {session['phases']['crystallization']['n_insights']}\n\n"
            
            return [TextContent(type="text", text=response)]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error accessing history: {str(e)}"
            )]
    
    def _format_statistics(self, stats: Dict) -> str:
        """Format statistics for display"""
        
        lines = []
        
        if 'fragments' in stats:
            lines.append(f"Fragments: {stats['fragments']['total']} "
                        f"(avg activation: {stats['fragments']['avg_activation']:.2f})")
        
        if 'patterns' in stats:
            lines.append(f"Patterns: {stats['patterns']['total']} total")
            for ptype, count in stats['patterns']['by_type'].items():
                if count > 0:
                    lines.append(f"  • {ptype}: {count}")
        
        if 'insights' in stats:
            lines.append(f"Insights: {stats['insights']['total']} "
                        f"(confidence: {stats['insights']['avg_confidence']:.0%}, "
                        f"novelty: {stats['insights']['avg_novelty']:.0%})")
        
        return '\n'.join(lines)
    
    def _detect_contradiction(self, text_a: str, text_b: str) -> bool:
        """Simple contradiction detection"""
        
        negation_words = ['not', 'never', 'no', 'opposite', 'contrary', 'but']
        
        for neg in negation_words:
            if (neg in text_a.lower() and neg not in text_b.lower()) or \
               (neg in text_b.lower() and neg not in text_a.lower()):
                return True
        
        return False
    
    def _detect_harmony(self, text_a: str, text_b: str) -> float:
        """Simple harmony detection"""
        
        words_a = set(text_a.lower().split())
        words_b = set(text_b.lower().split())
        
        if not words_a or not words_b:
            return 0.0
        
        overlap = len(words_a & words_b)
        total = len(words_a | words_b)
        
        return overlap / total if total > 0 else 0.0
    
    async def run(self, host: str = "localhost", port: int = 3333):
        """Run the EPH-MCP server"""
        
        print(f"🚀 Starting EPH-MCP server on {host}:{port}")
        print("💫 Emergent Pattern Hunter ready for reasoning!")
        
        try:
            await self.server.run(host=host, port=port)
        except KeyboardInterrupt:
            print("\n👋 EPH-MCP server shutting down...")
        except Exception as e:
            print(f"❌ Server error: {e}")

def main():
    """Main entry point"""
    
    import argparse
    
    parser = argparse.ArgumentParser(description='EPH-MCP Server')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    parser.add_argument('--port', type=int, default=3333, help='Port to bind to')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Load config if provided
    config = None
    if args.config:
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    # Create and run server
    server = EPHMCPServer(config)
    asyncio.run(server.run(host=args.host, port=args.port))

if __name__ == '__main__':
    main()
