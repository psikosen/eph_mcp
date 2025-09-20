# 🕸️ EPH-MCP: Emergent Pattern Hunter

**A revolutionary thinking architecture for LLMs via MCP (Model Context Protocol)**

EPH-MCP transforms how AI systems reason by simulating the emergence of insights from interacting thought fragments, similar to how patterns arise in complex physical systems.

## Key Features

- **Bottom-up Insight Emergence**: Instead of forcing conclusions, the insights just show up once all the pieces bounce around enough.  
- **Quantum-like Thought Dynamics**: Ideas overlap, collide, and stick together—sometimes they’re in two states at once until the picture clears.  
- **Multi-scale Pattern Detection**: We can spot the small stuff and the big picture at the same time—like zooming from street level to skyline.  
- **Contradiction as Feature**: Tension isn’t a bug, it’s fuel. Conflicts push the thinking somewhere new.  
- **Field-based Reasoning**: Everything plays out in this high-dimensional “idea space,” where concepts pull, push, and interact like a living grid.  


## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/eph-mcp.git
cd eph-mcp

# Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Quick test
python quickstart.py
```

### Basic Usage
 
### Start MCP Server

```bash
python -m eph_mcp.server
```

The server will start on `localhost:3333` by default.

##  How It Works

EPH uses a 5-phase process:

### Phase 1: Thought Explosion
First we blow up the question into a bunch of little sparks—50 to 150 fragments, each one a different angle or half-formed idea.  
We mix in every trick we’ve got: free association, “what if” games, parallel universes, quantum superposition vibes.  
Each fragment lands in some wild high-dimensional space, like confetti drifting around a cosmic dance floor.  

### Phase 2: Interaction Dynamics
Now those fragments start bumping into each other like charged particles.  
- Similar ones pull together.  
- Opposites push apart.  
- Some bind tightly, others spin off.  

It’s basically like running a mini-universe simulation where ideas collide until the system chills into something stable (simulated annealing).  

### Phase 3: Pattern Detection
From the chaos, we spot emergent shapes—like finding constellations in the stars:  
- Crystalline lattices → clean, regular structures  
- Strange attractors → looping chaos  
- Phase transitions → that “sudden click” when ideas reorganize  
- Soliton waves → insights that keep traveling without losing shape  
- …plus more funky forms  

### Phase 4: Pattern Crystallization
Here, the raw patterns solidify into actual insights.  
We check each one for:  
- Confidence (does it hold up?)  
- Novelty (is it fresh?)  
- Clarity (can you actually explain it to a friend?)  

We don’t force everything to agree—contradictions are saved too, like tension in a good story.  

### Phase 5: Pattern Weaving
Finally, we stitch the insights together into something you can actually use.  
Different ways to weave:  
- Convergent synthesis → pull it all into one neat answer  
- Dialectical → thesis + antithesis → synthesis  
- Narrative threading → tell it like a story, connecting the dots naturally  


## 📊 Configuration

Create a `config.json` file to customize behavior:

```json
{
  "explosion": {
    "n_fragments": 100,
    "temperature": 1.5,
    "embedding_model": "all-MiniLM-L6-v2"
  },
  "interaction": {
    "iterations": 150,
    "initial_temperature": 1.0,
    "cooling_rate": 0.995
  },
  "detection": {
    "min_pattern_size": 3,
    "pattern_threshold": 0.5
  },
  "crystallization": {
    "confidence_threshold": 0.5,
    "novelty_threshold": 0.3
  },
  "weaving": {
    "max_insights": 5,
    "coherence_threshold": 0.6
  }
}
```

## 🛠️ MCP Tools

The server exposes 4 main tools via MCP:

### `think_emergently`
Main reasoning tool - applies full EPH process
```python
{
  "query": "Your question here",
  "return_intermediate": false,
  "visualize": true
}
```

### `analyze_patterns`
Analyze text for emergent patterns without full reasoning
```python
{
  "text": "Text to analyze",
  "pattern_types": ["contradiction", "harmony"],
  "min_confidence": 0.5
}
```

### `compare_thoughts`
Compare multiple ideas for relationships
```python
{
  "thoughts": ["idea 1", "idea 2", "idea 3"],
  "find_contradictions": true,
  "find_harmonies": true
}
```

### `reasoning_history`
Access and analyze past reasoning sessions
```python
{
  "last_n": 5,
  "analyze": true
}
``` 

Enable with `visualization.enabled: true` in config.

## Testing

Run the test suite:

```bash
# Basic tests
python tests/test_basic.py

# Full test suite (if available)
pytest tests/
```

## 📚 Examples

Explore different reasoning scenarios:

```bash
python examples/usage_examples.py
```  

##  Contributing

Contributions are welcome! Areas of interest:

- New generation strategies for thought explosion
- Alternative pattern detection algorithms
- Visualization improvements
- Performance optimization
- Integration with other MCP tools
 

## Acknowledgments

- Inspired by physics and emergent systems 

*"In the dance of fragments, meaning emerges"* - EPH Philosophy
