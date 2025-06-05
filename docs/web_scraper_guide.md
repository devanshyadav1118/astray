# Web Scraper Guide: Fallback Chart Calculation

## ⚠️ Important Notice

**This web scraper is provided as a FALLBACK OPTION only.** It goes against the core philosophy of your Astrology AI project:

- ❌ **Less accurate** than Swiss Ephemeris
- ❌ **External dependency** on astro-seek.com
- ❌ **Vulnerable** to website changes
- ❌ **Requires internet** connection
- ❌ **Not self-contained**

**Recommended Approach:** Use the Swiss Ephemeris-based chart calculator instead:
```bash
python main.py chart calculate --birth-date 1990-05-15 --birth-time 10:30 --location "New Delhi, India"
```

## 🎯 When to Use Web Scraping

**Only use web scraping when:**
1. Swiss Ephemeris installation fails due to architecture issues (Apple Silicon)
2. You need a quick chart for testing/demo purposes
3. Swiss Ephemeris dependencies cannot be resolved
4. Emergency fallback situation

**Do NOT use for:**
- Production chart analysis
- Professional astrology work
- Personal learning (accuracy matters)
- Building your astrology knowledge base

## 🛠️ Installation

### Step 1: Install Web Scraping Dependencies

```bash
# Install required packages
pip install selenium beautifulsoup4 requests webdriver-manager

# Or install all requirements
pip install -r requirements.txt
```

### Step 2: Install ChromeDriver

The scraper uses Chrome WebDriver. Install options:

**Option A: Automatic (Recommended)**
```bash
# webdriver-manager will auto-download ChromeDriver
pip install webdriver-manager
```

**Option B: Manual Installation**
1. Download ChromeDriver from https://chromedriver.chromium.org/
2. Add to PATH or place in project directory
3. Ensure Chrome browser is installed

### Step 3: Validate Installation

```bash
# Check if web scraping works
python main.py chart scrape-demo
```

## 🕷️ Usage Examples

### Basic Web Scraping

```bash
# Scrape birth chart from astro-seek.com
python main.py chart scrape \
  --birth-date "15/05/1990" \
  --birth-time "10:30" \
  --birth-location "New Delhi, India"
```

### With Additional Options

```bash
# Include timezone and validation
python main.py chart scrape \
  --birth-date "1990-05-15" \
  --birth-time "10:30" \
  --birth-location "London, UK" \
  --timezone "Europe/London" \
  --validate

# Export as JSON
python main.py chart scrape \
  --birth-date "15/05/1990" \
  --birth-time "22:45" \
  --birth-location "Mumbai, India" \
  --format json
```

### Visual Debugging

```bash
# Run with visible browser (for debugging)
python main.py chart scrape \
  --birth-date "15/05/1990" \
  --birth-time "10:30" \
  --birth-location "Sydney, Australia" \
  --no-headless
```

### Method Comparison

```bash
# Compare Swiss Ephemeris vs Web Scraping
python main.py chart compare-methods \
  --birth-date "1990-05-15" \
  --birth-time "10:30" \
  --location "New Delhi, India"
```

## 📊 Expected Output

### Successful Scraping

```
🕷️ Starting web scraping fallback method...
============================================================
⚠️ WARNING: Web scraping is not recommended for this project
   • Less accurate than Swiss Ephemeris
   • Creates external dependencies
   • Vulnerable to website changes
   • Requires internet connection

💡 Recommended: Use Swiss Ephemeris instead
   python main.py chart calculate --birth-date 15/05/1990 --birth-time 10:30 --location 'New Delhi, India'
============================================================

Continue with web scraping anyway? [y/N]: y

🔍 Initializing web scraper...
📅 Birth Date: 15/05/1990
🕐 Birth Time: 10:30
📍 Location: New Delhi, India

🕷️ Scraping from: https://horoscopes.astro-seek.com/birth-chart-horoscope-online

============================================================
BIRTH CHART - WEB SCRAPED FROM ASTRO-SEEK
============================================================

Birth Details:
Date: 15/05/1990
Time: 10:30
Location: New Delhi, India

Ascendant: 15°32' Cancer

Planetary Positions:
--------------------------------------------------
Sun      | 24°21' Taurus       | House 11
Moon     | 12°45' Libra        | House 4
Mercury  |  8°15' Gemini       | House 12
Venus    | 28°09' Aries        | House 10
Mars     |  2°34' Scorpio      | House 5 (R)
Jupiter  | 16°23' Cancer       | House 1
Saturn   | 21°45' Capricorn    | House 7
Rahu     | 28°56' Aquarius     | House 8
Ketu     | 28°56' Leo          | House 2

Scraping Details:
Source: https://horoscopes.astro-seek.com/birth-chart-horoscope-online?...
Scraped: 2024-01-15 14:30:22.123456

⚠️ Web scraped data - accuracy may vary
   Recommended: Use Swiss Ephemeris for precise calculations
============================================================

🎯 Web scraping completed!
   Planets extracted: 9
   Source: https://horoscopes.astro-seek.com/...
   Scraped at: 2024-01-15 14:30:22.123456

💡 For more accurate results, install Swiss Ephemeris:
   python main.py chart validate-deps
```

