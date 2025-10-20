"""
Trading Bot with Pattern Recognition
Connects to Binance API and executes trades based on detected patterns
"""

import os
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

from pattern_recognition import PatternRecognizer, PatternType


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('trading_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TradingBot:
    """
    Main Trading Bot class with pattern recognition
    """
    
    def __init__(self):
        """Initialize the trading bot"""
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.use_testnet = os.getenv('USE_TESTNET', 'True').lower() == 'true'
        
        # Trading Configuration
        self.symbol = os.getenv('TRADING_SYMBOL', 'BTCUSDT')
        self.timeframe = os.getenv('TIMEFRAME', '1h')
        self.lookback_periods = int(os.getenv('LOOKBACK_PERIODS', '100'))
        
        # Risk Management
        self.max_trade_amount = float(os.getenv('MAX_TRADE_AMOUNT', '0.01'))
        self.stop_loss_pct = float(os.getenv('STOP_LOSS_PERCENTAGE', '2.0'))
        self.take_profit_pct = float(os.getenv('TAKE_PROFIT_PERCENTAGE', '5.0'))
        
        # Pattern Recognition
        min_confidence = float(os.getenv('MIN_PATTERN_CONFIDENCE', '0.7'))
        self.pattern_recognizer = PatternRecognizer(min_confidence=min_confidence)
        
        # Pattern enable flags
        self.enable_head_shoulders = os.getenv('ENABLE_HEAD_SHOULDERS', 'True').lower() == 'true'
        self.enable_double_patterns = os.getenv('ENABLE_DOUBLE_TOP_BOTTOM', 'True').lower() == 'true'
        self.enable_wedges = os.getenv('ENABLE_WEDGES', 'True').lower() == 'true'
        self.enable_triangles = os.getenv('ENABLE_TRIANGLES', 'True').lower() == 'true'
        
        # Initialize Binance client
        self.client = None
        self._initialize_client()
        
        # Active positions
        self.active_positions = []
        
        logger.info(f"Trading Bot initialized - Symbol: {self.symbol}, Timeframe: {self.timeframe}")
        logger.info(f"Mode: {'TESTNET' if self.use_testnet else 'REAL TRADING'}")
    
    def _initialize_client(self):
        """Initialize Binance API client"""
        try:
            if not self.api_key or not self.api_secret:
                logger.error("API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in .env file")
                return
            
            if self.use_testnet:
                self.client = Client(self.api_key, self.api_secret, testnet=True)
                logger.info("Connected to Binance Testnet")
            else:
                self.client = Client(self.api_key, self.api_secret)
                logger.info("Connected to Binance Production")
            
            # Test connection
            self.client.ping()
            logger.info("Binance API connection successful")
            
        except BinanceAPIException as e:
            logger.error(f"Failed to initialize Binance client: {e}")
            self.client = None
        except Exception as e:
            logger.error(f"Unexpected error initializing client: {e}")
            self.client = None
    
    def get_historical_data(self) -> Optional[pd.DataFrame]:
        """
        Fetch historical OHLCV data from Binance
        
        Returns:
            DataFrame with OHLCV data or None if error
        """
        try:
            if not self.client:
                logger.error("Binance client not initialized")
                return None
            
            # Get klines (candlestick data)
            klines = self.client.get_klines(
                symbol=self.symbol,
                interval=self.timeframe,
                limit=self.lookback_periods
            )
            
            # Convert to DataFrame
            df = pd.DataFrame(klines, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume',
                'close_time', 'quote_volume', 'trades', 'taker_buy_base',
                'taker_buy_quote', 'ignore'
            ])
            
            # Convert to appropriate types
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            for col in ['open', 'high', 'low', 'close', 'volume']:
                df[col] = df[col].astype(float)
            
            logger.info(f"Fetched {len(df)} candles for {self.symbol}")
            return df
            
        except BinanceAPIException as e:
            logger.error(f"Error fetching historical data: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching data: {e}")
            return None
    
    def analyze_patterns(self, df: pd.DataFrame) -> List[Dict]:
        """
        Analyze price data for patterns
        
        Args:
            df: DataFrame with OHLCV data
        
        Returns:
            List of detected patterns
        """
        if df is None or len(df) < 20:
            logger.warning("Insufficient data for pattern analysis")
            return []
        
        # Detect patterns
        patterns = self.pattern_recognizer.analyze(df)
        
        # Filter patterns based on enabled settings
        filtered_patterns = []
        for pattern in patterns:
            pattern_type = pattern['type']
            
            if (PatternType.HEAD_SHOULDERS.value in pattern_type or 
                PatternType.INVERSE_HEAD_SHOULDERS.value in pattern_type) and self.enable_head_shoulders:
                filtered_patterns.append(pattern)
            elif (PatternType.DOUBLE_TOP.value in pattern_type or 
                  PatternType.DOUBLE_BOTTOM.value in pattern_type) and self.enable_double_patterns:
                filtered_patterns.append(pattern)
            elif (PatternType.RISING_WEDGE.value in pattern_type or 
                  PatternType.FALLING_WEDGE.value in pattern_type) and self.enable_wedges:
                filtered_patterns.append(pattern)
            elif 'Triangle' in pattern_type and self.enable_triangles:
                filtered_patterns.append(pattern)
        
        if filtered_patterns:
            logger.info(f"Detected {len(filtered_patterns)} pattern(s):")
            for p in filtered_patterns:
                logger.info(f"  - {p['type']} (Confidence: {p['confidence']:.2%}, Direction: {p['direction']})")
        
        return filtered_patterns
    
    def get_current_price(self) -> Optional[float]:
        """
        Get current market price
        
        Returns:
            Current price or None if error
        """
        try:
            if not self.client:
                return None
            
            ticker = self.client.get_symbol_ticker(symbol=self.symbol)
            return float(ticker['price'])
            
        except Exception as e:
            logger.error(f"Error fetching current price: {e}")
            return None
    
    def calculate_position_size(self, current_price: float) -> float:
        """
        Calculate position size based on risk management rules
        
        Args:
            current_price: Current market price
        
        Returns:
            Position size in base currency
        """
        # Simple position sizing - can be made more sophisticated
        return self.max_trade_amount
    
    def place_order(self, side: str, quantity: float, stop_loss: float, take_profit: float) -> Optional[Dict]:
        """
        Place a market order with stop loss and take profit
        
        Args:
            side: 'BUY' or 'SELL'
            quantity: Amount to trade
            stop_loss: Stop loss price
            take_profit: Take profit price
        
        Returns:
            Order response or None if error
        """
        try:
            if not self.client:
                logger.error("Cannot place order: Binance client not initialized")
                return None
            
            logger.info(f"Placing {side} order for {quantity} {self.symbol}")
            logger.info(f"Stop Loss: {stop_loss}, Take Profit: {take_profit}")
            
            # Place market order
            order = self.client.create_order(
                symbol=self.symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            logger.info(f"Order placed successfully: {order['orderId']}")
            
            # Note: In production, you would also place OCO (One-Cancels-Other) orders
            # for stop loss and take profit. This is a simplified version.
            
            return order
            
        except BinanceAPIException as e:
            logger.error(f"Error placing order: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            return None
    
    def execute_trade_signal(self, pattern: Dict, current_price: float) -> bool:
        """
        Execute a trade based on pattern signal
        
        Args:
            pattern: Detected pattern with trading signal
            current_price: Current market price
        
        Returns:
            True if trade executed successfully
        """
        direction = pattern['direction']
        pattern_type = pattern['type']
        confidence = pattern['confidence']
        
        logger.info(f"Processing trade signal from {pattern_type} (Confidence: {confidence:.2%})")
        
        # Determine trade direction
        if direction == 'bullish':
            side = 'BUY'
            stop_loss = current_price * (1 - self.stop_loss_pct / 100)
            take_profit = current_price * (1 + self.take_profit_pct / 100)
        elif direction == 'bearish':
            side = 'SELL'
            stop_loss = current_price * (1 + self.stop_loss_pct / 100)
            take_profit = current_price * (1 - self.take_profit_pct / 100)
        else:
            logger.info(f"Pattern direction is neutral, no trade executed")
            return False
        
        # Calculate position size
        quantity = self.calculate_position_size(current_price)
        
        # Place order
        order = self.place_order(side, quantity, stop_loss, take_profit)
        
        if order:
            # Track position
            self.active_positions.append({
                'pattern': pattern_type,
                'side': side,
                'entry_price': current_price,
                'quantity': quantity,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'timestamp': datetime.now(),
                'order_id': order.get('orderId')
            })
            logger.info(f"Trade executed successfully - {side} {quantity} at {current_price}")
            return True
        
        return False
    
    def run(self, continuous: bool = False, interval: int = 300):
        """
        Run the trading bot
        
        Args:
            continuous: If True, run continuously
            interval: Sleep interval between iterations (seconds)
        """
        logger.info("Starting Trading Bot...")
        
        if not self.client:
            logger.error("Cannot start bot: Binance client not initialized")
            logger.error("Please check your API credentials in .env file")
            return
        
        iteration = 0
        
        try:
            while True:
                iteration += 1
                logger.info(f"\n{'='*60}")
                logger.info(f"Iteration #{iteration} - {datetime.now()}")
                logger.info(f"{'='*60}")
                
                # Fetch data
                df = self.get_historical_data()
                if df is None:
                    logger.warning("Failed to fetch data, skipping iteration")
                    if not continuous:
                        break
                    time.sleep(interval)
                    continue
                
                # Analyze patterns
                patterns = self.analyze_patterns(df)
                
                if patterns:
                    # Get current price
                    current_price = self.get_current_price()
                    if current_price:
                        logger.info(f"Current {self.symbol} price: ${current_price:,.2f}")
                        
                        # Get highest confidence pattern
                        best_pattern = max(patterns, key=lambda x: x['confidence'])
                        
                        logger.info(f"\nBest pattern: {best_pattern['type']}")
                        logger.info(f"Confidence: {best_pattern['confidence']:.2%}")
                        logger.info(f"Direction: {best_pattern['direction']}")
                        
                        # Execute trade based on pattern
                        # Note: In production, add additional filters and risk management
                        if best_pattern['confidence'] >= 0.75:
                            logger.info("\nHigh confidence pattern detected - Evaluating trade...")
                            # Uncomment to enable actual trading
                            # self.execute_trade_signal(best_pattern, current_price)
                            logger.warning("Trading is disabled by default. Uncomment code to enable.")
                        else:
                            logger.info("Pattern confidence below threshold for trade execution")
                else:
                    logger.info("No significant patterns detected")
                
                if not continuous:
                    break
                
                logger.info(f"\nSleeping for {interval} seconds...")
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\nBot stopped by user")
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
        finally:
            logger.info("Trading Bot shutdown complete")
    
    def get_active_positions(self) -> List[Dict]:
        """
        Get list of active positions
        
        Returns:
            List of active positions
        """
        return self.active_positions
    
    def display_summary(self):
        """Display summary of bot status and positions"""
        logger.info("\n" + "="*60)
        logger.info("TRADING BOT SUMMARY")
        logger.info("="*60)
        logger.info(f"Symbol: {self.symbol}")
        logger.info(f"Timeframe: {self.timeframe}")
        logger.info(f"Active Positions: {len(self.active_positions)}")
        
        if self.active_positions:
            logger.info("\nPositions:")
            for i, pos in enumerate(self.active_positions, 1):
                logger.info(f"\n  Position #{i}:")
                logger.info(f"    Pattern: {pos['pattern']}")
                logger.info(f"    Side: {pos['side']}")
                logger.info(f"    Entry: ${pos['entry_price']:,.2f}")
                logger.info(f"    Quantity: {pos['quantity']}")
                logger.info(f"    Stop Loss: ${pos['stop_loss']:,.2f}")
                logger.info(f"    Take Profit: ${pos['take_profit']:,.2f}")
        
        logger.info("="*60 + "\n")


def main():
    """Main entry point"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║     TRADING BOT WITH PATTERN RECOGNITION                  ║
    ║     Developed for Binance Trading                         ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Create and run bot
    bot = TradingBot()
    
    # Display initial summary
    bot.display_summary()
    
    # Run bot
    # Set continuous=True to run indefinitely
    # Set continuous=False to run once
    bot.run(continuous=False, interval=300)


if __name__ == "__main__":
    main()
