# 🚀 Quick Reference Guide - Astrology AI Commands

## System Commands
```bash
# Test system setup
python main.py cli test-setup

# Show configuration
python main.py config

# Initial setup
python main.py setup

# Demo functionality
python main.py demo
```

## Phase 1: Knowledge Base Commands
```bash
# Process a single book
python main.py cli process-book data/books/book.pdf \
  --source-title "Book Title" \
  --author "Author Name" \
  --authority classical \
  --extract-rules

# Batch process books
python main.py cli batch-process data/books/ \
  --authority classical \
  --extract-rules

# Show statistics
python main.py cli stats

# Search rules
python main.py cli search-rules --planet Mars --house 7
python main.py cli search-rules --planet Jupiter --min-confidence 0.8
python main.py cli search-rules --source "Book Title"

# Export knowledge
python main.py cli export-knowledge --output knowledge.json
```

## Phase 2: Chart Commands
```bash
# Demo chart functionality
python main.py cli chart demo

# Create chart template
python main.py cli chart create-template --name my_chart --format json

# Import chart from text file
python main.py cli chart import \
  --file my_chart.txt \
  --name "My_Chart" \
  --birth-date "1990-01-15" \
  --birth-time "14:30" \
  --birth-location "New Delhi, India"

# List all charts
python main.py cli chart list

# Load and display chart
python main.py cli chart load My_Chart.json

# Validate chart
python main.py cli chart validate My_Chart.json

# Interpret chart (automatically saves to file)
python main.py cli chart interpret My_Chart.json
python main.py cli chart interpret My_Chart.json --category career
python main.py cli chart interpret My_Chart.json --detailed

# Convert chart format
python main.py cli chart convert My_Chart.json --to-format yaml

# List saved interpretation files
python main.py cli chart outputs
python main.py cli chart outputs --chart-name Devansh --detailed
python main.py cli chart outputs --category career
```

## 📄 Output File Management

### Automatic File Saving
Every chart interpretation automatically saves to:
```
data/output/interpretations/{ChartName}_{YYYYMMDD_HHMMSS}_{category}_{detailed}.txt
```

### Examples:
- `Devansh_Yadav_20250605_093232.txt` - Complete analysis
- `Devansh_Yadav_20250605_093237_career_detailed.txt` - Detailed career analysis  
- `Devansh_Yadav_20250605_093241_wealth.txt` - Wealth analysis

### Managing Output Files:
```bash
# List all interpretation files
python main.py cli chart outputs

# Filter by chart name
python main.py cli chart outputs --chart-name Devansh

# Filter by category
python main.py cli chart outputs --category career

# Show detailed info with content preview
python main.py cli chart outputs --detailed

# View a specific file
cat data/output/interpretations/filename.txt
```

## Chart Text Format
```
Sun,Taurus,11°28'
Moon,Pisces,26°36'
Mercury,Aries,18°55'
Venus,Aries,18°57'
Mars,Capricorn,26°02'
Jupiter,Cancer,18°09'
Saturn,Gemini,5°05'
Uranus,Aquarius,8°52'
Neptune,Capricorn,19°15',R
Pluto,Scorpio,25°04',R
Node,Taurus,5°23',R
ASC,Gemini,0°00'
MC,Aquarius,16°05'
```

## Important Notes
- All commands start with `python main.py cli`
- Chart interpretations automatically save timestamped files
- Use the exact format for planet positions
- Add `,R` for retrograde planets
- Include `ASC` for Ascendant and `MC` for Midheaven
- Birth details are optional but recommended for full functionality
- Output files are organized chronologically and by category 