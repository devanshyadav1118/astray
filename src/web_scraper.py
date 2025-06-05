"""
Web Scraper for Astro-Seek Birth Chart Generator
Alternative/Fallback implementation for chart calculation

⚠️  IMPORTANT NOTE:
This web scraper is provided as a fallback option when Swiss Ephemeris is not available.
However, it goes against the core philosophy of this project:
- Creates external dependencies
- Less accurate than Swiss Ephemeris
- Requires internet connection
- Vulnerable to website changes
- Not self-contained

Recommended: Use the PersonalVedicChartCalculator with Swiss Ephemeris instead.
"""

# Handle missing dependencies gracefully
import re
import time
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# Try to import web scraping dependencies
try:
    import requests
    from bs4 import BeautifulSoup
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import Select, WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    
    WEB_SCRAPING_AVAILABLE = True
    
except ImportError as e:
    WEB_SCRAPING_AVAILABLE = False
    _IMPORT_ERROR = str(e)
    
    # Create placeholder classes so the module can still be imported
    class webdriver:
        class Chrome:
            pass
    class TimeoutException(Exception):
        pass
    class NoSuchElementException(Exception):
        pass

@dataclass
class ScrapedPlanetPosition:
    """Planetary position data from web scraping"""
    name: str
    sign: str
    degree: float
    minute: float
    house: Optional[int] = None
    retrograde: bool = False

@dataclass
class ScrapedChartData:
    """Complete chart data from web scraping"""
    birth_date: str
    birth_time: str
    birth_location: str
    planetary_positions: List[ScrapedPlanetPosition]
    ascendant: Optional[ScrapedPlanetPosition] = None
    houses: Optional[Dict[int, str]] = None
    source_url: str = ""
    scraping_timestamp: datetime = None

def check_web_scraping_dependencies():
    """Check if web scraping dependencies are available"""
    if not WEB_SCRAPING_AVAILABLE:
        missing_deps = [
            "selenium>=4.15.0",
            "beautifulsoup4>=4.12.0", 
            "requests>=2.31.0",
            "webdriver-manager>=4.0.1"
        ]
        
        raise ImportError(
            f"Web scraping dependencies not installed.\n"
            f"Missing: {', '.join(missing_deps)}\n\n"
            f"Install with:\n"
            f"pip install selenium beautifulsoup4 requests webdriver-manager\n\n"
            f"Original error: {_IMPORT_ERROR}\n\n"
            f"💡 Better alternative: Install Swiss Ephemeris instead:\n"
            f"python main.py chart validate-deps"
        )

