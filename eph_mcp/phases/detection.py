"""
Phase 3: Pattern Detection
Identify emergent structures in thought cloud
"""
import numpy as np
from typing import List, Dict, Set, Tuple, Optional, Union
from sklearn.cluster import SpectralClustering, DBSCAN
from sklearn.decomposition import PCA
from scipy.spatial import ConvexHull
from scipy.stats import entropy
import networkx as nx
from .. import ThoughtFragment, EmergentPattern, PatternType, ReasoningField
import asyncio

class PatternDetector:
    """Identifies emergent structures in thought cloud"""
    
    def __init__(self):
        """Initialize pattern detector"""
        self.min_pattern_size = 3  # Minimum fragments for a pattern
        self.pattern_threshold = 0.5  # Minimum strength for pattern
        
        # Pattern detection parameters
        self.clustering_eps = 0.3
        self.min_samples = 2
        self.spectral_clusters = 'auto'
        
        # Detected patterns
        self.patterns = {}
    
    async def detect_patterns(self, field: ReasoningField) -> Dict[str, List[EmergentPattern]]:
        """Detect all types of patterns in the field"""
        
        patterns = {
            'crystalline_lattices': await self._find_crystalline_lattices(field),
            'strange_attractors': await self._find_strange_attractors(field),
            'phase_transitions': await self._find_phase_transitions(field),
            'soliton_waves': await self._find_soliton_waves(field),
            'interference_patterns': await self._find_interference_patterns(field),
            'vortices': await self._find_vortices(field),
            'bridges': await self._find_bridges(field),
            'harmonics': await self._find_harmonics(field),
            'fractals': await self._find_fractals(field),
            'emergence': await self._find_true_emergence(field)
        }
        
        # Filter out weak patterns
        for pattern_type in patterns:
            patterns[pattern_type] = [
                p for p in patterns[pattern_type] 
                if p.strength > self.pattern_threshold
            ]
        
        # Store in field
        for pattern_type, pattern_list in patterns.items():
            for pattern in pattern_list:
                field.patterns[pattern.id] = pattern
        
        return patterns
    
    async def _find_crystalline_lattices(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find regular, repeating structures"""
        
        lattices = []
        fragments = list(field.fragments.values())
        
        if len(fragments) < self.min_pattern_size:
            return lattices
        
        # Build adjacency matrix from bonds
        n = len(fragments)
        adjacency = np.zeros((n, n))
        frag_indices = {f.id: i for i, f in enumerate(fragments)}
        
        for bond in field.bonds:
            if bond.fragment_a in frag_indices and bond.fragment_b in frag_indices:
                i, j = frag_indices[bond.fragment_a], frag_indices[bond.fragment_b]
                adjacency[i, j] = bond.strength
                adjacency[j, i] = bond.strength
        
        # Spectral clustering to find regular structures
        if np.any(adjacency):
            try:
                # Use default number of clusters if auto
                n_clusters = 3 if self.spectral_clusters == 'auto' else self.spectral_clusters
                clustering = SpectralClustering(
                    n_clusters=n_clusters,
                    affinity='precomputed',
                    random_state=42
                )
                
                # Convert to similarity matrix (positive values only)
                similarity = np.maximum(adjacency, 0)
                if np.any(similarity):
                    labels = clustering.fit_predict(similarity)
                    
                    # Analyze each cluster for regularity
                    for cluster_id in np.unique(labels):
                        cluster_fragments = [
                            fragments[i] for i in range(n) 
                            if labels[i] == cluster_id
                        ]
                        
                        if len(cluster_fragments) >= self.min_pattern_size:
                            regularity = self._measure_regularity(cluster_fragments, field)
                            
                            if regularity > 0.7:
                                pattern = EmergentPattern(
                                    pattern_type=PatternType.CRYSTALLINE_LATTICE,
                                    fragments=[f.id for f in cluster_fragments],
                                    strength=regularity,
                                    stability=self._calculate_stability(cluster_fragments),
                                    coherence=np.mean([f.coherence for f in cluster_fragments]),
                                    symmetry=self._classify_symmetry(cluster_fragments, field)
                                )
                                
                                # Find the unit cell
                                pattern.central_insight = self._extract_unit_cell(cluster_fragments)
                                
                                # Find defects (imperfections)
                                defects = self._find_defects(cluster_fragments, field)
                                pattern.variations = [f"Defect: {d}" for d in defects[:3]]
                                
                                lattices.append(pattern)
            
            except Exception as e:
                print(f"Spectral clustering failed: {e}")
        
        return lattices
    
    async def _find_strange_attractors(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find cyclic but chaotic patterns"""
        
        attractors = []
        
        # Analyze trajectories through semantic space
        trajectories = self._trace_semantic_trajectories(field)
        
        for trajectory in trajectories:
            if len(trajectory) < 10:  # Need enough points for analysis
                continue
            
            # Build recurrence plot
            recurrence = self._build_recurrence_matrix(trajectory)
            
            # Find basins of attraction
            basins = self._find_attraction_basins(recurrence)
            
            for basin in basins:
                if self._is_strange_attractor(basin):
                    # Calculate Lyapunov exponent (chaos measure)
                    lyapunov = self._calculate_lyapunov_exponent(basin['trajectory'])
                    
                    pattern = EmergentPattern(
                        pattern_type=PatternType.STRANGE_ATTRACTOR,
                        fragments=basin['fragments'],
                        strength=basin['strength'],
                        stability=1.0 / (1.0 + abs(lyapunov)),  # Less chaos = more stable
                        entropy=basin['entropy'],
                        dimensionality=self._calculate_fractal_dimension(basin['trajectory'])
                    )
                    
                    # Extract central tension
                    pattern.central_insight = self._extract_central_tension(basin['center'])
                    
                    # Extract orbital perspectives
                    pattern.variations = self._extract_orbital_perspectives(basin['trajectory'])
                    
                    attractors.append(pattern)
        
        return attractors
    
    async def _find_phase_transitions(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find sudden reorganizations in the system"""
        
        transitions = []
        
        # Analyze field history for discontinuities
        if len(field.history) < 20:
            return transitions
        
        # Calculate order parameters over time
        order_params = []
        for state in field.history:
            order_params.append({
                'entropy': state.get('entropy', 0),
                'avg_bonds': state.get('avg_bonds', 0),
                'avg_coherence': state.get('avg_coherence', 0),
                'total_energy': state.get('total_energy', 0)
            })
        
        # Detect sudden changes
        for i in range(1, len(order_params) - 1):
            prev = order_params[i-1]
            curr = order_params[i]
            next_param = order_params[i+1]
            
            # Calculate rate of change
            entropy_change = abs(curr['entropy'] - prev['entropy'])
            bond_change = abs(curr['avg_bonds'] - prev['avg_bonds'])
            
            if entropy_change > 0.5 or bond_change > 1.0:
                # Phase transition detected
                pattern = EmergentPattern(
                    pattern_type=PatternType.PHASE_TRANSITION,
                    strength=entropy_change + bond_change,
                    entropy=curr['entropy']
                )
                
                # Identify fragments involved in transition
                pattern.fragments = self._identify_transition_fragments(field, i)
                
                # Describe the transition
                pattern.central_insight = f"System reorganization: entropy Δ={entropy_change:.2f}"
                
                transitions.append(pattern)
        
        return transitions
    
    async def _find_soliton_waves(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find propagating insights that maintain form"""
        
        solitons = []
        
        # Track activation energy propagation
        fragments = list(field.fragments.values())
        
        # Group fragments by activation patterns
        activation_waves = self._detect_activation_waves(fragments, field)
        
        for wave in activation_waves:
            if self._is_soliton(wave):
                pattern = EmergentPattern(
                    pattern_type=PatternType.SOLITON_WAVE,
                    fragments=[f.id for f in wave['fragments']],
                    strength=wave['amplitude'],
                    stability=wave['stability']
                )
                
                pattern.central_insight = f"Self-reinforcing insight: {wave['content']}"
                pattern.variations = [f"Wave speed: {wave['speed']}", 
                                     f"Wavelength: {wave['wavelength']}"]
                
                solitons.append(pattern)
        
        return solitons
    
    async def _find_interference_patterns(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find constructive and destructive interference"""
        
        patterns = []
        fragments = list(field.fragments.values())
        
        # Find oscillating fragments
        oscillators = [f for f in fragments if f.resonance_frequency > 0]
        
        # Check pairs for interference
        for i, osc_a in enumerate(oscillators):
            for osc_b in oscillators[i+1:]:
                # Calculate phase difference
                phase_diff = abs(osc_a.phase - osc_b.phase)
                freq_ratio = osc_a.resonance_frequency / (osc_b.resonance_frequency + 0.001)
                
                # Constructive interference (in phase)
                if phase_diff < 0.5 or phase_diff > 2*np.pi - 0.5:
                    pattern = EmergentPattern(
                        pattern_type=PatternType.INTERFERENCE,
                        fragments=[osc_a.id, osc_b.id],
                        strength=osc_a.amplitude * osc_b.amplitude,
                        coherence=(osc_a.coherence + osc_b.coherence) / 2
                    )
                    
                    pattern.central_insight = f"Reinforcing resonance: {osc_a.content[:20]} + {osc_b.content[:20]}"
                    pattern.variations = ["Constructive interference"]
                    
                    patterns.append(pattern)
                
                # Destructive interference (out of phase)
                elif np.pi - 0.5 < phase_diff < np.pi + 0.5:
                    pattern = EmergentPattern(
                        pattern_type=PatternType.INTERFERENCE,
                        fragments=[osc_a.id, osc_b.id],
                        strength=-osc_a.amplitude * osc_b.amplitude,
                        coherence=(osc_a.coherence + osc_b.coherence) / 2
                    )
                    
                    pattern.central_insight = f"Canceling ideas: {osc_a.content[:20]} vs {osc_b.content[:20]}"
                    pattern.variations = ["Destructive interference"]
                    pattern.contradictions = [osc_a.content, osc_b.content]
                    
                    patterns.append(pattern)
        
        return patterns
    
    async def _find_vortices(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find swirling contradictions"""
        
        vortices = []
        
        # Find circular bond patterns
        G = self._build_bond_graph(field)
        
        # Find cycles in the graph
        cycles = list(nx.simple_cycles(G))
        
        for cycle in cycles:
            if len(cycle) >= 3:
                # Check if cycle contains contradictions
                has_contradiction = False
                cycle_fragments = [field.fragments[node] for node in cycle if node in field.fragments]
                
                for i, frag in enumerate(cycle_fragments):
                    next_frag = cycle_fragments[(i+1) % len(cycle_fragments)]
                    
                    # Check bonds between consecutive fragments
                    for bond in frag.bonds:
                        if bond.fragment_b == next_frag.id and bond.bond_type == "contradiction":
                            has_contradiction = True
                            break
                
                if has_contradiction:
                    pattern = EmergentPattern(
                        pattern_type=PatternType.VORTEX,
                        fragments=cycle,
                        strength=len(cycle),
                        entropy=self._calculate_cycle_entropy(cycle_fragments)
                    )
                    
                    pattern.central_insight = f"Circular contradiction involving {len(cycle)} ideas"
                    pattern.contradictions = [f.content[:30] for f in cycle_fragments]
                    
                    vortices.append(pattern)
        
        return vortices
    
    async def _find_bridges(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find unexpected connections between clusters"""
        
        bridges = []
        
        # Build graph and find connected components
        G = self._build_bond_graph(field)
        
        if len(G) == 0:
            return bridges
        
        # Find bridge edges (removal disconnects graph)
        # Convert to undirected for bridge detection
        G_undirected = G.to_undirected()
        bridge_edges = list(nx.bridges(G_undirected))
        
        for edge in bridge_edges:
            frag_a_id, frag_b_id = edge
            
            if frag_a_id in field.fragments and frag_b_id in field.fragments:
                frag_a = field.fragments[frag_a_id]
                frag_b = field.fragments[frag_b_id]
                
                # Calculate semantic distance
                if frag_a.embedding is not None and frag_b.embedding is not None:
                    distance = np.linalg.norm(frag_a.embedding - frag_b.embedding)
                    
                    # Unexpected if semantically distant but connected
                    if distance > 0.7:
                        pattern = EmergentPattern(
                            pattern_type=PatternType.BRIDGE,
                            fragments=[frag_a_id, frag_b_id],
                            strength=1.0 / distance,  # Stronger if more unexpected
                            coherence=(frag_a.coherence + frag_b.coherence) / 2
                        )
                        
                        pattern.central_insight = f"Unexpected link: {frag_a.content[:20]} ⟷ {frag_b.content[:20]}"
                        
                        bridges.append(pattern)
        
        return bridges
    
    async def _find_harmonics(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find resonating ideas at harmonic frequencies"""
        
        harmonics = []
        fragments = list(field.fragments.values())
        
        # Group by frequency ratios
        for i, frag_a in enumerate(fragments):
            if frag_a.resonance_frequency == 0:
                continue
            
            harmonic_group = [frag_a]
            base_freq = frag_a.resonance_frequency
            
            for frag_b in fragments[i+1:]:
                if frag_b.resonance_frequency == 0:
                    continue
                
                freq_ratio = frag_b.resonance_frequency / base_freq
                
                # Check for harmonic ratios (1:2, 1:3, 2:3, etc.)
                harmonic_ratios = [2.0, 3.0, 1.5, 4.0, 0.5, 0.33, 0.67]
                
                for ratio in harmonic_ratios:
                    if abs(freq_ratio - ratio) < 0.1:
                        harmonic_group.append(frag_b)
                        break
            
            if len(harmonic_group) >= 2:
                pattern = EmergentPattern(
                    pattern_type=PatternType.HARMONIC,
                    fragments=[f.id for f in harmonic_group],
                    strength=len(harmonic_group),
                    coherence=np.mean([f.coherence for f in harmonic_group])
                )
                
                pattern.central_insight = f"Harmonic resonance at {base_freq:.1f}Hz base"
                pattern.variations = [f"{f.content[:20]} @ {f.resonance_frequency:.1f}Hz" 
                                     for f in harmonic_group[:3]]
                
                harmonics.append(pattern)
        
        return harmonics
    
    async def _find_fractals(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find self-similar patterns at different scales"""
        
        fractals = []
        
        # Hierarchical clustering to find scale-invariant structures
        fragments = list(field.fragments.values())
        
        if len(fragments) < 10:
            return fractals
        
        # Get embeddings
        embeddings = []
        valid_fragments = []
        for f in fragments:
            if f.embedding is not None:
                embeddings.append(f.embedding)
                valid_fragments.append(f)
        
        if len(embeddings) < 10:
            return fractals
        
        embeddings = np.array(embeddings)
        
        # Multi-scale clustering
        scales = [0.1, 0.3, 0.5, 0.7, 0.9]
        clusters_at_scales = []
        
        for scale in scales:
            clustering = DBSCAN(eps=scale, min_samples=2)
            labels = clustering.fit_predict(embeddings)
            clusters_at_scales.append(labels)
        
        # Find fragments that maintain relationships across scales
        consistent_groups = self._find_scale_invariant_groups(clusters_at_scales, valid_fragments)
        
        for group in consistent_groups:
            if len(group) >= self.min_pattern_size:
                pattern = EmergentPattern(
                    pattern_type=PatternType.FRACTAL,
                    fragments=[f.id for f in group],
                    strength=len(group) / len(valid_fragments),
                    dimensionality=self._calculate_fractal_dimension([f.embedding for f in group])
                )
                
                pattern.central_insight = f"Self-similar structure across {len(scales)} scales"
                pattern.topology = "scale-invariant"
                
                fractals.append(pattern)
        
        return fractals
    
    async def _find_true_emergence(self, field: ReasoningField) -> List[EmergentPattern]:
        """Find truly novel patterns not reducible to parts"""
        
        emergent = []
        
        # Look for patterns that appear only in combinations
        fragments = list(field.fragments.values())
        
        # Build interaction network
        G = self._build_bond_graph(field)
        
        # Find dense subgraphs (potential emergence sites)
        if len(G) > 0:
            # Find k-cores (subgraphs where each node has at least k connections)
            for k in range(3, min(10, len(G))):
                # Convert to undirected for k-core
                G_undirected = G.to_undirected()
                k_core = nx.k_core(G_undirected, k)
                
                if len(k_core) >= self.min_pattern_size:
                    core_fragments = [field.fragments[n] for n in k_core.nodes() 
                                    if n in field.fragments]
                    
                    # Check for emergent properties
                    collective_property = self._detect_collective_property(core_fragments)
                    
                    if collective_property:
                        pattern = EmergentPattern(
                            pattern_type=PatternType.EMERGENCE,
                            fragments=[f.id for f in core_fragments],
                            strength=k / len(G),  # Normalized by graph size
                            coherence=np.mean([f.coherence for f in core_fragments]),
                            entropy=self._calculate_emergence_entropy(core_fragments)
                        )
                        
                        pattern.central_insight = collective_property
                        pattern.topology = f"{k}-core structure"
                        
                        emergent.append(pattern)
        
        return emergent
    
    # Helper methods
    
    def _measure_regularity(self, fragments: List[ThoughtFragment], 
                           field: ReasoningField) -> float:
        """Measure how regular/crystalline a structure is"""
        
        if len(fragments) < 2:
            return 0.0
        
        # Calculate pairwise distances
        distances = []
        for i, frag_a in enumerate(fragments):
            for frag_b in fragments[i+1:]:
                if frag_a.position is not None and frag_b.position is not None:
                    dist = np.linalg.norm(frag_a.position - frag_b.position)
                    distances.append(dist)
        
        if not distances:
            return 0.0
        
        # Regular structures have consistent distances
        regularity = 1.0 / (1.0 + np.std(distances))
        
        return min(regularity, 1.0)
    
    def _calculate_stability(self, fragments: List[ThoughtFragment]) -> float:
        """Calculate pattern stability"""
        
        # Stability based on:
        # 1. Average activation energy (higher = less stable)
        # 2. Coherence (higher = more stable)
        # 3. Decay rate (lower = more stable)
        
        avg_activation = np.mean([f.activation_energy for f in fragments])
        avg_coherence = np.mean([f.coherence for f in fragments])
        avg_decay = np.mean([f.decay_rate for f in fragments])
        
        stability = avg_coherence / (1.0 + avg_activation * avg_decay)
        
        return min(stability, 1.0)
    
    def _classify_symmetry(self, fragments: List[ThoughtFragment], 
                          field: ReasoningField) -> str:
        """Classify the type of symmetry in the pattern"""
        
        # Simple classification based on bond patterns
        bond_types = set()
        for fragment in fragments:
            for bond in fragment.bonds:
                bond_types.add(bond.bond_type)
        
        if len(bond_types) == 1:
            return "uniform"
        elif len(bond_types) == 2:
            return "binary"
        else:
            return "complex"
    
    def _extract_unit_cell(self, fragments: List[ThoughtFragment]) -> str:
        """Extract the minimal repeating unit"""
        
        if not fragments:
            return ""
        
        # Find most common content patterns
        contents = [f.content for f in fragments]
        
        # Simple approach: find shortest content that appears in multiple fragments
        common_words = set(contents[0].split())
        for content in contents[1:]:
            common_words &= set(content.split())
        
        if common_words:
            return f"Unit: {' '.join(list(common_words)[:3])}"
        
        return f"Unit: {fragments[0].content[:30]}"
    
    def _find_defects(self, fragments: List[ThoughtFragment], 
                     field: ReasoningField) -> List[str]:
        """Find defects in crystalline structure"""
        
        defects = []
        
        # Defects are fragments with unusual properties
        avg_activation = np.mean([f.activation_energy for f in fragments])
        std_activation = np.std([f.activation_energy for f in fragments])
        
        for fragment in fragments:
            # High activation = defect
            if fragment.activation_energy > avg_activation + 2 * std_activation:
                defects.append(f"High energy: {fragment.content[:20]}")
            
            # Low coherence = defect
            if fragment.coherence < 0.3:
                defects.append(f"Decoherent: {fragment.content[:20]}")
            
            # No bonds = vacancy defect
            if len(fragment.bonds) == 0:
                defects.append(f"Isolated: {fragment.content[:20]}")
        
        return defects
    
    def _trace_semantic_trajectories(self, field: ReasoningField) -> List[List[Dict]]:
        """Trace trajectories through semantic space"""
        
        trajectories = []
        
        # Group fragments by generation time
        fragments = sorted(field.fragments.values(), 
                         key=lambda f: f.creation_time)
        
        # Create trajectory for each seed fragment
        for seed in fragments[:5]:  # Start with first 5 fragments
            trajectory = []
            current = seed
            visited = set()
            
            while current and current.id not in visited:
                visited.add(current.id)
                trajectory.append({
                    'fragment': current,
                    'position': current.position.copy() if current.position is not None else None,
                    'activation': current.activation_energy
                })
                
                # Follow strongest bond
                strongest_bond = None
                max_strength = 0
                
                for bond in current.bonds:
                    if abs(bond.strength) > max_strength:
                        next_id = bond.fragment_b if bond.fragment_a == current.id else bond.fragment_a
                        if next_id not in visited and next_id in field.fragments:
                            strongest_bond = bond
                            max_strength = abs(bond.strength)
                
                if strongest_bond:
                    next_id = strongest_bond.fragment_b if strongest_bond.fragment_a == current.id else strongest_bond.fragment_a
                    current = field.fragments.get(next_id)
                else:
                    current = None
            
            if len(trajectory) > 3:
                trajectories.append(trajectory)
        
        return trajectories
    
    def _build_recurrence_matrix(self, trajectory: List[Dict]) -> np.ndarray:
        """Build recurrence plot for trajectory"""
        
        n = len(trajectory)
        recurrence = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if trajectory[i]['position'] is not None and trajectory[j]['position'] is not None:
                    dist = np.linalg.norm(trajectory[i]['position'] - trajectory[j]['position'])
                    recurrence[i, j] = 1.0 / (1.0 + dist)
        
        return recurrence
    
    def _find_attraction_basins(self, recurrence: np.ndarray) -> List[Dict]:
        """Find basins of attraction in recurrence plot"""
        
        basins = []
        n = recurrence.shape[0]
        
        # Find recurring regions (high recurrence density)
        for i in range(n):
            recurring_indices = np.where(recurrence[i] > 0.7)[0]
            
            if len(recurring_indices) > 2:
                basin = {
                    'center': i,
                    'fragments': recurring_indices.tolist(),
                    'strength': np.mean(recurrence[i, recurring_indices]),
                    'entropy': entropy(recurrence[i]),
                    'trajectory': recurring_indices
                }
                basins.append(basin)
        
        return basins
    
    def _is_strange_attractor(self, basin: Dict) -> bool:
        """Check if basin is a strange attractor (chaotic but bounded)"""
        
        # Strange if:
        # 1. Non-periodic (high entropy)
        # 2. Bounded (limited range)
        # 3. Sensitive to initial conditions
        
        return basin['entropy'] > 0.5 and len(basin['fragments']) > 5
    
    def _calculate_lyapunov_exponent(self, trajectory: np.ndarray) -> float:
        """Calculate Lyapunov exponent (measure of chaos)"""
        
        if len(trajectory) < 2:
            return 0.0
        
        # Simplified calculation
        divergence_rate = 0.0
        for i in range(1, len(trajectory)):
            if i > 0:
                divergence_rate += np.log(abs(trajectory[i] - trajectory[i-1]) + 0.001)
        
        return divergence_rate / len(trajectory)
    
    def _calculate_fractal_dimension(self, points: Union[List, np.ndarray]) -> float:
        """Calculate fractal dimension using box-counting method"""
        
        if len(points) < 10:
            return 1.0
        
        points = np.array(points)
        
        # Box-counting algorithm
        scales = [0.1, 0.2, 0.4, 0.8, 1.6]
        counts = []
        
        for scale in scales:
            # Count boxes needed to cover points
            mins = np.min(points, axis=0)
            maxs = np.max(points, axis=0)
            
            n_boxes = 1
            for dim in range(points.shape[1]):
                if maxs[dim] > mins[dim]:
                    n_boxes *= int((maxs[dim] - mins[dim]) / scale) + 1
            
            counts.append(n_boxes)
        
        # Fit line to log-log plot
        if len(counts) > 1:
            coeffs = np.polyfit(np.log(scales), np.log(counts), 1)
            return -coeffs[0]  # Negative slope = fractal dimension
        
        return 1.0
    
    def _extract_central_tension(self, center_idx: int) -> str:
        """Extract the central tension from attractor center"""
        
        return f"Unresolved tension at index {center_idx}"
    
    def _extract_orbital_perspectives(self, trajectory: List) -> List[str]:
        """Extract different perspectives from orbital trajectory"""
        
        perspectives = []
        for i, point in enumerate(trajectory[:5]):
            perspectives.append(f"Perspective {i+1} at position {point}")
        
        return perspectives
    
    def _identify_transition_fragments(self, field: ReasoningField, 
                                      time_index: int) -> List[str]:
        """Identify fragments involved in phase transition"""
        
        # Return fragments with high activation at transition time
        fragments = list(field.fragments.values())
        transition_fragments = []
        
        for fragment in fragments:
            if fragment.activation_energy > 1.5:
                transition_fragments.append(fragment.id)
        
        return transition_fragments[:10]  # Limit to 10
    
    def _detect_activation_waves(self, fragments: List[ThoughtFragment], 
                                field: ReasoningField) -> List[Dict]:
        """Detect waves of activation propagating through fragments"""
        
        waves = []
        
        # Group fragments by activation patterns
        high_activation = [f for f in fragments if f.activation_energy > 1.0]
        
        if len(high_activation) > 2:
            # Simple wave detection
            wave = {
                'fragments': high_activation,
                'amplitude': np.mean([f.activation_energy for f in high_activation]),
                'stability': np.std([f.activation_energy for f in high_activation]),
                'speed': 1.0,  # Placeholder
                'wavelength': len(high_activation),
                'content': high_activation[0].content[:30] if high_activation else ""
            }
            waves.append(wave)
        
        return waves
    
    def _is_soliton(self, wave: Dict) -> bool:
        """Check if wave is a soliton (maintains form while propagating)"""
        
        # Soliton if stable (low variance) and high amplitude
        return wave['stability'] < 0.5 and wave['amplitude'] > 1.0
    
    def _build_bond_graph(self, field: ReasoningField) -> nx.DiGraph:
        """Build directed graph from bonds"""
        
        G = nx.DiGraph()
        
        for bond in field.bonds:
            if bond.strength > 0:
                G.add_edge(bond.fragment_a, bond.fragment_b, 
                          weight=bond.strength, type=bond.bond_type)
            else:
                # Negative bonds as reverse edges
                G.add_edge(bond.fragment_b, bond.fragment_a, 
                          weight=-bond.strength, type=bond.bond_type)
        
        return G
    
    def _calculate_cycle_entropy(self, fragments: List[ThoughtFragment]) -> float:
        """Calculate entropy of a cycle"""
        
        if not fragments:
            return 0.0
        
        # Entropy based on activation distribution
        activations = [f.activation_energy for f in fragments]
        if sum(activations) > 0:
            probs = np.array(activations) / sum(activations)
            return entropy(probs)
        
        return 0.0
    
    def _find_scale_invariant_groups(self, clusters_at_scales: List[np.ndarray], 
                                    fragments: List[ThoughtFragment]) -> List[List[ThoughtFragment]]:
        """Find groups that maintain structure across scales"""
        
        groups = []
        n_fragments = len(fragments)
        
        # Find fragments that stay together across scales
        for i in range(n_fragments):
            group = [fragments[i]]
            
            for j in range(i+1, n_fragments):
                together_count = 0
                
                for scale_labels in clusters_at_scales:
                    if scale_labels[i] == scale_labels[j] and scale_labels[i] != -1:
                        together_count += 1
                
                # If together in most scales
                if together_count >= len(clusters_at_scales) * 0.6:
                    group.append(fragments[j])
            
            if len(group) >= 3:
                groups.append(group)
        
        return groups
    
    def _detect_collective_property(self, fragments: List[ThoughtFragment]) -> Optional[str]:
        """Detect emergent collective property"""
        
        if not fragments:
            return None
        
        # Look for properties that appear only in combination
        individual_words = set()
        for fragment in fragments:
            individual_words.update(fragment.content.lower().split())
        
        # Check if combination creates new meaning
        combined = " ".join([f.content for f in fragments])
        combined_words = set(combined.lower().split())
        
        # Emergent words (appear in combination but not individually)
        emergent_words = combined_words - individual_words
        
        if emergent_words:
            return f"Emergent concept: {' '.join(list(emergent_words)[:3])}"
        
        # Check for semantic emergence
        if len(fragments) > 3:
            avg_coherence = np.mean([f.coherence for f in fragments])
            if avg_coherence > 0.8:
                return f"Collective coherence: {combined[:50]}"
        
        return None
    
    def _calculate_emergence_entropy(self, fragments: List[ThoughtFragment]) -> float:
        """Calculate entropy of emergent pattern"""
        
        if not fragments:
            return 0.0
        
        # Multiple entropy sources
        activation_entropy = entropy([f.activation_energy for f in fragments])
        coherence_entropy = entropy([f.coherence for f in fragments])
        frequency_entropy = entropy([f.resonance_frequency for f in fragments 
                                    if f.resonance_frequency > 0])
        
        return np.mean([activation_entropy, coherence_entropy, frequency_entropy])

from typing import Union
