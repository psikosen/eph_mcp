"""
Visualization module for EPH reasoning process
Creates interactive visualizations of thought patterns
"""
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime

from . import ReasoningField, EmergentPattern, CrystallizedInsight, ThoughtFragment

class FieldVisualizer:
    """Visualizes the reasoning field and emergent patterns"""
    
    def __init__(self, output_dir: str = '/tmp/eph-mcp/visualizations'):
        """Initialize visualizer"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Color schemes for different pattern types
        self.pattern_colors = {
            'crystalline_lattices': '#4169E1',  # Royal Blue
            'strange_attractors': '#FF6347',     # Tomato
            'phase_transitions': '#FFD700',      # Gold
            'soliton_waves': '#00CED1',         # Dark Turquoise
            'interference_patterns': '#9370DB',  # Medium Purple
            'vortices': '#FF1493',               # Deep Pink
            'bridges': '#32CD32',                # Lime Green
            'harmonics': '#FF8C00',              # Dark Orange
            'fractals': '#8B008B',               # Dark Magenta
            'emergence': '#00FF00'               # Lime
        }
    
    async def visualize_field(self, field: ReasoningField) -> str:
        """Create 3D visualization of the reasoning field"""
        
        # Extract fragment positions
        fragments = list(field.fragments.values())
        
        if not fragments or fragments[0].position is None:
            return "No spatial data available for visualization"
        
        # Reduce dimensions for visualization (if needed)
        positions = np.array([f.position for f in fragments])
        
        if positions.shape[1] > 3:
            # Use PCA to reduce to 3D
            from sklearn.decomposition import PCA
            pca = PCA(n_components=3)
            positions = pca.fit_transform(positions)
        
        # Create 3D scatter plot
        fig = go.Figure()
        
        # Add fragments as points
        fig.add_trace(go.Scatter3d(
            x=positions[:, 0],
            y=positions[:, 1],
            z=positions[:, 2] if positions.shape[1] > 2 else np.zeros(len(positions)),
            mode='markers+text',
            marker=dict(
                size=[f.activation_energy * 5 for f in fragments],
                color=[f.coherence for f in fragments],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Coherence"),
                opacity=0.8
            ),
            text=[f.content[:20] for f in fragments],
            hovertemplate='%{text}<br>Activation: %{marker.size:.2f}<br>Coherence: %{marker.color:.2f}'
        ))
        
        # Add bonds as lines
        for bond in field.bonds[:100]:  # Limit bonds for clarity
            if bond.fragment_a in field.fragments and bond.fragment_b in field.fragments:
                frag_a = field.fragments[bond.fragment_a]
                frag_b = field.fragments[bond.fragment_b]
                
                if frag_a.position is not None and frag_b.position is not None:
                    # Get positions
                    idx_a = fragments.index(frag_a)
                    idx_b = fragments.index(frag_b)
                    
                    # Determine line color based on bond type
                    if bond.strength > 0:
                        line_color = 'rgba(0, 255, 0, 0.3)'  # Green for attractive
                    else:
                        line_color = 'rgba(255, 0, 0, 0.3)'  # Red for repulsive
                    
                    fig.add_trace(go.Scatter3d(
                        x=[positions[idx_a, 0], positions[idx_b, 0]],
                        y=[positions[idx_a, 1], positions[idx_b, 1]],
                        z=[positions[idx_a, 2] if positions.shape[1] > 2 else 0,
                           positions[idx_b, 2] if positions.shape[1] > 2 else 0],
                        mode='lines',
                        line=dict(color=line_color, width=abs(bond.strength) * 2),
                        showlegend=False,
                        hoverinfo='skip'
                    ))
        
        # Update layout
        fig.update_layout(
            title=f'Reasoning Field - {len(fragments)} Fragments, {len(field.bonds)} Bonds',
            scene=dict(
                xaxis_title='Dimension 1',
                yaxis_title='Dimension 2',
                zaxis_title='Dimension 3'
            ),
            width=1000,
            height=800
        )
        
        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f'field_{timestamp}.html')
        fig.write_html(filepath)
        
        return filepath
    
    async def visualize_patterns(self, patterns: Dict[str, List[EmergentPattern]], 
                                field: ReasoningField) -> str:
        """Visualize detected patterns"""
        
        # Create subplots for different pattern types
        n_pattern_types = len([k for k, v in patterns.items() if v])
        
        if n_pattern_types == 0:
            return "No patterns to visualize"
        
        # Create network graph of patterns
        G = nx.Graph()
        
        # Add nodes for each pattern
        pattern_nodes = []
        pattern_labels = {}
        pattern_node_colors = []
        
        for pattern_type, pattern_list in patterns.items():
            for i, pattern in enumerate(pattern_list):
                node_id = f"{pattern_type}_{i}"
                G.add_node(node_id)
                pattern_nodes.append(node_id)
                pattern_labels[node_id] = f"{pattern_type[:10]}\n{pattern.strength:.2f}"
                pattern_node_colors.append(self.pattern_colors.get(pattern_type, '#808080'))
                
                # Add edges between patterns that share fragments
                for other_type, other_list in patterns.items():
                    for j, other_pattern in enumerate(other_list):
                        if pattern != other_pattern:
                            shared = set(pattern.fragments) & set(other_pattern.fragments)
                            if shared:
                                other_id = f"{other_type}_{j}"
                                G.add_edge(node_id, other_id, weight=len(shared))
        
        if not G.nodes():
            return "No pattern connections to visualize"
        
        # Calculate layout
        pos = nx.spring_layout(G, k=2, iterations=50)
        
        # Create plotly figure
        fig = go.Figure()
        
        # Add edges
        edge_traces = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=G[edge[0]][edge[1]]['weight'] * 0.5, color='#888'),
                hoverinfo='none'
            )
            edge_traces.append(edge_trace)
        
        for trace in edge_traces:
            fig.add_trace(trace)
        
        # Add nodes
        node_x = []
        node_y = []
        node_text = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(pattern_labels[node])
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=node_text,
            textposition='top center',
            marker=dict(
                color=pattern_node_colors,
                size=20,
                line=dict(color='white', width=2)
            ),
            hoverinfo='text'
        )
        
        fig.add_trace(node_trace)
        
        # Update layout
        fig.update_layout(
            title='Pattern Network',
            showlegend=False,
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            width=1000,
            height=800
        )
        
        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f'patterns_{timestamp}.html')
        fig.write_html(filepath)
        
        return filepath
    
    async def visualize_insights(self, insights: List[CrystallizedInsight]) -> str:
        """Visualize crystallized insights"""
        
        if not insights:
            return "No insights to visualize"
        
        # Create a radar chart of insight properties
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Insight Properties', 'Confidence vs Novelty',
                          'Insight Types', 'Quality Distribution'),
            specs=[[{'type': 'polar'}, {'type': 'scatter'}],
                  [{'type': 'bar'}, {'type': 'box'}]]
        )
        
        # Radar chart of properties
        for i, insight in enumerate(insights[:5]):  # Limit to 5
            fig.add_trace(
                go.Scatterpolar(
                    r=[insight.confidence, insight.novelty, insight.clarity,
                       len(insight.variations)/5, len(insight.implications)/5],
                    theta=['Confidence', 'Novelty', 'Clarity', 'Variations', 'Implications'],
                    fill='toself',
                    name=f'Insight {i+1}'
                ),
                row=1, col=1
            )
        
        # Scatter plot: Confidence vs Novelty
        fig.add_trace(
            go.Scatter(
                x=[i.confidence for i in insights],
                y=[i.novelty for i in insights],
                mode='markers+text',
                marker=dict(
                    size=[len(i.core_pattern) / 10 for i in insights],
                    color=[i.confidence * i.novelty for i in insights],
                    colorscale='Viridis',
                    showscale=True
                ),
                text=[f"I{j+1}" for j in range(len(insights))],
                hovertext=[i.core_pattern[:50] for i in insights]
            ),
            row=1, col=2
        )
        
        # Bar chart of insight types
        insight_types = {}
        for insight in insights:
            # Categorize by content
            if 'paradox' in insight.core_pattern.lower():
                type_name = 'Paradoxical'
            elif 'emergence' in insight.core_pattern.lower():
                type_name = 'Emergent'
            elif 'tension' in insight.core_pattern.lower():
                type_name = 'Tensional'
            elif 'resonance' in insight.core_pattern.lower():
                type_name = 'Resonant'
            else:
                type_name = 'Other'
            
            insight_types[type_name] = insight_types.get(type_name, 0) + 1
        
        fig.add_trace(
            go.Bar(
                x=list(insight_types.keys()),
                y=list(insight_types.values()),
                marker_color='lightblue'
            ),
            row=2, col=1
        )
        
        # Box plot of quality scores
        quality_scores = [i.confidence * 0.4 + i.novelty * 0.4 + i.clarity * 0.2 
                         for i in insights]
        
        fig.add_trace(
            go.Box(
                y=quality_scores,
                name='Quality',
                marker_color='lightgreen'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title='Insight Analysis',
            showlegend=True,
            width=1200,
            height=900
        )
        
        # Update axes
        fig.update_xaxes(title_text="Confidence", row=1, col=2)
        fig.update_yaxes(title_text="Novelty", row=1, col=2)
        fig.update_xaxes(title_text="Type", row=2, col=1)
        fig.update_yaxes(title_text="Count", row=2, col=1)
        fig.update_yaxes(title_text="Quality Score", row=2, col=2)
        
        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f'insights_{timestamp}.html')
        fig.write_html(filepath)
        
        return filepath
    
    async def generate_summary(self, field: ReasoningField, 
                              patterns: Dict[str, List[EmergentPattern]], 
                              insights: List[CrystallizedInsight],
                              session: Dict) -> str:
        """Generate summary visualization of entire reasoning process"""
        
        # Create multi-panel summary
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=(
                'Phase Timeline', 'Energy Evolution',
                'Pattern Distribution', 'Insight Quality',
                'Field Entropy', 'Fragment Coherence'
            ),
            specs=[[{'type': 'bar'}, {'type': 'scatter'}],
                  [{'type': 'pie'}, {'type': 'scatter'}],
                  [{'type': 'scatter'}, {'type': 'histogram'}]]
        )
        
        # Phase timeline
        phases = session.get('phases', {})
        phase_names = list(phases.keys())
        phase_durations = [phases[p].get('duration', 0) for p in phase_names]
        
        fig.add_trace(
            go.Bar(x=phase_names, y=phase_durations, name='Duration (s)'),
            row=1, col=1
        )
        
        # Energy evolution (if history available)
        if field.history:
            iterations = [h['iteration'] for h in field.history]
            total_energy = [h.get('total_energy', 0) for h in field.history]
            
            fig.add_trace(
                go.Scatter(x=iterations, y=total_energy, mode='lines', name='Total Energy'),
                row=1, col=2
            )
        
        # Pattern distribution
        pattern_counts = {}
        for pattern_type, pattern_list in patterns.items():
            if pattern_list:
                pattern_counts[pattern_type] = len(pattern_list)
        
        if pattern_counts:
            fig.add_trace(
                go.Pie(labels=list(pattern_counts.keys()), 
                      values=list(pattern_counts.values()),
                      hole=0.3),
                row=2, col=1
            )
        
        # Insight quality scatter
        if insights:
            fig.add_trace(
                go.Scatter(
                    x=list(range(len(insights))),
                    y=[i.confidence * i.novelty for i in insights],
                    mode='markers+lines',
                    name='Quality',
                    marker=dict(size=10)
                ),
                row=2, col=2
            )
        
        # Field entropy over time
        if field.history:
            fig.add_trace(
                go.Scatter(
                    x=iterations,
                    y=[h.get('entropy', 0) for h in field.history],
                    mode='lines',
                    name='Entropy'
                ),
                row=3, col=1
            )
        
        # Fragment coherence distribution
        coherences = [f.coherence for f in field.fragments.values()]
        
        fig.add_trace(
            go.Histogram(x=coherences, nbinsx=20, name='Coherence'),
            row=3, col=2
        )
        
        # Update layout
        fig.update_layout(
            title=f'EPH Reasoning Summary - "{session.get("query", "")[:50]}"',
            showlegend=False,
            width=1400,
            height=1000
        )
        
        # Save
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = os.path.join(self.output_dir, f'summary_{timestamp}.html')
        fig.write_html(filepath)
        
        # Also save as static image if possible
        try:
            fig.write_image(filepath.replace('.html', '.png'))
        except:
            pass  # Image export requires additional dependencies
        
        return filepath
    
    def generate_report(self, session: Dict) -> str:
        """Generate text report of reasoning session"""
        
        report = []
        report.append("=" * 80)
        report.append("EMERGENT PATTERN HUNTER - REASONING REPORT")
        report.append("=" * 80)
        report.append(f"\nQuery: {session.get('query', 'N/A')}")
        report.append(f"Session ID: {session.get('id', 'N/A')}")
        report.append(f"Duration: {session.get('duration', 0):.2f} seconds")
        report.append("\n" + "-" * 40)
        report.append("PHASE BREAKDOWN")
        report.append("-" * 40)
        
        phases = session.get('phases', {})
        
        for phase_name, phase_data in phases.items():
            report.append(f"\n{phase_name.upper()}:")
            report.append(f"  Duration: {phase_data.get('duration', 0):.3f}s")
            
            for key, value in phase_data.items():
                if key != 'duration':
                    report.append(f"  {key}: {value}")
        
        report.append("\n" + "-" * 40)
        report.append("PATTERN ANALYSIS")
        report.append("-" * 40)
        
        if 'detection' in phases:
            report.append(f"\nTotal patterns detected: {phases['detection'].get('total_patterns', 0)}")
            
            pattern_counts = phases['detection'].get('pattern_counts', {})
            if pattern_counts:
                report.append("\nPattern distribution:")
                for pattern_type, count in pattern_counts.items():
                    report.append(f"  {pattern_type}: {count}")
        
        report.append("\n" + "-" * 40)
        report.append("INSIGHT SYNTHESIS")
        report.append("-" * 40)
        
        if 'crystallization' in phases:
            report.append(f"\nInsights generated: {phases['crystallization'].get('n_insights', 0)}")
            report.append(f"Average confidence: {phases['crystallization'].get('avg_confidence', 0):.2%}")
            report.append(f"Average novelty: {phases['crystallization'].get('avg_novelty', 0):.2%}")
        
        report.append("\n" + "-" * 40)
        report.append("VISUALIZATION FILES")
        report.append("-" * 40)
        
        viz = session.get('visualizations', {})
        for viz_type, filepath in viz.items():
            report.append(f"\n{viz_type}: {filepath}")
        
        report.append("\n" + "=" * 80)
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = os.path.join(self.output_dir, f'report_{timestamp}.txt')
        
        with open(report_path, 'w') as f:
            f.write('\n'.join(report))
        
        return report_path
