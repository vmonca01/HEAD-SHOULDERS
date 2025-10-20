"""
Test and Demo Script for Pattern Recognition
Demonstrates pattern detection without requiring Binance API
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pattern_recognition import PatternRecognizer, PatternType


def generate_sample_data(pattern_type: str = 'head_shoulders', periods: int = 100) -> pd.DataFrame:
    """
    Generate synthetic price data with specific patterns
    
    Args:
        pattern_type: Type of pattern to generate
        periods: Number of data points
    
    Returns:
        DataFrame with OHLCV data
    """
    np.random.seed(42)
    
    # Base price trend
    base_price = 50000
    timestamps = [datetime.now() - timedelta(hours=periods-i) for i in range(periods)]
    
    if pattern_type == 'head_shoulders':
        # Create head and shoulders pattern
        prices = []
        for i in range(periods):
            if i < 20:
                # Initial trend
                price = base_price + i * 100 + np.random.randn() * 50
            elif i < 30:
                # Left shoulder
                price = base_price + 2000 + (i - 20) * 150 + np.random.randn() * 50
            elif i < 40:
                # Dip after left shoulder
                price = base_price + 2000 - (i - 30) * 100 + np.random.randn() * 50
            elif i < 50:
                # Head (higher peak)
                price = base_price + 1000 + (i - 40) * 200 + np.random.randn() * 50
            elif i < 60:
                # Dip after head
                price = base_price + 2000 - (i - 50) * 100 + np.random.randn() * 50
            elif i < 70:
                # Right shoulder
                price = base_price + 1000 + (i - 60) * 150 + np.random.randn() * 50
            else:
                # Decline
                price = base_price + 2500 - (i - 70) * 80 + np.random.randn() * 50
            prices.append(max(price, base_price * 0.8))
    
    elif pattern_type == 'double_top':
        # Create double top pattern
        prices = []
        for i in range(periods):
            if i < 30:
                # Uptrend to first peak
                price = base_price + i * 80 + np.random.randn() * 50
            elif i < 45:
                # Decline from first peak
                price = base_price + 2400 - (i - 30) * 60 + np.random.randn() * 50
            elif i < 60:
                # Rise to second peak
                price = base_price + 1500 + (i - 45) * 80 + np.random.randn() * 50
            else:
                # Decline
                price = base_price + 2600 - (i - 60) * 70 + np.random.randn() * 50
            prices.append(max(price, base_price * 0.8))
    
    elif pattern_type == 'rising_wedge':
        # Create rising wedge pattern
        prices = []
        for i in range(periods):
            # Both highs and lows rise, but converge
            base_trend = base_price + i * 30
            amplitude = 500 - i * 3  # Decreasing amplitude
            price = base_trend + np.sin(i * 0.3) * amplitude + np.random.randn() * 30
            prices.append(max(price, base_price * 0.8))
    
    elif pattern_type == 'falling_wedge':
        # Create falling wedge pattern
        prices = []
        for i in range(periods):
            # Both highs and lows fall, but converge
            base_trend = base_price + 3000 - i * 25
            amplitude = 500 - i * 3  # Decreasing amplitude
            price = base_trend + np.sin(i * 0.3) * amplitude + np.random.randn() * 30
            prices.append(max(price, base_price * 0.8))
    
    else:
        # Random walk
        prices = [base_price]
        for i in range(1, periods):
            change = np.random.randn() * 100
            prices.append(max(prices[-1] + change, base_price * 0.5))
    
    # Create OHLC data from prices
    data = []
    for i, price in enumerate(prices):
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


def plot_pattern(df: pd.DataFrame, patterns: list, title: str = "Pattern Detection"):
    """
    Plot price data with detected patterns
    
    Args:
        df: DataFrame with OHLCV data
        patterns: List of detected patterns
        title: Plot title
    """
    plt.figure(figsize=(14, 8))
    
    # Plot price
    plt.plot(df.index, df['close'], 'b-', label='Close Price', linewidth=2)
    plt.plot(df.index, df['high'], 'g-', alpha=0.3, label='High', linewidth=1)
    plt.plot(df.index, df['low'], 'r-', alpha=0.3, label='Low', linewidth=1)
    
    # Plot patterns
    for pattern in patterns:
        pattern_type = pattern['type']
        indices = pattern.get('indices', {})
        
        if 'Head and Shoulders' in pattern_type or 'Double' in pattern_type:
            # Mark key points
            for key, idx in indices.items():
                if idx < len(df):
                    plt.scatter(idx, df.iloc[idx]['high'], s=200, marker='v', 
                              color='red', zorder=5, label=key if key == list(indices.keys())[0] else "")
        
        # Add pattern label
        if indices:
            mid_idx = sum(indices.values()) // len(indices)
            if mid_idx < len(df):
                plt.annotate(f"{pattern_type}\n({pattern['confidence']:.1%})",
                           xy=(mid_idx, df.iloc[mid_idx]['high']),
                           xytext=(mid_idx, df.iloc[mid_idx]['high'] * 1.05),
                           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7),
                           fontsize=10, ha='center')
    
    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel('Time Period', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.legend(loc='best')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    filename = f"pattern_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(filename, dpi=100)
    print(f"Plot saved as: {filename}")
    plt.close()


def test_pattern_recognition():
    """Test pattern recognition on different synthetic datasets"""
    print("\n" + "="*70)
    print("PATTERN RECOGNITION TEST SUITE")
    print("="*70)
    
    recognizer = PatternRecognizer(min_confidence=0.65)
    
    test_cases = [
        ('head_shoulders', 'Head and Shoulders Pattern'),
        ('double_top', 'Double Top Pattern'),
        ('rising_wedge', 'Rising Wedge Pattern'),
        ('falling_wedge', 'Falling Wedge Pattern'),
    ]
    
    for pattern_type, description in test_cases:
        print(f"\n{'-'*70}")
        print(f"Testing: {description}")
        print(f"{'-'*70}")
        
        # Generate sample data
        df = generate_sample_data(pattern_type=pattern_type, periods=100)
        print(f"Generated {len(df)} data points")
        print(f"Price range: ${df['close'].min():,.2f} - ${df['close'].max():,.2f}")
        
        # Analyze patterns
        patterns = recognizer.analyze(df)
        
        if patterns:
            print(f"\n✓ Detected {len(patterns)} pattern(s):")
            for i, p in enumerate(patterns, 1):
                print(f"\n  Pattern #{i}:")
                print(f"    Type: {p['type']}")
                print(f"    Confidence: {p['confidence']:.2%}")
                print(f"    Direction: {p['direction']}")
                if 'target' in p:
                    print(f"    Target Price: ${p['target']:,.2f}")
                if 'indices' in p:
                    print(f"    Key Points: {p['indices']}")
            
            # Plot the pattern
            plot_pattern(df, patterns, f"{description} Detection")
        else:
            print("\n✗ No patterns detected with sufficient confidence")
    
    print("\n" + "="*70)
    print("TEST SUITE COMPLETE")
    print("="*70 + "\n")


def demo_live_simulation():
    """Demonstrate pattern recognition in a simulated live environment"""
    print("\n" + "="*70)
    print("LIVE PATTERN RECOGNITION SIMULATION")
    print("="*70)
    
    recognizer = PatternRecognizer(min_confidence=0.70)
    
    # Generate realistic market data
    print("\nGenerating realistic market data...")
    df = generate_sample_data(pattern_type='head_shoulders', periods=150)
    
    # Simulate rolling analysis
    window_size = 100
    print(f"\nAnalyzing data with rolling window of {window_size} periods...")
    
    for i in range(window_size, len(df), 10):
        window_df = df.iloc[i-window_size:i].copy()
        window_df.reset_index(drop=True, inplace=True)
        
        patterns = recognizer.analyze(window_df)
        
        if patterns:
            current_price = window_df.iloc[-1]['close']
            print(f"\n{'='*70}")
            print(f"Time: Period {i} | Current Price: ${current_price:,.2f}")
            print(f"{'='*70}")
            
            best_pattern = max(patterns, key=lambda x: x['confidence'])
            print(f"Pattern Detected: {best_pattern['type']}")
            print(f"Confidence: {best_pattern['confidence']:.2%}")
            print(f"Direction: {best_pattern['direction']}")
            
            if best_pattern['direction'] == 'bullish':
                print("💹 SIGNAL: Consider LONG position")
            elif best_pattern['direction'] == 'bearish':
                print("📉 SIGNAL: Consider SHORT position")
            
            if 'target' in best_pattern:
                print(f"Target Price: ${best_pattern['target']:,.2f}")
                print(f"Potential Move: {((best_pattern['target'] / current_price - 1) * 100):+.2f}%")
    
    print("\n" + "="*70)
    print("SIMULATION COMPLETE")
    print("="*70 + "\n")


def main():
    """Main test function"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║        PATTERN RECOGNITION TEST & DEMONSTRATION           ║
    ║                                                           ║
    ║  This script tests pattern recognition algorithms         ║
    ║  without requiring Binance API credentials                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Run tests
    test_pattern_recognition()
    
    # Run live simulation
    demo_live_simulation()
    
    print("\n✓ All tests completed successfully!")
    print("\nNext steps:")
    print("  1. Copy .env.example to .env")
    print("  2. Add your Binance API credentials")
    print("  3. Run 'python trading_bot.py' to start live trading")
    print("\n⚠️  WARNING: Start with testnet mode (USE_TESTNET=True) before live trading!\n")


if __name__ == "__main__":
    main()
