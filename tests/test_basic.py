#!/usr/bin/env python3
"""
Basic tests for EPH-MCP
"""
import asyncio
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from eph_mcp.reasoning_engine import EPHReasoningEngine
from eph_mcp.server import EPHMCPServer, AnalyzePatternInput
from eph_mcp import ThoughtFragment, EmergentPattern, PatternType

class TestEPHBasics(unittest.TestCase):
    """Basic functionality tests"""
    
    def setUp(self):
        """Set up test environment"""
        self.engine = EPHReasoningEngine({
            'explosion': {'n_fragments': 10},
            'interaction': {'iterations': 5},
            'visualization': {'enabled': False}
        })
    
    def test_thought_fragment_creation(self):
        """Test creating thought fragments"""
        fragment = ThoughtFragment(
            content="Test thought",
            activation_energy=1.0
        )
        
        self.assertIsNotNone(fragment.id)
        self.assertEqual(fragment.content, "Test thought")
        self.assertEqual(fragment.activation_energy, 1.0)
    
    def test_pattern_creation(self):
        """Test creating patterns"""
        pattern = EmergentPattern(
            pattern_type=PatternType.EMERGENCE,
            central_insight="Test pattern"
        )
        
        self.assertIsNotNone(pattern.id)
        self.assertEqual(pattern.pattern_type, PatternType.EMERGENCE)
        self.assertEqual(pattern.central_insight, "Test pattern")
    
    def test_reasoning_engine_initialization(self):
        """Test engine initialization"""
        self.assertIsNotNone(self.engine)
        self.assertIsNotNone(self.engine.explosion)
        self.assertIsNotNone(self.engine.interaction)
        self.assertIsNotNone(self.engine.detector)
        self.assertIsNotNone(self.engine.crystallizer)
        self.assertIsNotNone(self.engine.weaver)

class TestAsyncReasoning(unittest.TestCase):
    """Test async reasoning operations"""
    
    def setUp(self):
        """Set up test environment"""
        self.engine = EPHReasoningEngine({
            'explosion': {'n_fragments': 5},
            'interaction': {'iterations': 3},
            'visualization': {'enabled': False}
        })
    
    def test_simple_reasoning(self):
        """Test simple reasoning query"""
        async def run_test():
            result = await self.engine.reason(
                "What is the nature of creativity?",
                return_intermediate=False
            )
            
            self.assertIsNotNone(result)
            self.assertIn('response', result)
            self.assertIn('session_id', result)
            self.assertIn('duration', result)
            self.assertIn('statistics', result)
            
            # Check statistics
            stats = result['statistics']
            self.assertIn('fragments', stats)
            self.assertIn('patterns', stats)
            self.assertIn('insights', stats)
            
            return result
        
        result = asyncio.run(run_test())
        print(f"\n✓ Reasoning completed in {result['duration']:.2f}s")
        print(f"  Response preview: {result['response'][:100]}...")
    
    def test_reasoning_with_intermediate(self):
        """Test reasoning with intermediate results"""
        async def run_test():
            result = await self.engine.reason(
                "How do patterns emerge?",
                return_intermediate=True
            )
            
            self.assertIn('intermediate', result)
            intermediate = result['intermediate']
            
            self.assertIn('fragments', intermediate)
            self.assertIn('field_state', intermediate)
            self.assertIn('patterns', intermediate)
            self.assertIn('insights', intermediate)
            
            return result
        
        result = asyncio.run(run_test())
        print("\n✓ Reasoning with intermediate data completed")
        print(f"  Generated {len(result['intermediate']['fragments'])} fragment samples")

    def test_reasoning_config_override(self):
        """Ensure per-request configuration overrides are respected"""

        async def run_test():
            result = await self.engine.reason(
                "How do overrides change reasoning?",
                config_overrides={'explosion': {'n_fragments': 3}},
                return_intermediate=False
            )

            self.assertIn('session_id', result)
            session = self.engine.reasoning_history[-1]

            self.assertEqual(session['config']['explosion']['n_fragments'], 3)
            self.assertEqual(session['phases']['explosion']['n_fragments'], 3)
            self.assertEqual(self.engine.config['explosion']['n_fragments'], 5)

            return result

        asyncio.run(run_test())

    def test_error_handling(self):
        """Test error handling in reasoning"""
        async def run_test():
            # Create engine with invalid config to trigger controlled error
            engine = EPHReasoningEngine({
                'explosion': {'n_fragments': 0},  # Invalid: 0 fragments
                'visualization': {'enabled': False}
            })
            
            result = await engine.reason("Test query")
            
            # Should still return a result, even with error
            self.assertIsNotNone(result)
            self.assertIn('response', result)
            
            return result
        
        asyncio.run(run_test())
        print("\n✓ Error handling test completed")

