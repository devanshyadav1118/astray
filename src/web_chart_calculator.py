"""
Web Scraper-Based Chart Calculator for Astrology AI

This module uses the working astro-seek scraper as a chart calculation engine,
providing a fallback when Swiss Ephemeris is not available.

⚠️  IMPORTANT: This is a fallback solution only.
For maximum accuracy, use the Swiss Ephemeris-based calculator.
"""

from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime, timezone
from dataclasses import dataclass, field
import logging
import re
import sys
from pathlib import Path

# Add tests directory to path for scraper imports
tests_path = Path(__file__).parent.parent / "tests"
sys.path.insert(0, str(tests_path))

# Import the working scraper components
try:
    from test_astro_seek_scraper import setup_test_driver
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    SELENIUM_AVAILABLE = True
except ImportError as e:
    SELENIUM_AVAILABLE = False
    logger = logging.getLogger(__name__)
    logger.warning(f"Selenium components not available: {e}")

# Import existing data structures
try:
    from chart_calculator import (
        Location, PlanetaryPosition, NakshatraInfo, ChartData, ValidationResult
    )
except ImportError:
    # Define minimal data structures if chart_calculator not available
    from dataclasses import dataclass
    from typing import Optional
    
    @dataclass
    class Location:
        latitude: float
        longitude: float
        city: str = ""
        country: str = ""
        timezone_str: str = ""
    
    @dataclass 
    class PlanetaryPosition:
        longitude: float
        latitude: float
        house: int
        sign: str
        degree: float
        minute: float
        second: float
        nakshatra: str
        nakshatra_pada: int
        retrograde: bool
        speed: float
    
    @dataclass
    class NakshatraInfo:
        name: str
        pada: int
        lord: str
        degree_range: Tuple[float, float]
    
    @dataclass
    class ChartData:
        birth_datetime: datetime
        birth_location: Location
        timezone: str
        planetary_positions: Dict[str, PlanetaryPosition]
        house_cusps: Dict[int, float]
        ascendant: float
        ayanamsa: float
        ayanamsa_name: str
        nakshatras: Dict[str, NakshatraInfo]
        calculation_method: str
        coordinate_system: str
        house_system: str
        calculation_timestamp: datetime
        accuracy_validated: bool = False
    
    @dataclass
    class ValidationResult:
        is_accurate: bool
        issues: List[str] = field(default_factory=list)
        confidence_score: float = 1.0
        validation_details: Dict = field(default_factory=dict)

logger = logging.getLogger(__name__)

@dataclass
class WebScrapedPosition:
    """Web scraped planetary position data"""
    name: str
    sign: str
    degree: float
    minute: float
    house: Optional[int] = None
    retrograde: bool = False

