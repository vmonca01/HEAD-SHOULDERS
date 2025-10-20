"""
Example Script: Using Pattern Recognition with Your Own Data
This shows how to integrate the pattern recognition module with your existing trading bot
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pattern_recognition import PatternRecognizer, PatternType


def example_with_custom_data():
    """Example: Using pattern recognition with your own price data"""
    print("="*70)
    print("EXAMPLE 1: Pattern Recognition with Custom Data")
    print("="*70)
    
    # Simulate fetching your own data (replace with your actual data source)
    # Your data should have columns: timestamp, open, high, low, close, volume
    
    # Example: Creating a DataFrame with your price data
    periods = 100
    timestamps = [datetime.now() - timedelta(hours=periods-i) for i in range(periods)]
    
    # Replace this with your actual price data from Binance or other source
    np.random.seed(42)
    base_price = 45000
    
    data = []
    for i in range(periods):
        # Example price movement
        price = base_price + i * 50 + np.random.randn() * 200
        
        data.append({
            'timestamp': timestamps[i],
            'open': price + np.random.randn() * 50,
            'high': price + abs(np.random.randn() * 100),
            'low': price - abs(np.random.randn() * 100),
            'close': price,
            'volume': 1000 + np.random.rand() * 500
        })
    
    df = pd.DataFrame(data)
    
    print(f"\nData loaded: {len(df)} candles")
    print(f"Price range: ${df['close'].min():,.2f} - ${df['close'].max():,.2f}")
    
    # Create pattern recognizer
    recognizer = PatternRecognizer(min_confidence=0.70)
    
    # Analyze patterns
    patterns = recognizer.analyze(df)
    
    # Display results
    if patterns:
        print(f"\n✓ Found {len(patterns)} pattern(s):")
        for i, pattern in enumerate(patterns, 1):
            print(f"\n  Pattern #{i}:")
            print(f"    Type: {pattern['type']}")
            print(f"    Confidence: {pattern['confidence']:.2%}")
            print(f"    Direction: {pattern['direction']}")
            
            if pattern['direction'] == 'bullish':
                print(f"    💹 SIGNAL: Consider LONG/BUY")
            elif pattern['direction'] == 'bearish':
                print(f"    📉 SIGNAL: Consider SHORT/SELL")
            
            if 'target' in pattern:
                current_price = df.iloc[-1]['close']
                print(f"    Target: ${pattern['target']:,.2f}")
                print(f"    Potential: {((pattern['target'] / current_price - 1) * 100):+.2f}%")
    else:
        print("\n✗ No significant patterns detected")
    
    print("\n" + "="*70)


def example_integration_with_binance():
    """Example: How to integrate with Binance API in your existing bot"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Integration Pattern for Your Existing Bot")
    print("="*70)
    
    print("""
    # In your existing trading bot, add pattern recognition:
    
    from pattern_recognition import PatternRecognizer, PatternType
    
    # Initialize once when bot starts
    pattern_recognizer = PatternRecognizer(min_confidence=0.70)
    
    # In your trading loop (where you already fetch data):
    def analyze_and_trade(symbol='BTCUSDT'):
        # 1. Fetch OHLCV data (you already do this)
        klines = client.get_klines(
            symbol=symbol,
            interval='1h',
            limit=100
        )
        
        # 2. Convert to DataFrame
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_volume', 'trades', 'taker_buy_base',
            'taker_buy_quote', 'ignore'
        ])
        
        # Convert types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = df[col].astype(float)
        
        # 3. Analyze patterns (NEW CODE)
        patterns = pattern_recognizer.analyze(df)
        
        # 4. Make trading decisions based on patterns
        if patterns:
            best_pattern = max(patterns, key=lambda x: x['confidence'])
            
            if best_pattern['confidence'] >= 0.75:
                print(f"High confidence pattern: {best_pattern['type']}")
                
                if best_pattern['direction'] == 'bullish':
                    # Your existing code to place BUY order
                    place_buy_order(symbol, quantity)
                    
                elif best_pattern['direction'] == 'bearish':
                    # Your existing code to place SELL order
                    place_sell_order(symbol, quantity)
    """)
    
    print("="*70)


