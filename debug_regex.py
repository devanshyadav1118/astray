#!/usr/bin/env python3
"""Debug regex patterns for planetary position parsing"""

import re

# Test data from the actual cleaned output
test_lines = [
    "Sun in Leo 22°30', in 9th House",
    "Moon in Aquarius 3°07', in 2nd House", 
    "Mercury in Virgo 19°51', in 10th House",
    "Venus in Libra 7°50', in 10th House",
    "Mars in Leo 18°15', in 9th House",
    "Jupiter in Scorpio 0°00', in 11th House",
    "Saturn in Taurus 22°16', in 6th House",
    "North Node in Pisces 3°16', Retrograde, in 3rd House"
]

# Test current patterns from the web scraper
patterns = [
    # Pattern 1: "Planet in Sign degree°minute', in House" (exact format from astro-seek)
    r'(\w+)\s+in\s+(\w+)\s+(\d+)°(\d+)\',\s+in\s+(\d+)(?:st|nd|rd|th)?\s+House',
    # Pattern 2: "Planet in Sign degree°minute'" (without house)
    r'(\w+)\s+in\s+(\w+)\s+(\d+)°(\d+)\'',
    # Pattern 3: "Planet Sign degree°minute'" (no "in")
    r'(\w+)\s+(\w+)\s+(\d+)°(\d+)\'',
    # Pattern 4: "Planet: Sign degree°minute'"
    r'(\w+):\s*(\w+)\s+(\d+)°(\d+)\'',
]

print("🧪 Testing Regex Patterns Against Cleaned Lines")
print("=" * 60)

for line in test_lines:
    print(f"\n🔍 Testing line: {line}")
    print("-" * 50)
    
    found_match = False
    for pattern_num, pattern in enumerate(patterns, 1):
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            print(f"✅ Pattern {pattern_num} MATCHES: {match.groups()}")
            found_match = True
            break
        else:
            print(f"❌ Pattern {pattern_num}: No match")
    
    if not found_match:
        print(f"🚨 NO PATTERN MATCHED THIS LINE!")

print(f"\n🔬 Special Character Analysis")
print("=" * 40)

test_line = "Sun in Leo 22°30', in 9th House"
print(f"Analyzing: {test_line}")

for i, char in enumerate(test_line):
    if char in "°'":
        print(f"Position {i}: '{char}' (ord: {ord(char)})")

# Test simplified patterns
print(f"\n🛠️  Simplified Pattern Tests")
print("=" * 35)

simple_patterns = [
    r'(\w+)\s+in\s+(\w+)\s+(\d+)°(\d+)\'',
    r'(\w+)\s+in\s+(\w+)\s+(\d+)°(\d+)\',\s+in\s+(\d+)',
    r'(Sun|Moon|Mercury|Venus|Mars|Jupiter|Saturn)\s+in\s+(\w+)\s+(\d+)°(\d+)\',\s+in\s+(\d+)',
]

for i, pattern in enumerate(simple_patterns, 1):
    print(f"\nSimple Pattern {i}: {pattern}")
    match = re.search(pattern, test_line, re.IGNORECASE)
    if match:
        print(f"✅ MATCH: {match.groups()}")
    else:
        print(f"❌ No match")
        
# Test with exactly what we see
print(f"\n🎯 Exact String Test")
print("=" * 25)

exact_pattern = r'(\w+)\s+in\s+(\w+)\s+(\d+)°(\d+)\',\s+in\s+(\d+)(?:st|nd|rd|th)?\s+House'
exact_line = "Sun in Leo 22°30', in 9th House"

print(f"Pattern: {exact_pattern}")
print(f"Line:    {exact_line}")

import re
match = re.search(exact_pattern, exact_line, re.IGNORECASE)
if match:
    print(f"✅ SUCCESS: {match.groups()}")
else:
    print(f"❌ FAILED")
    # Try step by step
    print("Step by step analysis:")
    
    # Test each part
    parts = [
        (r'(\w+)', "Sun"),
        (r'\s+in\s+', " in "),  
        (r'(\w+)', "Leo"),
        (r'\s+', " "),
        (r'(\d+)', "22"),
        (r'°', "°"),
        (r'(\d+)', "30"),
        (r'\'', "'"),
        (r',\s+in\s+', ", in "),
        (r'(\d+)', "9"),
        (r'(?:st|nd|rd|th)?\s+House', "th House")
    ]
    
    test_string = exact_line
    position = 0
    
    for part_pattern, expected in parts:
        part_match = re.search(part_pattern, test_string[position:])
        if part_match:
            print(f"  ✅ '{part_pattern}' matches '{expected}' at pos {position}")
            position += part_match.end()
        else:
            print(f"  ❌ '{part_pattern}' failed to match '{expected}' at pos {position}")
            print(f"      Remaining text: '{test_string[position:]}'")
            break 