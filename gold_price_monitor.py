#!/usr/bin/env python3
"""
Gold Price Monitor for Malaysia (Enhanced)
Monitors gold prices from goldprice.org API and sends macOS notifications
when the price changes by more than 2 RM/gram.

Uses the direct API endpoint: https://data-asg.goldprice.org/dbXRates/MYR
This is much lighter and faster than parsing HTML.

Features:
- Real-time price monitoring
- Native macOS notifications
- Price history tracking
- Configurable thresholds
- Graceful shutdown
"""

import requests
import json
import time
import subprocess
import os
from datetime import datetime
import signal
import sys
import argparse

# Configuration
API_URL = "https://data-asg.goldprice.org/dbXRates/MYR"
PRICE_THRESHOLD = 2.0  # RM per gram
CHECK_INTERVAL = 25  # Check every 25 seconds
PRICE_HISTORY_FILE = os.path.expanduser("~/.gold_price_history.json")

def get_gold_price():
    """
    Fetch the current gold price in RM per gram from the API.
    The API returns price in RM per troy ounce, so we convert to per gram.
    1 troy ounce = 31.1035 grams
    
    Returns a tuple of (price_per_gram, timestamp) or (None, None) if failed.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract the gold price in RM per troy ounce
        if 'items' in data and len(data['items']) > 0:
            item = data['items'][0]
            price_per_oz = item.get('xauPrice')
            
            if price_per_oz:
                # Convert from RM per troy ounce to RM per gram
                price_per_gram = price_per_oz / 31.1035
                timestamp = datetime.now().isoformat()
                return price_per_gram, timestamp
        
        return None, None
    except Exception as e:
        print(f"❌ Error fetching gold price: {e}")
        return None, None

def send_notification(title, message, verbose=False):
    """
    Send a macOS notification using osascript.
    
    Args:
        title: Notification title
        message: Notification message
        verbose: Print debug information
    """
    try:
        if verbose:
            print(f"\n📢 Sending notification...")
            print(f"   Title: {title}")
            print(f"   Message: {message}\n")
        
        # Escape quotes in the message and title
        message_escaped = message.replace('"', '\\"').replace("'", "\\'")
        title_escaped = title.replace('"', '\\"').replace("'", "\\'")
        
        # Build the osascript command
        script = f'display notification "{message_escaped}" with title "{title_escaped}"'
        
        # Execute the notification
        result = subprocess.run(
            ['osascript', '-e', script],
            check=False,
            capture_output=True,
            timeout=5,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ Notification sent: {title}")
            return True
        else:
            print(f"⚠️  osascript returned code {result.returncode}")
            if result.stderr:
                print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Notification timeout (osascript took too long)")
        return False
    except FileNotFoundError:
        print("❌ Error: osascript not found. This script requires macOS.")
        return False
    except Exception as e:
        print(f"❌ Error sending notification: {e}")
        return False

def load_price_history():
    """
    Load the price history from file.
    """
    if os.path.exists(PRICE_HISTORY_FILE):
        try:
            with open(PRICE_HISTORY_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Error loading price history: {e}")
    return {"last_price": None, "last_timestamp": None}

def save_price_history(price, timestamp):
    """
    Save the price history to file.
    """
    try:
        history = {
            "last_price": price,
            "last_timestamp": timestamp
        }
        with open(PRICE_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"⚠️  Error saving price history: {e}")

def format_notification_message(current_price, previous_price):
    """
    Format the notification message with NOW vs THEN format.
    """
    change = current_price - previous_price
    change_str = f"+{change:.2f}" if change > 0 else f"{change:.2f}"
    
    message = f"NOW: {current_price:.2f} RM/g vs THEN: {previous_price:.2f} RM/g (Change: {change_str} RM/g)"
    return message

def test_notification():
    """
    Test notification functionality.
    """
    print("🧪 Testing notification system...\n")
    
    title = "💰 Gold Price Alert - TEST"
    message = "NOW: 285.50 RM/g vs THEN: 283.25 RM/g (Change: +2.25 RM/g)"
    
    print(f"Sending test notification...")
    success = send_notification(title, message, verbose=True)
    
    if success:
        print("✅ Test notification sent successfully!")
        print("\nIf you didn't see a notification on your Mac:")
        print("1. Check System Preferences → Notifications")
        print("2. Ensure notifications are enabled for Terminal")
        print("3. Check if 'Do Not Disturb' is enabled")
    else:
        print("❌ Test notification failed!")
        print("\nMake sure you're running this on macOS.")
    
    sys.exit(0)

def signal_handler(sig, frame):
    """
    Handle Ctrl+C gracefully.
    """
    print("\n\n⏹️  Gold price monitor stopped.")
    sys.exit(0)

def main(test_mode=False, verbose=False, interval=None, threshold=None):
    """
    Main monitoring loop.
    
    Args:
        test_mode: Run in test mode (send notification and exit)
        verbose: Print verbose output
        interval: Custom check interval (overrides default)
        threshold: Custom price threshold (overrides default)
    """
    global CHECK_INTERVAL, PRICE_THRESHOLD
    
    if interval:
        CHECK_INTERVAL = interval
    if threshold:
        PRICE_THRESHOLD = threshold
    
    print("=" * 60)
    print("🔍 Gold Price Monitor - Malaysia")
    print("=" * 60)
    print(f"📍 API: {API_URL}")
    print(f"⚠️  Alert threshold: {PRICE_THRESHOLD} RM/gram")
    print(f"⏱️  Check interval: {CHECK_INTERVAL} seconds")
    print(f"📊 Price history: {PRICE_HISTORY_FILE}")
    
    if verbose:
        print(f"🔧 Verbose mode: ON")
    
    print("\nPress Ctrl+C to stop.\n")
    print("=" * 60 + "\n")
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Load initial price history
    history = load_price_history()
    last_price = history.get("last_price")
    
    iteration = 0
    
    while True:
        iteration += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[{current_time}] Check #{iteration}...", end=" ", flush=True)
        
        # Fetch current price
        current_price, timestamp = get_gold_price()
        
        if current_price is None:
            print("❌ Failed to fetch price")
            time.sleep(CHECK_INTERVAL)
            continue
        
        print(f"Current price: {current_price:.2f} RM/g", end=" ")
        
        # Check if this is the first price or if there's a significant change
        if last_price is not None:
            price_change = abs(current_price - last_price)
            
            if price_change >= PRICE_THRESHOLD:
                print(f"⚠️  CHANGE DETECTED: {price_change:.2f} RM/g")
                
                # Send notification
                title = "💰 Gold Price Alert"
                message = format_notification_message(current_price, last_price)
                send_notification(title, message, verbose=verbose)
                
                # Update history
                save_price_history(current_price, timestamp)
                last_price = current_price
            else:
                print(f"(Change: {price_change:.2f} RM/g - below threshold)")
        else:
            print("(First reading)")
            save_price_history(current_price, timestamp)
            last_price = current_price
        
        # Wait before next check
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Gold Price Monitor - Monitor gold prices and receive macOS notifications",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 gold_price_monitor.py              # Run normally
  python3 gold_price_monitor.py --test       # Test notifications
  python3 gold_price_monitor.py --verbose    # Verbose output
  python3 gold_price_monitor.py --interval 60 --threshold 1.5  # Custom settings
        """
    )
    
    parser.add_argument(
        '--test',
        action='store_true',
        help='Test notification system and exit'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--interval',
        type=int,
        help='Check interval in seconds (default: 300)'
    )
    
    parser.add_argument(
        '--threshold',
        type=float,
        help='Price change threshold in RM/gram (default: 2.0)'
    )
    
    args = parser.parse_args()
    
    if args.test:
        test_notification()
    else:
        main(
            test_mode=False,
            verbose=args.verbose,
            interval=args.interval,
            threshold=args.threshold
        )
