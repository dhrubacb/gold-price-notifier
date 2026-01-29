Gold Price Monitor Setup Guide (Optimized)

Overview

The Gold Price Monitor is a lightweight Python script that monitors gold prices using the official goldprice.org API endpoint and sends you macOS desktop notifications whenever the gold price changes by more than 2 RM/gram.

The notifications display the price in the format: "NOW vs THEN (in RM/GRAM)"

Why This Version is Better

✅ Lightweight - Uses direct API instead of HTML parsing
✅ Fast - Minimal network overhead, quick responses
✅ Reliable - No JavaScript rendering needed
✅ Efficient - Very low CPU and memory usage
✅ No dependencies - Only uses requests library (pre-installed on most Macs)

Features

•
✅ Monitors gold prices in Malaysian Ringgit (RM) per gram

•
✅ Sends native macOS notifications when price changes exceed 2 RM/gram

•
✅ Runs in the background without requiring a browser

•
✅ Checks price every 5 minutes (configurable)

•
✅ Keeps track of price history in a local file

•
✅ Can be set to launch automatically at startup

•
✅ Uses the official goldprice.org API: https://data-asg.goldprice.org/dbXRates/MYR

Requirements

•
macOS (Monterey or later recommended )

•
Python 3.7 or higher

•
Internet connection

•
requests library (usually pre-installed)

Installation

Step 1: Copy the Script to Your Mac

Download the gold_price_monitor.py file and save it to a convenient location, such as:

Bash


mkdir -p ~/Scripts
# Copy gold_price_monitor.py to ~/Scripts/



Step 2: Make the Script Executable

Open Terminal and run:

Bash


chmod +x ~/Scripts/gold_price_monitor.py



Step 3: Install Dependencies (if needed)

The script uses the requests library. If it's not installed:

Bash


pip3 install requests



Or:

Bash


python3 -m pip install requests



Step 4: Test the Script

Run the script manually to verify it works:

Bash


python3 ~/Scripts/gold_price_monitor.py



You should see output like:

Plain Text


🔍 Gold Price Monitor Started (Optimized)
📍 API: https://data-asg.goldprice.org/dbXRates/MYR
⚠️  Alert threshold: 2.0 RM/gram
⏱️  Check interval: 300 seconds

Press Ctrl+C to stop.

[2026-01-29 01:16:50]: # "Check #1... Current price: 703.37 RM/g (First reading )"



Press Ctrl+C to stop the script.

Running the Script

Option 1: Run Manually

Simply open Terminal and run:

Bash


python3 ~/Scripts/gold_price_monitor.py



The script will run indefinitely, checking the price every 5 minutes and sending notifications when the price changes by more than 2 RM/gram.

Option 2: Run in the Background

To run the script in the background and free up your Terminal:

Bash


python3 ~/Scripts/gold_price_monitor.py > ~/Scripts/gold_price_monitor.log 2>&1 &



To check if the script is running:

Bash


ps aux | grep gold_price_monitor



To stop the background process:

Bash


pkill -f gold_price_monitor



Option 3: Launch at Startup (Recommended)

To have the script launch automatically when you start your Mac:

Using LaunchAgent (Recommended Method)

1.
Create a LaunchAgent configuration file:

Bash


mkdir -p ~/Library/LaunchAgents
nano ~/Library/LaunchAgents/com.user.goldpricemonitor.plist



1.
Paste the following content (adjust the path if necessary):

XML


<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.goldpricemonitor</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/Scripts/gold_price_monitor.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/YOUR_USERNAME/Scripts/gold_price_monitor.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/YOUR_USERNAME/Scripts/gold_price_monitor_error.log</string>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>



1.
Important: Replace YOUR_USERNAME with your actual macOS username. To find it, run:

Bash


whoami



1.
Save the file (press Ctrl+X, then Y, then Enter in nano ).

2.
Load the LaunchAgent:

Bash


launchctl load ~/Library/LaunchAgents/com.user.goldpricemonitor.plist



1.
Verify it's running:

Bash


launchctl list | grep goldpricemonitor



To Unload (Stop Automatic Startup)

Bash


launchctl unload ~/Library/LaunchAgents/com.user.goldpricemonitor.plist



Configuration

You can customize the script by editing the following variables at the top of gold_price_monitor.py:

Python


PRICE_THRESHOLD = 2.0  # Change alert threshold (in RM/gram)
CHECK_INTERVAL = 300   # Change check interval (in seconds)
                       # 300 = 5 minutes, 600 = 10 minutes, etc.



