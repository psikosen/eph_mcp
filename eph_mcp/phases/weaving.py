"""
Phase 5: Pattern Weaver
Weave crystallized insights into coherent response
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from .. import CrystallizedInsight
import asyncio

class PatternWeaver:
    """Weaves crystallized insights into coherent response"""
    
    def __init__(self):
        """Initialize weaver"""
        self.max_insights_per_response = 5
        self.coherence_threshold = 0.6
        
        # Weaving strategies
        self.weaving_strategies = [
            'hierarchical',    # Most important first
            'narrative',       # Tell a story
            'dialectical',     # Thesis-antithesis-synthesis
            'convergent',      # Multiple paths to same conclusion
            'exploratory',     # Open-ended exploration
            'crystalline'      # Clear structured presentation
        ]
        
    async def weave(self, insights: List[CrystallizedInsight], 
                   original_query: str) -> str:
        """Weave insights into final response"""
        
        if not insights:
            return await self._generate_fallback_response(original_query)
        
        # Select weaving strategy based on insights
        strategy = self._select_weaving_strategy(insights, original_query)
        
        # Create loom (structure for weaving)
        loom = self._initialize_loom(original_query, strategy)
        
        # Sort insights by relevance and strength
        sorted_insights = self._prioritize_insights(insights, original_query)
        
        # Select top insights
        selected = sorted_insights[:self.max_insights_per_response]
        
        # Weave based on strategy
        weaving_methods = {
            'hierarchical': self._weave_hierarchical,
            'narrative': self._weave_narrative,
            'dialectical': self._weave_dialectical,
            'convergent': self._weave_convergent,
            'exploratory': self._weave_exploratory,
            'crystalline': self._weave_crystalline
        }
        
        method = weaving_methods.get(strategy, self._weave_hierarchical)
        response = await method(selected, loom)
        
        # Add meta-commentary if appropriate
        if self._should_add_meta_commentary(selected):
            response += self._generate_meta_commentary(selected)
        
        return response
    
    def _select_weaving_strategy(self, insights: List[CrystallizedInsight], 
                                query: str) -> str:
        """Select appropriate weaving strategy"""
        
        # Analyze insights characteristics
        has_contradictions = any(i.contradictions for i in insights)
        has_high_novelty = any(i.novelty > 0.8 for i in insights)
        has_convergence = self._check_convergence(insights)
        is_question = '?' in query
        
        # Select strategy based on characteristics
        if has_contradictions:
            return 'dialectical'
        elif has_convergence:
            return 'convergent'
        elif has_high_novelty:
            return 'exploratory'
        elif is_question:
            return 'crystalline'
        elif len(insights) > 3:
            return 'narrative'
        else:
            return 'hierarchical'
    
    def _initialize_loom(self, query: str, strategy: str) -> Dict:
        """Initialize weaving structure"""
        
        return {
            'query': query,
            'strategy': strategy,
            'threads': [],  # Individual insight threads
            'pattern': [],  # How threads connect
            'texture': 'smooth',  # Smooth vs rough texture
            'density': 'medium',  # How tightly woven
            'color_scheme': 'balanced'  # Emotional tone
        }
    
    def _prioritize_insights(self, insights: List[CrystallizedInsight], 
                           query: str) -> List[CrystallizedInsight]:
        """Prioritize insights by relevance and quality"""
        
        query_words = set(query.lower().split())
        
        for insight in insights:
            # Calculate relevance to query
            insight_words = set(insight.core_pattern.lower().split())
            relevance = len(query_words & insight_words) / max(len(query_words), 1)
            
            # Combined score
            insight.weaving_score = (
                relevance * 0.3 +
                insight.confidence * 0.3 +
                insight.novelty * 0.2 +
                insight.clarity * 0.2
            )
        
        return sorted(insights, key=lambda i: i.weaving_score, reverse=True)
    
    async def _weave_hierarchical(self, insights: List[CrystallizedInsight], 
                                 loom: Dict) -> str:
        """Hierarchical weaving - most important first"""
        
        response_parts = []
        
        # Lead with strongest insight
        if insights:
            primary = insights[0]
            response_parts.append(f"{primary.core_pattern}\n")
            
            # Add supporting insights
            if len(insights) > 1:
                response_parts.append("\nThis connects to several key observations:\n")
                
                for insight in insights[1:]:
                    response_parts.append(f"\n• {insight.core_pattern}")
                    
                    # Add one key variation or implication
                    if insight.variations:
                        response_parts.append(f"\n  - {insight.variations[0]}")
            
            # Conclude with synthesis
            if len(insights) > 2:
                synthesis = self._synthesize_insights(insights)
                response_parts.append(f"\n\n{synthesis}")
        
        return "".join(response_parts)
    
    async def _weave_narrative(self, insights: List[CrystallizedInsight], 
                              loom: Dict) -> str:
        """Narrative weaving - tell a story"""
        
        response_parts = []
        
        # Opening - set the scene
        response_parts.append("The pattern begins to emerge through multiple layers:\n\n")
        
        # Development - unfold insights sequentially
        for i, insight in enumerate(insights):
            if i == 0:
                response_parts.append(f"First, {insight.core_pattern.lower()}\n")
            elif i == len(insights) - 1:
                response_parts.append(f"\nFinally, {insight.core_pattern.lower()}\n")
            else:
                transition = self._get_transition_phrase(insights[i-1], insight)
                response_parts.append(f"\n{transition}, {insight.core_pattern.lower()}\n")
            
            # Add color with variations
            if insight.variations and i < 2:  # Only for first two
                response_parts.append(f"({insight.variations[0]})\n")
        
        # Resolution - what it means
        if insights:
            implications = self._extract_key_implications(insights)
            response_parts.append(f"\n{implications}")
        
        return "".join(response_parts)
    
    async def _weave_dialectical(self, insights: List[CrystallizedInsight], 
                                loom: Dict) -> str:
        """Dialectical weaving - thesis, antithesis, synthesis"""
        
        response_parts = []
        
        # Find contradictions
        thesis_insights = []
        antithesis_insights = []
        
        for insight in insights:
            if insight.contradictions:
                antithesis_insights.append(insight)
            else:
                thesis_insights.append(insight)
        
        # Present thesis
        if thesis_insights:
            response_parts.append("**Thesis:**\n")
            response_parts.append(f"{thesis_insights[0].core_pattern}\n")
        
        # Present antithesis
        if antithesis_insights:
            response_parts.append("\n**Antithesis:**\n")
            response_parts.append(f"{antithesis_insights[0].core_pattern}\n")
            
            if antithesis_insights[0].contradictions:
                response_parts.append("The contradiction lies in:\n")
                for contradiction in antithesis_insights[0].contradictions[:2]:
                    response_parts.append(f"- {contradiction}\n")
        
        # Synthesis
        response_parts.append("\n**Synthesis:**\n")
        
        if thesis_insights and antithesis_insights:
            synthesis = self._create_dialectical_synthesis(thesis_insights[0], 
                                                          antithesis_insights[0])
            response_parts.append(synthesis)
        else:
            # Fallback if no clear contradiction
            response_parts.append(self._synthesize_insights(insights))
        
        return "".join(response_parts)
    
    async def _weave_convergent(self, insights: List[CrystallizedInsight], 
                               loom: Dict) -> str:
        """Convergent weaving - multiple paths to same conclusion"""
        
        response_parts = []
        
        # Find convergence point
        convergence = self._find_convergence_point(insights)
        
        response_parts.append(f"Multiple perspectives converge on a central insight: "
                            f"{convergence}\n\n")
        
        # Show different paths
        response_parts.append("Different angles reveal the same truth:\n\n")
        
        for i, insight in enumerate(insights[:3]):  # Limit to 3 paths
            response_parts.append(f"Path {i+1}: {insight.core_pattern}\n")
            
            if insight.implications:
                response_parts.append(f"→ {insight.implications[0]}\n\n")
        
        # Convergence conclusion
        response_parts.append(f"All paths lead to: {convergence}\n")
        
        return "".join(response_parts)
    
    async def _weave_exploratory(self, insights: List[CrystallizedInsight], 
                                loom: Dict) -> str:
        """Exploratory weaving - open-ended exploration"""
        
        response_parts = []
        
        # Open with wonder
        response_parts.append("This reveals fascinating emergent patterns:\n\n")
        
        # Explore each insight as a possibility
        for insight in insights:
            response_parts.append(f"**{self._generate_insight_title(insight)}**\n")
            response_parts.append(f"{insight.core_pattern}\n")
            
            # Add what-if explorations
            if insight.implications:
                response_parts.append("\nThis opens the possibility that:\n")
                for implication in insight.implications[:2]:
                    response_parts.append(f"• {implication}\n")
            
            response_parts.append("\n")
        
        # End with open questions
        questions = self._generate_exploratory_questions(insights)
        if questions:
            response_parts.append("This raises intriguing questions:\n")
            for question in questions:
                response_parts.append(f"- {question}\n")
        
        return "".join(response_parts)
    
    async def _weave_crystalline(self, insights: List[CrystallizedInsight], 
                                loom: Dict) -> str:
        """Crystalline weaving - clear structured presentation"""
        
        response_parts = []
        
        # Clear answer upfront
        if insights:
            response_parts.append(f"**Core Answer:** {insights[0].core_pattern}\n\n")
        
        # Supporting structure
        if len(insights) > 1:
            response_parts.append("**Supporting Patterns:**\n")
            
            for i, insight in enumerate(insights[1:], 1):
                response_parts.append(f"\n{i}. {insight.core_pattern}")
                
                # Add confidence indicator
                confidence_marker = "●" * int(insight.confidence * 5)
                response_parts.append(f" [{confidence_marker}]")
                
                # Add brief explanation
                if insight.variations:
                    response_parts.append(f"\n   {insight.variations[0]}")
                
                response_parts.append("\n")
        
        # Clear implications
        all_implications = []
        for insight in insights:
            all_implications.extend(insight.implications)
        
        if all_implications:
            response_parts.append("\n**What This Means:**\n")
            for impl in all_implications[:3]:
                response_parts.append(f"→ {impl}\n")
        
        return "".join(response_parts)
    
    async def _generate_fallback_response(self, query: str) -> str:
        """Generate response when no clear patterns emerge"""
        
        return (
            f"The thought explosion for '{query}' created interesting fragments, "
            f"but no strong emergent patterns crystallized. This might suggest:\n\n"
            f"• The question touches on truly novel territory\n"
            f"• The concepts resist traditional categorization\n"
            f"• More exploration time might reveal deeper patterns\n\n"
            f"Sometimes the absence of clear patterns is itself meaningful - "
            f"it indicates we're at the edge of structured understanding."
        )
    
    def _should_add_meta_commentary(self, insights: List[CrystallizedInsight]) -> bool:
        """Decide if meta-commentary would be valuable"""
        
        # Add meta-commentary if:
        # - Very high novelty insights
        # - Strong contradictions
        # - Low confidence overall
        
        avg_novelty = np.mean([i.novelty for i in insights])
        avg_confidence = np.mean([i.confidence for i in insights])
        has_contradictions = any(i.contradictions for i in insights)
        
        return avg_novelty > 0.8 or avg_confidence < 0.5 or has_contradictions
    
    def _generate_meta_commentary(self, insights: List[CrystallizedInsight]) -> str:
        """Generate meta-commentary about the reasoning process"""
        
        parts = ["\n\n---\n*Pattern emergence note: "]
        
        avg_novelty = np.mean([i.novelty for i in insights])
        avg_confidence = np.mean([i.confidence for i in insights])
        
        if avg_novelty > 0.8:
            parts.append("These patterns are highly novel and unexpected. ")
        
        if avg_confidence < 0.5:
            parts.append("The patterns show lower confidence, suggesting tentative insights. ")
        
        if any(i.contradictions for i in insights):
            parts.append("Unresolved contradictions indicate deep tensions in the concept space. ")
        
        parts.append("The emergence process revealed ")
        parts.append(f"{len(insights)} primary patterns")
        
        # Describe the dominant pattern types
        pattern_types = self._identify_pattern_types(insights)
        if pattern_types:
            parts.append(f", primarily {', '.join(pattern_types[:2])}")
        
        parts.append(".*")
        
        return "".join(parts)
    
    # Helper methods
    
    def _check_convergence(self, insights: List[CrystallizedInsight]) -> bool:
        """Check if insights converge on similar conclusions"""
        
        if len(insights) < 2:
            return False
        
        # Check implication overlap
        implication_sets = []
        for insight in insights:
            if insight.implications:
                implication_sets.append(set(insight.implications))
        
        if len(implication_sets) >= 2:
            # Check for significant overlap
            intersection = set.intersection(*implication_sets)
            return len(intersection) > 0
        
        return False
    
    def _synthesize_insights(self, insights: List[CrystallizedInsight]) -> str:
        """Create synthesis from multiple insights"""
        
        if not insights:
            return ""
        
        if len(insights) == 1:
            return f"In essence: {insights[0].core_pattern}"
        
        # Find common themes
        all_words = []
        for insight in insights:
            all_words.extend(insight.core_pattern.lower().split())
        
        word_freq = {}
        for word in all_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Find recurring meaningful words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                    'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were'}
        
        themes = [(w, f) for w, f in word_freq.items() 
                 if w not in stopwords and f >= 2]
        themes.sort(key=lambda x: x[1], reverse=True)
        
        if themes:
            key_themes = [w for w, f in themes[:3]]
            return f"Together, these patterns reveal the importance of {', '.join(key_themes)}"
        
        return f"These {len(insights)} patterns together form a complex understanding"
    
    def _get_transition_phrase(self, prev_insight: CrystallizedInsight, 
                              next_insight: CrystallizedInsight) -> str:
        """Generate transition between insights"""
        
        transitions = [
            "Building on this",
            "This leads to another observation",
            "From another angle",
            "Simultaneously",
            "In parallel",
            "Interestingly",
            "This connects to",
            "Furthermore"
        ]
        
        # Choose based on relationship
        if any(word in next_insight.core_pattern.lower() 
               for word in prev_insight.core_pattern.lower().split()):
            return "Expanding on this"
        elif next_insight.confidence > prev_insight.confidence:
            return "More clearly"
        elif next_insight.novelty > prev_insight.novelty:
            return "Surprisingly"
        else:
            return np.random.choice(transitions)
    
    def _extract_key_implications(self, insights: List[CrystallizedInsight]) -> str:
        """Extract and synthesize key implications"""
        
        all_implications = []
        for insight in insights:
            all_implications.extend(insight.implications)
        
        if not all_implications:
            return "The full implications are still emerging."
        
        # Find most important (appearing multiple times or first)
        implication_freq = {}
        for impl in all_implications:
            key = impl.lower()
            implication_freq[key] = implication_freq.get(key, 0) + 1
        
        # Get most frequent or first
        if implication_freq:
            top_implication = max(implication_freq, key=implication_freq.get)
            # Find original casing
            for impl in all_implications:
                if impl.lower() == top_implication:
                    return f"This suggests: {impl}"
        
        return f"This suggests: {all_implications[0]}"
    
    def _create_dialectical_synthesis(self, thesis: CrystallizedInsight, 
                                     antithesis: CrystallizedInsight) -> str:
        """Create synthesis from thesis and antithesis"""
        
        synthesis_templates = [
            "The tension between {thesis} and {antithesis} reveals a higher truth: "
            "both are aspects of a more complex reality where {resolution}",
            
            "Rather than choosing between {thesis} and {antithesis}, "
            "we can transcend the contradiction by {resolution}",
            
            "The paradox dissolves when we realize that {thesis} and {antithesis} "
            "are complementary rather than contradictory: {resolution}"
        ]
        
        # Extract key concepts
        thesis_key = thesis.core_pattern[:50]
        antithesis_key = antithesis.core_pattern[:50]
        
        # Generate resolution
        if thesis.implications and antithesis.implications:
            resolution = "both perspectives contribute essential insights"
        else:
            resolution = "the truth encompasses both extremes"
        
        template = np.random.choice(synthesis_templates)
        
        return template.format(
            thesis=thesis_key,
            antithesis=antithesis_key,
            resolution=resolution
        )
    
    def _find_convergence_point(self, insights: List[CrystallizedInsight]) -> str:
        """Find where insights converge"""
        
        # Look for common implications
        implication_sets = []
        for insight in insights:
            if insight.implications:
                implication_sets.append(set(insight.implications))
        
        if implication_sets:
            common = set.intersection(*implication_sets)
            if common:
                return list(common)[0]
        
        # Look for common words in core patterns
        pattern_words = []
        for insight in insights:
            pattern_words.append(set(insight.core_pattern.lower().split()))
        
        if pattern_words:
            common_words = set.intersection(*pattern_words)
            meaningful = [w for w in common_words 
                         if w not in {'the', 'a', 'an', 'and', 'or', 'but'}]
            
            if meaningful:
                return f"the centrality of {' and '.join(meaningful[:2])}"
        
        return "a unified understanding emerging from diversity"
    
    def _generate_insight_title(self, insight: CrystallizedInsight) -> str:
        """Generate a title for an insight"""
        
        # Extract key concept
        words = insight.core_pattern.split()
        
        # Find most distinctive words
        distinctive = []
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'this', 'that'}
        
        for word in words:
            if word.lower() not in common_words and len(word) > 3:
                distinctive.append(word)
                if len(distinctive) >= 2:
                    break
        
        if distinctive:
            return " ".join(distinctive).title()
        
        return "Emergent Pattern"
    
    def _generate_exploratory_questions(self, 
                                       insights: List[CrystallizedInsight]) -> List[str]:
        """Generate exploratory questions from insights"""
        
        questions = []
        
        for insight in insights[:2]:  # Limit to 2 insights
            # Generate what-if question
            if insight.variations:
                questions.append(f"What if {insight.variations[0].lower()}?")
            
            # Generate why question
            if insight.implications:
                questions.append(f"Why might {insight.implications[0].lower()}?")
        
        return questions[:3]  # Limit total questions
    
    def _identify_pattern_types(self, insights: List[CrystallizedInsight]) -> List[str]:
        """Identify the types of patterns present"""
        
        types = []
        
        for insight in insights:
            if "paradox" in insight.core_pattern.lower():
                types.append("paradoxical")
            elif "resonance" in insight.core_pattern.lower():
                types.append("resonant")
            elif "tension" in insight.core_pattern.lower():
                types.append("tensional")
            elif "emergence" in insight.core_pattern.lower():
                types.append("emergent")
            elif "connection" in insight.core_pattern.lower():
                types.append("connective")
        
        return list(set(types))  # Unique types
