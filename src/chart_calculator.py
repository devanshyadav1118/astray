# src/chart_calculator.py
"""
Chart Calculator Module for Astrology AI - Phase 2 Implementation

This module will handle astronomical calculations for birth chart generation.
Currently a placeholder for future development.

Phase 2 Features (Future):
- Swiss Ephemeris integration for precise planetary positions
- Vedic chart calculation (D-1, D-9, D-10, etc.)
- Ayanamsa calculations
- House systems (Placidus, Equal House, etc.)
- Chart visualization and rendering
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, field
from pathlib import Path

# Import configuration
import sys
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

try:
    from settings import get_config
except ImportError:
    def get_config():
        return None

try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError as e:
    print("⚠️  Swiss Ephemeris not available.")
    print("This is likely due to architecture incompatibility (x86_64 vs ARM64).")
    print("For Apple Silicon Macs, try:")
    print("  conda install -c astropy pyswisseph")
    print("  OR")
    print("  arch -x86_64 pip install pyswisseph  # if using Rosetta")
    print()
    print("For now, using fallback calculation methods...")
    SWISSEPH_AVAILABLE = False
    swe = None

import pytz
from geopy.geocoders import Nominatim
import logging

logger = logging.getLogger(__name__)

@dataclass
class Location:
    """Birth location data"""
    latitude: float
    longitude: float
    city: str = ""
    country: str = ""
    timezone_str: str = ""

@dataclass
class PlanetaryPosition:
    """Individual planet position data"""
    longitude: float                       # Ecliptic longitude
    latitude: float                        # Ecliptic latitude  
    house: int                            # House placement (1-12)
    sign: str                             # Zodiac sign
    degree: float                         # Degree within sign (0-30)
    minute: float                         # Minute within degree
    second: float                         # Second within minute
    nakshatra: str                        # Nakshatra placement
    nakshatra_pada: int                   # Pada within nakshatra (1-4)
    retrograde: bool                      # Retrograde motion status
    speed: float                          # Daily motion in degrees

@dataclass
class NakshatraInfo:
    """Nakshatra information"""
    name: str
    pada: int
    lord: str
    degree_range: Tuple[float, float]

@dataclass
class ChartData:
    """Complete Vedic birth chart data"""
    # Birth Information
    birth_datetime: datetime
    birth_location: Location
    timezone: str
    
    # Planetary Positions
    planetary_positions: Dict[str, PlanetaryPosition]
    house_cusps: Dict[int, float]           # House cusp degrees
    ascendant: float                        # Lagna degree
    
    # Vedic Specific
    ayanamsa: float                        # Ayanamsa value used
    ayanamsa_name: str                     # Ayanamsa system used
    nakshatras: Dict[str, NakshatraInfo]   # Nakshatra placements
    
    # Calculation Metadata
    calculation_method: str                # Swiss Ephemeris details
    coordinate_system: str                 # Sidereal
    house_system: str                      # Whole Sign, Placidus, etc.
    calculation_timestamp: datetime = field(default_factory=datetime.now)
    accuracy_validated: bool = False

@dataclass
class ValidationResult:
    """Chart calculation validation results"""
    is_accurate: bool
    issues: List[str] = field(default_factory=list)
    confidence_score: float = 1.0
    validation_details: Dict = field(default_factory=dict)

class PersonalVedicChartCalculator:
    """
    High-precision Vedic chart calculator for personal use
    Optimized for accuracy and learning
    """
    
    def __init__(self):
        """Initialize calculator with Swiss Ephemeris if available"""
        
        # Check Swiss Ephemeris availability
        if not SWISSEPH_AVAILABLE:
            logger.warning("Swiss Ephemeris not available - using fallback methods")
            logger.warning("Chart accuracy may be reduced without Swiss Ephemeris")
            
        self.ephemeris_available = SWISSEPH_AVAILABLE
        
        # Initialize planet mappings based on availability
        if SWISSEPH_AVAILABLE:
            self.planet_mappings = {
                'Sun': swe.SUN,
                'Moon': swe.MOON,
                'Mercury': swe.MERCURY,
                'Venus': swe.VENUS,
                'Mars': swe.MARS,
                'Jupiter': swe.JUPITER,
                'Saturn': swe.SATURN,
                'Rahu': swe.MEAN_NODE,  # North Node
                'Ketu': swe.MEAN_NODE,  # South Node (calculated as opposite)
            }
        else:
            # Fallback mappings (just for reference, calculations will be different)
            self.planet_mappings = {
                'Sun': 0,
                'Moon': 1,
                'Mercury': 2,
                'Venus': 3,
                'Mars': 4,
                'Jupiter': 5,
                'Saturn': 6,
                'Rahu': 7,
                'Ketu': 8,
            }
        
        # Ayanamsa setting
        if SWISSEPH_AVAILABLE:
            swe.set_sid_mode(swe.SIDM_LAHIRI)  # Set Lahiri ayanamsa
        
        # House system (using whole sign houses for Vedic)
        self.house_system = b'W'  # Whole sign houses
        
        # Constants for calculations
        self.signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        self.nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
            'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
            'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
            'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
        ]
        
        self.nakshatra_lords = [
            'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu',
            'Jupiter', 'Saturn', 'Mercury', 'Ketu', 'Venus', 'Sun',
            'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury',
            'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu',
            'Jupiter', 'Saturn', 'Mercury'
        ]
        
        self.geocoder = Nominatim(user_agent="astrology_ai_personal")
        
        logger.info("PersonalVedicChartCalculator initialized with Swiss Ephemeris")
    
    def get_coordinates_for_location(self, location_string: str) -> Location:
        """Get coordinates for a location string"""
        try:
            location = self.geocoder.geocode(location_string)
            if location:
                return Location(
                    latitude=location.latitude,
                    longitude=location.longitude,
                    city=location_string,
                    timezone_str=self._get_timezone_for_coordinates(
                        location.latitude, location.longitude
                    )
                )
            else:
                raise ValueError(f"Could not find coordinates for: {location_string}")
        except Exception as e:
            logger.error(f"Geocoding failed for {location_string}: {e}")
            raise ValueError(f"Location lookup failed: {e}")
    
    def _get_timezone_for_coordinates(self, latitude: float, longitude: float) -> str:
        """Get timezone string for coordinates"""
        try:
            from timezonefinder import TimezoneFinder
            tf = TimezoneFinder()
            timezone_str = tf.timezone_at(lat=latitude, lng=longitude)
            return timezone_str or "UTC"
        except ImportError:
            logger.warning("timezonefinder not available, using UTC")
            return "UTC"
        except Exception as e:
            logger.warning(f"Timezone lookup failed: {e}, using UTC")
            return "UTC"
    
    def calculate_personal_chart(self, 
                               birth_datetime: datetime,
                               latitude: float, 
                               longitude: float,
                               location_name: str = "",
                               validate: bool = True) -> ChartData:
        """Generate highly accurate Vedic chart with validation"""
        
        logger.info(f"Calculating chart for {birth_datetime} at {latitude}, {longitude}")
        
        if not self.ephemeris_available:
            logger.error("Swiss Ephemeris not available - cannot calculate accurate chart")
            raise RuntimeError(
                "❌ Swiss Ephemeris Required for Chart Calculation\n\n"
                "Chart calculation requires Swiss Ephemeris for ±1 degree precision.\n"
                "This is essential for your astrology AI project accuracy.\n\n"
                "🔧 INSTALLATION SOLUTIONS:\n"
                "1. For Apple Silicon (M1/M2/M3) Macs:\n"
                "   conda install -c conda-forge pyswisseph\n"
                "   OR\n"
                "   arch -x86_64 pip install pyswisseph  # Use Rosetta\n\n"
                "2. For Intel Macs/Linux/Windows:\n"
                "   pip install pyswisseph\n\n"
                "3. Alternative: Use Docker with x86_64 image\n\n"
                "💡 TEMPORARY WORKAROUND:\n"
                "While fixing Swiss Ephemeris, you can use the web scraper:\n"
                "   python main.py chart scrape --birth-date 1990-05-15 --birth-time 10:30 --birth-location Delhi\n\n"
                "⚠️  However, web scraping goes against this project's philosophy:\n"
                "   • External dependencies (browser, internet)\n" 
                "   • Less accurate than Swiss Ephemeris\n"
                "   • Prone to breaking when websites change\n\n"
                "🎯 RECOMMENDED: Fix Swiss Ephemeris installation for:\n"
                "   • Self-contained calculations\n"
                "   • Professional astronomical accuracy\n"
                "   • No external dependencies\n"
                "   • Aligns with project philosophy"
            )
        
        try:
            # Convert to Julian Day for Swiss Ephemeris
            julian_day = self._datetime_to_julian_day(birth_datetime)
            
            # Set ayanamsa
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            ayanamsa = swe.get_ayanamsa(julian_day)
            
            # Calculate planetary positions
            planetary_positions = self._calculate_planetary_positions(julian_day)
            
            # Calculate houses
            house_cusps, ascendant = self._calculate_houses(julian_day, latitude, longitude)
            
            # Assign houses to planets
            self._assign_houses_to_planets(planetary_positions, house_cusps)
            
            # Calculate nakshatras
            nakshatras = self._calculate_nakshatras(planetary_positions)
            
            # Create chart data
            chart_data = ChartData(
                birth_datetime=birth_datetime,
                birth_location=Location(latitude, longitude, location_name),
                timezone=birth_datetime.tzinfo.zone if birth_datetime.tzinfo else "UTC",
                planetary_positions=planetary_positions,
                house_cusps=house_cusps,
                ascendant=ascendant,
                ayanamsa=ayanamsa,
                ayanamsa_name="Lahiri",
                nakshatras=nakshatras,
                calculation_method="Swiss Ephemeris",
                coordinate_system="Sidereal",
                house_system="Whole Sign"
            )
            
            # Validate accuracy if requested
            if validate:
                validation_result = self._validate_chart_accuracy(chart_data)
                chart_data.accuracy_validated = validation_result.is_accurate
                
                if not validation_result.is_accurate:
                    logger.warning(f"Chart accuracy validation issues: {validation_result.issues}")
            
            logger.info("Chart calculation completed successfully")
            return chart_data
            
        except Exception as e:
            logger.error(f"Chart calculation failed: {e}")
            raise RuntimeError(f"Chart calculation failed: {e}")
    
    def _datetime_to_julian_day(self, dt: datetime) -> float:
        """Convert datetime to Julian Day for Swiss Ephemeris"""
        
        # Ensure datetime is timezone-aware
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        # Convert to UTC for calculations
        utc_dt = dt.astimezone(timezone.utc)
        
        # Calculate Julian Day
        julian_day = swe.julday(
            utc_dt.year, utc_dt.month, utc_dt.day,
            utc_dt.hour + utc_dt.minute/60 + utc_dt.second/3600
        )
        
        return julian_day
    
    def _calculate_planetary_positions(self, julian_day: float) -> Dict[str, PlanetaryPosition]:
        """Calculate positions for all planets"""
        
        positions = {}
        
        for planet_name, planet_id in self.planet_mappings.items():
            if planet_name == 'Ketu':
                # Calculate Ketu as Rahu + 180 degrees
                rahu_pos = positions.get('Rahu')
                if rahu_pos:
                    ketu_long = (rahu_pos.longitude + 180) % 360
                    positions[planet_name] = PlanetaryPosition(
                        longitude=ketu_long,
                        latitude=0,  # Nodes have 0 latitude
                        house=0,  # Will be assigned later
                        sign=self._longitude_to_sign(ketu_long),
                        degree=ketu_long % 30,
                        minute=(ketu_long % 1) * 60,
                        second=((ketu_long % 1) * 60 % 1) * 60,
                        nakshatra="",  # Will be calculated later
                        nakshatra_pada=0,
                        retrograde=False,  # Ketu motion follows Rahu
                        speed=0  # Will be calculated
                    )
                continue
            
            try:
                # Calculate planet position
                result = swe.calc_ut(julian_day, planet_id, swe.FLG_SIDEREAL)
                
                longitude = result[0][0]  # Sidereal longitude
                latitude = result[0][1]   # Latitude
                speed = result[0][3]      # Daily motion
                
                # Check if retrograde (negative speed for most planets)
                retrograde = speed < 0 if planet_name not in ['Rahu', 'Ketu'] else speed > 0
                
                positions[planet_name] = PlanetaryPosition(
                    longitude=longitude,
                    latitude=latitude,
                    house=0,  # Will be assigned later
                    sign=self._longitude_to_sign(longitude),
                    degree=longitude % 30,
                    minute=(longitude % 1) * 60,
                    second=((longitude % 1) * 60 % 1) * 60,
                    nakshatra="",  # Will be calculated later
                    nakshatra_pada=0,
                    retrograde=retrograde,
                    speed=abs(speed)
                )
                
            except Exception as e:
                logger.error(f"Failed to calculate position for {planet_name}: {e}")
                raise
        
        return positions
    
    def _calculate_houses(self, julian_day: float, latitude: float, longitude: float) -> Tuple[Dict[int, float], float]:
        """Calculate house cusps and ascendant"""
        
        try:
            # Calculate houses using Swiss Ephemeris
            houses = swe.houses(julian_day, latitude, longitude, self.house_system)
            
            house_cusps = {}
            cusps = houses[0]  # House cusps
            ascendant = cusps[0]  # 1st house cusp = Ascendant
            
            # Convert to sidereal using current ayanamsa
            ayanamsa = swe.get_ayanamsa(julian_day)
            
            for i in range(12):
                sidereal_cusp = (cusps[i] - ayanamsa) % 360
                house_cusps[i + 1] = sidereal_cusp
            
            sidereal_ascendant = (ascendant - ayanamsa) % 360
            
            return house_cusps, sidereal_ascendant
            
        except Exception as e:
            logger.error(f"House calculation failed: {e}")
            raise
    
    def _assign_houses_to_planets(self, planetary_positions: Dict[str, PlanetaryPosition], house_cusps: Dict[int, float]):
        """Assign house numbers to planets based on their positions"""
        
        for planet_name, position in planetary_positions.items():
            planet_long = position.longitude
            
            # Find which house the planet is in
            for house in range(1, 13):
                current_cusp = house_cusps[house]
                next_house = (house % 12) + 1
                next_cusp = house_cusps[next_house]
                
                # Handle wraparound at 360/0 degrees
                if current_cusp <= next_cusp:
                    if current_cusp <= planet_long < next_cusp:
                        position.house = house
                        break
                else:  # Wraparound case
                    if planet_long >= current_cusp or planet_long < next_cusp:
                        position.house = house
                        break
    
    def _calculate_nakshatras(self, planetary_positions: Dict[str, PlanetaryPosition]) -> Dict[str, NakshatraInfo]:
        """Calculate nakshatra placements for all planets"""
        
        nakshatras = {}
        
        for planet_name, position in planetary_positions.items():
            nakshatra_info = self._longitude_to_nakshatra(position.longitude)
            nakshatras[planet_name] = nakshatra_info
            
            # Update planet position with nakshatra info
            position.nakshatra = nakshatra_info.name
            position.nakshatra_pada = nakshatra_info.pada
        
        return nakshatras
    
    def _longitude_to_sign(self, longitude: float) -> str:
        """Convert longitude to zodiac sign"""
        sign_index = int(longitude // 30)
        return self.signs[sign_index % 12]
    
    def _longitude_to_nakshatra(self, longitude: float) -> NakshatraInfo:
        """Convert longitude to nakshatra and pada"""
        
        # Each nakshatra is 13°20' (800 minutes)
        # Total 27 nakshatras = 360°
        nakshatra_size = 360 / 27  # 13.333... degrees
        pada_size = nakshatra_size / 4  # 3.333... degrees per pada
        
        nakshatra_index = int(longitude / nakshatra_size)
        pada_index = int((longitude % nakshatra_size) / pada_size) + 1
        
        nakshatra_name = self.nakshatras[nakshatra_index]
        nakshatra_lord = self.nakshatra_lords[nakshatra_index]
        
        start_degree = nakshatra_index * nakshatra_size
        end_degree = start_degree + nakshatra_size
        
        return NakshatraInfo(
            name=nakshatra_name,
            pada=pada_index,
            lord=nakshatra_lord,
            degree_range=(start_degree, end_degree)
        )
    
    def _validate_chart_accuracy(self, chart: ChartData) -> ValidationResult:
        """Validate chart calculation accuracy"""
        
        issues = []
        validation_details = {}
        
        # Check planetary positions are within expected ranges
        for planet, position in chart.planetary_positions.items():
            if not (0 <= position.longitude <= 360):
                issues.append(f"{planet} longitude out of range: {position.longitude}")
                
            if position.house < 1 or position.house > 12:
                issues.append(f"{planet} house assignment invalid: {position.house}")
        
        # Validate house cusp calculations
        house_cusps = list(chart.house_cusps.values())
        for i in range(12):
            cusp = house_cusps[i]
            if not (0 <= cusp <= 360):
                issues.append(f"House {i+1} cusp out of range: {cusp}")
        
        # Check ascendant
        if not (0 <= chart.ascendant <= 360):
            issues.append(f"Ascendant out of range: {chart.ascendant}")
        
        # Validate nakshatra calculations
        for planet, nakshatra_info in chart.nakshatras.items():
            if nakshatra_info.name not in self.nakshatras:
                issues.append(f"Unknown nakshatra for {planet}: {nakshatra_info.name}")
            
            if not (1 <= nakshatra_info.pada <= 4):
                issues.append(f"Invalid pada for {planet}: {nakshatra_info.pada}")
        
        # Calculate confidence score
        confidence_score = max(0.0, 1.0 - (len(issues) * 0.1))
        
        validation_details = {
            "total_planets_calculated": len(chart.planetary_positions),
            "ayanamsa_value": chart.ayanamsa,
            "calculation_method": chart.calculation_method,
            "house_system": chart.house_system
        }
        
        return ValidationResult(
            is_accurate=len(issues) == 0,
            issues=issues,
            confidence_score=confidence_score,
            validation_details=validation_details
        )
    
    def format_chart_for_display(self, chart: ChartData) -> str:
        """Format chart data for readable display"""
        
        output = []
        output.append("=" * 60)
        output.append("VEDIC BIRTH CHART - PERSONAL ANALYSIS")
        output.append("=" * 60)
        
        # Birth details
        output.append(f"\nBirth Details:")
        output.append(f"Date & Time: {chart.birth_datetime}")
        output.append(f"Location: {chart.birth_location.city} ({chart.birth_location.latitude:.4f}, {chart.birth_location.longitude:.4f})")
        output.append(f"Timezone: {chart.timezone}")
        output.append(f"Ayanamsa: {chart.ayanamsa_name} ({chart.ayanamsa:.4f}°)")
        
        # Ascendant
        output.append(f"\nAscendant (Lagna): {chart.ascendant:.2f}° ({self._longitude_to_sign(chart.ascendant)})")
        
        # Planetary positions
        output.append(f"\nPlanetary Positions:")
        output.append("-" * 40)
        
        for planet, pos in chart.planetary_positions.items():
            retro_marker = " (R)" if pos.retrograde else ""
            output.append(
                f"{planet:8} | {pos.longitude:7.2f}° | {pos.sign:11} | "
                f"House {pos.house:2d} | {pos.nakshatra:15} {pos.nakshatra_pada}/4{retro_marker}"
            )
        
        # House cusps
        output.append(f"\nHouse Cusps:")
        output.append("-" * 30)
        
        for house, cusp in chart.house_cusps.items():
            sign = self._longitude_to_sign(cusp)
            output.append(f"House {house:2d}: {cusp:7.2f}° ({sign})")
        
        # Calculation metadata
        output.append(f"\nCalculation Details:")
        output.append(f"Method: {chart.calculation_method}")
        output.append(f"Coordinate System: {chart.coordinate_system}")
        output.append(f"House System: {chart.house_system}")
        output.append(f"Accuracy Validated: {'✅' if chart.accuracy_validated else '❌'}")
        output.append(f"Calculated: {chart.calculation_timestamp}")
        
        output.append("=" * 60)
        
        return "\n".join(output)

# Example usage function
def calculate_sample_chart():
    """Example function showing how to use the calculator"""
    
    calculator = PersonalVedicChartCalculator()
    
    # Example birth data (replace with your own)
    birth_datetime = datetime(1990, 5, 15, 10, 30, 0, tzinfo=pytz.timezone('Asia/Kolkata'))
    latitude = 28.6139  # New Delhi
    longitude = 77.2090
    
    try:
        chart = calculator.calculate_personal_chart(
            birth_datetime=birth_datetime,
            latitude=latitude,
            longitude=longitude,
            location_name="New Delhi, India",
            validate=True
        )
        
        print(calculator.format_chart_for_display(chart))
        
        return chart
        
    except Exception as e:
        print(f"Chart calculation failed: {e}")
        return None

if __name__ == "__main__":
    # Demo the calculator
    calculate_sample_chart()