How the API Works

The script uses the official goldprice.org API endpoint:

Plain Text


https://data-asg.goldprice.org/dbXRates/MYR



This endpoint returns JSON data with:

•
xauPrice: Gold price in RM per troy ounce

•
xagPrice: Silver price in RM per troy ounce

•
chgXau: Change in gold price

•
pcXau: Percentage change in gold price

The script converts the troy ounce price to grams using the conversion factor:

Plain Text


1 troy ounce = 31.1035 grams



Notification Examples

When the price changes by more than 2 RM/gram, you'll receive a notification like:

Title: 💰 Gold Price Alert

Message: NOW: 705.37 RM/g vs THEN: 703.37 RM/g (Change: +2.00 RM/g )

Troubleshooting

Script Not Sending Notifications

1.
Check if notifications are enabled:

•
Go to System Preferences → Notifications

•
Find "Script Editor" or "Terminal" in the list

•
Ensure notifications are allowed



2.
Check the log file:

Bash


tail -f ~/Scripts/gold_price_monitor.log



1.
Test osascript manually:

Bash


osascript -e 'display notification "Test" with title "Gold Price Monitor"'



Script Not Fetching Price

1.
Check internet connection:

Bash


curl -I https://data-asg.goldprice.org/dbXRates/MYR



1.
Test the API endpoint:

Bash


curl -H "User-Agent: Mozilla/5.0" https://data-asg.goldprice.org/dbXRates/MYR



1.
Check the error log:

Bash


tail -f ~/Scripts/gold_price_monitor_error.log



LaunchAgent Not Starting

1.
Verify the plist file syntax:

Bash


plutil -lint ~/Library/LaunchAgents/com.user.goldpricemonitor.plist



1.
Check the username in the plist file:

Bash


whoami



1.
Reload the LaunchAgent:

Bash


launchctl unload ~/Library/LaunchAgents/com.user.goldpricemonitor.plist
launchctl load ~/Library/LaunchAgents/com.user.goldpricemonitor.plist



"requests" Library Not Found

If you get an error about the requests library:

Bash


pip3 install requests



Or if that doesn't work:

Bash


python3 -m pip install requests



Price History

The script saves the last recorded price in:

Plain Text


~/.gold_price_history.json



You can view the history:

Bash


cat ~/.gold_price_history.json



Example output:

JSON


{
    "last_price": 703.37,
    "last_timestamp": "2026-01-29T01:16:50.123456"
}



Uninstallation

To completely remove the gold price monitor:

1.
Stop the LaunchAgent:

Bash


launchctl unload ~/Library/LaunchAgents/com.user.goldpricemonitor.plist



1.
Remove the LaunchAgent file:

Bash


rm ~/Library/LaunchAgents/com.user.goldpricemonitor.plist



1.
Remove the script:

Bash


rm ~/Scripts/gold_price_monitor.py



1.
Remove the log files (optional ):

Bash


rm ~/Scripts/gold_price_monitor.log
rm ~/Scripts/gold_price_monitor_error.log



1.
Remove the price history (optional):

Bash


rm ~/.gold_price_history.json



Support

If you encounter any issues:

1.
Check the log files for error messages

2.
Verify the script runs manually without errors

3.
Ensure your internet connection is stable

4.
Test the API endpoint directly with curl

5.
Check that the website (goldprice.org) is accessible

Notes

•
The script checks the price every 5 minutes by default

•
Notifications are only sent when the price change exceeds 2 RM/gram

•
The script runs continuously until manually stopped or the computer is shut down

•
If using LaunchAgent, the script will restart automatically if it crashes

•
Price history is stored locally and persists between script runs

•
The API endpoint is lightweight and uses minimal bandwidth

API Information

Endpoint: https://data-asg.goldprice.org/dbXRates/MYR

Response Format:

JSON


{
    "ts": 1769667401044,
    "tsj": 1769667397630,
    "date": "Jan 29th 2026, 01:16:37 am NY",
    "items": [
        {
            "curr": "MYR",
            "xauPrice": 21877.3436,
            "xagPrice": 469.1346,
            "chgXau": 1086.0688,
            "chgXag": 24.6302,
            "pcXau": 5.2237,
            "pcXag": 5.541,
            "xauClose": 20791.27475,
            "xagClose": 444.50435
        }
    ]
}






Last Updated: January 2026

