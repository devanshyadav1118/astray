"""
Chart Data Manager - File-based chart data system
Replaces web scraping and complex calculations with simple file-based input
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict, fields

from .data_models import BirthChart, PlanetaryPosition, HouseInfo


@dataclass
class SimpleChartData:
    """Simplified chart data structure for manual input"""
    name: str
    birth_date: str  # "1990-01-15"
    birth_time: str  # "14:30"
    birth_location: str  # "New Delhi, India"
    
    # Planetary positions - simple format
    planets: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    # Example: {"Sun": {"sign": "Capricorn", "house": 1, "degree": 25.5}}
    
    # House information
    houses: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    # Example: {1: {"sign": "Capricorn", "lord": "Saturn"}}
    
    # Basic chart info
    ascendant: str = ""
    moon_sign: str = ""
    sun_sign: str = ""
    
    # Extended ascendant info (optional)
    ascendant_longitude: str = ""
    ascendant_nakshatra: str = ""
    ascendant_pada: int = 0
    
    # Optional metadata
    notes: str = ""
    source: str = "Manual Input"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON/YAML export"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimpleChartData':
        """Create from dictionary loaded from JSON/YAML - ignores unknown fields"""
        # Get the field names that the class expects
        field_names = {f.name for f in fields(cls)}
        
        # Filter the data to only include known fields
        filtered_data = {k: v for k, v in data.items() if k in field_names}
        
        return cls(**filtered_data)


class ChartDataManager:
    """Manages chart data files - replaces web scraping and calculations"""
    
    def __init__(self, charts_directory: Path = None):
        self.charts_dir = charts_directory or Path("data/charts")
        self.charts_dir.mkdir(parents=True, exist_ok=True)
        
        # Create templates directory
        self.templates_dir = self.charts_dir / "templates"
        self.templates_dir.mkdir(exist_ok=True)
        
        # Ensure templates exist
        self._create_templates()
    
    def _create_templates(self):
        """Create template files for easy chart creation"""
        
        # JSON template
        json_template = {
            "name": "Sample Person",
            "birth_date": "1990-01-15",
            "birth_time": "14:30",
            "birth_location": "New Delhi, India",
            "planets": {
                "Sun": {"sign": "Capricorn", "house": 1, "degree": 25.5},
                "Moon": {"sign": "Scorpio", "house": 11, "degree": 12.3},
                "Mars": {"sign": "Sagittarius", "house": 12, "degree": 8.7},
                "Mercury": {"sign": "Capricorn", "house": 1, "degree": 15.2},
                "Jupiter": {"sign": "Gemini", "house": 6, "degree": 22.8},
                "Venus": {"sign": "Aquarius", "house": 2, "degree": 5.4},
                "Saturn": {"sign": "Capricorn", "house": 1, "degree": 18.9},
                "Rahu": {"sign": "Aquarius", "house": 2, "degree": 28.1},
                "Ketu": {"sign": "Leo", "house": 8, "degree": 28.1}
            },
            "houses": {
                1: {"sign": "Capricorn", "lord": "Saturn"},
                2: {"sign": "Aquarius", "lord": "Saturn"},
                3: {"sign": "Pisces", "lord": "Jupiter"},
                4: {"sign": "Aries", "lord": "Mars"},
                5: {"sign": "Taurus", "lord": "Venus"},
                6: {"sign": "Gemini", "lord": "Mercury"},
                7: {"sign": "Cancer", "lord": "Moon"},
                8: {"sign": "Leo", "lord": "Sun"},
                9: {"sign": "Virgo", "lord": "Mercury"},
                10: {"sign": "Libra", "lord": "Venus"},
                11: {"sign": "Scorpio", "lord": "Mars"},
                12: {"sign": "Sagittarius", "lord": "Jupiter"}
            },
            "ascendant": "Capricorn",
            "moon_sign": "Scorpio",
            "sun_sign": "Capricorn",
            "notes": "Sample chart for demonstration",
            "source": "Manual Input"
        }
        
        json_template_path = self.templates_dir / "chart_template.json"
        if not json_template_path.exists():
            with open(json_template_path, 'w') as f:
                json.dump(json_template, f, indent=2)
        
        # YAML template
        yaml_template_path = self.templates_dir / "chart_template.yaml"
        if not yaml_template_path.exists():
            with open(yaml_template_path, 'w') as f:
                yaml.dump(json_template, f, default_flow_style=False, sort_keys=False)
        
        # Simple text template
        text_template = """# Simple Chart Data Template
