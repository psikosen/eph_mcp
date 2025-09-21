"""
Phase 2: Interaction Dynamics
Simulate interactions between thought fragments in semantic field
"""
import numpy as np
from typing import List, Dict
from scipy.spatial.distance import cosine, euclidean
from .. import ThoughtFragment, Bond, BondType, ReasoningField
import asyncio

class InteractionField:
    """Thoughts interact like particles in a field"""
    
    def __init__(self, dimensions: int = 512):
        """Initialize interaction field"""
        self.dimensions = dimensions
        self.field = ReasoningField(dimensions=dimensions)
        
        # Interaction parameters
        self.coupling_constants = {
            BondType.SEMANTIC: 1.0,
            BondType.CAUSAL: 2.0,
            BondType.CONTRADICTION: -1.5,
            BondType.METAPHORICAL: 0.8,
            BondType.TEMPORAL: 0.6,
            BondType.HIERARCHICAL: 1.2,
            BondType.RESONANT: 1.5,
            BondType.ENTANGLED: 3.0
        }
        
        # Field parameters
        self.temperature = 1.0  # System temperature
        self.friction = 0.1  # Damping factor
        self.dt = 0.01  # Time step
        self.cooling_rate = 0.995
        
        # Tracking
        self.interaction_history = []
        self.phase_transitions = []
    
    async def simulate(self, fragments: List[ThoughtFragment],
                       iterations: int = 100) -> ReasoningField:
        """Simulate field evolution with fragment interactions"""

        # Reset field state for a fresh simulation
        self.field = ReasoningField(dimensions=self.dimensions)
        self.interaction_history = []
        self.phase_transitions = []

        # Get actual embedding dimensions from fragments
        if fragments and fragments[0].embedding is not None:
            self.dimensions = len(fragments[0].embedding)
            self.field.dimensions = self.dimensions

        # Initialize field with fragments
        for fragment in fragments:
            self.field.add_fragment(fragment)
        
        # Run simulation
        for iteration in range(iterations):
            await self._simulation_step(iteration)
            
            # Cool system gradually (simulated annealing)
            self.temperature *= self.cooling_rate
            
            # Check for phase transitions
            if self._detect_phase_transition():
                self.phase_transitions.append({
                    'iteration': iteration,
                    'temperature': self.temperature,
                    'entropy': self.field.entropy
                })
        
        return self.field
    
    async def _simulation_step(self, iteration: int):
        """Single step of field simulation"""
        
        fragments = list(self.field.fragments.values())
        
        # Calculate all pairwise interactions
        tasks = []
        for i, frag_a in enumerate(fragments):
            for j, frag_b in enumerate(fragments[i+1:], i+1):
                task = self._calculate_interaction(frag_a, frag_b)
                tasks.append(task)
        
        # Process interactions in parallel
        interactions = await asyncio.gather(*tasks)
        
        # Apply forces to update positions
        forces = self._aggregate_forces(fragments, interactions)
        self._update_positions(fragments, forces)
        
        # Update bonds based on distances
        self._update_bonds(fragments, interactions)
        
        # Apply quantum effects
        self._apply_quantum_effects(fragments)
        
        # Track state
        self.field.step(self.dt)
        self._record_state(iteration)
    
    async def _calculate_interaction(self, frag_a: ThoughtFragment, 
                                    frag_b: ThoughtFragment) -> Dict:
        """Calculate interaction between two fragments"""
        
        if frag_a.embedding is None or frag_b.embedding is None:
            return {'force': 0.0, 'bond_type': None}
        
        # Semantic similarity (attractive)
        semantic_sim = 1 - cosine(frag_a.embedding, frag_b.embedding)
        semantic_force = semantic_sim * self.coupling_constants[BondType.SEMANTIC]
        
        # Check for contradiction (repulsive)
        contradiction = self._detect_contradiction(frag_a.content, frag_b.content)
        contradiction_force = contradiction * self.coupling_constants[BondType.CONTRADICTION]
        
        # Check for causal relationship (strongly attractive)
        causality = self._detect_causality(frag_a.content, frag_b.content)
        causal_force = causality * self.coupling_constants[BondType.CAUSAL]
        
        # Metaphorical resonance
        metaphor_resonance = self._calculate_metaphorical_similarity(frag_a, frag_b)
        metaphor_force = metaphor_resonance * self.coupling_constants[BondType.METAPHORICAL]
        
        # Temporal correlation
        temporal = self._detect_temporal_relation(frag_a.content, frag_b.content)
        temporal_force = temporal * self.coupling_constants[BondType.TEMPORAL]
        
        # Quantum entanglement (non-local correlation)
        entanglement = self._calculate_entanglement(frag_a, frag_b)
        entangle_force = entanglement * self.coupling_constants[BondType.ENTANGLED]
        
        # Total force
        total_force = (semantic_force + causal_force + metaphor_force + 
                      temporal_force + entangle_force + contradiction_force)
        
        # Determine dominant bond type
        forces = {
            BondType.SEMANTIC: semantic_force,
            BondType.CAUSAL: causal_force,
            BondType.CONTRADICTION: abs(contradiction_force),
            BondType.METAPHORICAL: metaphor_force,
            BondType.TEMPORAL: temporal_force,
            BondType.ENTANGLED: entangle_force
        }
        
        dominant_bond = max(forces, key=forces.get)
        
        return {
            'frag_a': frag_a.id,
            'frag_b': frag_b.id,
            'force': total_force,
            'bond_type': dominant_bond,
            'strength': forces[dominant_bond],
            'distance': euclidean(frag_a.position, frag_b.position) if frag_a.position is not None else 0,
            'components': forces
        }
    
    def _detect_contradiction(self, content_a: str, content_b: str) -> float:
        """Detect logical contradiction between contents"""
        
        # Simple contradiction patterns
        negation_words = ['not', 'never', 'no', 'opposite', 'inverse', 'anti']
        
        # Check for explicit negation
        for neg in negation_words:
            if neg in content_a.lower() and neg not in content_b.lower():
                return 0.5
            if neg in content_b.lower() and neg not in content_a.lower():
                return 0.5
        
        # Check for opposing concepts
        opposites = [
            ('increase', 'decrease'), ('up', 'down'), ('left', 'right'),
            ('positive', 'negative'), ('order', 'chaos'), ('simple', 'complex'),
            ('convergent', 'divergent'), ('stable', 'unstable')
        ]
        
        for opp_a, opp_b in opposites:
            if (opp_a in content_a.lower() and opp_b in content_b.lower()) or \
               (opp_b in content_a.lower() and opp_a in content_b.lower()):
                return 0.8
        
        return 0.0
    
    def _detect_causality(self, content_a: str, content_b: str) -> float:
        """Detect causal relationship"""
        
        causal_markers = [
            'causes', 'leads to', 'results in', 'because', 'therefore',
            'implies', 'enables', 'requires', 'depends on', 'follows from'
        ]
        
        for marker in causal_markers:
            if marker in content_a.lower() or marker in content_b.lower():
                return 0.7
        
        # Check for temporal sequence suggesting causality
        temporal_markers = ['then', 'after', 'before', 'when', 'while']
        for marker in temporal_markers:
            if marker in content_a.lower() or marker in content_b.lower():
                return 0.3
        
        return 0.0
    
    def _calculate_metaphorical_similarity(self, frag_a: ThoughtFragment, 
                                          frag_b: ThoughtFragment) -> float:
        """Calculate metaphorical resonance"""
        
        # Check for metaphorical language
        metaphor_markers = ['like', 'as', 'resonates', 'mirrors', 'reflects', 'echoes']
        
        score = 0.0
        for marker in metaphor_markers:
            if marker in frag_a.content.lower() or marker in frag_b.content.lower():
                score += 0.2
        
        # Check for shared domains (e.g., both use water metaphors)
        domains = ['water', 'fire', 'garden', 'music', 'dance', 'war', 'journey']
        for domain in domains:
            if domain in frag_a.content.lower() and domain in frag_b.content.lower():
                score += 0.3
        
        return min(score, 1.0)
    
    def _detect_temporal_relation(self, content_a: str, content_b: str) -> float:
        """Detect temporal relationships"""
        
        temporal_words = [
            'past', 'present', 'future', 'before', 'after', 'during',
            'always', 'never', 'sometimes', 'cycle', 'phase', 'period'
        ]
        
        score = 0.0
        for word in temporal_words:
            if word in content_a.lower() and word in content_b.lower():
                score += 0.3
        
        return min(score, 1.0)
    
    def _calculate_entanglement(self, frag_a: ThoughtFragment, 
                               frag_b: ThoughtFragment) -> float:
        """Calculate quantum-like entanglement"""
        
        # Entanglement increases with:
        # 1. Shared parent fragments
        # 2. Similar generation strategies
        # 3. Phase correlation
        
        score = 0.0
        
        # Shared parents
        shared_parents = set(frag_a.parent_fragments) & set(frag_b.parent_fragments)
        if shared_parents:
            score += 0.5
        
        # Same generation strategy
        if frag_a.generation_strategy == frag_b.generation_strategy:
            score += 0.2
        
        # Phase correlation (quantum-like)
        phase_diff = abs(frag_a.phase - frag_b.phase)
        phase_correlation = np.cos(phase_diff)
        score += 0.3 * phase_correlation
        
        # Coherence product (more coherent = more entangled)
        score *= frag_a.coherence * frag_b.coherence
        
        return score
    
    def _aggregate_forces(self, fragments: List[ThoughtFragment], 
                         interactions: List[Dict]) -> Dict[str, np.ndarray]:
        """Aggregate all forces acting on each fragment"""
        
        forces = {}
        
        for fragment in fragments:
            forces[fragment.id] = np.zeros(self.dimensions)
        
        for interaction in interactions:
            if interaction and interaction['force'] != 0:
                frag_a_id = interaction['frag_a']
                frag_b_id = interaction['frag_b']
                
                # Find fragments
                frag_a = next((f for f in fragments if f.id == frag_a_id), None)
                frag_b = next((f for f in fragments if f.id == frag_b_id), None)
                
                if frag_a and frag_b and frag_a.position is not None and frag_b.position is not None:
                    # Calculate force direction
                    direction = frag_b.position - frag_a.position
                    distance = np.linalg.norm(direction)
                    
                    if distance > 0:
                        direction = direction / distance
                        
                        # Apply force (F = strength / distance^2)
                        force_magnitude = interaction['force'] / (distance ** 2 + 0.1)
                        force_vector = direction * force_magnitude
                        
                        # Newton's third law
                        forces[frag_a_id] += force_vector
                        forces[frag_b_id] -= force_vector
        
        return forces
    
    def _update_positions(self, fragments: List[ThoughtFragment], 
                         forces: Dict[str, np.ndarray]):
        """Update fragment positions based on forces"""
        
        for fragment in fragments:
            if fragment.id in forces and fragment.position is not None:
                # F = ma, assume m = 1
                acceleration = forces[fragment.id]
                
                # Add thermal noise
                thermal_noise = np.random.normal(0, self.temperature * 0.01, 
                                                self.dimensions)
                acceleration += thermal_noise
                
                # Update velocity with friction
                fragment.velocity = (fragment.velocity * (1 - self.friction) + 
                                   acceleration * self.dt)
                
                # Update position
                fragment.position += fragment.velocity * self.dt
                
                # Update kinetic energy
                fragment.kinetic_energy = 0.5 * np.sum(fragment.velocity ** 2)
    
    def _update_bonds(self, fragments: List[ThoughtFragment], 
                     interactions: List[Dict]):
        """Update bonds between fragments based on interactions"""
        
        # Clear existing bonds
        for fragment in fragments:
            fragment.bonds = []
        
        # Create new bonds for strong interactions
        bond_threshold = 0.5
        
        for interaction in interactions:
            if interaction and abs(interaction['force']) > bond_threshold:
                bond = Bond(
                    fragment_a=interaction['frag_a'],
                    fragment_b=interaction['frag_b'],
                    bond_type=interaction['bond_type'],
                    strength=interaction['strength'],
                    energy=-abs(interaction['force'])  # Negative = binding
                )
                
                # Add bond to fragments
                frag_a = next((f for f in fragments if f.id == interaction['frag_a']), None)
                frag_b = next((f for f in fragments if f.id == interaction['frag_b']), None)
                
                if frag_a and frag_b:
                    frag_a.bonds.append(bond)
                    frag_b.bonds.append(bond)
                    self.field.bonds.append(bond)
    
    def _apply_quantum_effects(self, fragments: List[ThoughtFragment]):
        """Apply quantum-like effects to fragments"""
        
        for fragment in fragments:
            # Decoherence over time
            fragment.coherence *= 0.99
            
            # Quantum tunneling (random activation)
            if np.random.random() < 0.01 * fragment.coherence:
                fragment.activation_energy += np.random.uniform(0.5, 1.5)
            
            # Wave function collapse (measurement effect)
            if len(fragment.bonds) > 3:  # Many observations
                fragment.coherence *= 0.9  # Faster decoherence
            
            # Entanglement spreading
            for bond in fragment.bonds:
                if bond.bond_type == BondType.ENTANGLED:
                    # Find entangled partner
                    partner_id = bond.fragment_b if bond.fragment_a == fragment.id else bond.fragment_a
                    fragment.entanglement.add(partner_id)
    
    def _detect_phase_transition(self) -> bool:
        """Detect if system is undergoing phase transition"""
        
        if len(self.interaction_history) < 10:
            return False
        
        # Look for sudden changes in order parameters
        recent_history = self.interaction_history[-10:]
        
        # Calculate order parameters
        avg_bonds = [h['avg_bonds'] for h in recent_history]
        bond_variance = np.var(avg_bonds)
        
        # Phase transition indicated by high variance
        return bond_variance > 1.0
    
    def _record_state(self, iteration: int):
        """Record current state for history"""
        
        fragments = list(self.field.fragments.values())
        
        # Calculate statistics
        avg_activation = np.mean([f.activation_energy for f in fragments])
        avg_coherence = np.mean([f.coherence for f in fragments])
        avg_bonds = np.mean([len(f.bonds) for f in fragments])
        
        total_kinetic = sum(f.kinetic_energy for f in fragments)
        total_potential = sum(f.potential_energy for f in fragments)
        
        state = {
            'iteration': iteration,
            'temperature': self.temperature,
            'entropy': self.field.entropy,
            'avg_activation': avg_activation,
            'avg_coherence': avg_coherence,
            'avg_bonds': avg_bonds,
            'total_energy': total_kinetic + total_potential,
            'num_fragments': len(fragments),
            'num_bonds': len(self.field.bonds)
        }
        
        self.interaction_history.append(state)
        self.field.history.append(state)
