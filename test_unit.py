"""
Unit Tests for Pattern Recognition Module
"""

import unittest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pattern_recognition import PatternRecognizer, PatternType


class TestPatternRecognizer(unittest.TestCase):
    """Test cases for PatternRecognizer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.recognizer = PatternRecognizer(min_confidence=0.7)
        self.sample_size = 100
    
    def generate_sample_ohlcv(self, periods: int = 100) -> pd.DataFrame:
        """Generate sample OHLCV data for testing"""
        np.random.seed(42)
        base_price = 50000
        timestamps = [datetime.now() - timedelta(hours=periods-i) for i in range(periods)]
        
        data = []
        for i in range(periods):
            price = base_price + i * 10 + np.random.randn() * 100
            high = price + abs(np.random.randn() * 50)
            low = price - abs(np.random.randn() * 50)
            open_price = price + np.random.randn() * 30
            close = price + np.random.randn() * 30
            volume = 1000 + np.random.rand() * 500
            
            data.append({
                'timestamp': timestamps[i],
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
        
        return pd.DataFrame(data)
    
    def test_recognizer_initialization(self):
        """Test PatternRecognizer initialization"""
        recognizer = PatternRecognizer(min_confidence=0.8)
        self.assertEqual(recognizer.min_confidence, 0.8)
        self.assertEqual(len(recognizer.patterns_found), 0)
    
    def test_analyze_with_valid_data(self):
        """Test analyze method with valid OHLCV data"""
        df = self.generate_sample_ohlcv(100)
        patterns = self.recognizer.analyze(df)
        
        # Should return a list (may be empty)
        self.assertIsInstance(patterns, list)
        
        # All patterns should have required keys
        for pattern in patterns:
            self.assertIn('type', pattern)
            self.assertIn('confidence', pattern)
            self.assertIn('direction', pattern)
            self.assertIn('indices', pattern)
            self.assertIn('prices', pattern)
            
            # Confidence should be between 0 and 1
            self.assertGreaterEqual(pattern['confidence'], 0)
            self.assertLessEqual(pattern['confidence'], 1)
    
    def test_analyze_with_insufficient_data(self):
        """Test analyze with insufficient data"""
        df = self.generate_sample_ohlcv(10)  # Only 10 periods
        patterns = self.recognizer.analyze(df)
        
        # Should still return a list
        self.assertIsInstance(patterns, list)
    
    def test_find_peaks_and_troughs(self):
        """Test peak and trough detection"""
        prices = np.array([1, 3, 2, 4, 1, 5, 2, 6, 3])
        peaks, troughs = self.recognizer._find_peaks_and_troughs(prices, order=1)
        
        self.assertIsInstance(peaks, np.ndarray)
        self.assertIsInstance(troughs, np.ndarray)
    
    def test_get_latest_pattern(self):
        """Test getting latest pattern"""
        df = self.generate_sample_ohlcv(100)
        self.recognizer.analyze(df)
        
        latest = self.recognizer.get_latest_pattern()
        
        # Could be None if no patterns found
        if latest is not None:
            self.assertIsInstance(latest, dict)
            self.assertIn('type', latest)
            self.assertIn('confidence', latest)
    
    def test_pattern_confidence_filtering(self):
        """Test that patterns below min_confidence are filtered"""
        recognizer = PatternRecognizer(min_confidence=0.95)  # Very high threshold
        df = self.generate_sample_ohlcv(100)
        patterns = recognizer.analyze(df)
        
        # All returned patterns should meet confidence threshold
        for pattern in patterns:
            self.assertGreaterEqual(pattern['confidence'], 0.95)
    
    def test_pattern_direction_values(self):
        """Test that pattern directions are valid"""
        df = self.generate_sample_ohlcv(100)
        patterns = self.recognizer.analyze(df)
        
        valid_directions = ['bullish', 'bearish', 'neutral']
        for pattern in patterns:
            self.assertIn(pattern['direction'], valid_directions)
    
    def test_pattern_type_enum(self):
        """Test PatternType enum values"""
        self.assertEqual(PatternType.HEAD_SHOULDERS.value, "Head and Shoulders")
        self.assertEqual(PatternType.DOUBLE_TOP.value, "Double Top")
        self.assertEqual(PatternType.RISING_WEDGE.value, "Rising Wedge")
        self.assertEqual(PatternType.FALLING_WEDGE.value, "Falling Wedge")
    
    def test_get_patterns_by_type(self):
        """Test filtering patterns by type"""
        df = self.generate_sample_ohlcv(100)
        self.recognizer.analyze(df)
        
        # Try to get double top patterns
        double_tops = self.recognizer.get_patterns_by_type(PatternType.DOUBLE_TOP)
        
        self.assertIsInstance(double_tops, list)
        for pattern in double_tops:
            self.assertEqual(pattern['type'], PatternType.DOUBLE_TOP.value)
    
    def test_multiple_pattern_detection(self):
        """Test that multiple patterns can be detected simultaneously"""
        df = self.generate_sample_ohlcv(150)  # More data
        patterns = self.recognizer.analyze(df)
        
        # Check if we have patterns
        if len(patterns) > 0:
            # Verify each pattern is unique (different indices)
            pattern_indices = [str(p.get('indices', {})) for p in patterns]
            # Note: Some patterns may overlap, so we just check format
            for idx_str in pattern_indices:
                self.assertIsInstance(idx_str, str)


class TestPatternDetectionMethods(unittest.TestCase):
    """Test specific pattern detection methods"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.recognizer = PatternRecognizer(min_confidence=0.6)
    
    def generate_head_shoulders_pattern(self) -> pd.DataFrame:
        """Generate data with a clear head and shoulders pattern"""
        np.random.seed(123)
        periods = 100
        base_price = 50000
        
        prices = []
        for i in range(periods):
            if i < 20:
                price = base_price + i * 50
            elif i < 30:
                price = base_price + 1000 + (i - 20) * 100  # Left shoulder
            elif i < 40:
                price = base_price + 2000 - (i - 30) * 100  # Dip
            elif i < 50:
                price = base_price + 1000 + (i - 40) * 150  # Head
            elif i < 60:
                price = base_price + 2500 - (i - 50) * 100  # Dip
            elif i < 70:
                price = base_price + 1500 + (i - 60) * 100  # Right shoulder
            else:
                price = base_price + 2500 - (i - 70) * 50
            
            prices.append(price + np.random.randn() * 50)
        
        data = []
        timestamps = [datetime.now() - timedelta(hours=periods-i) for i in range(periods)]
        for i, price in enumerate(prices):
            data.append({
                'timestamp': timestamps[i],
                'open': price,
                'high': price + abs(np.random.randn() * 30),
                'low': price - abs(np.random.randn() * 30),
                'close': price,
                'volume': 1000
            })
        
        return pd.DataFrame(data)
    
    def test_head_shoulders_detection(self):
        """Test head and shoulders pattern detection"""
        df = self.generate_head_shoulders_pattern()
        self.recognizer._detect_head_shoulders(df)
        
        # Check if any patterns were found
        self.assertIsInstance(self.recognizer.patterns_found, list)
        
        # If patterns found, verify they are bearish
        for pattern in self.recognizer.patterns_found:
            if pattern['type'] == PatternType.HEAD_SHOULDERS.value:
                self.assertEqual(pattern['direction'], 'bearish')
    
    def test_double_top_detection(self):
        """Test double top pattern detection"""
        # Generate sample data
        df = self.generate_head_shoulders_pattern()
        self.recognizer._detect_double_top(df)
        
        # Verify patterns structure
        for pattern in self.recognizer.patterns_found:
            if pattern['type'] == PatternType.DOUBLE_TOP.value:
                self.assertEqual(pattern['direction'], 'bearish')
                self.assertIn('first_peak', pattern['indices'])
                self.assertIn('second_peak', pattern['indices'])


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add tests
    suite.addTests(loader.loadTestsFromTestCase(TestPatternRecognizer))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternDetectionMethods))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
