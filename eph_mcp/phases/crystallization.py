"""
Phase 4: Pattern Crystallization
Convert emergent patterns into coherent insights
"""
import numpy as np
from typing import List, Dict, Optional, Tuple
from .. import (
    EmergentPattern, CrystallizedInsight, ThoughtFragment, 
    PatternType, ReasoningField
)
import asyncio

class PatternCrystallizer:
    """Converts emergent patterns into coherent insights"""
    
    def __init__(self):
        """Initialize crystallizer"""
        self.confidence_threshold = 0.5
        self.novelty_threshold = 0.3
        
    async def crystallize_patterns(self, 
                                  patterns: Dict[str, List[EmergentPattern]], 
                                  field: ReasoningField) -> List[CrystallizedInsight]:
        """Crystallize all patterns into insights"""
        
        insights = []
        
        # Process each pattern type
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                insight = await self._crystallize_pattern(pattern, field)
                if insight and insight.confidence > self.confidence_threshold:
                    insights.append(insight)
        
        # Merge related insights
        merged_insights = await self._merge_related_insights(insights)
        
        # Rank by quality
        ranked_insights = self._rank_insights(merged_insights)
        
        return ranked_insights
    
    async def _crystallize_pattern(self, pattern: EmergentPattern, 
                                  field: ReasoningField) -> Optional[CrystallizedInsight]:
        """Crystallize a single pattern into insight"""
        
        # Route to specific crystallization method based on pattern type
        crystallization_methods = {
            PatternType.CRYSTALLINE_LATTICE: self._crystallize_lattice,
            PatternType.STRANGE_ATTRACTOR: self._crystallize_attractor,
            PatternType.PHASE_TRANSITION: self._crystallize_transition,
            PatternType.SOLITON_WAVE: self._crystallize_soliton,
            PatternType.INTERFERENCE: self._crystallize_interference,
            PatternType.VORTEX: self._crystallize_vortex,
            PatternType.BRIDGE: self._crystallize_bridge,
            PatternType.HARMONIC: self._crystallize_harmonic,
            PatternType.FRACTAL: self._crystallize_fractal,
            PatternType.EMERGENCE: self._crystallize_emergence
        }
        
        method = crystallization_methods.get(pattern.pattern_type)
        if method:
            return await method(pattern, field)
        
        # Default crystallization
        return await self._default_crystallization(pattern, field)
    
    async def _crystallize_lattice(self, pattern: EmergentPattern, 
                                  field: ReasoningField) -> CrystallizedInsight:
        """Crystallize regular lattice structure"""
        
        insight = CrystallizedInsight()
        
        # Extract fragments
        fragments = [field.fragments[fid] for fid in pattern.fragments 
                    if fid in field.fragments]
        
        # Find the binding principle (what holds the lattice together)
        binding_principle = self._extract_binding_principle(fragments, field)
        
        # Find the unit cell (minimal repeating unit)
        unit_cell = self._extract_detailed_unit_cell(fragments)
        
        # Identify defects and what they reveal
        defect_insights = self._analyze_defects(fragments, pattern.variations)
        
        # Build core insight
        insight.core_pattern = f"{binding_principle}. The pattern repeats with {unit_cell}"
        
        if defect_insights:
            insight.core_pattern += f", but breaks at key points: {defect_insights[0]}"
        
        # Add variations
        insight.variations = pattern.variations[:3] if pattern.variations else []
        
        # Add perspectives
        insight.perspectives = {
            "Structure": f"Regular {pattern.symmetry} symmetry",
            "Stability": f"{pattern.stability:.1%} stable configuration",
            "Coherence": f"{pattern.coherence:.1%} internal consistency"
        }
        
        # Calculate confidence
        insight.confidence = pattern.strength * pattern.stability
        
        # Calculate novelty
        insight.novelty = self._calculate_novelty(fragments)
        
        # Add implications
        insight.implications = [
            f"This regularity suggests a fundamental principle",
            f"Deviations from the pattern may be especially significant",
            f"The structure could be extended or scaled"
        ]
        
        # Track emergence path
        insight.emergence_path = [{
            'stage': 'lattice_formation',
            'fragments': len(fragments),
            'binding_energy': pattern.calculate_binding_energy(field.fragments)
        }]
        
        return insight
    
    async def _crystallize_attractor(self, pattern: EmergentPattern, 
                                    field: ReasoningField) -> CrystallizedInsight:
        """Crystallize strange attractor pattern"""
        
        insight = CrystallizedInsight()
        
        # The center represents an unresolved tension
        central_tension = pattern.central_insight
        
        # The orbit describes different perspectives on the tension
        orbital_perspectives = pattern.variations
        
        # Build core insight
        insight.core_pattern = f"Cyclic tension: {central_tension}. "
        insight.core_pattern += f"The system oscillates between {len(orbital_perspectives)} states "
        insight.core_pattern += f"without resolution, suggesting this tension is fundamental"
        
        # Add perspectives
        for i, perspective in enumerate(orbital_perspectives[:3]):
            insight.perspectives[f"State {i+1}"] = perspective
        
        # Chaos measure indicates vitality
        chaos_level = 1.0 - pattern.stability  # Inverse of stability
        if chaos_level > 0.7:
            insight.variations.append("High chaos: the tension is very active")
        elif chaos_level > 0.3:
            insight.variations.append("Moderate chaos: the tension is dynamic but bounded")
        else:
            insight.variations.append("Low chaos: the tension is relatively stable")
        
        # Confidence inversely related to chaos
        insight.confidence = pattern.stability
        
        # Novelty high for strange attractors
        insight.novelty = 0.8
        
        # Implications
        insight.implications = [
            "This unresolved tension may be irreducible",
            "Solutions might require embracing the oscillation",
            "The pattern suggests a deeper paradox"
        ]
        
        # Track emergence
        insight.emergence_path = [{
            'stage': 'attractor_formation',
            'dimensionality': pattern.dimensionality,
            'entropy': pattern.entropy
        }]
        
        return insight
    
    async def _crystallize_transition(self, pattern: EmergentPattern, 
                                     field: ReasoningField) -> CrystallizedInsight:
        """Crystallize phase transition pattern"""
        
        insight = CrystallizedInsight()
        
        # Phase transitions represent sudden reorganizations
        insight.core_pattern = f"Critical transition point: {pattern.central_insight}. "
        insight.core_pattern += "The system underwent sudden reorganization, "
        insight.core_pattern += "suggesting a tipping point or threshold was crossed"
        
        # Analyze what changed
        fragments = [field.fragments[fid] for fid in pattern.fragments 
                    if fid in field.fragments]
        
        before_state = self._reconstruct_state_before(fragments, field)
        after_state = self._reconstruct_state_after(fragments, field)
        
        insight.variations = [
            f"Before: {before_state}",
            f"After: {after_state}",
            f"Trigger: Entropy change of {pattern.entropy:.2f}"
        ]
        
        # High confidence for clear transitions
        insight.confidence = min(pattern.strength, 1.0)
        
        # High novelty for phase transitions
        insight.novelty = 0.9
        
        # Implications
        insight.implications = [
            "The system has multiple stable states",
            "Small changes can trigger large reorganizations",
            "Understanding the trigger could enable controlled transitions"
        ]
        
        return insight
    
    async def _crystallize_soliton(self, pattern: EmergentPattern, 
                                  field: ReasoningField) -> CrystallizedInsight:
        """Crystallize soliton wave pattern"""
        
        insight = CrystallizedInsight()
        
        # Solitons are self-reinforcing insights
        insight.core_pattern = f"Self-sustaining insight: {pattern.central_insight}. "
        insight.core_pattern += "This idea maintains its form while propagating, "
        insight.core_pattern += "suggesting it has inherent stability and truth"
        
        # Wave properties
        insight.variations = pattern.variations
        
        # High confidence for solitons
        insight.confidence = pattern.stability
        
        # Moderate novelty
        insight.novelty = 0.6
        
        # Implications
        insight.implications = [
            "This insight will likely persist and spread",
            "It represents a fundamental truth or principle",
            "Building on this could lead to stable solutions"
        ]
        
        return insight
    
    async def _crystallize_interference(self, pattern: EmergentPattern, 
                                       field: ReasoningField) -> CrystallizedInsight:
        """Crystallize interference pattern"""
        
        insight = CrystallizedInsight()
        
        if pattern.strength > 0:
            # Constructive interference
            insight.core_pattern = f"Reinforcing resonance: {pattern.central_insight}. "
            insight.core_pattern += "These ideas amplify each other, "
            insight.core_pattern += "creating a stronger combined effect"
            
            insight.implications = [
                "Combining these perspectives strengthens both",
                "The resonance suggests deep compatibility",
                "This combination could be especially powerful"
            ]
        else:
            # Destructive interference
            insight.core_pattern = f"Canceling opposition: {pattern.central_insight}. "
            insight.core_pattern += "These ideas interfere destructively, "
            insight.core_pattern += "suggesting they cannot coexist"
            
            insight.contradictions = pattern.contradictions
            
            insight.implications = [
                "These perspectives are fundamentally incompatible",
                "Choosing one negates the other",
                "The opposition might reveal a hidden assumption"
            ]
        
        insight.confidence = abs(pattern.strength)
        insight.novelty = 0.5
        
        return insight
    
    async def _crystallize_vortex(self, pattern: EmergentPattern, 
                                 field: ReasoningField) -> CrystallizedInsight:
        """Crystallize vortex pattern"""
        
        insight = CrystallizedInsight()
        
        # Vortices are swirling contradictions
        insight.core_pattern = f"Circular paradox: {pattern.central_insight}. "
        insight.core_pattern += f"These {len(pattern.contradictions)} ideas form a closed loop "
        insight.core_pattern += "of mutual contradiction, creating an intellectual whirlpool"
        
        # List the contradictions
        insight.contradictions = pattern.contradictions
        
        # Moderate confidence
        insight.confidence = 0.6
        
        # High novelty for vortices
        insight.novelty = 0.8
        
        # Implications
        insight.implications = [
            "This circular logic cannot be resolved linearly",
            "The paradox might require a higher-level perspective",
            "Each element is both cause and effect"
        ]
        
        return insight
    
    async def _crystallize_bridge(self, pattern: EmergentPattern, 
                                 field: ReasoningField) -> CrystallizedInsight:
        """Crystallize bridge pattern"""
        
        insight = CrystallizedInsight()
        
        # Bridges are unexpected connections
        insight.core_pattern = f"Unexpected connection: {pattern.central_insight}. "
        insight.core_pattern += "This link between disparate concepts "
        insight.core_pattern += "opens new pathways for understanding"
        
        # High confidence for clear bridges
        insight.confidence = pattern.strength
        
        # Very high novelty for unexpected connections
        insight.novelty = 0.95
        
        # Implications
        insight.implications = [
            "This connection suggests hidden relationships",
            "Exploring this bridge could yield new insights",
            "The link might generalize to other domains"
        ]
        
        return insight
    
    async def _crystallize_harmonic(self, pattern: EmergentPattern, 
                                   field: ReasoningField) -> CrystallizedInsight:
        """Crystallize harmonic pattern"""
        
        insight = CrystallizedInsight()
        
        # Harmonics are resonating ideas
        insight.core_pattern = f"Harmonic alignment: {pattern.central_insight}. "
        insight.core_pattern += "These concepts resonate at related frequencies, "
        insight.core_pattern += "creating a symphony of compatible ideas"
        
        # List the harmonics
        insight.variations = pattern.variations
        
        # High confidence for harmonics
        insight.confidence = pattern.coherence
        
        # Moderate novelty
        insight.novelty = 0.6
        
        # Implications
        insight.implications = [
            "These ideas naturally support each other",
            "The harmonic relationship suggests deep structure",
            "Combining them could create emergent properties"
        ]
        
        return insight
    
    async def _crystallize_fractal(self, pattern: EmergentPattern, 
                                  field: ReasoningField) -> CrystallizedInsight:
        """Crystallize fractal pattern"""
        
        insight = CrystallizedInsight()
        
        # Fractals are self-similar across scales
        insight.core_pattern = f"Scale-invariant structure: {pattern.central_insight}. "
        insight.core_pattern += f"This pattern repeats at {pattern.dimensionality:.1f} fractal dimensions, "
        insight.core_pattern += "suggesting a universal principle that transcends scale"
        
        # Describe the self-similarity
        insight.variations = [
            f"Microscale: Same pattern in details",
            f"Mesoscale: Same pattern in relationships",
            f"Macroscale: Same pattern in structure"
        ]
        
        # High confidence for fractals
        insight.confidence = pattern.strength
        
        # High novelty for fractal patterns
        insight.novelty = 0.85
        
        # Implications
        insight.implications = [
            "This principle applies at all levels of analysis",
            "Zooming in or out reveals the same structure",
            "The pattern is likely fundamental to the domain"
        ]
        
        return insight
    
    async def _crystallize_emergence(self, pattern: EmergentPattern, 
                                    field: ReasoningField) -> CrystallizedInsight:
        """Crystallize true emergence pattern"""
        
        insight = CrystallizedInsight()
        
        # True emergence creates new properties
        insight.core_pattern = f"Genuine emergence: {pattern.central_insight}. "
        insight.core_pattern += "This property exists only in the collective, "
        insight.core_pattern += "irreducible to individual components"
        
        # Describe the emergent property
        insight.variations = [
            f"Collective property: {pattern.central_insight}",
            f"Individual components: {len(pattern.fragments)} fragments",
            f"Emergence strength: {pattern.strength:.1%}"
        ]
        
        # High confidence for clear emergence
        insight.confidence = pattern.coherence
        
        # Maximum novelty for true emergence
        insight.novelty = 1.0
        
        # Implications
        insight.implications = [
            "The whole is genuinely greater than its parts",
            "Reductionist analysis will miss this property",
            "This emergence might indicate a new level of organization"
        ]
        
        return insight
    
    async def _default_crystallization(self, pattern: EmergentPattern, 
                                      field: ReasoningField) -> CrystallizedInsight:
        """Default crystallization for unknown pattern types"""
        
        insight = CrystallizedInsight()
        
        insight.core_pattern = pattern.central_insight or "Unclassified pattern detected"
        insight.variations = pattern.variations[:3] if pattern.variations else []
        insight.confidence = pattern.strength * pattern.stability
        insight.novelty = 0.5
        
        return insight
    
    async def _merge_related_insights(self, 
                                     insights: List[CrystallizedInsight]) -> List[CrystallizedInsight]:
        """Merge insights that are closely related"""
        
        if len(insights) <= 1:
            return insights
        
        merged = []
        used = set()
        
        for i, insight_a in enumerate(insights):
            if i in used:
                continue
            
            # Find related insights
            related = [insight_a]
            
            for j, insight_b in enumerate(insights[i+1:], i+1):
                if j not in used:
                    similarity = self._calculate_insight_similarity(insight_a, insight_b)
                    
                    if similarity > 0.7:
                        related.append(insight_b)
                        used.add(j)
            
            # Merge if multiple related
            if len(related) > 1:
                merged_insight = self._merge_insights(related)
                merged.append(merged_insight)
            else:
                merged.append(insight_a)
        
        return merged
    
    def _merge_insights(self, insights: List[CrystallizedInsight]) -> CrystallizedInsight:
        """Merge multiple insights into one"""
        
        merged = CrystallizedInsight()
        
        # Combine core patterns
        patterns = [i.core_pattern for i in insights]
        merged.core_pattern = self._synthesize_patterns(patterns)
        
        # Combine variations (unique ones)
        all_variations = []
        for insight in insights:
            all_variations.extend(insight.variations)
        merged.variations = list(set(all_variations))[:5]
        
        # Average confidence
        merged.confidence = np.mean([i.confidence for i in insights])
        
        # Maximum novelty
        merged.novelty = max(i.novelty for i in insights)
        
        # Combine implications
        all_implications = []
        for insight in insights:
            all_implications.extend(insight.implications)
        merged.implications = list(set(all_implications))[:5]
        
        return merged
    
    def _rank_insights(self, insights: List[CrystallizedInsight]) -> List[CrystallizedInsight]:
        """Rank insights by quality score"""
        
        for insight in insights:
            # Quality score combines confidence, novelty, and clarity
            insight.quality_score = (
                insight.confidence * 0.4 +
                insight.novelty * 0.4 +
                insight.clarity * 0.2
            )
        
        # Sort by quality score
        return sorted(insights, key=lambda i: i.quality_score, reverse=True)
    
    # Helper methods
    
    def _extract_binding_principle(self, fragments: List[ThoughtFragment], 
                                  field: ReasoningField) -> str:
        """Extract what binds fragments together"""
        
        # Analyze common themes
        contents = [f.content for f in fragments]
        
        # Find common words
        if contents:
            words = [set(c.lower().split()) for c in contents]
            common = set.intersection(*words) if words else set()
            
            if common:
                return f"Unified by: {' '.join(list(common)[:3])}"
        
        # Analyze bond types
        bond_types = {}
        for fragment in fragments:
            for bond in fragment.bonds:
                bond_type = str(bond.bond_type)
                bond_types[bond_type] = bond_types.get(bond_type, 0) + 1
        
        if bond_types:
            dominant = max(bond_types, key=bond_types.get)
            return f"Connected through {dominant} relationships"
        
        return "Coherent structure"
    
    def _extract_detailed_unit_cell(self, fragments: List[ThoughtFragment]) -> str:
        """Extract detailed unit cell description"""
        
        if not fragments:
            return "empty pattern"
        
        # Find shortest common pattern
        contents = [f.content for f in fragments[:5]]
        
        if len(contents) > 1:
            # Find common prefix
            prefix = ""
            for chars in zip(*contents):
                if len(set(chars)) == 1:
                    prefix += chars[0]
                else:
                    break
            
            if prefix:
                return f"pattern: '{prefix.strip()}...'"
        
        return f"pattern: '{fragments[0].content[:20]}...'"
    
    def _analyze_defects(self, fragments: List[ThoughtFragment], 
                        variations: List[str]) -> List[str]:
        """Analyze what defects reveal about the pattern"""
        
        insights = []
        
        for variation in variations:
            if "Defect:" in variation:
                defect = variation.replace("Defect:", "").strip()
                
                if "High energy" in defect:
                    insights.append("tension points reveal stress in the structure")
                elif "Decoherent" in defect:
                    insights.append("some elements resist integration")
                elif "Isolated" in defect:
                    insights.append("outliers may indicate boundaries")
        
        return insights
    
    def _calculate_novelty(self, fragments: List[ThoughtFragment]) -> float:
        """Calculate how novel/unexpected the insight is"""
        
        if not fragments:
            return 0.0
        
        # Novelty based on:
        # 1. Unusual generation strategies
        # 2. Low coherence (quantum/paradox)
        # 3. High activation variance
        
        strategies = [f.generation_strategy for f in fragments]
        unusual_strategies = ['quantum_superpose', 'paradox_generate', 'analogize_wildly']
        unusual_count = sum(1 for s in strategies if s in unusual_strategies)
        
        strategy_novelty = unusual_count / len(fragments)
        
        avg_coherence = np.mean([f.coherence for f in fragments])
        coherence_novelty = 1.0 - avg_coherence  # Low coherence = high novelty
        
        activation_variance = np.var([f.activation_energy for f in fragments])
        variance_novelty = min(activation_variance / 2.0, 1.0)
        
        return np.mean([strategy_novelty, coherence_novelty, variance_novelty])
    
    def _reconstruct_state_before(self, fragments: List[ThoughtFragment], 
                                 field: ReasoningField) -> str:
        """Reconstruct state before transition"""
        
        # Find fragments with low activation
        low_activation = [f for f in fragments if f.activation_energy < 0.5]
        
        if low_activation:
            return f"Low energy state: {low_activation[0].content[:30]}"
        
        return "Stable initial state"
    
    def _reconstruct_state_after(self, fragments: List[ThoughtFragment], 
                                field: ReasoningField) -> str:
        """Reconstruct state after transition"""
        
        # Find fragments with high activation
        high_activation = [f for f in fragments if f.activation_energy > 1.5]
        
        if high_activation:
            return f"High energy state: {high_activation[0].content[:30]}"
        
        return "Reorganized final state"
    
    def _calculate_insight_similarity(self, insight_a: CrystallizedInsight, 
                                     insight_b: CrystallizedInsight) -> float:
        """Calculate similarity between two insights"""
        
        # Simple word overlap for now
        words_a = set(insight_a.core_pattern.lower().split())
        words_b = set(insight_b.core_pattern.lower().split())
        
        if not words_a or not words_b:
            return 0.0
        
        intersection = words_a & words_b
        union = words_a | words_b
        
        return len(intersection) / len(union)
    
    def _synthesize_patterns(self, patterns: List[str]) -> str:
        """Synthesize multiple patterns into one description"""
        
        if not patterns:
            return ""
        
        if len(patterns) == 1:
            return patterns[0]
        
        # Find common themes
        all_words = []
        for pattern in patterns:
            all_words.extend(pattern.lower().split())
        
        # Count word frequencies
        word_freq = {}
        for word in all_words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Find most common meaningful words
        stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'}
        meaningful = [(w, f) for w, f in word_freq.items() 
                     if w not in stopwords and f > 1]
        meaningful.sort(key=lambda x: x[1], reverse=True)
        
        if meaningful:
            themes = [w for w, f in meaningful[:3]]
            return f"Multiple patterns converging on: {', '.join(themes)}"
        
        return f"Synthesis of {len(patterns)} related patterns"
