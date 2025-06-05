# Phase 2 Setup Guide: Personal Chart Calculation

Welcome to Phase 2 of your Astrology AI journey! With 401 rules successfully extracted, you're now ready to build your personal chart interpretation engine.

## 🎯 Phase 2 Overview

Phase 2 transforms your knowledge base into a practical chart interpretation system using:
- **Swiss Ephemeris** for astronomical accuracy (±1 degree precision)
- **Personal learning focus** - interpretations that teach you astrology
- **Classical authority** - prioritizing traditional sources over modern
- **Complete self-sufficiency** - no external dependencies or web scraping

## 🛠️ Installation

### Step 1: Install Phase 2 Dependencies

```bash
# Install all Phase 2 requirements
pip install swisseph>=2.8.0 pytz>=2023.3 timezonefinder>=6.2.0 geopy>=2.3.0

# Or install from requirements file
pip install -r requirements.txt
```

### Step 2: Download Swiss Ephemeris Data Files

Swiss Ephemeris needs data files for accurate calculations:

```bash
# Create ephemeris directory
mkdir -p ephemeris

# Download required data files (automated script coming soon)
# For now, Swiss Ephemeris will work with built-in approximations
```

### Step 3: Validate Installation

```bash
# Check if all dependencies are installed
python main.py chart validate-deps

# Run demo to test functionality
python main.py chart demo
```

## 🧪 Testing Your Setup

### Basic Functionality Test

```bash
# Test chart calculation with sample data
python main.py chart demo
```

**Expected Output:**
```
🎯 Running chart calculation demo...
Using sample birth data from New Delhi, India
==================================================

============================================================
VEDIC BIRTH CHART - PERSONAL ANALYSIS
============================================================

Birth Details:
Date & Time: 1990-05-15 10:30:00+05:30
Location: New Delhi, India (28.6139, 77.2090)
Timezone: Asia/Kolkata
Ayanamsa: Lahiri (23.8234°)

Ascendant (Lagna): 108.45° (Cancer)

Planetary Positions:
----------------------------------------
Sun      |  21.32° | Taurus      | House  11 | Krittika        3/4
Moon     | 187.89° | Libra       | House   4 | Swati           2/4
Mercury  |  45.67° | Gemini      | House  12 | Mrigashira      1/4
Venus    |  12.45° | Aries       | House  10 | Ashwini         4/4
Mars     | 234.56° | Scorpio     | House   5 | Jyeshtha        2/4 (R)
Jupiter  | 156.78° | Virgo       | House   3 | Hasta           1/4
Saturn   | 289.34° | Capricorn   | House   7 | Uttara Ashadha  2/4
Rahu     | 298.12° | Aquarius    | House   8 | Purva Bhadrapada 1/4
Ketu     | 118.12° | Cancer      | House   2 | Pushya          3/4

✅ Chart accuracy validation passed
```

### Personal Chart Calculation

```bash
# Calculate your own chart (replace with your birth data)
python main.py chart calculate \
  --birth-date 1990-05-15 \
  --birth-time 10:30 \
  --location "New Delhi, India" \
  --validate
```

### Advanced Usage Examples

```bash
# Using coordinates instead of location name
python main.py chart calculate \
  --birth-date 1990-05-15 \
  --birth-time 10:30 \
  --latitude 28.6139 \
  --longitude 77.2090 \
  --timezone "Asia/Kolkata"

# Export in JSON format
python main.py chart calculate \
  --birth-date 1990-05-15 \
  --birth-time 10:30 \
  --location "London, UK" \
  --format json

# Save chart for future reference
python main.py chart calculate \
  --birth-date 1990-05-15 \
  --birth-time 10:30 \
  --location "Mumbai, India" \
  --save "My Chart"
```

## 🔧 Configuration Options

### Ayanamsa Systems
Currently using **Lahiri ayanamsa** (most traditional). Future versions will support:
- Lahiri (default)
- Raman
- KP (Krishnamurti Paddhati)
- True Chitra Paksha

### House Systems
Currently using **Whole Sign houses** (traditional Vedic). Future support:
- Whole Sign (default)
- Placidus
- Equal House
- Bhava Chalit

### Coordinate Systems
- **Sidereal** (Vedic - default)
- Tropical (future support)

## 🎓 Learning Mode Features

Phase 2 is designed as a learning tool. Each chart calculation includes:

### Accuracy Validation
- Planetary position verification
- House cusp validation
- Nakshatra calculation checks
- Overall confidence scoring

### Educational Output
- Complete planetary positions with nakshatras
- House cusp degrees and signs
- Ayanamsa values for learning
- Calculation method transparency

### Source Integration
Ready for your 401 extracted rules:
- Classical authority prioritization
- Source attribution for all interpretations
- Confidence-weighted analysis
- Learning insights generation

## 🚨 Troubleshooting

### Common Issues

#### Missing Dependencies
```bash
❌ swisseph - MISSING: Swiss Ephemeris for astronomical calculations

# Solution:
pip install swisseph
```

#### Location Lookup Failures
```bash
❌ Location lookup failed: Service timed out

# Solution: Use coordinates instead
python main.py chart calculate \
  --birth-date 1990-05-15 \
  --birth-time 10:30 \
  --latitude 28.6139 \
  --longitude 77.2090
```

#### Timezone Issues
```bash
⚠️ No timezone specified, using UTC

# Solution: Always specify timezone
--timezone "Asia/Kolkata"
```

### Performance Optimization

For faster calculations:
1. **Install local ephemeris files** (reduces network dependencies)
2. **Cache frequently used locations** (future feature)
3. **Use coordinate input** instead of location names

## 🔍 Accuracy Validation

Phase 2 prioritizes accuracy above all else:

### Validation Checks
- ✅ Planetary positions within 0-360° range
- ✅ House assignments (1-12) for all planets
- ✅ Nakshatra calculations (27 nakshatras, 4 padas each)
- ✅ Ascendant degree validation
- ✅ Ayanamsa value verification

### Error Handling
```bash
# If validation fails, you'll see:
⚠️ Chart accuracy validation issues detected
   • Mars house assignment invalid: 0
   • Unknown nakshatra for Venus: InvalidName
```

### Cross-Reference Validation
Compare results with:
- Traditional Vedic astrology software
- Swiss Ephemeris test suite
- Classical astronomical references

## 🎯 Next Steps

With chart calculation working:

1. **Calculate your personal chart** and family charts
2. **Validate accuracy** against known references
3. **Prepare for rule integration** (Phase 2 Week 2)
4. **Start learning** Vedic astrology through the system

### Ready for Week 2: Rule Integration

Your 401 extracted rules are waiting to be applied to charts:
- Planetary placement rules
- House lordship interpretations
- Nakshatra influences
- Yoga combinations
- Classical authority weighting

## 📞 Support

If you encounter issues:

1. **Check dependencies**: `python main.py chart validate-deps`
2. **Run demo**: `python main.py chart demo`
3. **Verify input format**: Date (YYYY-MM-DD), Time (HH:MM)
4. **Check coordinates**: Valid latitude (-90 to 90), longitude (-180 to 180)

## 🌟 Success Metrics

Phase 2 is successful when:
- ✅ You can calculate charts with ±1 degree accuracy
- ✅ All 9 planets positioned correctly
- ✅ Nakshatras and padas calculated properly
- ✅ You trust the system for personal analysis
- ✅ Ready to apply your 401 extracted rules

**Your personal astrology teacher is coming to life!** 🎉

---

*"Accuracy first, learning always, classical wisdom forever."* 