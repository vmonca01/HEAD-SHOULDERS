"""
Pattern Recognition Module for Trading Bot
Identifies classic trading patterns in price data
"""

import numpy as np
import pandas as pd
from scipy.signal import argrelextrema, find_peaks
from typing import Dict, List, Tuple, Optional
from enum import Enum


class PatternType(Enum):
    """Enumeration of supported pattern types"""
    HEAD_SHOULDERS = "Head and Shoulders"
    INVERSE_HEAD_SHOULDERS = "Inverse Head and Shoulders"
    DOUBLE_TOP = "Double Top"
    DOUBLE_BOTTOM = "Double Bottom"
    RISING_WEDGE = "Rising Wedge"
    FALLING_WEDGE = "Falling Wedge"
    ASCENDING_TRIANGLE = "Ascending Triangle"
    DESCENDING_TRIANGLE = "Descending Triangle"
    SYMMETRICAL_TRIANGLE = "Symmetrical Triangle"


class PatternRecognizer:
    """
    Main class for recognizing trading patterns in price data
    """
    
    def __init__(self, min_confidence: float = 0.7):
        """
        Initialize the pattern recognizer
        
        Args:
            min_confidence: Minimum confidence level for pattern detection (0-1)
        """
        self.min_confidence = min_confidence
        self.patterns_found = []
    
    def analyze(self, df: pd.DataFrame) -> List[Dict]:
        """
        Analyze price data and detect all patterns
        
        Args:
            df: DataFrame with OHLCV data (columns: open, high, low, close, volume)
        
        Returns:
            List of detected patterns with metadata
        """
        self.patterns_found = []
        
        # Detect all pattern types
        self._detect_head_shoulders(df)
        self._detect_inverse_head_shoulders(df)
        self._detect_double_top(df)
        self._detect_double_bottom(df)
        self._detect_rising_wedge(df)
        self._detect_falling_wedge(df)
        self._detect_triangles(df)
        
        # Filter by confidence
        self.patterns_found = [
            p for p in self.patterns_found 
            if p['confidence'] >= self.min_confidence
        ]
        
        return self.patterns_found
    
    def _find_peaks_and_troughs(self, prices: np.ndarray, order: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Find local maxima (peaks) and minima (troughs) in price data
        
        Args:
            prices: Array of price values
            order: How many points on each side to use for comparison
        
        Returns:
            Tuple of (peak_indices, trough_indices)
        """
        # Find peaks (local maxima)
        peaks = argrelextrema(prices, np.greater, order=order)[0]
        
        # Find troughs (local minima)
        troughs = argrelextrema(prices, np.less, order=order)[0]
        
        return peaks, troughs
    
    def _detect_head_shoulders(self, df: pd.DataFrame) -> None:
        """
        Detect Head and Shoulders pattern (bearish reversal)
        Pattern: Left Shoulder - Head - Right Shoulder
        """
        prices = df['high'].values
        peaks, _ = self._find_peaks_and_troughs(prices, order=5)
        
        if len(peaks) < 3:
            return
        
        # Look for potential head and shoulders patterns
        for i in range(len(peaks) - 2):
            left_shoulder_idx = peaks[i]
            head_idx = peaks[i + 1]
            right_shoulder_idx = peaks[i + 2]
            
            left_shoulder = prices[left_shoulder_idx]
            head = prices[head_idx]
            right_shoulder = prices[right_shoulder_idx]
            
            # Head should be higher than shoulders
            if head > left_shoulder and head > right_shoulder:
                # Shoulders should be relatively equal (within 5% tolerance)
                shoulder_diff = abs(left_shoulder - right_shoulder) / left_shoulder
                
                if shoulder_diff < 0.05:
                    # Find neckline (support level between shoulders)
                    neckline_start_idx = left_shoulder_idx
                    neckline_end_idx = right_shoulder_idx
                    neckline_prices = df['low'].values[neckline_start_idx:neckline_end_idx]
                    neckline_level = np.mean(neckline_prices)
                    
                    # Calculate confidence based on pattern characteristics
                    head_prominence = (head - max(left_shoulder, right_shoulder)) / head
                    confidence = min(0.9, 0.6 + head_prominence * 2)
                    
                    if confidence >= self.min_confidence:
                        pattern = {
                            'type': PatternType.HEAD_SHOULDERS.value,
                            'confidence': confidence,
                            'direction': 'bearish',
                            'indices': {
                                'left_shoulder': int(left_shoulder_idx),
                                'head': int(head_idx),
                                'right_shoulder': int(right_shoulder_idx)
                            },
                            'prices': {
                                'left_shoulder': float(left_shoulder),
                                'head': float(head),
                                'right_shoulder': float(right_shoulder),
                                'neckline': float(neckline_level)
                            },
                            'target': float(neckline_level - (head - neckline_level))
                        }
                        self.patterns_found.append(pattern)
    
    def _detect_inverse_head_shoulders(self, df: pd.DataFrame) -> None:
        """
        Detect Inverse Head and Shoulders pattern (bullish reversal)
        Pattern: Left Shoulder - Head - Right Shoulder (inverted)
        """
        prices = df['low'].values
        _, troughs = self._find_peaks_and_troughs(prices, order=5)
        
        if len(troughs) < 3:
            return
        
        # Look for potential inverse head and shoulders patterns
        for i in range(len(troughs) - 2):
            left_shoulder_idx = troughs[i]
            head_idx = troughs[i + 1]
            right_shoulder_idx = troughs[i + 2]
            
            left_shoulder = prices[left_shoulder_idx]
            head = prices[head_idx]
            right_shoulder = prices[right_shoulder_idx]
            
            # Head should be lower than shoulders
            if head < left_shoulder and head < right_shoulder:
                # Shoulders should be relatively equal (within 5% tolerance)
                shoulder_diff = abs(left_shoulder - right_shoulder) / left_shoulder
                
                if shoulder_diff < 0.05:
                    # Find neckline (resistance level between shoulders)
                    neckline_start_idx = left_shoulder_idx
                    neckline_end_idx = right_shoulder_idx
                    neckline_prices = df['high'].values[neckline_start_idx:neckline_end_idx]
                    neckline_level = np.mean(neckline_prices)
                    
                    # Calculate confidence
                    head_prominence = (min(left_shoulder, right_shoulder) - head) / head
                    confidence = min(0.9, 0.6 + head_prominence * 2)
                    
                    if confidence >= self.min_confidence:
                        pattern = {
                            'type': PatternType.INVERSE_HEAD_SHOULDERS.value,
                            'confidence': confidence,
                            'direction': 'bullish',
                            'indices': {
                                'left_shoulder': int(left_shoulder_idx),
                                'head': int(head_idx),
                                'right_shoulder': int(right_shoulder_idx)
                            },
                            'prices': {
                                'left_shoulder': float(left_shoulder),
                                'head': float(head),
                                'right_shoulder': float(right_shoulder),
                                'neckline': float(neckline_level)
                            },
                            'target': float(neckline_level + (neckline_level - head))
                        }
                        self.patterns_found.append(pattern)
    
    def _detect_double_top(self, df: pd.DataFrame) -> None:
        """
        Detect Double Top pattern (bearish reversal)
        Two peaks at approximately the same level
        """
        prices = df['high'].values
        peaks, _ = self._find_peaks_and_troughs(prices, order=5)
        
        if len(peaks) < 2:
            return
        
        # Look for two consecutive peaks at similar levels
        for i in range(len(peaks) - 1):
            first_peak_idx = peaks[i]
            second_peak_idx = peaks[i + 1]
            
            first_peak = prices[first_peak_idx]
            second_peak = prices[second_peak_idx]
            
            # Peaks should be within 2% of each other
            peak_diff = abs(first_peak - second_peak) / first_peak
            
            if peak_diff < 0.02:
                # Find the trough between the peaks
                between_prices = df['low'].values[first_peak_idx:second_peak_idx]
                if len(between_prices) > 0:
                    trough_level = np.min(between_prices)
                    
                    # Ensure there's a significant dip between peaks
                    dip_percentage = (min(first_peak, second_peak) - trough_level) / min(first_peak, second_peak)
                    
                    if dip_percentage > 0.03:  # At least 3% dip
                        confidence = min(0.9, 0.6 + (1 - peak_diff) * 0.3 + dip_percentage)
                        
                        if confidence >= self.min_confidence:
                            pattern = {
                                'type': PatternType.DOUBLE_TOP.value,
                                'confidence': confidence,
                                'direction': 'bearish',
                                'indices': {
                                    'first_peak': int(first_peak_idx),
                                    'second_peak': int(second_peak_idx)
                                },
                                'prices': {
                                    'first_peak': float(first_peak),
                                    'second_peak': float(second_peak),
                                    'support': float(trough_level)
                                },
                                'target': float(trough_level - (first_peak - trough_level))
                            }
                            self.patterns_found.append(pattern)
    
    def _detect_double_bottom(self, df: pd.DataFrame) -> None:
        """
        Detect Double Bottom pattern (bullish reversal)
        Two troughs at approximately the same level
        """
        prices = df['low'].values
        _, troughs = self._find_peaks_and_troughs(prices, order=5)
        
        if len(troughs) < 2:
            return
        
        # Look for two consecutive troughs at similar levels
        for i in range(len(troughs) - 1):
            first_trough_idx = troughs[i]
            second_trough_idx = troughs[i + 1]
            
            first_trough = prices[first_trough_idx]
            second_trough = prices[second_trough_idx]
            
            # Troughs should be within 2% of each other
            trough_diff = abs(first_trough - second_trough) / first_trough
            
            if trough_diff < 0.02:
                # Find the peak between the troughs
                between_prices = df['high'].values[first_trough_idx:second_trough_idx]
                if len(between_prices) > 0:
                    peak_level = np.max(between_prices)
                    
                    # Ensure there's a significant rise between troughs
                    rise_percentage = (peak_level - max(first_trough, second_trough)) / max(first_trough, second_trough)
                    
                    if rise_percentage > 0.03:  # At least 3% rise
                        confidence = min(0.9, 0.6 + (1 - trough_diff) * 0.3 + rise_percentage)
                        
                        if confidence >= self.min_confidence:
                            pattern = {
                                'type': PatternType.DOUBLE_BOTTOM.value,
                                'confidence': confidence,
                                'direction': 'bullish',
                                'indices': {
                                    'first_trough': int(first_trough_idx),
                                    'second_trough': int(second_trough_idx)
                                },
                                'prices': {
                                    'first_trough': float(first_trough),
                                    'second_trough': float(second_trough),
                                    'resistance': float(peak_level)
                                },
                                'target': float(peak_level + (peak_level - first_trough))
                            }
                            self.patterns_found.append(pattern)
    
    def _detect_rising_wedge(self, df: pd.DataFrame) -> None:
        """
        Detect Rising Wedge pattern (bearish)
        Higher highs and higher lows converging upward
        """
        prices_high = df['high'].values
        prices_low = df['low'].values
        
        # Need at least 20 candles to form a wedge
        if len(df) < 20:
            return
        
        # Look at recent data windows
        window_size = min(50, len(df))
        for start_idx in range(len(df) - window_size, max(0, len(df) - window_size - 20), -10):
            if start_idx < 0:
                break
                
            window_high = prices_high[start_idx:start_idx + window_size]
            window_low = prices_low[start_idx:start_idx + window_size]
            
            # Find peaks and troughs in window
            peaks, troughs = self._find_peaks_and_troughs(window_high, order=3)
            _, window_troughs = self._find_peaks_and_troughs(window_low, order=3)
            
            if len(peaks) >= 2 and len(window_troughs) >= 2:
                # Check if highs are rising
                recent_peaks = peaks[-2:]
                if window_high[recent_peaks[-1]] > window_high[recent_peaks[0]]:
                    # Check if lows are also rising
                    recent_troughs = window_troughs[-2:]
                    if window_low[recent_troughs[-1]] > window_low[recent_troughs[0]]:
                        # Calculate slopes
                        high_slope = (window_high[recent_peaks[-1]] - window_high[recent_peaks[0]]) / (recent_peaks[-1] - recent_peaks[0])
                        low_slope = (window_low[recent_troughs[-1]] - window_low[recent_troughs[0]]) / (recent_troughs[-1] - recent_troughs[0])
                        
                        # Check if lines are converging (low slope > high slope indicates convergence)
                        if low_slope > high_slope and low_slope > 0:
                            convergence_ratio = low_slope / high_slope if high_slope > 0 else 2.0
                            confidence = min(0.9, 0.65 + min(convergence_ratio * 0.1, 0.25))
                            
                            if confidence >= self.min_confidence:
                                pattern = {
                                    'type': PatternType.RISING_WEDGE.value,
                                    'confidence': confidence,
                                    'direction': 'bearish',
                                    'indices': {
                                        'start': int(start_idx),
                                        'end': int(start_idx + window_size - 1)
                                    },
                                    'prices': {
                                        'upper_line_start': float(window_high[recent_peaks[0]]),
                                        'upper_line_end': float(window_high[recent_peaks[-1]]),
                                        'lower_line_start': float(window_low[recent_troughs[0]]),
                                        'lower_line_end': float(window_low[recent_troughs[-1]])
                                    }
                                }
                                self.patterns_found.append(pattern)
                                break
    
    def _detect_falling_wedge(self, df: pd.DataFrame) -> None:
        """
        Detect Falling Wedge pattern (bullish)
        Lower highs and lower lows converging downward
        """
        prices_high = df['high'].values
        prices_low = df['low'].values
        
        # Need at least 20 candles to form a wedge
        if len(df) < 20:
            return
        
        # Look at recent data windows
        window_size = min(50, len(df))
        for start_idx in range(len(df) - window_size, max(0, len(df) - window_size - 20), -10):
            if start_idx < 0:
                break
                
            window_high = prices_high[start_idx:start_idx + window_size]
            window_low = prices_low[start_idx:start_idx + window_size]
            
            # Find peaks and troughs in window
            peaks, troughs = self._find_peaks_and_troughs(window_high, order=3)
            _, window_troughs = self._find_peaks_and_troughs(window_low, order=3)
            
            if len(peaks) >= 2 and len(window_troughs) >= 2:
                # Check if highs are falling
                recent_peaks = peaks[-2:]
                if window_high[recent_peaks[-1]] < window_high[recent_peaks[0]]:
                    # Check if lows are also falling
                    recent_troughs = window_troughs[-2:]
                    if window_low[recent_troughs[-1]] < window_low[recent_troughs[0]]:
                        # Calculate slopes (negative values expected)
                        high_slope = (window_high[recent_peaks[-1]] - window_high[recent_peaks[0]]) / (recent_peaks[-1] - recent_peaks[0])
                        low_slope = (window_low[recent_troughs[-1]] - window_low[recent_troughs[0]]) / (recent_troughs[-1] - recent_troughs[0])
                        
                        # Check if lines are converging (high slope > low slope for falling wedge)
                        if high_slope > low_slope and high_slope < 0:
                            convergence_ratio = abs(high_slope / low_slope) if low_slope < 0 else 2.0
                            confidence = min(0.9, 0.65 + min(convergence_ratio * 0.1, 0.25))
                            
                            if confidence >= self.min_confidence:
                                pattern = {
                                    'type': PatternType.FALLING_WEDGE.value,
                                    'confidence': confidence,
                                    'direction': 'bullish',
                                    'indices': {
                                        'start': int(start_idx),
                                        'end': int(start_idx + window_size - 1)
                                    },
                                    'prices': {
                                        'upper_line_start': float(window_high[recent_peaks[0]]),
                                        'upper_line_end': float(window_high[recent_peaks[-1]]),
                                        'lower_line_start': float(window_low[recent_troughs[0]]),
                                        'lower_line_end': float(window_low[recent_troughs[-1]])
                                    }
                                }
                                self.patterns_found.append(pattern)
                                break
    
    def _detect_triangles(self, df: pd.DataFrame) -> None:
        """
        Detect Triangle patterns (Ascending, Descending, Symmetrical)
        """
        prices_high = df['high'].values
        prices_low = df['low'].values
        
        # Need at least 20 candles to form a triangle
        if len(df) < 20:
            return
        
        # Look at recent data windows
        window_size = min(50, len(df))
        for start_idx in range(len(df) - window_size, max(0, len(df) - window_size - 20), -10):
            if start_idx < 0:
                break
                
            window_high = prices_high[start_idx:start_idx + window_size]
            window_low = prices_low[start_idx:start_idx + window_size]
            
            # Find peaks and troughs in window
            peaks, troughs = self._find_peaks_and_troughs(window_high, order=3)
            _, window_troughs = self._find_peaks_and_troughs(window_low, order=3)
            
            if len(peaks) >= 2 and len(window_troughs) >= 2:
                recent_peaks = peaks[-2:]
                recent_troughs = window_troughs[-2:]
                
                # Calculate slopes
                high_diff = window_high[recent_peaks[-1]] - window_high[recent_peaks[0]]
                low_diff = window_low[recent_troughs[-1]] - window_low[recent_troughs[0]]
                
                high_slope = high_diff / (recent_peaks[-1] - recent_peaks[0])
                low_slope = low_diff / (recent_troughs[-1] - recent_troughs[0])
                
                # Ascending Triangle: flat top, rising bottom
                if abs(high_diff) < window_high[recent_peaks[0]] * 0.02 and low_slope > 0:
                    confidence = min(0.9, 0.7 + min(low_slope / window_low[recent_troughs[0]] * 100, 0.2))
                    if confidence >= self.min_confidence:
                        pattern = {
                            'type': PatternType.ASCENDING_TRIANGLE.value,
                            'confidence': confidence,
                            'direction': 'bullish',
                            'indices': {
                                'start': int(start_idx),
                                'end': int(start_idx + window_size - 1)
                            },
                            'prices': {
                                'resistance': float(np.mean(window_high[recent_peaks])),
                                'support_start': float(window_low[recent_troughs[0]]),
                                'support_end': float(window_low[recent_troughs[-1]])
                            }
                        }
                        self.patterns_found.append(pattern)
                        break
                
                # Descending Triangle: falling top, flat bottom
                elif high_slope < 0 and abs(low_diff) < window_low[recent_troughs[0]] * 0.02:
                    confidence = min(0.9, 0.7 + min(abs(high_slope) / window_high[recent_peaks[0]] * 100, 0.2))
                    if confidence >= self.min_confidence:
                        pattern = {
                            'type': PatternType.DESCENDING_TRIANGLE.value,
                            'confidence': confidence,
                            'direction': 'bearish',
                            'indices': {
                                'start': int(start_idx),
                                'end': int(start_idx + window_size - 1)
                            },
                            'prices': {
                                'resistance_start': float(window_high[recent_peaks[0]]),
                                'resistance_end': float(window_high[recent_peaks[-1]]),
                                'support': float(np.mean(window_low[recent_troughs]))
                            }
                        }
                        self.patterns_found.append(pattern)
                        break
                
                # Symmetrical Triangle: converging lines
                elif high_slope < 0 and low_slope > 0:
                    convergence_quality = abs(high_slope) + low_slope
                    confidence = min(0.9, 0.65 + min(convergence_quality / window_high[recent_peaks[0]] * 50, 0.25))
                    if confidence >= self.min_confidence:
                        pattern = {
                            'type': PatternType.SYMMETRICAL_TRIANGLE.value,
                            'confidence': confidence,
                            'direction': 'neutral',
                            'indices': {
                                'start': int(start_idx),
                                'end': int(start_idx + window_size - 1)
                            },
                            'prices': {
                                'upper_line_start': float(window_high[recent_peaks[0]]),
                                'upper_line_end': float(window_high[recent_peaks[-1]]),
                                'lower_line_start': float(window_low[recent_troughs[0]]),
                                'lower_line_end': float(window_low[recent_troughs[-1]])
                            }
                        }
                        self.patterns_found.append(pattern)
                        break
    
    def get_latest_pattern(self) -> Optional[Dict]:
        """
        Get the most recent pattern with highest confidence
        
        Returns:
            Latest pattern dict or None if no patterns found
        """
        if not self.patterns_found:
            return None
        
        # Sort by confidence and return highest
        sorted_patterns = sorted(self.patterns_found, key=lambda x: x['confidence'], reverse=True)
        return sorted_patterns[0]
    
    def get_patterns_by_type(self, pattern_type: PatternType) -> List[Dict]:
        """
        Get all patterns of a specific type
        
        Args:
            pattern_type: The pattern type to filter by
        
        Returns:
            List of patterns matching the type
        """
        return [p for p in self.patterns_found if p['type'] == pattern_type.value]
