"""
Core data structures for Emergent Pattern Hunter
"""
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Set
from enum import Enum
import uuid
from datetime import datetime
import json

class BondType(Enum):
    """Types of connections between thought fragments"""
    SEMANTIC = "semantic"          # Meaning similarity
    CAUSAL = "causal"              # Cause-effect relationship
    CONTRADICTION = "contradiction" # Logical opposition
    METAPHORICAL = "metaphorical"  # Analogical connection
    TEMPORAL = "temporal"          # Time-based relationship
    HIERARCHICAL = "hierarchical"  # Parent-child concept
    RESONANT = "resonant"          # Harmonic reinforcement
    ENTANGLED = "entangled"        # Quantum-like correlation

class PatternType(Enum):
    """Types of emergent patterns"""
    CRYSTALLINE_LATTICE = "crystalline_lattice"  # Regular repeating structure
    STRANGE_ATTRACTOR = "strange_attractor"      # Cyclic but chaotic
    PHASE_TRANSITION = "phase_transition"        # Sudden reorganization
    SOLITON_WAVE = "soliton_wave"               # Propagating insight
    INTERFERENCE = "interference"                # Constructive/destructive
    VORTEX = "vortex"                           # Swirling contradiction
    BRIDGE = "bridge"                           # Unexpected connection
    HARMONIC = "harmonic"                       # Resonating ideas
    FRACTAL = "fractal"                         # Self-similar at scales
    EMERGENCE = "emergence"                     # Truly novel pattern

@dataclass
class ThoughtFragment:
    """Atomic unit of reasoning - deliberately incomplete"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    content: str = ""  # 10-50 tokens max
    embedding: Optional[np.ndarray] = None  # High-dimensional representation
    position: Optional[np.ndarray] = None  # Position in semantic space
    velocity: Optional[np.ndarray] = None  # Movement in semantic space
    
    # Energy and activation
    activation_energy: float = 1.0  # How "excited" this thought is
    potential_energy: float = 0.0   # Energy from position in field
    kinetic_energy: float = 0.0     # Energy from movement
    
    # Connections and bonds
    bonds: List['Bond'] = field(default_factory=list)
    bond_energies: Dict[str, float] = field(default_factory=dict)
    
    # Quantum-like properties
    coherence: float = 1.0  # Quantum coherence (0=decoherent, 1=pure)
    entanglement: Set[str] = field(default_factory=set)  # Entangled fragments
    superposition: List[str] = field(default_factory=list)  # Superposed states
    
    # Resonance and frequency
    resonance_frequency: float = 0.0  # Natural frequency
    phase: float = 0.0  # Current phase
    amplitude: float = 1.0  # Oscillation amplitude
    
    # Decay and lifetime
    decay_rate: float = 0.1  # How quickly it fades
    creation_time: datetime = field(default_factory=datetime.now)
    lifetime: float = 0.0  # Time since creation
    
    # Metadata
    generation_strategy: str = ""  # How it was created
    parent_fragments: List[str] = field(default_factory=list)
    child_fragments: List[str] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)
    
    def add_quantum_noise(self, noise_level: float = 0.1):
        """Add small random perturbations"""
        if self.embedding is not None:
            noise = np.random.normal(0, noise_level, self.embedding.shape)
            self.embedding += noise
            self.embedding /= np.linalg.norm(self.embedding)  # Renormalize
    
    def measure_coherence(self) -> float:
        """Measure quantum coherence of the fragment"""
        # Coherence decreases with number of bonds and time
        base_coherence = np.exp(-self.lifetime * self.decay_rate)
        bond_decoherence = np.exp(-len(self.bonds) * 0.1)
        return base_coherence * bond_decoherence * self.coherence
    
    def oscillate(self, dt: float):
        """Update oscillation state"""
        self.phase += self.resonance_frequency * dt
        self.phase = self.phase % (2 * np.pi)
        
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            'id': self.id,
            'content': self.content,
            'activation_energy': self.activation_energy,
            'coherence': self.coherence,
            'resonance_frequency': self.resonance_frequency,
            'bonds': len(self.bonds),
            'tags': list(self.tags),
            'generation_strategy': self.generation_strategy
        }

@dataclass
class Bond:
    """Connection between two thought fragments"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    fragment_a: str = ""  # ID of first fragment
    fragment_b: str = ""  # ID of second fragment
    bond_type: BondType = BondType.SEMANTIC
    strength: float = 0.0  # -1 to 1 (negative = repulsion)
    energy: float = 0.0  # Binding energy
    formation_time: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def is_attractive(self) -> bool:
        return self.strength > 0
    
    def is_repulsive(self) -> bool:
        return self.strength < 0

