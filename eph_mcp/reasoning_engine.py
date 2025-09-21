"""
Main Reasoning Engine for Emergent Pattern Hunter
Orchestrates all phases of the EPH process
"""
import time
import copy
import uuid
from typing import Dict, List, Optional, Any

from .phases.explosion import ThoughtExplosion
from .phases.interaction import InteractionField
from .phases.detection import PatternDetector
from .phases.crystallization import PatternCrystallizer
from .phases.weaving import PatternWeaver
from . import ReasoningField, ThoughtFragment, EmergentPattern, CrystallizedInsight
from .visualization import FieldVisualizer
from .logging_utils import get_logger

class EPHReasoningEngine:
    """Main engine that orchestrates the EPH reasoning process"""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize reasoning engine with configuration"""

        # Default configuration
        self.config = {
            'explosion': {
                'n_fragments': 75,
                'temperature': 1.5,
                'embedding_model': 'all-MiniLM-L6-v2'
            },
            'interaction': {
                'iterations': 100,
                'initial_temperature': 1.0,
                'cooling_rate': 0.995,
                'dt': 0.01
            },
            'detection': {
                'min_pattern_size': 3,
                'pattern_threshold': 0.5
            },
            'crystallization': {
                'confidence_threshold': 0.5,
                'novelty_threshold': 0.3
            },
            'weaving': {
                'max_insights': 5,
                'coherence_threshold': 0.6
            },
            'visualization': {
                'enabled': True,
                'output_dir': '/tmp/eph-mcp/visualizations'
            }
        }
        
        # Update with provided config
        if config:
            self._update_config(self.config, config)

        self.logger = get_logger(__name__, "reasoning_engine", classname=self.__class__.__name__)

        # Initialize phases
        self.explosion = ThoughtExplosion(
            model_name=self.config['explosion']['embedding_model']
        )
        self.interaction = InteractionField()
        self.detector = PatternDetector()
        self.crystallizer = PatternCrystallizer()
        self.weaver = PatternWeaver()
        
        # Initialize visualizer if enabled
        self.visualizer = None
        if self.config['visualization']['enabled']:
            self.visualizer = FieldVisualizer(
                output_dir=self.config['visualization']['output_dir']
            )
        
        # Tracking
        self.reasoning_history = []
        self.current_session = None
        
    async def reason(self, query: str,
                    return_intermediate: bool = False,
                    *,
                    config_overrides: Optional[Dict[str, Any]] = None,
                    visualize: Optional[bool] = None) -> Dict[str, Any]:
        """
        Main reasoning method - orchestrates all phases

        Args:
            query: The question or prompt to reason about
            return_intermediate: Whether to return intermediate results
            config_overrides: Per-request configuration overrides
            visualize: Optional override to enable/disable visualization

        Returns:
            Dict containing response and optionally intermediate results
        """

        effective_config = copy.deepcopy(self.config)
        if config_overrides:
            self._update_config(effective_config, config_overrides)

        if visualize is not None:
            effective_config.setdefault('visualization', {})
            effective_config['visualization']['enabled'] = visualize

        visualization_config = effective_config.get('visualization', {})
        visualization_enabled = visualization_config.get('enabled', False)
        visualizer = None

        if visualization_enabled:
            output_dir = visualization_config.get(
                'output_dir',
                self.config['visualization']['output_dir']
            )

            if self.visualizer is None or self.visualizer.output_dir != output_dir:
                self.visualizer = FieldVisualizer(output_dir=output_dir)
            visualizer = self.visualizer

        start_time = time.time()

        # Create session
        session_id = f"session_{uuid.uuid4().hex}"
        self.current_session = {
            'id': session_id,
            'query': query,
            'start_time': start_time,
            'phases': {},
            'config': effective_config
        }

        self.logger.info(
            "Starting reasoning session",
            extra={
                'context': {
                    'session_id': session_id,
                    'query_preview': query[:80],
                    'visualization': visualization_enabled
                }
            }
        )

        try:
            # Phase 1: Thought Explosion
            self.logger.info(
                "Phase 1: Thought explosion",
                extra={'context': {'session_id': session_id}}
            )
            fragments = await self._phase_explosion(query, effective_config)

            # Phase 2: Interaction Dynamics
            self.logger.info(
                "Phase 2: Interaction dynamics",
                extra={'context': {'session_id': session_id, 'fragment_count': len(fragments)}}
            )
            field = await self._phase_interaction(fragments, effective_config)

            # Phase 3: Pattern Detection
            self.logger.info(
                "Phase 3: Pattern detection",
                extra={'context': {'session_id': session_id}}
            )
            patterns = await self._phase_detection(field, effective_config)

            # Phase 4: Pattern Crystallization
            self.logger.info(
                "Phase 4: Pattern crystallization",
                extra={
                    'context': {
                        'session_id': session_id,
                        'pattern_total': sum(len(p) for p in patterns.values())
                    }
                }
            )
            insights = await self._phase_crystallization(patterns, field, effective_config)

            # Phase 5: Pattern Weaving
            self.logger.info(
                "Phase 5: Pattern weaving",
                extra={'context': {'session_id': session_id, 'insight_count': len(insights)}}
            )
            response = await self._phase_weaving(insights, query, effective_config)

            # Generate visualization if enabled
            if visualizer:
                await self._generate_visualizations(field, patterns, insights, visualizer)

            # Prepare results
            end_time = time.time()
            self.current_session['end_time'] = end_time
            self.current_session['duration'] = end_time - start_time

            result = {
                'response': response,
                'session_id': session_id,
                'duration': end_time - start_time,
                'statistics': self._generate_statistics(field, patterns, insights)
            }

            if return_intermediate:
                result['intermediate'] = {
                    'fragments': [f.to_dict() for f in fragments[:10]],
                    'field_state': field.get_state(),
                    'patterns': self._serialize_patterns(patterns),
                    'insights': [self._serialize_insight(i) for i in insights]
                }

            # Store in history
            self.reasoning_history.append(self.current_session)

            self.logger.info(
                "Reasoning session completed",
                extra={
                    'context': {
                        'session_id': session_id,
                        'duration_seconds': round(end_time - start_time, 3),
                        'insight_count': len(insights)
                    }
                }
            )

            return result

        except Exception as e:
            self.logger.error(
                "Error during reasoning session",
                extra={'error': str(e), 'context': {'session_id': session_id}}
            )
            self.current_session = None
            return {
                'response': f"An error occurred during reasoning: {str(e)}",
                'error': str(e),
                'session_id': session_id
            }
    
    async def _phase_explosion(self, query: str, config: Dict[str, Any]) -> List[ThoughtFragment]:
        """Phase 1: Thought Explosion"""

        phase_start = time.time()

        explosion_config = config.get('explosion', {})

        n_fragments = max(1, int(explosion_config.get(
            'n_fragments',
            self.config['explosion']['n_fragments']
        )))

        temperature = explosion_config.get('temperature')
        if temperature is not None:
            self.explosion.temperature = max(0.1, float(temperature))

        model_name = explosion_config.get('embedding_model')
        if model_name:
            try:
                self.explosion.set_embedding_model(model_name)
            except Exception as exc:
                self.logger.error(
                    "Failed to update embedding model",
                    extra={'error': str(exc), 'context': {'model_name': model_name}}
                )

        fragments = await self.explosion.explode(
            query,
            n=n_fragments
        )

        self.current_session['phases']['explosion'] = {
            'duration': time.time() - phase_start,
            'n_fragments': len(fragments),
            'strategies_used': list(set(f.generation_strategy for f in fragments)),
            'temperature': self.explosion.temperature
        }

        return fragments

    async def _phase_interaction(self, fragments: List[ThoughtFragment],
                                 config: Dict[str, Any]) -> ReasoningField:
        """Phase 2: Interaction Dynamics"""
        
        phase_start = time.time()
        
        interaction_config = config.get('interaction', {})

        initial_temperature = float(interaction_config.get(
            'initial_temperature',
            self.config['interaction']['initial_temperature']
        ))
        dt = float(interaction_config.get('dt', self.config['interaction']['dt']))
        iterations = max(1, int(interaction_config.get(
            'iterations',
            self.config['interaction']['iterations']
        )))
        cooling_rate = float(interaction_config.get(
            'cooling_rate',
            self.config['interaction']['cooling_rate']
        ))

        # Set interaction parameters
        self.interaction.temperature = initial_temperature
        self.interaction.dt = dt
        self.interaction.cooling_rate = cooling_rate
        self.interaction.phase_transitions = []

        # Run simulation
        field = await self.interaction.simulate(
            fragments,
            iterations=iterations
        )

        self.current_session['phases']['interaction'] = {
            'duration': time.time() - phase_start,
            'iterations': iterations,
            'final_temperature': self.interaction.temperature,
            'n_bonds': len(field.bonds),
            'phase_transitions': len(self.interaction.phase_transitions),
            'cooling_rate': self.interaction.cooling_rate
        }

        return field

    async def _phase_detection(self, field: ReasoningField,
                               config: Dict[str, Any]) -> Dict[str, List[EmergentPattern]]:
        """Phase 3: Pattern Detection"""
        
        phase_start = time.time()
        
        # Configure detector
        detection_config = config.get('detection', {})
        self.detector.min_pattern_size = detection_config.get(
            'min_pattern_size',
            self.config['detection']['min_pattern_size']
        )
        self.detector.pattern_threshold = detection_config.get(
            'pattern_threshold',
            self.config['detection']['pattern_threshold']
        )
        
        # Detect patterns
        patterns = await self.detector.detect_patterns(field)
        
        # Count patterns by type
        pattern_counts = {}
        for pattern_type, pattern_list in patterns.items():
            pattern_counts[pattern_type] = len(pattern_list)
        
        self.current_session['phases']['detection'] = {
            'duration': time.time() - phase_start,
            'pattern_counts': pattern_counts,
            'total_patterns': sum(pattern_counts.values())
        }
        
        return patterns
    
    async def _phase_crystallization(self, patterns: Dict[str, List[EmergentPattern]],
                                    field: ReasoningField,
                                    config: Dict[str, Any]) -> List[CrystallizedInsight]:
        """Phase 4: Pattern Crystallization"""
        
        phase_start = time.time()
        
        # Configure crystallizer
        crystallization_config = config.get('crystallization', {})
        self.crystallizer.confidence_threshold = crystallization_config.get(
            'confidence_threshold',
            self.config['crystallization']['confidence_threshold']
        )
        self.crystallizer.novelty_threshold = crystallization_config.get(
            'novelty_threshold',
            self.config['crystallization']['novelty_threshold']
        )
        
        # Crystallize patterns
        insights = await self.crystallizer.crystallize_patterns(patterns, field)
        
        self.current_session['phases']['crystallization'] = {
            'duration': time.time() - phase_start,
            'n_insights': len(insights),
            'avg_confidence': sum(i.confidence for i in insights) / max(len(insights), 1),
            'avg_novelty': sum(i.novelty for i in insights) / max(len(insights), 1)
        }
        
        return insights
    
    async def _phase_weaving(self, insights: List[CrystallizedInsight],
                            query: str,
                            config: Dict[str, Any]) -> str:
        """Phase 5: Pattern Weaving"""
        
        phase_start = time.time()
        
        # Configure weaver
        weaving_config = config.get('weaving', {})
        self.weaver.max_insights_per_response = weaving_config.get(
            'max_insights',
            self.config['weaving']['max_insights']
        )
        self.weaver.coherence_threshold = weaving_config.get(
            'coherence_threshold',
            self.config['weaving']['coherence_threshold']
        )
        
        # Weave response
        response = await self.weaver.weave(insights, query)
        
        self.current_session['phases']['weaving'] = {
            'duration': time.time() - phase_start,
            'insights_used': min(len(insights), self.weaver.max_insights_per_response),
            'response_length': len(response)
        }

        return response
    
    async def _generate_visualizations(self, field: ReasoningField,
                                      patterns: Dict[str, List[EmergentPattern]],
                                      insights: List[CrystallizedInsight],
                                      visualizer: Optional[FieldVisualizer]):
        """Generate visualizations of the reasoning process"""

        if not visualizer:
            return

        try:
            # Visualize field state
            field_viz = await visualizer.visualize_field(field)

            # Visualize patterns
            pattern_viz = await visualizer.visualize_patterns(patterns, field)

            # Visualize insight network
            insight_viz = await visualizer.visualize_insights(insights)

            # Generate summary visualization
            summary_viz = await visualizer.generate_summary(
                field, patterns, insights, self.current_session
            )

            self.current_session['visualizations'] = {
                'field': field_viz,
                'patterns': pattern_viz,
                'insights': insight_viz,
                'summary': summary_viz
            }

        except Exception as e:
            self.logger.error(
                "Visualization generation failed",
                extra={
                    'error': str(e),
                    'context': {
                        'session_id': self.current_session['id'] if self.current_session else None
                    }
                }
            )
    
    def _generate_statistics(self, field: ReasoningField, 
                           patterns: Dict[str, List[EmergentPattern]], 
                           insights: List[CrystallizedInsight]) -> Dict:
        """Generate statistics about the reasoning process"""
        
        return {
            'fragments': {
                'total': len(field.fragments),
                'avg_activation': sum(f.activation_energy for f in field.fragments.values()) / max(len(field.fragments), 1),
                'avg_coherence': sum(f.coherence for f in field.fragments.values()) / max(len(field.fragments), 1)
            },
            'field': {
                'entropy': field.entropy,
                'temperature': field.temperature,
                'n_bonds': len(field.bonds),
                'phase_transitions': len(field.phase_transitions)
            },
            'patterns': {
                'total': sum(len(p) for p in patterns.values()),
                'by_type': {k: len(v) for k, v in patterns.items()}
            },
            'insights': {
                'total': len(insights),
                'avg_confidence': sum(i.confidence for i in insights) / max(len(insights), 1),
                'avg_novelty': sum(i.novelty for i in insights) / max(len(insights), 1),
                'with_contradictions': sum(1 for i in insights if i.contradictions)
            }
        }
    
    def _serialize_patterns(self, patterns: Dict[str, List[EmergentPattern]]) -> Dict:
        """Serialize patterns for output"""
        
        serialized = {}
        
        for pattern_type, pattern_list in patterns.items():
            serialized[pattern_type] = []
            
            for pattern in pattern_list[:3]:  # Limit to 3 per type
                serialized[pattern_type].append({
                    'type': str(pattern.pattern_type),
                    'strength': pattern.strength,
                    'stability': pattern.stability,
                    'n_fragments': len(pattern.fragments),
                    'central_insight': pattern.central_insight
                })
        
        return serialized
    
    def _serialize_insight(self, insight: CrystallizedInsight) -> Dict:
        """Serialize insight for output"""
        
        return {
            'core_pattern': insight.core_pattern,
            'confidence': insight.confidence,
            'novelty': insight.novelty,
            'variations': insight.variations[:3] if insight.variations else [],
            'implications': insight.implications[:3] if insight.implications else [],
            'has_contradictions': bool(insight.contradictions)
        }
    
    def _update_config(self, base: Dict, update: Dict):
        """Recursively update configuration"""
        
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._update_config(base[key], value)
            else:
                base[key] = value
    
    async def analyze_reasoning_history(self) -> Dict:
        """Analyze patterns across reasoning history"""
        
        if not self.reasoning_history:
            return {'message': 'No reasoning history available'}
        
        analysis = {
            'total_sessions': len(self.reasoning_history),
            'avg_duration': sum(s['duration'] for s in self.reasoning_history) / len(self.reasoning_history),
            'total_patterns_detected': sum(
                s['phases']['detection']['total_patterns'] 
                for s in self.reasoning_history
            ),
            'pattern_type_frequency': {},
            'avg_insights_per_query': sum(
                s['phases']['crystallization']['n_insights'] 
                for s in self.reasoning_history
            ) / len(self.reasoning_history)
        }
        
        # Analyze pattern types
        for session in self.reasoning_history:
            for pattern_type, count in session['phases']['detection']['pattern_counts'].items():
                if pattern_type not in analysis['pattern_type_frequency']:
                    analysis['pattern_type_frequency'][pattern_type] = 0
                analysis['pattern_type_frequency'][pattern_type] += count
        
        return analysis
    
    def get_session_details(self, session_id: str) -> Optional[Dict]:
        """Get details of a specific reasoning session"""
        
        for session in self.reasoning_history:
            if session['id'] == session_id:
                return session
        return None
    
    def clear_history(self):
        """Clear reasoning history"""
        
        self.reasoning_history = []
        self.current_session = None
