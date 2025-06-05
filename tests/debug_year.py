#!/usr/bin/env python3
"""
Quick debug script for the year dropdown issue
"""

from test_astro_seek_scraper import setup_test_driver, debug_year_dropdown
from selenium.webdriver.support.ui import WebDriverWait
import time

def main():
    print("🔍 QUICK YEAR DROPDOWN DEBUG")
    print("=" * 40)
    
    # Setup driver (non-headless so we can see what's happening)
    driver = setup_test_driver(headless=False)
    if not driver:
        print("❌ Could not setup driver")
        return
    
    try:
        # Navigate to astro-seek
        print("🌐 Loading astro-seek...")
        driver.get("https://horoscopes.astro-seek.com/birth-chart-horoscope-online")
        
        # Wait for page to load
        wait = WebDriverWait(driver, 15)
        time.sleep(5)  # Give page time to fully load
        
        # Debug the year dropdown
        print("\n" + "="*50)
        debug_result = debug_year_dropdown(driver, wait)
        print("="*50)
        
        if debug_result:
            print("✅ Year dropdown debugging completed")
        else:
            print("❌ Year dropdown debugging failed")
            
        # Keep browser open for a moment to inspect
        print("\n📋 Browser will stay open for 10 seconds for manual inspection...")
        time.sleep(10)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        driver.quit()
        print("🔧 Browser closed")

if __name__ == "__main__":
    main() 