class TestPhases(unittest.TestCase):
    """Test individual phases"""

    def setUp(self):
        """Set up test environment"""
        self.engine = EPHReasoningEngine({
            'explosion': {'n_fragments': 5},
            'visualization': {'enabled': False}
        })
    
    def test_explosion_phase(self):
        """Test thought explosion phase"""
        async def run_test():
            fragments = await self.engine.explosion.explode(
                "Test query for explosion",
                n=5
            )
            
            self.assertEqual(len(fragments), 5)
            
            for fragment in fragments:
                self.assertIsNotNone(fragment.content)
                self.assertIsNotNone(fragment.embedding)
                self.assertIsNotNone(fragment.generation_strategy)
            
            return fragments
        
        fragments = asyncio.run(run_test())
        print(f"\n✓ Explosion phase: Generated {len(fragments)} fragments")
        
        # Show strategies used
        strategies = set(f.generation_strategy for f in fragments)
        print(f"  Strategies used: {', '.join(strategies)}")
    
    def test_interaction_phase(self):
        """Test interaction dynamics phase"""
        async def run_test():
            # First get some fragments
            fragments = await self.engine.explosion.explode(
                "Order and chaos",
                n=3
            )
            
            # Run interaction simulation
            field = await self.engine.interaction.simulate(
                fragments,
                iterations=5
            )
            
            self.assertIsNotNone(field)
            self.assertGreater(len(field.fragments), 0)
            
            # Check field state
            state = field.get_state()
            self.assertIn('entropy', state)
            self.assertIn('temperature', state)
            self.assertIn('num_fragments', state)
            
            return field
        
        field = asyncio.run(run_test())
        state = field.get_state()
        print("\n✓ Interaction phase completed")
        print(f"  Field entropy: {state['entropy']:.2f}")
        print(f"  Bonds formed: {state['num_bonds']}")


class TestServerUtilities(unittest.TestCase):
    """Server level utilities"""

    @classmethod
    def setUpClass(cls):
        cls.server = EPHMCPServer({
            'explosion': {'n_fragments': 5},
            'interaction': {'iterations': 3},
            'visualization': {'enabled': False}
        })

    def test_analyze_patterns_filter(self):
        """Verify pattern type filtering in analyze_patterns"""

        async def run_test():
            input_model = AnalyzePatternInput(
                text=(
                    "Collaboration improves outcomes. "
                    "Collaboration does not improve outcomes. "
                    "Collaboration improves teamwork. "
                    "Collaboration improves trust."
                ),
                pattern_types=["contradiction"],
                min_confidence=0.6
            )

            response = await self.server.analyze_patterns(input_model)
            self.assertTrue(response)

            texts = [item.text for item in response if hasattr(item, 'text')]
            combined = "\n".join(texts)
            self.assertIn("Contradiction", combined)
            self.assertNotIn("Repetition", combined)

        asyncio.run(run_test())

def main():
    """Run tests"""
    print("\n" + "=" * 60)
    print("EPH-MCP BASIC TESTS")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEPHBasics))
    suite.addTests(loader.loadTestsFromTestCase(TestAsyncReasoning))
    suite.addTests(loader.loadTestsFromTestCase(TestPhases))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print(" ALL TESTS PASSED!")
    else:
        print(f" {len(result.failures)} tests failed")
        print(f" {len(result.errors)} tests had errors")
    print("=" * 60)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(main())