## 🔧 Troubleshooting

### Common Issues

#### ChromeDriver Not Found
```
❌ Web scraping failed: WebDriver setup failed: 'chromedriver' executable needs to be in PATH

# Solution:
pip install webdriver-manager
# Or manually install ChromeDriver
```

#### ChromeDriver Version Mismatch (Very Common!)
```
❌ Web scraping failed: ChromeDriver version mismatch detected!
This version of ChromeDriver only supports Chrome version 114
Current browser version is 137.0.7151.68

# This happens when:
- Chrome browser auto-updates to a newer version
- ChromeDriver remains on an older version
- Creates immediate compatibility break

# Quick Fix:
pip install webdriver-manager
# This automatically downloads the correct ChromeDriver version

# Manual Fix:
1. Check your Chrome version: chrome://version/
2. Download matching ChromeDriver from https://chromedriver.chromium.org/
3. Replace old ChromeDriver with new one

# Root Cause:
This demonstrates why web scraping is inherently fragile:
• Browser updates happen automatically
• ChromeDriver compatibility breaks frequently  
• Requires constant maintenance
• Swiss Ephemeris never has this problem
```

#### Website Changes
```
❌ Web scraping failed: Could not find planetary positions table

# The astro-seek.com website may have changed
# Solutions:
1. Check if website is accessible
2. Try again later (temporary issue)
3. Use Swiss Ephemeris instead (recommended)
```

#### Network Issues
```
❌ Web scraping failed: Timeout waiting for results page

# Solutions:
1. Check internet connection
2. Try with --no-headless to see what's happening
3. Increase timeout in scraper settings
```

#### Invalid Date Format
```
❌ Web scraping failed: Invalid date format: 1990-05-15

# Solutions:
1. Use DD/MM/YYYY format: "15/05/1990"
2. Or MM/DD/YYYY format: "05/15/1990"
3. The scraper will auto-convert YYYY-MM-DD
```

### Debug Mode

```bash
# Run with visible browser to see what's happening
python main.py chart scrape \
  --birth-date "15/05/1990" \
  --birth-time "10:30" \
  --birth-location "New Delhi, India" \
  --no-headless
```

This opens Chrome visually so you can see:
- Form filling process
- Website interactions
- Any error messages
- Results page structure

## 📈 Accuracy Comparison

### Swiss Ephemeris vs Web Scraping

| Aspect | Swiss Ephemeris | Web Scraping |
|--------|----------------|---------------|
| **Accuracy** | ±1 degree precision | Variable (±2-5 degrees) |
| **Reliability** | Always consistent | Depends on website |
| **Speed** | Very fast (local) | Slower (network + parsing) |
| **Dependencies** | Self-contained | External website |
| **Offline** | ✅ Works offline | ❌ Requires internet |
| **Professional Use** | ✅ Recommended | ❌ Not suitable |

### Example Comparison Output

```bash
$ python main.py chart compare-methods --birth-date 1990-05-15 --birth-time 10:30 --location "New Delhi, India"

⚖️ Comparing calculation methods...
==================================================

🔬 Method 1: Swiss Ephemeris (Recommended)
✅ Swiss Ephemeris calculation successful
   Accuracy: ±1 degree precision
   Ascendant: 108.45°
   Planets calculated: 9

🕷️ Method 2: Web Scraping (Fallback Only)
✅ Web scraping successful
   Accuracy: Variable (depends on external site)
   Ascendant: 15°32'
   Planets extracted: 9

==================================================
⚖️ COMPARISON RESULTS
==================================================
📊 Both methods successful - showing differences:

Ascendant difference: 2.35 degrees

🎯 RECOMMENDATION:
   ✅ Use Swiss Ephemeris for:
      • Maximum accuracy (±1 degree)
      • Self-contained calculations
      • Professional analysis
      • Offline capability
   ⚠️ Use web scraping only for:
      • Emergency fallback
      • When Swiss Ephemeris unavailable
      • Quick approximations
```