def example_filtering_patterns():
    """Example: Filtering and selecting specific patterns"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Filtering Specific Patterns")
    print("="*70)
    
    # Create sample data
    periods = 100
    timestamps = [datetime.now() - timedelta(hours=periods-i) for i in range(periods)]
    np.random.seed(123)
    
    data = []
    for i in range(periods):
        price = 50000 + i * 30 + np.random.randn() * 200
        data.append({
            'timestamp': timestamps[i],
            'open': price,
            'high': price + abs(np.random.randn() * 100),
            'low': price - abs(np.random.randn() * 100),
            'close': price,
            'volume': 1000
        })
    
    df = pd.DataFrame(data)
    
    # Analyze
    recognizer = PatternRecognizer(min_confidence=0.65)
    patterns = recognizer.analyze(df)
    
    print(f"\nTotal patterns found: {len(patterns)}")
    
    # Filter only bullish patterns
    bullish_patterns = [p for p in patterns if p['direction'] == 'bullish']
    print(f"Bullish patterns: {len(bullish_patterns)}")
    
    # Filter only bearish patterns
    bearish_patterns = [p for p in patterns if p['direction'] == 'bearish']
    print(f"Bearish patterns: {len(bearish_patterns)}")
    
    # Filter by specific pattern type
    head_shoulders = recognizer.get_patterns_by_type(PatternType.HEAD_SHOULDERS)
    print(f"Head & Shoulders patterns: {len(head_shoulders)}")
    
    # Get highest confidence pattern
    if patterns:
        best = max(patterns, key=lambda x: x['confidence'])
        print(f"\nHighest confidence pattern:")
        print(f"  Type: {best['type']}")
        print(f"  Confidence: {best['confidence']:.2%}")
        print(f"  Direction: {best['direction']}")
    
    print("\n" + "="*70)


def example_risk_management():
    """Example: Using pattern targets for stop loss and take profit"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Risk Management with Pattern Targets")
    print("="*70)
    
    print("""
    # When a pattern is detected, use its target for risk management:
    
    def calculate_trade_levels(pattern, current_price):
        '''Calculate entry, stop loss, and take profit based on pattern'''
        
        direction = pattern['direction']
        confidence = pattern['confidence']
        pattern_target = pattern.get('target')
        
        if direction == 'bullish':
            # For bullish patterns
            entry = current_price
            
            # Stop loss: below recent support
            stop_loss = current_price * 0.98  # 2% below entry
            
            # Take profit: pattern target or risk-reward ratio
            if pattern_target:
                take_profit = pattern_target
            else:
                # Use 2:1 risk-reward ratio
                risk = entry - stop_loss
                take_profit = entry + (risk * 2)
            
            return {
                'side': 'BUY',
                'entry': entry,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk_reward_ratio': (take_profit - entry) / (entry - stop_loss)
            }
        
        elif direction == 'bearish':
            # For bearish patterns
            entry = current_price
            
            # Stop loss: above recent resistance
            stop_loss = current_price * 1.02  # 2% above entry
            
            # Take profit: pattern target or risk-reward ratio
            if pattern_target:
                take_profit = pattern_target
            else:
                # Use 2:1 risk-reward ratio
                risk = stop_loss - entry
                take_profit = entry - (risk * 2)
            
            return {
                'side': 'SELL',
                'entry': entry,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'risk_reward_ratio': (entry - take_profit) / (stop_loss - entry)
            }
        
        return None
    
    # Example usage:
    # pattern = recognizer.get_latest_pattern()
    # if pattern and pattern['confidence'] >= 0.75:
    #     levels = calculate_trade_levels(pattern, current_price)
    #     if levels:
    #         place_order(
    #             side=levels['side'],
    #             entry=levels['entry'],
    #             stop_loss=levels['stop_loss'],
    #             take_profit=levels['take_profit']
    #         )
    """)
    
    print("="*70)


def main():
    """Run all examples"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║          PATTERN RECOGNITION EXAMPLES                     ║
    ║                                                           ║
    ║  These examples show how to use the pattern recognition   ║
    ║  module in your trading bot                               ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Run examples
    example_with_custom_data()
    example_integration_with_binance()
    example_filtering_patterns()
    example_risk_management()
    
    print("\n" + "="*70)
    print("✓ All examples completed!")
    print("="*70)
    print("\nNext steps:")
    print("1. Review the examples above")
    print("2. Integrate pattern recognition into your existing bot")
    print("3. Test with small amounts first")
    print("4. Monitor and adjust confidence thresholds")
    print("\n")


if __name__ == "__main__":
    main()