class AstroSeekScraper:
    """Web scraper for Astro-Seek birth chart generator"""
    
    BASE_URL = "https://horoscopes.astro-seek.com/birth-chart-horoscope-online"
    
    def __init__(self, headless: bool = True, timeout: int = 30):
        """Initialize the scraper with browser options"""
        
        # Check dependencies first
        check_web_scraping_dependencies()
        
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        
        # Planet name mappings (website might use different names)
        self.planet_mappings = {
            'Sun': ['Sun', 'Sol', '☉'],
            'Moon': ['Moon', 'Luna', '☽'],
            'Mercury': ['Mercury', 'Mer', '☿'],
            'Venus': ['Venus', 'Ven', '♀'],
            'Mars': ['Mars', 'Mar', '♂'],
            'Jupiter': ['Jupiter', 'Jup', '♃'],
            'Saturn': ['Saturn', 'Sat', '♄'],
            'Uranus': ['Uranus', 'Ura', '♅'],
            'Neptune': ['Neptune', 'Nep', '♆'],
            'Pluto': ['Pluto', 'Plu', '♇'],
            'Rahu': ['North Node', 'NN', 'Rahu', '☊'],
            'Ketu': ['South Node', 'SN', 'Ketu', '☋']
        }
        
        # Zodiac sign mappings
        self.sign_mappings = {
            'Ari': 'Aries', 'Tau': 'Taurus', 'Gem': 'Gemini',
            'Can': 'Cancer', 'Leo': 'Leo', 'Vir': 'Virgo',
            'Lib': 'Libra', 'Sco': 'Scorpio', 'Sag': 'Sagittarius',
            'Cap': 'Capricorn', 'Aqu': 'Aquarius', 'Pis': 'Pisces'
        }
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Setup Chrome WebDriver with appropriate options and automatic driver management"""
        
        # Import here since it might not be available
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
        try:
            # Try to use webdriver-manager for automatic ChromeDriver management
            try:
                from webdriver_manager.chrome import ChromeDriverManager
                from selenium.webdriver.chrome.service import Service
                
                logger.info("Using webdriver-manager for automatic ChromeDriver management...")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("✅ ChromeDriver automatically managed and updated")
                
            except ImportError:
                # Fallback to system ChromeDriver
                logger.warning("webdriver-manager not available, using system ChromeDriver...")
                driver = webdriver.Chrome(options=chrome_options)
                
            driver.set_page_load_timeout(self.timeout)
            return driver
            
        except Exception as e:
            error_msg = str(e)
            
            # Handle specific ChromeDriver version mismatch
            if "This version of ChromeDriver only supports Chrome version" in error_msg:
                chrome_version_match = re.search(r"Current browser version is ([\d\.]+)", error_msg)
                driver_version_match = re.search(r"supports Chrome version (\d+)", error_msg)
                
                current_version = chrome_version_match.group(1) if chrome_version_match else "unknown"
                supported_version = driver_version_match.group(1) if driver_version_match else "unknown"
                
                logger.error(f"ChromeDriver version mismatch:")
                logger.error(f"  Chrome browser version: {current_version}")
                logger.error(f"  ChromeDriver supports: {supported_version}")
                
                raise RuntimeError(
                    f"ChromeDriver version mismatch detected!\n\n"
                    f"🔧 QUICK FIXES:\n"
                    f"1. Install webdriver-manager for automatic management:\n"
                    f"   pip install webdriver-manager\n\n"
                    f"2. Update ChromeDriver manually:\n"
                    f"   - Download from: https://chromedriver.chromium.org/\n"
                    f"   - Get version matching Chrome {current_version}\n\n"
                    f"3. Use conda for better dependency management:\n"
                    f"   conda install -c conda-forge selenium\n\n"
                    f"💡 BETTER SOLUTION: Avoid this complexity entirely!\n"
                    f"   python main.py chart calculate (uses Swiss Ephemeris)\n\n"
                    f"This is exactly why web scraping is problematic:\n"
                    f"• Browser version changes break the scraper\n"
                    f"• Constant maintenance required\n"
                    f"• External dependencies are unreliable\n"
                    f"• Swiss Ephemeris has none of these issues"
                )
            
            # Handle other WebDriver errors
            elif "chromedriver" in error_msg.lower():
                raise RuntimeError(
                    f"ChromeDriver setup failed: {error_msg}\n\n"
                    f"🔧 INSTALLATION FIXES:\n"
                    f"1. Install Chrome browser if not present\n"
                    f"2. Install automatic driver management:\n"
                    f"   pip install webdriver-manager\n\n"
                    f"3. Manual ChromeDriver installation:\n"
                    f"   - Download from https://chromedriver.chromium.org/\n"
                    f"   - Add to PATH or project directory\n\n"
                    f"💡 AVOID THIS COMPLEXITY:\n"
                    f"   python main.py chart calculate\n"
                    f"   (Uses reliable Swiss Ephemeris instead)"
                )
            
            # Generic error handling
            else:
                logger.error(f"WebDriver setup failed: {e}")
                raise RuntimeError(
                    f"WebDriver setup failed: {e}\n\n"
                    f"This demonstrates why web scraping is unreliable.\n"
                    f"Recommended: Use Swiss Ephemeris instead:\n"
                    f"python main.py chart validate-deps"
                )
    
    def scrape_birth_chart(self, 
                          birth_date: str,
                          birth_time: str, 
                          birth_location: str,
                          timezone: Optional[str] = None) -> ScrapedChartData:
        """
        Scrape birth chart data from Astro-Seek
        
        Args:
            birth_date: Birth date in format "DD/MM/YYYY" or "MM/DD/YYYY"
            birth_time: Birth time in format "HH:MM"
            birth_location: Birth location (city, country)
            timezone: Optional timezone string
            
        Returns:
            ScrapedChartData with planetary positions
        """
        
        self.driver = self._setup_driver()
        
        try:
            logger.info(f"Scraping chart for: {birth_date} {birth_time} at {birth_location}")
            
            # Load the birth chart page
            self.driver.get(self.BASE_URL)
            
            # Wait for page to load
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "form"))
            )
            
            # Fill out the birth chart form
            self._fill_birth_data_form(birth_date, birth_time, birth_location, timezone)
            
            # Submit the form
            self._submit_form()
            
            # Wait for results page to load
            self._wait_for_results()
            
            # Extract planetary positions
            planetary_positions = self._extract_planetary_positions()
            
            # Extract ascendant
            ascendant = self._extract_ascendant()
            
            # Extract house cusps (if available)
            houses = self._extract_houses()
            
            # Create chart data
            chart_data = ScrapedChartData(
                birth_date=birth_date,
                birth_time=birth_time,
                birth_location=birth_location,
                planetary_positions=planetary_positions,
                ascendant=ascendant,
                houses=houses,
                source_url=self.driver.current_url,
                scraping_timestamp=datetime.now()
            )
            
            logger.info(f"Successfully scraped chart data: {len(planetary_positions)} planets")
            return chart_data
            
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
            raise RuntimeError(f"Chart scraping failed: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()
    
    def _fill_birth_data_form(self, birth_date: str, birth_time: str, birth_location: str, timezone: Optional[str]):
        """Fill out the birth data form"""
        
        try:
            # Parse birth date (handle different formats)
            date_parts = birth_date.replace('-', '/').split('/')
            if len(date_parts) == 3:
                if len(date_parts[0]) == 4:  # YYYY/MM/DD format
                    year, month, day = date_parts
                else:  # DD/MM/YYYY or MM/DD/YYYY format
                    day, month, year = date_parts
            else:
                raise ValueError(f"Invalid date format: {birth_date}")
            
            # Parse birth time
            time_parts = birth_time.split(':')
            hour, minute = time_parts[0], time_parts[1] if len(time_parts) > 1 else "00"
            
            # Fill date fields
            day_field = self.driver.find_element(By.NAME, "narozeni_den")
            day_field.clear()
            day_field.send_keys(day)
            
            month_field = self.driver.find_element(By.NAME, "narozeni_mesic")
            month_field.clear()
            month_field.send_keys(month)
            
            year_field = self.driver.find_element(By.NAME, "narozeni_rok")
            year_field.clear()
            year_field.send_keys(year)
            
            # Fill time fields
            hour_field = self.driver.find_element(By.NAME, "narozeni_hodina")
            hour_field.clear()
            hour_field.send_keys(hour)
            
            minute_field = self.driver.find_element(By.NAME, "narozeni_minuta")
            minute_field.clear()
            minute_field.send_keys(minute)
            
            # Fill location
            location_field = self.driver.find_element(By.NAME, "narozeni_misto_hidden")
            location_field.clear()
            location_field.send_keys(birth_location)
            
            # Wait for location autocomplete and select first option
            time.sleep(2)
            
            # Try to click first autocomplete result
            try:
                autocomplete_results = self.driver.find_elements(By.CLASS_NAME, "ui-menu-item")
                if autocomplete_results:
                    autocomplete_results[0].click()
                    time.sleep(1)
            except NoSuchElementException:
                logger.warning("No autocomplete results found for location")
            
            # Set timezone if provided
            if timezone:
                try:
                    timezone_select = Select(self.driver.find_element(By.NAME, "cas_zona"))
                    timezone_select.select_by_visible_text(timezone)
                except NoSuchElementException:
                    logger.warning(f"Could not set timezone: {timezone}")
            
            logger.info("Birth data form filled successfully")
            
        except Exception as e:
            logger.error(f"Failed to fill form: {e}")
            raise
    
    def _submit_form(self):
        """Submit the birth chart form"""
        
        try:
            # Find and click submit button
            submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit' or @value='Show the chart']")
            submit_button.click()
            
            logger.info("Form submitted successfully")
            
        except Exception as e:
            logger.error(f"Failed to submit form: {e}")
            raise
    
    def _wait_for_results(self):
        """Wait for the results page to load"""
        
        try:
            # Wait for planetary positions table or chart to appear
            WebDriverWait(self.driver, self.timeout).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "planets")),
                    EC.presence_of_element_located((By.ID, "planety")),
                    EC.presence_of_element_located((By.CLASS_NAME, "chart-data"))
                )
            )
            
            logger.info("Results page loaded")
            
        except TimeoutException:
            logger.error("Timeout waiting for results page")
            raise
    
    def _extract_planetary_positions(self) -> List[ScrapedPlanetPosition]:
        """Extract planetary positions from the results page"""
        
        positions = []
        
        try:
            # Look for different possible table structures
            possible_selectors = [
                "table.planets tr",
                "#planety tr", 
                ".chart-data tr",
                "table tr"
            ]
            
            rows = []
            for selector in possible_selectors:
                try:
                    rows = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if rows:
                        break
                except NoSuchElementException:
                    continue
            
            if not rows:
                raise NoSuchElementException("Could not find planetary positions table")
            
            for row in rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) < 3:  # Skip header rows or invalid rows
                        continue
                    
                    # Extract planet name
                    planet_text = cells[0].text.strip()
                    planet_name = self._normalize_planet_name(planet_text)
                    
                    if not planet_name:
                        continue  # Skip if we can't identify the planet
                    
                    # Extract sign and degree information
                    position_text = cells[1].text.strip()
                    sign, degree, minute, retrograde = self._parse_position_text(position_text)
                    
                    # Extract house if available
                    house = None
                    if len(cells) > 2:
                        house_text = cells[2].text.strip()
                        house = self._parse_house_number(house_text)
                    
                    position = ScrapedPlanetPosition(
                        name=planet_name,
                        sign=sign,
                        degree=degree,
                        minute=minute,
                        house=house,
                        retrograde=retrograde
                    )
                    
                    positions.append(position)
                    
                except Exception as e:
                    logger.warning(f"Failed to parse row: {e}")
                    continue
            
            logger.info(f"Extracted {len(positions)} planetary positions")
            return positions
            
        except Exception as e:
            logger.error(f"Failed to extract planetary positions: {e}")
            return []
    
    def _extract_ascendant(self) -> Optional[ScrapedPlanetPosition]:
        """Extract ascendant information"""
        
        try:
            # Look for ascendant information
            possible_selectors = [
                "//td[contains(text(), 'Ascendant')]/../td[2]",
                "//td[contains(text(), 'ASC')]/../td[2]",
                "//td[contains(text(), 'Lagna')]/../td[2]"
            ]
            
            for selector in possible_selectors:
                try:
                    ascendant_element = self.driver.find_element(By.XPATH, selector)
                    position_text = ascendant_element.text.strip()
                    
                    sign, degree, minute, _ = self._parse_position_text(position_text)
                    
                    return ScrapedPlanetPosition(
                        name="Ascendant",
                        sign=sign,
                        degree=degree,
                        minute=minute,
                        house=1,  # Ascendant is always 1st house
                        retrograde=False
                    )
                    
                except NoSuchElementException:
                    continue
            
            logger.warning("Could not find ascendant information")
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract ascendant: {e}")
            return None
    
    def _extract_houses(self) -> Optional[Dict[int, str]]:
        """Extract house cusp information if available"""
        
        try:
            houses = {}
            
            # Look for house cusp table
            house_rows = self.driver.find_elements(By.XPATH, "//tr[contains(@class, 'house')]")
            
            for row in house_rows:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 2:
                        house_num_text = cells[0].text.strip()
                        house_position_text = cells[1].text.strip()
                        
                        house_num = int(re.findall(r'\d+', house_num_text)[0])
                        houses[house_num] = house_position_text
                        
                except (ValueError, IndexError):
                    continue
            
            return houses if houses else None
            
        except Exception as e:
            logger.warning(f"Could not extract house information: {e}")
            return None
    
    def _normalize_planet_name(self, text: str) -> Optional[str]:
        """Normalize planet name from various possible formats"""
        
        text = text.strip().lower()
        
        for standard_name, variations in self.planet_mappings.items():
            for variation in variations:
                if variation.lower() in text or text in variation.lower():
                    return standard_name
        
        # Check for partial matches
        for standard_name in self.planet_mappings.keys():
            if standard_name.lower() in text or text in standard_name.lower():
                return standard_name
        
        logger.warning(f"Could not normalize planet name: {text}")
        return None
    
    def _parse_position_text(self, text: str) -> Tuple[str, float, float, bool]:
        """Parse position text like '15°23' Aries' or '23Ar15'"""
        
        text = text.strip()
        retrograde = 'R' in text or '℞' in text
        
        # Remove retrograde markers
        text = text.replace('R', '').replace('℞', '').strip()
        
        # Pattern 1: "15°23' Aries" or "15° 23' Aries"
        pattern1 = r'(\d+)°?\s*(\d+)?\'?\s*([A-Za-z]+)'
        match1 = re.search(pattern1, text)
        
        if match1:
            degree = float(match1.group(1))
            minute = float(match1.group(2)) if match1.group(2) else 0.0
            sign_text = match1.group(3)
            sign = self._normalize_sign_name(sign_text)
            return sign, degree, minute, retrograde
        
        # Pattern 2: "23Ar15" (degree + abbreviated sign + minute)
        pattern2 = r'(\d+)([A-Za-z]{2,3})(\d+)'
        match2 = re.search(pattern2, text)
        
        if match2:
            degree = float(match2.group(1))
            sign_text = match2.group(2)
            minute = float(match2.group(3))
            sign = self._normalize_sign_name(sign_text)
            return sign, degree, minute, retrograde
        
        # Pattern 3: Just degrees "15.23" (need to extract sign separately)
        pattern3 = r'(\d+\.?\d*)'
        match3 = re.search(pattern3, text)
        
        if match3:
            degree = float(match3.group(1))
            minute = (degree % 1) * 60
            degree = int(degree)
            
            # Try to find sign in the text
            for abbrev, full_name in self.sign_mappings.items():
                if abbrev.lower() in text.lower() or full_name.lower() in text.lower():
                    return full_name, degree, minute, retrograde
            
            # Default to unknown sign
            return "Unknown", degree, minute, retrograde
        
        logger.warning(f"Could not parse position text: {text}")
        return "Unknown", 0.0, 0.0, retrograde
    
    def _normalize_sign_name(self, text: str) -> str:
        """Normalize zodiac sign name"""
        
        text = text.strip()
        
        # Check abbreviations first
        for abbrev, full_name in self.sign_mappings.items():
            if text.lower() == abbrev.lower():
                return full_name
        
        # Check full names
        for full_name in self.sign_mappings.values():
            if text.lower() == full_name.lower():
                return full_name
        
        # Partial match
        for full_name in self.sign_mappings.values():
            if text.lower() in full_name.lower() or full_name.lower().startswith(text.lower()):
                return full_name
        
        logger.warning(f"Could not normalize sign name: {text}")
        return text  # Return original if we can't normalize
    
    def _parse_house_number(self, text: str) -> Optional[int]:
        """Extract house number from text"""
        
        try:
            # Look for numbers in the text
            numbers = re.findall(r'\d+', text)
            if numbers:
                house_num = int(numbers[0])
                if 1 <= house_num <= 12:
                    return house_num
        except ValueError:
            pass
        
        return None