## 🚫 Limitations

### Website Dependency
- Relies on astro-seek.com availability
- Subject to website changes/updates
- May break without notice
- No control over calculation methods

### Accuracy Issues
- Cannot verify calculation methods used
- Different ayanamsa systems possible
- Rounding errors in web display
- No access to raw calculation data

### Reliability Concerns
- Network timeouts
- Website maintenance downtime
- Rate limiting/blocking
- Browser compatibility issues

### Data Quality
- Limited to displayed information
- May miss important details
- No access to calculation metadata
- Inconsistent data formats

## 💡 Best Practices

### When You Must Use Web Scraping

1. **Always validate results**:
   ```bash
   python main.py chart scrape ... --validate
   ```

2. **Compare with known sources**:
   - Cross-check with other astrology software
   - Verify against published ephemeris data
   - Use for approximation only

3. **Document limitations**:
   - Note it's web-scraped data
   - Include accuracy disclaimers
   - Mark as preliminary analysis

4. **Plan migration**:
   - Work towards Swiss Ephemeris installation
   - Use web scraping as temporary solution
   - Monitor for installation opportunities

### Error Handling

```python
# Example error handling in your code
try:
    chart_data = scraper_service.get_birth_chart(...)
    print("⚠️ Web scraped data - verify independently")
except Exception as e:
    print(f"Web scraping failed: {e}")
    print("Recommendation: Install Swiss Ephemeris")
    print("Run: python main.py chart validate-deps")
```

## 🎯 Migration Path

### From Web Scraping to Swiss Ephemeris

1. **Check current status**:
   ```bash
   python main.py chart validate-deps
   ```

2. **Install dependencies**:
   ```bash
   # For Apple Silicon
   conda install -c conda-forge pyswisseph
   
   # Or with Rosetta
   arch -x86_64 pip install pyswisseph
   ```

3. **Test Swiss Ephemeris**:
   ```bash
   python main.py chart demo
   ```

4. **Compare results**:
   ```bash
   python main.py chart compare-methods --birth-date ... --birth-time ... --location ...
   ```

5. **Switch to Swiss Ephemeris**:
   ```bash
   # Replace this:
   python main.py chart scrape ...
   
   # With this:
   python main.py chart calculate ...
   ```

## 🎉 Success Criteria

Web scraping is **successful** when:
- ✅ Extracts 7+ planetary positions
- ✅ Includes ascendant information
- ✅ Provides house placements
- ✅ Handles retrograde indicators
- ✅ Validates basic data quality

But remember: **Success with web scraping means it's time to migrate to Swiss Ephemeris!**

---

*"Use web scraping as a bridge, not a destination. Swiss Ephemeris is your true destination for accurate, self-contained astrology calculations."*

# Astro-Seek Web Scraper Test Guide

## Overview

This document explains the Astro-Seek birth chart web scraper test function that automates the process of extracting planetary positions from the website `https://horoscopes.astro-seek.com/birth-chart-horoscope-online`.

## ⚠️ Important Note

**This scraper is a testing/demonstration tool only.** For production use, we recommend using the Swiss Ephemeris integration in the main project:

```bash
python main.py chart calculate
```

## 🔧 Automated Steps

The scraper performs the following steps automatically:

1. **Navigate** to the birth chart form page
2. **Fill in birth data** (date, time, city)
3. **Select first option** from city dropdown autocomplete
4. **Click "Calculate chart"** button
5. **Find and click "Copy positions"** button on the result page
6. **Extract planetary positions** data and print to terminal

## 📋 Prerequisites

### 1. Required Dependencies

All dependencies are already included in `requirements.txt`:

```bash
pip install selenium>=4.15.0
pip install webdriver-manager>=4.0.1
pip install beautifulsoup4>=4.12.0
pip install requests>=2.31.0
```

### 2. Google Chrome Browser

You need Google Chrome installed on your system:

**Option A: Download from Google**
1. Visit: https://www.google.com/chrome/
2. Download and install Chrome for macOS
3. Make sure Chrome is in your Applications folder

**Option B: Install via Homebrew**
```bash
brew install --cask google-chrome
```

## 🚀 Running the Test

### Method 1: Direct Test File

```bash
cd /path/to/astrology_ai
python tests/test_astro_seek_scraper.py
```

Choose option:
- `1` - Full interactive scraper test (opens browser window)
- `2` - Simple connection test (headless mode)

### Method 2: Using the Runner Script

```bash
python run_scraper_test.py
```

This provides a more user-friendly interface.

## 📊 Test Data

