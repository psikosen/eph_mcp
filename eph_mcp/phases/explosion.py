"""
Phase 1: Thought Explosion
Generate diverse thought fragments using multiple strategies
"""
import random
import numpy as np
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import re
from .. import ThoughtFragment, BondType
import asyncio
import spacy

class ThoughtExplosion:
    """Generate diverse thought fragments from a query"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize with embedding model"""
        self.embedder = SentenceTransformer(model_name)
        self.nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
        self.temperature = 1.5  # High temperature for diversity
        
        # Strategy weights for selection
        self.strategy_weights = {
            'free_associate': 0.15,
            'decompose_mechanically': 0.15,
            'analogize_wildly': 0.10,
            'invert_assumptions': 0.10,
            'sensory_translate': 0.08,
            'temporal_shift': 0.08,
            'scale_transform': 0.08,
            'emotion_map': 0.06,
            'abstract_ladder': 0.05,
            'quantum_superpose': 0.05,
            'paradox_generate': 0.05,
            'metaphor_blend': 0.05
        }
    
    async def explode(self, query: str, n: int = 75) -> List[ThoughtFragment]:
        """Generate n diverse thought fragments from query"""
        fragments = []
        
        # Parse query for context
        query_embedding = self.embedder.encode(query)
        query_tokens = self.nlp(query)
        
        # Generate fragments using weighted random selection of strategies
        strategies = list(self.strategy_weights.keys())
        weights = list(self.strategy_weights.values())
        
        tasks = []
        for _ in range(n):
            strategy = random.choices(strategies, weights=weights)[0]
            task = self._generate_fragment(query, strategy, query_embedding)
            tasks.append(task)
        
        # Generate all fragments in parallel
        fragment_contents = await asyncio.gather(*tasks)
        
        # Create ThoughtFragment objects with embeddings
        for i, (content, strategy) in enumerate(fragment_contents):
            if content:  # Filter out None results
                fragment = ThoughtFragment(
                    content=content[:100],  # Limit length
                    generation_strategy=strategy,
                    activation_energy=random.uniform(0.5, 2.0),
                    resonance_frequency=random.uniform(0.1, 10.0),
                    decay_rate=random.uniform(0.05, 0.2)
                )
                
                # Generate embedding
                fragment.embedding = self.embedder.encode(content)
                
                # Initialize position in semantic space
                fragment.position = fragment.embedding + np.random.normal(0, 0.1, fragment.embedding.shape)
                fragment.velocity = np.random.normal(0, 0.01, fragment.embedding.shape)
                
                # Add quantum noise
                fragment.add_quantum_noise(self.temperature * 0.1)
                
                # Set initial coherence based on strategy
                fragment.coherence = self._get_strategy_coherence(strategy)
                
                fragments.append(fragment)
        
        return fragments
    
    async def _generate_fragment(self, query: str, strategy: str, query_embedding: np.ndarray) -> tuple:
        """Generate a single fragment using specified strategy"""
        method = getattr(self, f"_{strategy}", None)
        if method:
            content = await method(query, query_embedding)
            return (content, strategy)
        return (None, strategy)
    
    async def _free_associate(self, query: str, embedding: np.ndarray) -> str:
        """Random associations from query"""
        words = query.split()
        if not words:
            return query
        
        trigger = random.choice(words)
        associations = [
            f"{trigger} reminds me of",
            f"like {trigger} but different",
            f"the opposite of {trigger}",
            f"{trigger} makes me think of",
            f"beyond {trigger} lies",
            f"{trigger} transforms into",
            f"before {trigger} there was",
            f"{trigger} implies",
            f"without {trigger}",
            f"{trigger} resonates with"
        ]
        
        prefix = random.choice(associations)
        
        # Generate random continuation
        concepts = ["patterns", "chaos", "structure", "flow", "emergence", 
                   "cycles", "balance", "transformation", "connection", "void",
                   "potential", "resistance", "harmony", "disruption", "synthesis"]
        
        return f"{prefix} {random.choice(concepts)}"
    
    async def _decompose_mechanically(self, query: str, embedding: np.ndarray) -> str:
        """Break query into mechanical parts"""
        doc = self.nlp(query)
        
        # Extract different grammatical components
        nouns = [token.text for token in doc if token.pos_ == "NOUN"]
        verbs = [token.text for token in doc if token.pos_ == "VERB"]
        adjs = [token.text for token in doc if token.pos_ == "ADJ"]
        
        decompositions = []
        
        if nouns:
            decompositions.append(f"the essence of {random.choice(nouns)}")
            decompositions.append(f"{random.choice(nouns)} as a system")
            decompositions.append(f"breaking down {random.choice(nouns)}")
        
        if verbs:
            decompositions.append(f"the action of {random.choice(verbs)}")
            decompositions.append(f"what enables {random.choice(verbs)}")
            decompositions.append(f"resistance to {random.choice(verbs)}")
        
        if adjs:
            decompositions.append(f"the quality of being {random.choice(adjs)}")
            decompositions.append(f"degrees of {random.choice(adjs)}")
        
        if not decompositions:
            decompositions.append(f"components of: {query[:30]}")
        
        return random.choice(decompositions)
    
    async def _analogize_wildly(self, query: str, embedding: np.ndarray) -> str:
        """Create wild analogies"""
        
        domains = [
            "cooking", "music", "weather", "biology", "architecture",
            "dance", "warfare", "gardening", "chemistry", "mythology",
            "quantum physics", "ecology", "economics", "poetry", "geology"
        ]
        
        domain = random.choice(domains)
        
        analogies = [
            f"{query[:20]} is like {domain}:",
            f"imagine {query[:20]} as {domain}",
            f"if {query[:20]} were {domain}",
            f"{query[:20]} resonates with {domain}",
            f"the {domain} of {query[:20]}",
            f"{query[:20]} through the lens of {domain}"
        ]
        
        base = random.choice(analogies)
         
        domain_elements = {
            "cooking": ["simmering", "seasoning", "mixing flavors", "heat and timing"],
            "music": ["harmony", "dissonance", "rhythm", "crescendo", "silence between notes"],
            "weather": ["pressure systems", "storm formation", "climate patterns", "microclimate"],
            "biology": ["evolution", "adaptation", "symbiosis", "emergence", "metabolism"],
            "quantum physics": ["superposition", "entanglement", "wave collapse", "uncertainty"]
        }
        
        elements = domain_elements.get(domain, ["patterns", "flows", "structures"])
        return f"{base} {random.choice(elements)}"
    
    async def _invert_assumptions(self, query: str, embedding: np.ndarray) -> str:
        """Invert implicit assumptions"""
        
        inversions = [
            f"what if {query[:30]} is backwards",
            f"assuming the opposite of {query[:30]}",
            f"reversing {query[:30]}",
            f"{query[:30]} but inside-out",
            f"the shadow of {query[:30]}",
            f"anti-{query[:20]}",
            f"not {query[:30]} but its inverse",
            f"flipping {query[:30]}",
            f"the negative space of {query[:30]}"
        ]
        
        return random.choice(inversions)
    
    async def _sensory_translate(self, query: str, embedding: np.ndarray) -> str:
        """Translate to sensory descriptions"""
        
        senses = ["sounds", "feels", "tastes", "smells", "looks"]
        sense = random.choice(senses)
        
        translations = {
            "sounds": ["resonant", "sharp", "muffled", "harmonic", "discordant", "rhythmic"],
            "feels": ["smooth", "rough", "warm", "cold", "electric", "heavy", "light"],
            "tastes": ["bitter", "sweet", "complex", "simple", "rich", "subtle"],
            "smells": ["fresh", "ancient", "metallic", "organic", "sharp", "earthy"],
            "looks": ["fractal", "crystalline", "flowing", "angular", "luminous", "opaque"]
        }
        
        quality = random.choice(translations.get(sense, ["unique"]))
        return f"{query[:30]} {sense} {quality}"
    
    async def _temporal_shift(self, query: str, embedding: np.ndarray) -> str:
        """Shift temporal perspective"""
        
        shifts = [
            f"{query[:30]} in the distant past",
            f"{query[:30]} in the far future",
            f"the origin of {query[:30]}",
            f"the end state of {query[:30]}",
            f"{query[:30]} frozen in time",
            f"{query[:30]} accelerated",
            f"the cycle of {query[:30]}",
            f"{query[:30]} before it begins",
            f"the echo of {query[:30]}",
            f"timeless {query[:20]}"
        ]
        
        return random.choice(shifts)
    
    async def _scale_transform(self, query: str, embedding: np.ndarray) -> str:
        """Transform scale perspective"""
        
        scales = [
            f"zooming into {query[:30]}",
            f"zooming out from {query[:30]}",
            f"{query[:30]} at quantum scale",
            f"{query[:30]} at cosmic scale",
            f"microscopic {query[:20]}",
            f"macroscopic {query[:20]}",
            f"{query[:30]} as a fractal",
            f"the atoms of {query[:30]}",
            f"the universe of {query[:30]}"
        ]
        
        return random.choice(scales)
    
    async def _emotion_map(self, query: str, embedding: np.ndarray) -> str:
        """Map to emotional landscape"""
        
        emotions = [
            "joy", "fear", "anger", "sadness", "surprise",
            "anticipation", "trust", "disgust", "curiosity",
            "wonder", "confusion", "clarity", "tension", "relief"
        ]
        
        emotion = random.choice(emotions)
        
        mappings = [
            f"the {emotion} in {query[:30]}",
            f"{query[:30]} evokes {emotion}",
            f"{emotion} as a lens for {query[:30]}",
            f"transforming {query[:30]} through {emotion}",
            f"the {emotion} dimension of {query[:30]}"
        ]
        
        return random.choice(mappings)
    
    async def _abstract_ladder(self, query: str, embedding: np.ndarray) -> str:
        """Climb abstraction ladder"""
        
        directions = [
            f"abstracting {query[:30]}",
            f"concretizing {query[:30]}",
            f"the pattern behind {query[:30]}",
            f"an instance of {query[:30]}",
            f"generalizing {query[:30]}",
            f"specifying {query[:30]}",
            f"the category containing {query[:30]}",
            f"examples of {query[:30]}"
        ]
        
        return random.choice(directions)
    
    async def _quantum_superpose(self, query: str, embedding: np.ndarray) -> str:
        """Create quantum superposition"""
        
        superpositions = [
            f"{query[:20]} AND not {query[:20]}",
            f"{query[:30]} in multiple states",
            f"uncertain {query[:20]}",
            f"probability cloud of {query[:30]}",
            f"{query[:30]} before measurement",
            f"all possibilities of {query[:30]}",
            f"quantum {query[:20]}",
            f"superposed {query[:20]}"
        ]
        
        return random.choice(superpositions)
    
    async def _paradox_generate(self, query: str, embedding: np.ndarray) -> str:
        """Generate paradoxes"""
        
        paradoxes = [
            f"{query[:30]} creates its opposite",
            f"the more {query[:20]}, the less {query[:20]}",
            f"{query[:30]} requires its absence",
            f"achieving {query[:30]} by letting go",
            f"{query[:30]} is its own obstacle",
            f"the paradox of {query[:30]}"
        ]
        
        return random.choice(paradoxes)
    
    async def _metaphor_blend(self, query: str, embedding: np.ndarray) -> str:
        """Blend multiple metaphors"""
        
        metaphor_pairs = [
            ("river", "circuit"),
            ("garden", "mind"),
            ("symphony", "ecosystem"),
            ("dance", "negotiation"),
            ("weaving", "thinking"),
            ("crystal", "idea"),
            ("fire", "transformation"),
            ("mirror", "relationship")
        ]
        
        pair = random.choice(metaphor_pairs)
        
        blends = [
            f"{query[:30]} as {pair[0]} becoming {pair[1]}",
            f"between {pair[0]} and {pair[1]}: {query[:30]}",
            f"{query[:30]} bridges {pair[0]} and {pair[1]}",
            f"the {pair[0]}-{pair[1]} nature of {query[:30]}"
        ]
        
        return random.choice(blends)
    
    def _get_strategy_coherence(self, strategy: str) -> float:
        """Get initial coherence based on generation strategy"""
        coherence_map = {
            'free_associate': 0.6,
            'decompose_mechanically': 0.9,
            'analogize_wildly': 0.5,
            'invert_assumptions': 0.7,
            'sensory_translate': 0.6,
            'temporal_shift': 0.7,
            'scale_transform': 0.8,
            'emotion_map': 0.5,
            'abstract_ladder': 0.8,
            'quantum_superpose': 0.3,  # Low coherence = high superposition
            'paradox_generate': 0.4,
            'metaphor_blend': 0.6
        }
        return coherence_map.get(strategy, 0.5)