@dataclass
class EmergentPattern:
    """A pattern that emerged from fragment interactions"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    pattern_type: PatternType = PatternType.EMERGENCE
    fragments: List[str] = field(default_factory=list)  # Fragment IDs
    
    # Pattern properties
    strength: float = 0.0  # How strong/clear the pattern is
    stability: float = 0.0  # How stable over time
    coherence: float = 0.0  # Internal consistency
    entropy: float = 0.0  # Disorder measure
    
    # Geometric properties
    dimensionality: int = 0  # Effective dimensions
    symmetry: str = ""  # Type of symmetry
    topology: str = ""  # Topological structure
    
    # Dynamic properties
    formation_time: datetime = field(default_factory=datetime.now)
    lifetime: float = 0.0
    evolution_history: List[Dict] = field(default_factory=list)
    
    # Semantic properties
    central_insight: str = ""
    variations: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)
    
    def add_fragment(self, fragment_id: str):
        """Add a fragment to this pattern"""
        if fragment_id not in self.fragments:
            self.fragments.append(fragment_id)
    
    def calculate_binding_energy(self, fragments: Dict[str, ThoughtFragment]) -> float:
        """Calculate total binding energy of pattern"""
        total_energy = 0.0
        for i, frag_id_a in enumerate(self.fragments):
            for frag_id_b in self.fragments[i+1:]:
                if frag_id_a in fragments and frag_id_b in fragments:
                    frag_a = fragments[frag_id_a]
                    frag_b = fragments[frag_id_b]
                    # Energy from bonds between fragments
                    for bond in frag_a.bonds:
                        if bond.fragment_b == frag_id_b:
                            total_energy += bond.energy
        return total_energy

@dataclass
class CrystallizedInsight:
    """A coherent insight crystallized from patterns"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    core_pattern: str = ""  # Main insight
    supporting_patterns: List[str] = field(default_factory=list)  # Pattern IDs
    
    # Insight properties
    confidence: float = 0.0  # 0-1 confidence score
    novelty: float = 0.0  # How novel/unexpected
    clarity: float = 0.0  # How clear/well-formed
    
    # Evidence and support
    evidence_fragments: List[str] = field(default_factory=list)
    contradicting_fragments: List[str] = field(default_factory=list)
    contradictions: List[str] = field(default_factory=list)  # Actual contradictions found
    
    # Variations and perspectives
    variations: List[str] = field(default_factory=list)
    perspectives: Dict[str, str] = field(default_factory=dict)
    
    # Emergence path
    emergence_path: List[Dict] = field(default_factory=list)
    crystallization_time: datetime = field(default_factory=datetime.now)
    
    # Applications and implications
    implications: List[str] = field(default_factory=list)
    applications: List[str] = field(default_factory=list)
    
    def to_response(self) -> str:
        """Convert to human-readable response"""
        response = f"{self.core_pattern}\n\n"
        
        if self.variations:
            response += "Key variations:\n"
            for var in self.variations[:3]:  # Top 3 variations
                response += f"• {var}\n"
            response += "\n"
        
        if self.perspectives:
            response += "Different perspectives:\n"
            for perspective, view in list(self.perspectives.items())[:3]:
                response += f"• {perspective}: {view}\n"
            response += "\n"
        
        if self.implications:
            response += "This suggests:\n"
            for impl in self.implications[:3]:
                response += f"• {impl}\n"
        
        return response

@dataclass
class ReasoningField:
    """The field in which thought fragments interact"""
    dimensions: int = 384  # Embedding dimensions (matches all-MiniLM-L6-v2)
    temperature: float = 1.0  # System temperature
    entropy: float = 0.0  # Current entropy
    time: float = 0.0  # Current simulation time
    
    # Field properties
    potential_function: str = "coulomb"  # Type of potential
    coupling_constants: Dict[str, float] = field(default_factory=dict)
    
    # Fragments in the field
    fragments: Dict[str, ThoughtFragment] = field(default_factory=dict)
    bonds: List[Bond] = field(default_factory=list)
    patterns: Dict[str, EmergentPattern] = field(default_factory=dict)
    
    # History tracking
    history: List[Dict] = field(default_factory=list)
    phase_transitions: List[Tuple[float, str]] = field(default_factory=list)
    
    def add_fragment(self, fragment: ThoughtFragment):
        """Add a fragment to the field"""
        self.fragments[fragment.id] = fragment
        self.entropy += np.log(len(self.fragments) + 1)  # Increase entropy
    
    def step(self, dt: float = 0.01):
        """Advance field simulation by dt"""
        self.time += dt
        
        # Update fragment positions and energies
        for fragment in self.fragments.values():
            fragment.lifetime += dt
            fragment.oscillate(dt)
            
            # Apply decay
            fragment.activation_energy *= (1 - fragment.decay_rate * dt)
            
            # Check for phase transitions
            if self.detect_phase_transition():
                self.phase_transitions.append((self.time, "transition_detected"))
    
    def detect_phase_transition(self) -> bool:
        """Detect if system is undergoing phase transition"""
        if len(self.history) < 10:
            return False
        
        # Look for sudden changes in entropy or energy
        recent_entropies = [h.get('entropy', 0) for h in self.history[-10:]]
        entropy_variance = np.var(recent_entropies)
        
        return entropy_variance > 0.5  # Threshold for transition
    
    def get_state(self) -> Dict[str, Any]:
        """Get current field state"""
        return {
            'time': self.time,
            'temperature': self.temperature,
            'entropy': self.entropy,
            'num_fragments': len(self.fragments),
            'num_bonds': len(self.bonds),
            'num_patterns': len(self.patterns),
            'phase_transitions': len(self.phase_transitions)
        }