class ChartScrapingService:
    """High-level service for chart scraping with fallback and validation"""
    
    def __init__(self, headless: bool = True):
        self.scraper = AstroSeekScraper(headless=headless)
    
    def get_birth_chart(self, 
                       birth_date: str,
                       birth_time: str,
                       birth_location: str,
                       validate: bool = True) -> ScrapedChartData:
        """
        Get birth chart with validation and error handling
        
        Args:
            birth_date: Birth date (DD/MM/YYYY, MM/DD/YYYY, or YYYY-MM-DD)
            birth_time: Birth time (HH:MM)
            birth_location: Birth location
            validate: Whether to validate the scraped data
            
        Returns:
            ScrapedChartData with planetary positions
        """
        
        try:
            # Normalize date format
            normalized_date = self._normalize_date_format(birth_date)
            
            # Scrape the chart
            chart_data = self.scraper.scrape_birth_chart(
                birth_date=normalized_date,
                birth_time=birth_time,
                birth_location=birth_location
            )
            
            # Validate if requested
            if validate:
                validation_result = self._validate_chart_data(chart_data)
                if not validation_result['is_valid']:
                    logger.warning(f"Chart validation issues: {validation_result['issues']}")
            
            return chart_data
            
        except Exception as e:
            logger.error(f"Chart scraping service failed: {e}")
            raise
    
    def _normalize_date_format(self, birth_date: str) -> str:
        """Normalize date format for the website"""
        
        # Handle different input formats
        if '-' in birth_date:  # YYYY-MM-DD format
            parts = birth_date.split('-')
            if len(parts[0]) == 4:  # YYYY-MM-DD
                return f"{parts[2]}/{parts[1]}/{parts[0]}"  # Convert to DD/MM/YYYY
        
        return birth_date  # Return as-is for DD/MM/YYYY or MM/DD/YYYY
    
    def _validate_chart_data(self, chart_data: ScrapedChartData) -> Dict:
        """Validate scraped chart data for completeness and accuracy"""
        
        issues = []
        
        # Check if we have basic planetary positions
        expected_planets = ['Sun', 'Moon', 'Mercury', 'Venus', 'Mars', 'Jupiter', 'Saturn']
        found_planets = [pos.name for pos in chart_data.planetary_positions]
        
        for planet in expected_planets:
            if planet not in found_planets:
                issues.append(f"Missing planet: {planet}")
        
        # Check for valid degrees (0-30)
        for position in chart_data.planetary_positions:
            if not (0 <= position.degree <= 30):
                issues.append(f"{position.name} has invalid degree: {position.degree}")
        
        # Check for valid signs
        valid_signs = list(self.scraper.sign_mappings.values())
        for position in chart_data.planetary_positions:
            if position.sign not in valid_signs and position.sign != "Unknown":
                issues.append(f"{position.name} has invalid sign: {position.sign}")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'planet_count': len(chart_data.planetary_positions),
            'has_ascendant': chart_data.ascendant is not None
        }
    
    def format_chart_display(self, chart_data: ScrapedChartData) -> str:
        """Format scraped chart data for display"""
        
        output = []
        output.append("=" * 60)
        output.append("BIRTH CHART - WEB SCRAPED FROM ASTRO-SEEK")
        output.append("=" * 60)
        
        # Birth details
        output.append(f"\nBirth Details:")
        output.append(f"Date: {chart_data.birth_date}")
        output.append(f"Time: {chart_data.birth_time}")
        output.append(f"Location: {chart_data.birth_location}")
        
        # Ascendant
        if chart_data.ascendant:
            output.append(f"\nAscendant: {chart_data.ascendant.degree:.1f}°{chart_data.ascendant.minute:.0f}' {chart_data.ascendant.sign}")
        
        # Planetary positions
        output.append(f"\nPlanetary Positions:")
        output.append("-" * 50)
        
        for position in chart_data.planetary_positions:
            retrograde_marker = " (R)" if position.retrograde else ""
            house_info = f" | House {position.house}" if position.house else ""
            
            output.append(
                f"{position.name:8} | {position.degree:2.0f}°{position.minute:02.0f}' {position.sign:11}{house_info}{retrograde_marker}"
            )
        
        # Metadata
        output.append(f"\nScraping Details:")
        output.append(f"Source: {chart_data.source_url}")
        output.append(f"Scraped: {chart_data.scraping_timestamp}")
        output.append("\n⚠️  Web scraped data - accuracy may vary")
        output.append("   Recommended: Use Swiss Ephemeris for precise calculations")
        
        output.append("=" * 60)
        
        return "\n".join(output)

# Example usage functions
def scrape_sample_chart():
    """Example function showing how to use the scraper"""
    
    scraper_service = ChartScrapingService(headless=True)
    
    # Example birth data
    birth_date = "15/05/1990"  # DD/MM/YYYY format
    birth_time = "10:30"
    birth_location = "New Delhi, India"
    
    try:
        print("🕷️  Scraping birth chart from Astro-Seek...")
        print(f"Birth: {birth_date} {birth_time} at {birth_location}")
        
        chart_data = scraper_service.get_birth_chart(
            birth_date=birth_date,
            birth_time=birth_time,
            birth_location=birth_location,
            validate=True
        )
        
        print(scraper_service.format_chart_display(chart_data))
        
        return chart_data
        
    except Exception as e:
        print(f"❌ Scraping failed: {e}")
        return None

if __name__ == "__main__":
    # Demo the scraper
    scrape_sample_chart() 