# Copy this template and fill in your chart details

Name: Sample Person
Birth Date: 1990-01-15
Birth Time: 14:30
Birth Location: New Delhi, India

# Planetary Positions (Planet: Sign, House, Degree)
Sun: Capricorn, 1, 25.5
Moon: Scorpio, 11, 12.3
Mars: Sagittarius, 12, 8.7
Mercury: Capricorn, 1, 15.2
Jupiter: Gemini, 6, 22.8
Venus: Aquarius, 2, 5.4
Saturn: Capricorn, 1, 18.9
Rahu: Aquarius, 2, 28.1
Ketu: Leo, 8, 28.1

# House Signs (House: Sign, Lord)
1: Capricorn, Saturn
2: Aquarius, Saturn
3: Pisces, Jupiter
4: Aries, Mars
5: Taurus, Venus
6: Gemini, Mercury
7: Cancer, Moon
8: Leo, Sun
9: Virgo, Mercury
10: Libra, Venus
11: Scorpio, Mars
12: Sagittarius, Jupiter

# Basic Info
Ascendant: Capricorn
Moon Sign: Scorpio
Sun Sign: Capricorn

# Notes
Notes: Sample chart for demonstration
Source: Manual Input
"""
        
        text_template_path = self.templates_dir / "chart_template.txt"
        if not text_template_path.exists():
            with open(text_template_path, 'w') as f:
                f.write(text_template)
    
    def load_chart(self, filename: str) -> Optional[SimpleChartData]:
        """Load chart from file (supports JSON, YAML, or TXT format)"""
        
        file_path = self.charts_dir / filename
        if not file_path.exists():
            return None
        
        try:
            if filename.endswith('.json'):
                return self._load_json_chart(file_path)
            elif filename.endswith(('.yaml', '.yml')):
                return self._load_yaml_chart(file_path)
            elif filename.endswith('.txt'):
                return self._load_text_chart(file_path)
            else:
                raise ValueError(f"Unsupported file format: {filename}")
                
        except Exception as e:
            print(f"Error loading chart from {filename}: {e}")
            return None
    
    def _load_json_chart(self, file_path: Path) -> SimpleChartData:
        """Load chart from JSON file"""
        with open(file_path, 'r') as f:
            data = json.load(f)
        return SimpleChartData.from_dict(data)
    
    def _load_yaml_chart(self, file_path: Path) -> SimpleChartData:
        """Load chart from YAML file"""
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        return SimpleChartData.from_dict(data)
    
    def _load_text_chart(self, file_path: Path) -> SimpleChartData:
        """Load chart from simple text format"""
        chart_data = {
            "planets": {},
            "houses": {},
            "name": "",
            "birth_date": "",
            "birth_time": "",
            "birth_location": "",
            "ascendant": "",
            "moon_sign": "",
            "sun_sign": "",
            "notes": "",
            "source": "Manual Input"
        }
        
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Basic info
                if key.lower() == 'name':
                    chart_data['name'] = value
                elif key.lower() == 'birth date':
                    chart_data['birth_date'] = value
                elif key.lower() == 'birth time':
                    chart_data['birth_time'] = value
                elif key.lower() == 'birth location':
                    chart_data['birth_location'] = value
                elif key.lower() == 'ascendant':
                    chart_data['ascendant'] = value
                elif key.lower() == 'moon sign':
                    chart_data['moon_sign'] = value
                elif key.lower() == 'sun sign':
                    chart_data['sun_sign'] = value
                elif key.lower() == 'notes':
                    chart_data['notes'] = value
                
                # Planetary positions
                elif key in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']:
                    parts = [p.strip() for p in value.split(',')]
                    if len(parts) >= 3:
                        chart_data['planets'][key] = {
                            'sign': parts[0],
                            'house': int(parts[1]),
                            'degree': float(parts[2]) if parts[2].replace('.', '').isdigit() else 0.0
                        }
                
                # House information
                elif key.isdigit():
                    house_num = int(key)
                    parts = [p.strip() for p in value.split(',')]
                    if len(parts) >= 2:
                        chart_data['houses'][house_num] = {
                            'sign': parts[0],
                            'lord': parts[1]
                        }
        
        return SimpleChartData.from_dict(chart_data)
    
    def save_chart(self, chart_data: SimpleChartData, filename: str, format: str = 'json'):
        """Save chart to file in specified format"""
        
        if format == 'json':
            file_path = self.charts_dir / f"{filename}.json"
            with open(file_path, 'w') as f:
                json.dump(chart_data.to_dict(), f, indent=2)
        
        elif format in ['yaml', 'yml']:
            file_path = self.charts_dir / f"{filename}.yaml"
            with open(file_path, 'w') as f:
                yaml.dump(chart_data.to_dict(), f, default_flow_style=False)
        
        return file_path
    
    def list_available_charts(self) -> List[str]:
        """List all available chart files"""
        charts = []
        for file_path in self.charts_dir.glob("*"):
            if file_path.is_file() and file_path.suffix in ['.json', '.yaml', '.yml', '.txt']:
                if file_path.parent.name != 'templates':  # Exclude templates
                    charts.append(file_path.name)
        return sorted(charts)
    
    def convert_to_birth_chart(self, simple_chart: SimpleChartData) -> BirthChart:
        """Convert SimpleChartData to BirthChart format for compatibility"""
        
        # Parse datetime
        birth_datetime = datetime.fromisoformat(f"{simple_chart.birth_date}T{simple_chart.birth_time}:00")
        
        # Convert planetary positions
        planetary_positions = {}
        for planet, data in simple_chart.planets.items():
            planetary_positions[planet] = PlanetaryPosition(
                planet=planet,
                sign=data['sign'],
                house=data['house'],
                degree=data.get('degree', 0.0)
            )
        
        # Convert houses
        houses = {}
        for house_num, data in simple_chart.houses.items():
            houses[house_num] = HouseInfo(
                house_number=house_num,
                sign=data['sign'],
                house_lord=data['lord']
            )
        
        return BirthChart(
            birth_datetime=birth_datetime,
            latitude=0.0,  # Not used in this simplified system
            longitude=0.0,  # Not used in this simplified system
            timezone="UTC",  # Default
            planetary_positions=planetary_positions,
            houses=houses,
            ascendant=simple_chart.ascendant
        )
    
    def display_chart_summary(self, chart_data: SimpleChartData) -> str:
        """Create a formatted display of chart data"""
        
        output = []
        output.append("=" * 60)
        output.append(f"🌟 BIRTH CHART: {chart_data.name}")
        output.append("=" * 60)
        output.append(f"📅 Birth: {chart_data.birth_date} at {chart_data.birth_time}")
        output.append(f"📍 Location: {chart_data.birth_location}")
        output.append(f"🌅 Ascendant: {chart_data.ascendant}")
        output.append(f"🌙 Moon Sign: {chart_data.moon_sign}")
        output.append(f"☀️  Sun Sign: {chart_data.sun_sign}")
        output.append("")
        
        output.append("🪐 PLANETARY POSITIONS:")
        output.append("-" * 40)
        for planet, data in chart_data.planets.items():
            output.append(f"{planet:8} | {data['sign']:12} | House {data['house']:2} | {data['degree']:6.1f}°")
        
        output.append("")
        output.append("🏠 HOUSE CUSPS:")
        output.append("-" * 40)
        for house_num, data in chart_data.houses.items():
            output.append(f"House {house_num:2} | {data['sign']:12} | Lord: {data['lord']}")
        
        if chart_data.notes:
            output.append("")
            output.append(f"📝 Notes: {chart_data.notes}")
        
        output.append("")
        output.append(f"📚 Source: {chart_data.source}")
        output.append("=" * 60)
        
        return "\n".join(output)
    
    def parse_chart_from_text_format(self, chart_text: str, name: str = "Imported Chart", 
                                   birth_date: str = "", birth_time: str = "", 
                                   birth_location: str = "") -> SimpleChartData:
        """Parse chart from the specific text format provided by user"""
        
        chart_data = {
            "name": name,
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": birth_location,
            "planets": {},
            "houses": {},
            "ascendant": "",
            "moon_sign": "",
            "sun_sign": "",
            "notes": "Imported from text format",
            "source": "Manual Import"
        }
        
        # Mapping from the text format to our internal planet names
        planet_mapping = {
            "Sun": "Sun",
            "Moon": "Moon", 
            "Mercury": "Mercury",
            "Venus": "Venus",
            "Mars": "Mars",
            "Jupiter": "Jupiter",
            "Saturn": "Saturn",
            "Uranus": "Uranus",  # Western astrology
            "Neptune": "Neptune", # Western astrology
            "Pluto": "Pluto",    # Western astrology
            "Node": "Rahu",      # North Node = Rahu
            "Lilith": "Lilith",  # Keep as is
            "Chiron": "Chiron",  # Keep as is
            "Fortune": "Fortune", # Part of Fortune
            "Vertex": "Vertex"   # Keep as is
        }
        
        # Traditional Vedic planets we want to focus on
        core_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
        
        lines = chart_text.strip().split('\n')
        house_number = 1
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split(',')
            if len(parts) < 3:
                continue
                
            planet_name = parts[0].strip()
            sign = parts[1].strip()
            position_str = parts[2].strip()
            
            # Check for retrograde indicator
            retrograde = False
            if len(parts) > 3 and 'R' in parts[3]:
                retrograde = True
            elif 'R' in position_str:
                retrograde = True
                position_str = position_str.replace(',R', '').replace('R', '').strip()
            
            # Parse degree and minute
            try:
                if '°' in position_str and '\'' in position_str:
                    degree_part = position_str.split('°')[0]
                    minute_part = position_str.split('°')[1].replace('\'', '')
                    
                    degree = float(degree_part)
                    minute = float(minute_part) if minute_part else 0.0
                    total_degree = degree + (minute / 60.0)
                else:
                    total_degree = 0.0
            except:
                total_degree = 0.0
            
            # Handle special cases
            if planet_name == "ASC":
                chart_data["ascendant"] = sign
                continue
            elif planet_name == "MC":
                # Midheaven - can be stored as additional info
                continue
            elif planet_name.startswith("H"):
                # House cusp - extract house number
                try:
                    house_num = int(planet_name[1:])
                    chart_data["houses"][house_num] = {
                        "sign": sign,
                        "lord": self._get_house_lord(sign)
                    }
                except:
                    pass
                continue
            
            # Map planet name
            if planet_name in planet_mapping:
                internal_name = planet_mapping[planet_name]
                
                chart_data["planets"][internal_name] = {
                    "sign": sign,
                    "house": 1,  # Will be calculated after all data is parsed
                    "degree": total_degree,
                    "retrograde": retrograde
                }
        
        # Add Rahu/Ketu if we have Node
        if "Rahu" in chart_data["planets"]:
            rahu_data = chart_data["planets"]["Rahu"]
            # Ketu is always opposite to Rahu (180 degrees)
            ketu_sign = self._get_opposite_sign(rahu_data["sign"])
            
            chart_data["planets"]["Ketu"] = {
                "sign": ketu_sign,
                "house": 1,  # Will be calculated later
                "degree": rahu_data["degree"],
                "retrograde": True  # Ketu is always retrograde
            }
        
        # Set sun and moon signs
        if "Sun" in chart_data["planets"]:
            chart_data["sun_sign"] = chart_data["planets"]["Sun"]["sign"]
        if "Moon" in chart_data["planets"]:
            chart_data["moon_sign"] = chart_data["planets"]["Moon"]["sign"]
        
        # Fill missing houses with default signs
        if not chart_data["houses"]:
            self._fill_default_houses(chart_data, chart_data.get("ascendant", "Aries"))
        
        # Now calculate correct houses for all planets
        self._calculate_all_planet_houses(chart_data)
        
        return SimpleChartData.from_dict(chart_data)
    
    def _get_house_lord(self, sign: str) -> str:
        """Get the ruling planet for a zodiac sign"""
        lords = {
            "Aries": "Mars", "Taurus": "Venus", "Gemini": "Mercury",
            "Cancer": "Moon", "Leo": "Sun", "Virgo": "Mercury",
            "Libra": "Venus", "Scorpio": "Mars", "Sagittarius": "Jupiter",
            "Capricorn": "Saturn", "Aquarius": "Saturn", "Pisces": "Jupiter"
        }
        return lords.get(sign, "Unknown")
    
    def _calculate_house_from_sign(self, planet_sign: str, ascendant_sign: str) -> int:
        """Calculate house number based on planet sign and ascendant"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        try:
            planet_index = signs.index(planet_sign)
            ascendant_index = signs.index(ascendant_sign)
            
            # Calculate house (1-12)
            # The ascendant sign becomes the 1st house
            house = ((planet_index - ascendant_index) % 12) + 1
            return house
        except ValueError:
            return 1  # Default to 1st house if calculation fails
    
    def _get_opposite_sign(self, sign: str) -> str:
        """Get the opposite sign (for Ketu calculation)"""
        opposites = {
            "Aries": "Libra", "Taurus": "Scorpio", "Gemini": "Sagittarius",
            "Cancer": "Capricorn", "Leo": "Aquarius", "Virgo": "Pisces",
            "Libra": "Aries", "Scorpio": "Taurus", "Sagittarius": "Gemini",
            "Capricorn": "Cancer", "Aquarius": "Leo", "Pisces": "Virgo"
        }
        return opposites.get(sign, "Aries")
    
    def _fill_default_houses(self, chart_data: dict, ascendant: str):
        """Fill houses with default signs based on ascendant"""
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        try:
            start_index = signs.index(ascendant)
            for i in range(12):
                house_num = i + 1
                sign_index = (start_index + i) % 12
                sign = signs[sign_index]
                
                if house_num not in chart_data["houses"]:
                    chart_data["houses"][house_num] = {
                        "sign": sign,
                        "lord": self._get_house_lord(sign)
                    }
        except ValueError:
            # Fallback if ascendant not found
            for i in range(12):
                house_num = i + 1
                if house_num not in chart_data["houses"]:
                    chart_data["houses"][house_num] = {
                        "sign": signs[i % 12],
                        "lord": self._get_house_lord(signs[i % 12])
                    }
    
    def _calculate_all_planet_houses(self, chart_data: dict):
        """Calculate correct houses for all planets"""
        for planet, data in chart_data["planets"].items():
            if planet in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]:
                sign = data["sign"]
                house = self._calculate_house_from_sign(sign, chart_data["ascendant"])
                data["house"] = house
        
        # Ensure all houses are filled
        for house_num in range(1, 13):
            if house_num not in chart_data["houses"]:
                self._fill_default_houses(chart_data, chart_data["ascendant"]) 