The test uses hardcoded birth data (as requested):

```python
test_birth_data = {
    "date": "15/08/1990",  # DD/MM/YYYY format
    "time": "14:30",       # HH:MM format  
    "city": "New York"     # City name
}
```

## 🎯 Expected Output

### Successful Run

```
🚀 Starting Astro-Seek Birth Chart Scraper Test
==================================================
📊 Test birth data:
   Date: 15/08/1990
   Time: 14:30
   City: New York

🔧 Setting up browser driver...
   ✅ Found Chrome at: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
   ✅ ChromeDriver setup successful
🌐 Step 1: Navigating to birth chart form...
✅ Page loaded successfully
📝 Step 2: Filling in birth data...
   ✅ Date filled: 15/08/1990
   ✅ Time filled: 14:30
🏙️  Step 3: Filling city and selecting from autocomplete...
   ✅ City typed: New York
   ✅ First autocomplete option selected
🧮 Step 4: Clicking 'Calculate chart' button...
   ✅ Calculate button clicked
⏳ Waiting for results page to load...
📋 Step 5: Looking for 'Copy positions' button...
   ✅ Copy positions button clicked
🪐 Step 6: Extracting planetary positions data...

🎯 EXTRACTED PLANETARY POSITIONS:
========================================
Sun: 22°32' Leo
Moon: 15°47' Sagittarius
Mercury: 10°21' Virgo
Venus: 28°14' Cancer
Mars: 03°55' Gemini
Jupiter: 08°12' Leo
Saturn: 23°41' Capricorn
Uranus: 06°33' Capricorn
Neptune: 13°28' Capricorn
Pluto: 16°42' Scorpio
North Node: 01°55' Aquarius
----------------------------------------

✅ Test completed successfully!
🔧 Browser closed
```

## 🐛 Troubleshooting

### Chrome Not Found Error

```
❌ ChromeDriver setup failed: Message: unknown error: cannot find Chrome binary
```

**Solution**: Install Google Chrome browser (see Prerequisites section)

### Selenium Import Error

```
❌ Selenium not available: No module named 'selenium'
```

**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Website Changes

If the website structure changes, the scraper may fail to find elements. The test includes multiple fallback selectors, but you may need to update them.

### Timeout Issues

If the website is slow to respond:
1. The test waits up to 30 seconds for page loads
2. Increase timeout in `setup_test_driver()` if needed
3. Check your internet connection

## 🔍 Technical Details

### Element Selection Strategy

The scraper uses multiple fallback selectors for robustness:

```python
# Example: Date field selectors
date_selectors = [
    "input[name='narozeni_datum']",    # Czech name attribute
    "input[placeholder*='Date']",      # Placeholder text
    "input[type='date']",              # HTML5 date input
    "#datum"                           # ID selector
]
```

### Error Handling

- Graceful handling of missing elements
- Multiple selector fallbacks
- Clear error messages with solutions
- Automatic browser cleanup

### Browser Configuration

- Headless mode option for automated runs
- Realistic user agent to avoid blocking
- Appropriate window size for form interaction
- No-sandbox mode for compatibility

## 💡 Integration with Main Project

This scraper demonstrates web automation techniques that could be integrated into the main astrology AI project for:

1. **Data validation** - Compare Swiss Ephemeris calculations with online sources
2. **Bulk chart processing** - Process multiple birth charts automatically
3. **Source verification** - Cross-reference astrological calculations

However, for production use, prefer the Swiss Ephemeris approach:

```bash
# Better approach - no external dependencies
python main.py chart calculate \
  --date "1990-08-15" \
  --time "14:30" \
  --location "New York, NY"
```

## 🎓 Learning Outcomes

This test demonstrates:

- **Selenium WebDriver** automation
- **Form interaction** with date/time inputs and autocomplete
- **Dynamic content handling** with JavaScript-rendered pages
- **Error handling** for web scraping scenarios
- **Cross-platform compatibility** considerations

## 📚 Next Steps

1. **Extend the scraper** to handle more birth chart services
2. **Add data validation** against Swiss Ephemeris calculations
3. **Implement parallel processing** for multiple charts
4. **Create a comparison tool** between different calculation methods

## ⚖️ Legal and Ethical Considerations

- This scraper is for **educational and testing purposes** only
- Respect website terms of service and rate limits
- Consider the website's robots.txt file
- For production use, prefer API access or local calculations
- Always attribute sources when using scraped data

---

**Remember**: Web scraping should be a last resort. The Swiss Ephemeris approach in this project is more reliable, accurate, and doesn't depend on external websites. 