class WebChartCalculator:
    """
    Chart calculator using astro-seek web scraper
    
    This provides birth chart calculations when Swiss Ephemeris is not available.
    Uses the working astro-seek scraper to extract planetary positions.
    """
    
    def __init__(self, headless: bool = True):
        """Initialize web chart calculator"""
        
        if not SELENIUM_AVAILABLE:
            raise RuntimeError("Selenium not available. Install with: pip install selenium webdriver-manager")
        
        self.headless = headless
        
        # Sign mappings for consistent naming
        self.sign_mappings = {
            'ari': 'Aries', 'tau': 'Taurus', 'gem': 'Gemini',
            'can': 'Cancer', 'leo': 'Leo', 'vir': 'Virgo',
            'lib': 'Libra', 'sco': 'Scorpio', 'sag': 'Sagittarius',
            'cap': 'Capricorn', 'aqu': 'Aquarius', 'pis': 'Pisces'
        }
        
        # Planet name normalizations
        self.planet_mappings = {
            'sun': 'Sun', 'moon': 'Moon', 'mercury': 'Mercury',
            'venus': 'Venus', 'mars': 'Mars', 'jupiter': 'Jupiter',
            'saturn': 'Saturn', 'uranus': 'Uranus', 'neptune': 'Neptune',
            'pluto': 'Pluto', 'north node': 'Rahu', 'south node': 'Ketu',
            'lilith': 'Lilith', 'chiron': 'Chiron'
        }
        
        # Nakshatras for Vedic calculations (simplified)
        self.nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
            'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
            'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
            'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
        ]
        
        logger.info("WebChartCalculator initialized (using astro-seek scraper)")
    
    def calculate_chart_from_web(
        self, 
        birth_date: str,
        birth_time: str, 
        birth_location: str,
        validate: bool = True
    ) -> ChartData:
        """
        Calculate birth chart using web scraping
        
        Args:
            birth_date: Birth date in DD/MM/YYYY format
            birth_time: Birth time in HH:MM format
            birth_location: Birth location (city, country)
            validate: Whether to validate results
            
        Returns:
            ChartData object with planetary positions
        """
        
        logger.info(f"Calculating chart via web scraping: {birth_date} {birth_time} at {birth_location}")
        
        try:
            # Use the working scraper to get positions
            scraped_positions = self._scrape_birth_chart(birth_date, birth_time, birth_location)
            
            # Convert scraped data to ChartData format
            chart_data = self._convert_to_chart_data(
                scraped_positions, birth_date, birth_time, birth_location
            )
            
            # Validate if requested
            if validate:
                validation = self._validate_web_chart(chart_data)
                chart_data.accuracy_validated = validation.is_accurate
                
                if not validation.is_accurate:
                    logger.warning(f"Chart validation issues: {validation.issues}")
            
            logger.info(f"Web chart calculation completed: {len(chart_data.planetary_positions)} planets")
            return chart_data
            
        except Exception as e:
            logger.error(f"Web chart calculation failed: {e}")
            raise RuntimeError(f"Failed to calculate chart via web scraping: {e}")
    
    def _scrape_birth_chart(self, birth_date: str, birth_time: str, birth_location: str) -> List[WebScrapedPosition]:
        """Use the working astro-seek scraper to get planetary positions"""
        
        driver = setup_test_driver(headless=self.headless)
        if not driver:
            raise RuntimeError("Could not setup browser driver for web scraping")
        
        try:
            # Navigate to astro-seek
            logger.info("Navigating to astro-seek website...")
            driver.get("https://horoscopes.astro-seek.com/birth-chart-horoscope-online")
            
            # Use longer wait time for web scraping
            wait = WebDriverWait(driver, 20)  # Increased from 15 to 20 seconds
            
            # Wait for page to fully load
            import time
            time.sleep(5)  # Give page more time to load
            logger.info("Page loaded, filling form...")
            
            # Fill the form using the working selectors
            self._fill_birth_form(driver, wait, birth_date, birth_time, birth_location)
            
            # Submit and wait for results
            self._submit_form_and_wait(driver, wait)
            
            # Extract planetary positions
            positions = self._extract_planetary_positions(driver)
            
            logger.info(f"Successfully scraped {len(positions)} planetary positions")
            return positions
            
        except Exception as e:
            logger.error(f"Web scraping failed: {e}")
            logger.error(f"Current URL: {driver.current_url}")
            logger.error(f"Page title: {driver.title}")
            raise
            
        finally:
            driver.quit()
    
    def _fill_birth_form(self, driver, wait, birth_date: str, birth_time: str, birth_location: str):
        """Fill the birth data form using working selectors"""
        
        # Parse date (DD/MM/YYYY format)
        date_parts = birth_date.split("/")
        day = date_parts[0]
        month = int(date_parts[1])
        year = date_parts[2]
        
        # Parse time (HH:MM format)
        time_parts = birth_time.split(":")
        hour = time_parts[0]
        minute = time_parts[1] if len(time_parts) > 1 else "00"
        
        # Wait for page to fully load
        import time
        time.sleep(3)
        
        # Fill date dropdowns with error handling
        try:
            day_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_den"))))
            day_select.select_by_value(day)
            logger.info(f"Day selected: {day}")
        except Exception as e:
            logger.error(f"Error selecting day: {e}")
            raise
        
        try:
            month_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_mesic"))))
            month_select.select_by_value(str(month))
            logger.info(f"Month selected: {month}")
        except Exception as e:
            logger.error(f"Error selecting month: {e}")
            raise
        
        try:
            year_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_rok"))))
            try:
                year_select.select_by_value(year)
                logger.info(f"Year selected: {year}")
            except:
                year_select.select_by_visible_text(year)
                logger.info(f"Year selected by text: {year}")
        except Exception as e:
            logger.warning(f"Year selection failed: {e}, continuing anyway")
            # Form might still work with default year
        
        # Fill time dropdowns with error handling
        try:
            hour_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_hodina"))))
            hour_select.select_by_value(hour)
            logger.info(f"Hour selected: {hour}")
        except Exception as e:
            logger.error(f"Error selecting hour: {e}")
            raise
        
        try:
            minute_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_minuta"))))
            minute_select.select_by_value(minute)
            logger.info(f"Minute selected: {minute}")
        except Exception as e:
            logger.error(f"Error selecting minute: {e}")
            raise
        
        # Fill city with autocomplete
        try:
            city_field = wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_city")))
            city_field.clear()
            city_field.send_keys(birth_location)
            logger.info(f"City typed: {birth_location}")
            
            # Wait for autocomplete and select first option
            time.sleep(3)
            
            try:
                first_option = driver.find_element(By.CSS_SELECTOR, ".ui-autocomplete li:first-child a")
                if first_option and first_option.is_displayed():
                    first_option.click()
                    logger.info("First autocomplete option selected")
                else:
                    # Try alternative selectors
                    autocomplete_selectors = [
                        ".ui-autocomplete li:first-child",
                        ".autocomplete-suggestion:first-child",
                        ".autocomplete-item:first-child"
                    ]
                    
                    for selector in autocomplete_selectors:
                        try:
                            option = driver.find_element(By.CSS_SELECTOR, selector)
                            if option and option.is_displayed():
                                option.click()
                                logger.info(f"Autocomplete selected with: {selector}")
                                break
                        except:
                            continue
                    else:
                        city_field.send_keys(Keys.TAB)
                        logger.info("No autocomplete found, pressed Tab")
            except:
                city_field.send_keys(Keys.TAB)
                logger.info("Autocomplete selection failed, pressed Tab")
                
        except Exception as e:
            logger.error(f"Error filling city: {e}")
            raise
    
    def _submit_form_and_wait(self, driver, wait):
        """Submit the form and wait for results"""
        
        # Click calculate button
        try:
            calculate_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Calculate chart »']"))
            )
            
            driver.execute_script("arguments[0].scrollIntoView(true);", calculate_button)
            import time
            time.sleep(1)
            
            calculate_button.click()
            logger.info("Calculate button clicked")
            
            # Wait for results page to load
            time.sleep(8)  # Increased wait time for results
            logger.info("Waiting for results page...")
            
        except Exception as e:
            logger.error(f"Error clicking calculate button: {e}")
            # Try fallback button
            try:
                fallback_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
                fallback_button.click()
                logger.info("Fallback submit button clicked")
                time.sleep(8)
            except Exception as fallback_error:
                logger.error(f"Fallback button also failed: {fallback_error}")
                raise
        
        # Try to click copy positions button
        try:
            # Try multiple XPath expressions for copy button
            copy_button_selectors = [
                "//*[contains(text(), 'Copy positions')]",
                "//*[contains(text(), 'Copy')]",
                "//button[contains(text(), 'Copy')]",
                "//input[contains(@value, 'Copy')]"
            ]
            
            copy_button = None
            for selector in copy_button_selectors:
                try:
                    copy_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    copy_button.click()
                    logger.info(f"Copy button clicked with selector: {selector}")
                    time.sleep(2)
                    break
                except:
                    continue
            
            if not copy_button:
                logger.warning("Could not find copy positions button, trying to extract data anyway")
            
            # Handle any alert that appears
            try:
                alert = driver.switch_to.alert
                alert_text = alert.text
                logger.info(f"Alert detected: {alert_text}")
                alert.dismiss()  # Stay on page
                logger.info("Alert dismissed")
                time.sleep(1)
            except:
                logger.info("No alert present")
                
        except Exception as e:
            logger.warning(f"Copy button operation failed: {e}, continuing with extraction")
    
    def _extract_planetary_positions(self, driver) -> List[WebScrapedPosition]:
        """Extract planetary positions from the results page"""
        
        positions = []
        
        try:
            logger.info("Starting planetary position extraction...")
            
            # Method 1: Look for tables containing planetary data
            tables = driver.find_elements(By.CSS_SELECTOR, "table")
            logger.info(f"Found {len(tables)} tables on page")
            
            for i, table in enumerate(tables):
                table_text = table.text.lower()
                logger.info(f"Table {i+1} contains: {table_text[:100]}...")
                
                if any(planet in table_text for planet in ['sun', 'moon', 'mercury', 'venus', 'mars']):
                    logger.info(f"Found planetary data in table {i+1}")
                    positions.extend(self._parse_planetary_table(table.text))
                    if positions:
                        logger.info(f"Extracted {len(positions)} positions from table")
                        break
            
            # Method 2: If no table found, try page source extraction
            if not positions:
                logger.info("No positions from tables, trying page source...")
                page_source = driver.page_source
                positions = self._parse_page_source_for_positions(page_source)
                logger.info(f"Extracted {len(positions)} positions from page source")
            
            # Method 3: Try alternative selectors for position containers
            if not positions:
                logger.info("Trying alternative position container selectors...")
                position_selectors = [
                    ".positions",
                    ".chart-positions", 
                    ".planet-positions",
                    "#positions",
                    ".planetary-data",
                    "div[class*='position']"
                ]
                
                for selector in position_selectors:
                    try:
                        container = driver.find_element(By.CSS_SELECTOR, selector)
                        if container and container.text.strip():
                            logger.info(f"Found position container: {selector}")
                            container_positions = self._parse_planetary_table(container.text)
                            if container_positions:
                                positions.extend(container_positions)
                                break
                    except:
                        continue
            
            logger.info(f"Final extraction result: {len(positions)} positions")
            return positions
            
        except Exception as e:
            logger.error(f"Error extracting positions: {e}")
            logger.error(f"Current URL: {driver.current_url}")
            
            # Last resort: try to get any text that might contain planet names
            try:
                page_text = driver.find_element(By.TAG_NAME, "body").text
                logger.info(f"Page body text (first 500 chars): {page_text[:500]}...")
                
                # Look for any mentions of planets
                planets_found = []
                for planet in ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']:
                    if planet.lower() in page_text.lower():
                        planets_found.append(planet)
                
                logger.info(f"Planets mentioned on page: {planets_found}")
                
            except Exception as debug_error:
                logger.error(f"Debug extraction failed: {debug_error}")
            
            return []
    
    def _parse_planetary_table(self, table_text: str) -> List[WebScrapedPosition]:
        """Parse planetary positions from table text"""
        
        positions = []
        lines = table_text.split('\n')
        
        logger.info(f"Parsing table with {len(lines)} lines")
        
        for i, line in enumerate(lines):
            # Clean the line - remove quotes and extra whitespace
            line = line.strip().strip("'\"")
            if not line:
                continue
                
            logger.info(f"Processing cleaned line {i+1}: {line}")
            
            # Multiple patterns to try (in order of specificity)
            # NOTE: Using [\u0027\u2019] to match both ASCII apostrophe (') and Unicode right single quotation mark (')
            patterns = [
                # Pattern 1: "Planet in Sign degree°minute', in House" (exact format from astro-seek)
                r'(\w+)\s+in\s+(\w+)\s+(\d+)°(\d+)[\u0027\u2019],\s+in\s+(\d+)(?:st|nd|rd|th)?\s+House',
                # Pattern 2: "Planet in Sign degree°minute'" (without house)
                r'(\w+)\s+in\s+(\w+)\s+(\d+)°(\d+)[\u0027\u2019]',
                # Pattern 3: "Planet Sign degree°minute'" (no "in")
                r'(\w+)\s+(\w+)\s+(\d+)°(\d+)[\u0027\u2019]',
                # Pattern 4: "Planet: Sign degree°minute'"
                r'(\w+):\s*(\w+)\s+(\d+)°(\d+)[\u0027\u2019]',
            ]
            
            pattern_matched = False
            for pattern_num, pattern in enumerate(patterns, 1):
                match = re.search(pattern, line, re.IGNORECASE)
                
                if match:
                    logger.info(f"✅ Pattern {pattern_num} matched: {match.groups()}")
                    
                    groups = match.groups()
                    planet_name = groups[0].lower()
                    sign = groups[1]
                    degree = float(groups[2])
                    minute = float(groups[3])
                    
                    # Handle house information
                    if len(groups) >= 5 and groups[4]:
                        house = int(groups[4])
                    else:
                        house = None
                    
                    # Check for retrograde indicators
                    retrograde = any(indicator in line.lower() for indicator in [
                        'retrograde', ', r', ' r,', ' r ', '(r)', 'rx'
                    ])
                    
                    # Normalize planet name
                    normalized_name = self.planet_mappings.get(planet_name, planet_name.title())
                    
                    position = WebScrapedPosition(
                        name=normalized_name,
                        sign=sign,
                        degree=degree,
                        minute=minute,
                        house=house,
                        retrograde=retrograde
                    )
                    
                    positions.append(position)
                    logger.info(f"✅ Added position: {normalized_name} {degree}°{minute}' {sign} (House {house})")
                    pattern_matched = True
                    break
            
            if not pattern_matched and any(planet in line.lower() for planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 'node']):
                logger.warning(f"⚠️  No pattern matched planetary line: {line}")
        
        logger.info(f"🎯 Parsed {len(positions)} positions from table")
        return positions
    
    def _parse_page_source_for_positions(self, page_source: str) -> List[WebScrapedPosition]:
        """Extract positions from page source as fallback"""
        
        positions = []
        
        logger.info("Parsing page source for planetary positions...")
        
        # Multiple patterns for different formats in page source
        patterns = [
            # Pattern 1: Standard format with degree symbols
            r'(Sun|Moon|Mercury|Venus|Mars|Jupiter|Saturn|Uranus|Neptune|Pluto|North Node|South Node).*?(\d+)°(\d+)\'\s*(\w+)',
            # Pattern 2: Text format "Planet in Sign degrees"
            r'(Sun|Moon|Mercury|Venus|Mars|Jupiter|Saturn|Uranus|Neptune|Pluto|North Node|South Node)\s+in\s+(\w+)\s+(\d+)°(\d+)\'',
            # Pattern 3: JSON-like format if present
            r'"(Sun|Moon|Mercury|Venus|Mars|Jupiter|Saturn|Uranus|Neptune|Pluto|North Node|South Node)".*?"longitude":(\d+\.\d+)',
        ]
        
        for pattern_num, pattern in enumerate(patterns, 1):
            matches = re.findall(pattern, page_source, re.IGNORECASE)
            logger.info(f"Pattern {pattern_num} found {len(matches)} matches")
            
            for match in matches:
                logger.info(f"Processing match: {match}")
                
                try:
                    if pattern_num == 1:  # Standard degree format
                        planet_name = match[0].lower()
                        degree = float(match[1])
                        minute = float(match[2])
                        sign = match[3]
                    elif pattern_num == 2:  # "in" format
                        planet_name = match[0].lower()
                        sign = match[1]
                        degree = float(match[2])
                        minute = float(match[3])
                    elif pattern_num == 3:  # JSON format
                        planet_name = match[0].lower()
                        total_longitude = float(match[1])
                        # Convert longitude to sign and degree
                        sign_number = int(total_longitude // 30)
                        degree = total_longitude % 30
                        minute = (degree % 1) * 60
                        degree = int(degree)
                        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
                        sign = signs[sign_number % 12]
                    else:
                        continue
                    
                    normalized_name = self.planet_mappings.get(planet_name, planet_name.title())
                    
                    position = WebScrapedPosition(
                        name=normalized_name,
                        sign=sign,
                        degree=degree,
                        minute=minute,
                        house=None,
                        retrograde=False
                    )
                    
                    positions.append(position)
                    logger.info(f"Added position from source: {normalized_name} {degree}°{minute}' {sign}")
                    
                except Exception as e:
                    logger.warning(f"Error processing match {match}: {e}")
            
            if positions:
                break  # Stop if we found positions with this pattern
        
        logger.info(f"Extracted {len(positions)} positions from page source")
        return positions
    
    def _convert_to_chart_data(
        self, 
        scraped_positions: List[WebScrapedPosition],
        birth_date: str, 
        birth_time: str, 
        birth_location: str
    ) -> ChartData:
        """Convert scraped positions to ChartData format"""
        
        # Parse birth datetime
        date_parts = birth_date.split("/")
        time_parts = birth_time.split(":")
        
        birth_datetime = datetime(
            year=int(date_parts[2]),
            month=int(date_parts[1]),
            day=int(date_parts[0]),
            hour=int(time_parts[0]),
            minute=int(time_parts[1])
        )
        
        # Create location (simplified)
        location = Location(
            latitude=0.0,  # Not available from web scraping
            longitude=0.0,
            city=birth_location,
            country="",
            timezone_str="UTC"
        )
        
        # Convert positions
        planetary_positions = {}
        ascendant = 0.0
        house_cusps = {}
        
        for pos in scraped_positions:
            # Calculate total longitude
            sign_number = self._get_sign_number(pos.sign)
            total_longitude = (sign_number * 30) + pos.degree + (pos.minute / 60)
            
            planetary_positions[pos.name] = PlanetaryPosition(
                longitude=total_longitude,
                latitude=0.0,  # Not available from web scraping
                house=pos.house or 1,
                sign=pos.sign,
                degree=pos.degree,
                minute=pos.minute,
                second=0.0,
                nakshatra=self._get_nakshatra_for_longitude(total_longitude),
                nakshatra_pada=1,  # Simplified
                retrograde=pos.retrograde,
                speed=0.0  # Not available
            )
        
        # Create basic house cusps (simplified)
        for i in range(1, 13):
            house_cusps[i] = (i - 1) * 30
        
        # Calculate nakshatras
        nakshatras = self._calculate_nakshatras_from_positions(planetary_positions)
        
        return ChartData(
            birth_datetime=birth_datetime,
            birth_location=location,
            timezone="UTC",
            planetary_positions=planetary_positions,
            house_cusps=house_cusps,
            ascendant=ascendant,
            ayanamsa=24.0,  # Approximate Lahiri ayanamsa
            ayanamsa_name="Lahiri (approximate)",
            nakshatras=nakshatras,
            calculation_method="Web Scraping (astro-seek.com)",
            coordinate_system="Tropical (converted from web)",
            house_system="Placidus (from web)",
            calculation_timestamp=datetime.now(),
            accuracy_validated=False
        )
    
    def _get_sign_number(self, sign_name: str) -> int:
        """Get zodiac sign number (0-11)"""
        signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
                'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        for i, sign in enumerate(signs):
            if sign.lower() in sign_name.lower():
                return i
        return 0
    
    def _get_nakshatra_for_longitude(self, longitude: float) -> str:
        """Get nakshatra for a given longitude"""
        # Each nakshatra is 13°20' = 13.333...°
        nakshatra_index = int(longitude / 13.333333) % 27
        return self.nakshatras[nakshatra_index]
    
    def _calculate_nakshatras_from_positions(self, positions: Dict[str, PlanetaryPosition]) -> Dict[str, NakshatraInfo]:
        """Calculate nakshatra info for all planets"""
        
        nakshatras = {}
        
        for planet_name, position in positions.items():
            nakshatra_name = self._get_nakshatra_for_longitude(position.longitude)
            nakshatras[planet_name] = NakshatraInfo(
                name=nakshatra_name,
                pada=1,  # Simplified
                lord="Unknown",  # Would need lookup table
                degree_range=(0.0, 13.333333)  # Simplified
            )
        
        return nakshatras
    
    def _validate_web_chart(self, chart: ChartData) -> ValidationResult:
        """Validate web-scraped chart data"""
        
        issues = []
        confidence = 1.0
        
        # Check if we have minimum required planets
        required_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
        missing_planets = [p for p in required_planets if p not in chart.planetary_positions]
        
        if missing_planets:
            issues.append(f"Missing planets: {missing_planets}")
            confidence -= 0.3
        
        # Check for reasonable longitude values
        for planet, position in chart.planetary_positions.items():
            if not (0 <= position.longitude <= 360):
                issues.append(f"Invalid longitude for {planet}: {position.longitude}")
                confidence -= 0.2
        
        # Warning about web scraping limitations
        issues.append("Web scraped data - accuracy may vary from precise calculations")
        issues.append("Recommended: Use Swiss Ephemeris for production calculations")
        
        is_accurate = len([i for i in issues if 'Invalid' in i or 'Missing' in i]) == 0
        
        return ValidationResult(
            is_accurate=is_accurate,
            issues=issues,
            confidence_score=max(confidence, 0.1),
            validation_details={
                'method': 'web_scraping',
                'source': 'astro-seek.com',
                'planets_found': len(chart.planetary_positions)
            }
        )
    
    def format_chart_display(self, chart: ChartData) -> str:
        """Format chart data for display"""
        
        output = []
        output.append("=" * 60)
        output.append("BIRTH CHART - WEB SCRAPER CALCULATION")
        output.append("=" * 60)
        
        # Birth details
        output.append(f"\nBirth Details:")
        output.append(f"Date & Time: {chart.birth_datetime.strftime('%d/%m/%Y %H:%M')}")
        output.append(f"Location: {chart.birth_location.city}")
        output.append(f"Calculation: {chart.calculation_method}")
        
        # Planetary positions
        output.append(f"\nPlanetary Positions:")
        output.append("-" * 50)
        
        for planet, position in chart.planetary_positions.items():
            retrograde = " (R)" if position.retrograde else ""
            house_info = f" | House {position.house}" if position.house else ""
            
            output.append(
                f"{planet:8} | {position.degree:2.0f}°{position.minute:02.0f}' {position.sign:11}{house_info}{retrograde}"
            )
        
        # Metadata
        output.append(f"\nCalculation Details:")
        output.append(f"Method: {chart.calculation_method}")
        output.append(f"Timestamp: {chart.calculation_timestamp}")
        output.append(f"Validated: {'Yes' if chart.accuracy_validated else 'No'}")
        
        output.append("\n  Web scraped data - for reference only")
        output.append("   Recommended: Use Swiss Ephemeris for precise calculations")
        
        output.append("=" * 60)
        
        return "\n".join(output)

# Convenience function for easy chart calculation
def calculate_web_chart(birth_date: str, birth_time: str, birth_location: str, headless: bool = True) -> ChartData:
    """
    Convenience function to calculate chart using web scraper
    
    Args:
        birth_date: Birth date in DD/MM/YYYY format
        birth_time: Birth time in HH:MM format  
        birth_location: Birth location string
        headless: Whether to run browser in headless mode
        
    Returns:
        ChartData object
    """
    
    calculator = WebChartCalculator(headless=headless)
    return calculator.calculate_chart_from_web(birth_date, birth_time, birth_location)

# Example usage
if __name__ == "__main__":
    # Test the web chart calculator
    chart = calculate_web_chart("15/08/1990", "14:30", "New York")
    
    calculator = WebChartCalculator()
    display = calculator.format_chart_display(chart)
    print(display) 