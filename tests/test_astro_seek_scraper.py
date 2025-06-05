# """
# Test function for Astro-Seek birth chart web scraper
# Demonstrates the specific automation steps requested by the user.

# This test function automates:
# 1. Navigate to the birth chart form page
# 2. Fill in birth data (date, time, city)  
# 3. Select first option from city dropdown autocomplete
# 4. Click "Calculate chart" button
# 5. Find and click "Copy positions" button
# 6. Extract and print the copied planetary positions data
# """

# import time
# import logging
# from typing import Optional
# from datetime import datetime

# # Handle missing dependencies gracefully
# try:
#     from selenium import webdriver
#     from selenium.webdriver.common.by import By
#     from selenium.webdriver.support.ui import WebDriverWait, Select
#     from selenium.webdriver.support import expected_conditions as EC
#     from selenium.webdriver.chrome.options import Options
#     from selenium.webdriver.common.keys import Keys
#     from selenium.common.exceptions import TimeoutException, NoSuchElementException
#     from webdriver_manager.chrome import ChromeDriverManager
#     from selenium.webdriver.chrome.service import Service
    
#     SELENIUM_AVAILABLE = True
    
# except ImportError as e:
#     SELENIUM_AVAILABLE = False
#     IMPORT_ERROR = str(e)

# logger = logging.getLogger(__name__)

# def setup_test_driver(headless: bool = False) -> Optional[webdriver.Chrome]:
#     """Setup Chrome WebDriver for testing"""
    
#     if not SELENIUM_AVAILABLE:
#         print(f"❌ Selenium not available: {IMPORT_ERROR}")
#         print("Install with: pip install selenium webdriver-manager")
#         return None
    
#     print("🔧 Setting up browser driver...")
    
#     try:
#         chrome_options = Options()
        
#         if headless:
#             chrome_options.add_argument("--headless")
        
#         chrome_options.add_argument("--no-sandbox")
#         chrome_options.add_argument("--disable-dev-shm-usage")
#         chrome_options.add_argument("--disable-gpu")
#         chrome_options.add_argument("--window-size=1920,1080")
#         chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
        
#         # Try different Chrome binary locations for macOS
#         possible_chrome_paths = [
#             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
#             "/usr/bin/google-chrome",
#             "/usr/bin/google-chrome-stable",
#             "/usr/bin/chromium-browser",
#             "/opt/homebrew/bin/chromium",
#         ]
        
#         chrome_binary = None
#         for path in possible_chrome_paths:
#             try:
#                 import os
#                 if os.path.exists(path):
#                     chrome_binary = path
#                     print(f"   ✅ Found Chrome at: {chrome_binary}")
#                     break
#             except:
#                 continue
        
#         if chrome_binary:
#             chrome_options.binary_location = chrome_binary
        
#         try:
#             service = Service(ChromeDriverManager().install())
#             driver = webdriver.Chrome(service=service, options=chrome_options)
#             driver.set_page_load_timeout(30)
#             print("   ✅ ChromeDriver setup successful")
#             return driver
            
#         except Exception as chrome_error:
#             print(f"   ❌ ChromeDriver setup failed: {chrome_error}")
#             print("\n🔧 INSTALLATION INSTRUCTIONS:")
#             print("=" * 40)
#             print("To run this scraper, you need Google Chrome installed.")
#             print("\n📥 Install Google Chrome:")
#             print("1. Visit: https://www.google.com/chrome/")
#             print("2. Download and install Chrome for macOS")
#             print("3. Make sure Chrome is in your Applications folder")
#             print("\n🍺 Alternative - Install via Homebrew:")
#             print("   brew install --cask google-chrome")
#             print("\n🔄 After installing Chrome, run this test again:")
#             print("   python tests/test_astro_seek_scraper.py")
#             print("\n💡 Alternative browsers not supported by this test,")
#             print("   but the existing project has Swiss Ephemeris support:")
#             print("   python main.py chart calculate")
#             return None
        
#     except Exception as e:
#         print(f"❌ Failed to setup any browser driver: {e}")
#         return None

# def test_astro_seek_birth_chart_scraper():
#     """
#     Test function that demonstrates the complete astro-seek scraping workflow.
    
#     🔧 Steps automated:
#     1. Navigate to birth chart form page
#     2. Fill in birth data (date, time, city)
#     3. Select first option from city dropdown autocomplete  
#     4. Click "Calculate chart" button
#     5. Find and click "Copy positions" button
#     6. Extract and print planetary positions data
#     """
    
#     print("🚀 Starting Astro-Seek Birth Chart Scraper Test")
#     print("=" * 50)
    
#     # Test data (hardcoded as requested)
#     test_birth_data = {
#     "date": "27/05/2003",  # Your birth date
#     "time": "06:45",       # Your birth time  
#     "city": "Jhansi"       # Your birth city
#     }
    
#     print(f"📊 Test birth data:")
#     print(f"   Date: {test_birth_data['date']}")
#     print(f"   Time: {test_birth_data['time']}")
#     print(f"   City: {test_birth_data['city']}")
#     print()
    
#     # Setup browser
#     driver = setup_test_driver(headless=False)  # Set to True for headless mode
#     if not driver:
#         return False
    
#     try:
#         # Step 1: Navigate to the birth chart form page
#         print("🌐 Step 1: Navigating to birth chart form...")
#         url = "https://horoscopes.astro-seek.com/birth-chart-horoscope-online"
#         driver.get(url)
        
#         # Wait for page to load
#         wait = WebDriverWait(driver, 10)
#         print("✅ Page loaded successfully")
#         time.sleep(2)
        
#         # Step 2: Fill in birth data
#         print("📝 Step 2: Filling in birth data...")
        
#         # Fill date - use dropdown selectors (day, month, year)
#         try:
#             # Parse the date (15/08/1990 format) 
#             date_parts = test_birth_data["date"].split("/")
#             day = date_parts[0]
#             month = int(date_parts[1])  # Convert to integer for month selection
#             year = date_parts[2]
            
#             # Select day dropdown
#             try:
#                 day_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_den"))))
#                 day_select.select_by_value(day)
#                 print(f"   ✅ Day selected: {day}")
#             except Exception as e:
#                 print(f"   ❌ Error selecting day: {e}")
            
#             # Select month dropdown (use integer value 1-12)
#             try:
#                 month_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_mesic"))))
#                 month_select.select_by_value(str(month))
#                 print(f"   ✅ Month selected: {month}")
#             except Exception as e:
#                 print(f"   ❌ Error selecting month: {e}")
            
#             # Select year - Handle both select dropdown and input field
#             # Also handle disabled/hidden fields using JavaScript
#             print("📅 Handling year field...")
#             try:
#                 year_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_rok"))))
#                 year_select.select_by_value(str(year))
#                 print(f"   ✅ Year selected: {year}")
#             except Exception as e:
#                 print(f"   ❌ Error selecting year: {e}")
            
#             # try:
#             #     # Find the year element
#             #     year_element = wait.until(EC.presence_of_element_located((By.NAME, "narozeni_rok")))
                
#             #     # Get element properties
#             #     tag_name = year_element.tag_name.lower()
#             #     is_enabled = year_element.is_enabled()
#             #     is_displayed = year_element.is_displayed()
#             #     element_type = year_element.get_attribute("type")
                
#             #     print(f"   📋 Year element: {tag_name} (type: {element_type})")
#             #     print(f"   📊 Enabled: {is_enabled}, Displayed: {is_displayed}")
                
#             #     # Try different approaches based on element state
#             #     if tag_name == "select" and is_enabled and is_displayed:
#             #         # Handle as normal select dropdown
#             #         print("   📋 Using SELECT dropdown approach")
#             #         year_select = Select(year_element)
#             #         year_select.select_by_value(year)
#             #         print(f"   ✅ Year selected from dropdown: {year}")
                    
#             #     elif tag_name == "input" and is_enabled and is_displayed:
#             #         # Handle as normal input field
#             #         print("   ⌨️  Using INPUT field approach")
#             #         year_element.clear()
#             #         year_element.send_keys(year)
#             #         print(f"   ✅ Year typed into input field: {year}")
                    
#             #     else:
#             #         # Field is disabled, hidden, or unusual - use JavaScript
#             #         print(f"   🔧 Element not normally interactable, using JavaScript...")
                    
#             #         # Method 1: Enable the field and set value
#             #         try:
#             #             driver.execute_script("""
#             #                 var element = arguments[0];
#             #                 var year = arguments[1];
                            
#             #                 // Enable and show the element
#             #                 element.disabled = false;
#             #                 element.style.display = 'block';
#             #                 element.style.visibility = 'visible';
                            
#             #                 // Set the value
#             #                 element.value = year;
                            
#             #                 // Trigger events that might be expected
#             #                 element.dispatchEvent(new Event('input', {bubbles: true}));
#             #                 element.dispatchEvent(new Event('change', {bubbles: true}));
                            
#             #                 return element.value;
#             #             """, year_element, year)
                        
#             #             # Verify the value was set
#             #             new_value = year_element.get_attribute("value")
#             #             if new_value == year:
#             #                 print(f"   ✅ Year set via JavaScript: {year}")
#             #             else:
#             #                 print(f"   ⚠️  JavaScript set value to: '{new_value}' (expected: '{year}')")
                            
#             #         except Exception as js_error:
#             #             print(f"   ⚠️  JavaScript method failed: {js_error}")
                        
#             #             # Method 2: Try to find and set a hidden year field
#             #             try:
#             #                 driver.execute_script(f"""
#             #                     var yearInputs = document.querySelectorAll('input[name="narozeni_rok"], input[name*="year"], input[name*="Year"]');
#             #                     for (var i = 0; i < yearInputs.length; i++) {{
#             #                         yearInputs[i].value = '{year}';
#             #                         yearInputs[i].dispatchEvent(new Event('change'));
#             #                     }}
#             #                 """)
#             #                 print(f"   ✅ Year set via JavaScript (method 2): {year}")
                            
#             #             except Exception as js2_error:
#             #                 print(f"   ⚠️  All JavaScript methods failed: {js2_error}")
#             #                 print(f"   ℹ️  Form will use default year")
                
#             # except Exception as e:
#             #     print(f"   ❌ Year field handling failed: {e}")
#             #     print(f"   ℹ️  Continuing anyway - form often works with default year")
                
#             #     # Final fallback: just try to set any year-related field
#             #     try:
#             #         driver.execute_script(f"""
#             #             // Look for any year-related inputs and set them
#             #             var possibleSelectors = ['[name="narozeni_rok"]', '[name*="year"]', '[name*="Year"]', 'input[placeholder*="Year"]'];
#             #             for (var selector of possibleSelectors) {{
#             #                 var elements = document.querySelectorAll(selector);
#             #                 for (var element of elements) {{
#             #                     try {{
#             #                         element.value = '{year}';
#             #                         element.dispatchEvent(new Event('change'));
#             #                     }} catch(e) {{}}
#             #                 }}
#             #             }}
#             #         """)
#             #         print(f"   ✅ Final fallback: attempted to set year via JavaScript: {year}")
#             #     except:
#             #         pass
                
#         except Exception as e:
#             print(f"   ❌ Error parsing or filling date: {e}")
        
#         # Fill time - use dropdown selectors (hour, minute)
#         try:
#             # Parse the time (14:30 format)
#             time_parts = test_birth_data["time"].split(":")
#             hour = time_parts[0]
#             minute = time_parts[1] if len(time_parts) > 1 else "00"
            
#             # Select hour dropdown
#             try:
#                 hour_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_hodina"))))
#                 hour_select.select_by_value(hour)
#                 print(f"   ✅ Hour selected: {hour}")
#             except Exception as e:
#                 print(f"   ❌ Error selecting hour: {e}")
            
#             # Select minute dropdown
#             try:
#                 minute_select = Select(wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_minuta"))))
#                 minute_select.select_by_value(minute)
#                 print(f"   ✅ Minute selected: {minute}")
#             except Exception as e:
#                 print(f"   ❌ Error selecting minute: {e}")
                
#         except Exception as e:
#             print(f"   ❌ Error parsing or filling time: {e}")
        
#         # Step 3: Fill city and select first autocomplete option
#         print("🏙️  Step 3: Filling city and selecting from autocomplete...")
        
#         try:
#             # Use the correct city field selector
#             city_field = wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_city")))
            
#             if city_field:
#                 city_field.clear()
#                 city_field.send_keys(test_birth_data["city"])
#                 print(f"   ✅ City typed: {test_birth_data['city']}")
                
#                 # Wait for autocomplete dropdown
#                 time.sleep(3)
                
#                 # Try to select first autocomplete option
#                 autocomplete_selectors = [
#                     ".ui-autocomplete li:first-child a",
#                     ".ui-autocomplete li:first-child",
#                     ".autocomplete-suggestion:first-child",
#                     ".autocomplete-item:first-child", 
#                     ".suggestion:first-child",
#                     ".dropdown-item:first-child"
#                 ]
                
#                 autocomplete_found = False
#                 for selector in autocomplete_selectors:
#                     try:
#                         first_option = driver.find_element(By.CSS_SELECTOR, selector)
#                         if first_option and first_option.is_displayed():
#                             first_option.click()
#                             print("   ✅ First autocomplete option selected")
#                             autocomplete_found = True
#                             break
#                     except NoSuchElementException:
#                         continue
                
#                 if not autocomplete_found:
#                     # If no autocomplete found, just press Tab to move to next field
#                     city_field.send_keys(Keys.TAB)
#                     print("   ✅ Pressed Tab (no autocomplete found)")
                    
#             else:
#                 print("   ⚠️  Could not find city field")
                
#         except Exception as e:
#             print(f"   ❌ Error filling city: {e}")
        
#         time.sleep(2)
        
#         # Step 4: Click "Calculate chart" button
#         print("🧮 Step 4: Clicking 'Calculate chart' button...")
        
#         try:
#             # Use the exact submit button found in diagnostic
#             calculate_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='submit'][value='Calculate chart »']")))
            
#             if calculate_button:
#                 # Scroll into view if needed
#                 driver.execute_script("arguments[0].scrollIntoView(true);", calculate_button)
#                 time.sleep(1)
                
#                 calculate_button.click()
#                 print("   ✅ Calculate button clicked")
#             else:
#                 print("   ⚠️  Could not find calculate button")
                
#         except Exception as e:
#             print(f"   ❌ Error clicking calculate button: {e}")
            
#             # Fallback: try generic submit button
#             try:
#                 fallback_button = driver.find_element(By.CSS_SELECTOR, "input[type='submit']")
#                 fallback_button.click()
#                 print("   ✅ Fallback submit button clicked")
#             except Exception as fallback_error:
#                 print(f"   ❌ Fallback button also failed: {fallback_error}")
        
#         # Wait for results page to load
#         print("⏳ Waiting for results page to load...")
#         time.sleep(5)
        
#         # Step 5: Find and click "Copy positions" button
#         print("📋 Step 5: Looking for 'Copy positions' button...")
        
#         try:
#             copy_selectors = [
#                 "button:contains('Copy positions')",
#                 "input[value*='Copy positions']",
#                 ".copy-positions",
#                 "#copy-positions",
#                 "a:contains('Copy')",
#                 "button:contains('Copy')"
#             ]
            
#             copy_button = None
#             for selector in copy_selectors:
#                 try:
#                     # Use XPath for text-based selectors
#                     if ":contains(" in selector:
#                         text = selector.split("'")[1]
#                         xpath = f"//*[contains(text(), '{text}')]"
#                         copy_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
#                     else:
#                         copy_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
#                     break
#                 except TimeoutException:
#                     continue
            
#             if copy_button:
#                 copy_button.click()
#                 print("   ✅ Copy positions button clicked")
#                 time.sleep(2)
#             else:
#                 print("   ⚠️  Could not find copy positions button")
                
#         except Exception as e:
#             print(f"   ❌ Error clicking copy positions button: {e}")
        
#         # Step 6: Extract planetary positions data
#         print("🪐 Step 6: Extracting planetary positions data...")
        
#         try:
#             # First, handle any alert that might appear from copying positions
#             try:
#                 # Check if there's an alert present
#                 alert = driver.switch_to.alert
#                 alert_text = alert.text
#                 print(f"   📢 Alert detected: {alert_text}")
#                 alert.dismiss()  # Click Cancel to stay on the page
#                 print("   ✅ Alert dismissed")
#                 time.sleep(1)
#             except:
#                 # No alert present, continue normally
#                 pass
            
#             # Try to get data from clipboard or from visible elements
#             # First, try to find planetary positions in the page
            
#             positions_selectors = [
#                 ".planets-table",
#                 ".positions-table", 
#                 ".chart-data",
#                 "#positions",
#                 ".planetary-positions",
#                 "table"  # Generic table selector as fallback
#             ]
            
#             positions_data = []
            
#             for selector in positions_selectors:
#                 try:
#                     positions_container = driver.find_element(By.CSS_SELECTOR, selector)
#                     if positions_container and positions_container.text.strip():
#                         print(f"   ✅ Found positions container: {selector}")
#                         positions_data.append(positions_container.text)
#                         break
#                 except NoSuchElementException:
#                     continue
            
#             # If no specific container found, try to extract from entire page
#             if not positions_data:
#                 try:
#                     # Look for tables or structured data
#                     tables = driver.find_elements(By.CSS_SELECTOR, "table")
#                     for table in tables:
#                         table_text = table.text.lower()
#                         if any(planet in table_text for planet in ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn']):
#                             positions_data.append(table.text)
#                             print(f"   ✅ Found planetary data in table")
#                             break
#                 except:
#                     pass
            
#             # If still no data, try to get it from page source
#             if not positions_data:
#                 try:
#                     page_source = driver.page_source
#                     if any(planet in page_source.lower() for planet in ['sun', 'moon', 'mercury', 'venus', 'mars']):
#                         print("   ✅ Found planetary references in page source")
#                         # Extract a portion of the page source that might contain the positions
#                         import re
                        
#                         # Look for degree symbols and planet names
#                         planet_pattern = r'(Sun|Moon|Mercury|Venus|Mars|Jupiter|Saturn|Uranus|Neptune|Pluto|North Node|South Node).*?(\d+°\d+\'.*?)'
#                         matches = re.findall(planet_pattern, page_source, re.IGNORECASE)
                        
#                         if matches:
#                             extracted_positions = []
#                             for planet, position in matches:
#                                 extracted_positions.append(f"{planet}: {position}")
#                             positions_data.append("\n".join(extracted_positions))
#                             print(f"   ✅ Extracted {len(matches)} planetary positions from source")
#                 except:
#                     pass
            
#             # Display extracted data
#             if positions_data:
#                 print("\n🎯 EXTRACTED PLANETARY POSITIONS:")
#                 print("=" * 40)
#                 for data in positions_data:
#                     # Clean up the data for better display
#                     cleaned_data = data.strip()
#                     if len(cleaned_data) > 500:  # Truncate very long data
#                         cleaned_data = cleaned_data[:500] + "..."
#                     print(cleaned_data)
#                     print("-" * 40)
#             else:
#                 print("   ⚠️  No planetary positions data found")
#                 print("   📄 Checking page title and current URL:")
#                 print(f"      Title: {driver.title}")
#                 print(f"      URL: {driver.current_url}")
                
#         except Exception as e:
#             print(f"   ❌ Error extracting positions data: {e}")
        
#         print("\n✅ Test completed successfully!")
#         return True
        
#     except Exception as e:
#         print(f"❌ Test failed with error: {e}")
#         return False
        
#     finally:
#         # Clean up
#         if driver:
#             driver.quit()
#             print("🔧 Browser closed")

# def test_astro_seek_scraper_simple():
#     """
#     Simplified version of the scraper test for quick validation
#     """
#     print("🧪 Running simplified Astro-Seek scraper test...")
    
#     if not SELENIUM_AVAILABLE:
#         print(f"❌ Cannot run test - Selenium not available")
#         print(f"Install with: pip install selenium webdriver-manager")
#         return False
    
#     driver = setup_test_driver(headless=True)
#     if not driver:
#         print("❌ Could not setup browser driver")
#         return False
    
#     try:
#         # Just navigate and check if page loads
#         print("🌐 Navigating to astro-seek...")
#         driver.get("https://horoscopes.astro-seek.com/birth-chart-horoscope-online")
        
#         # Check if page loaded
#         if "astro-seek" in driver.title.lower():
#             print("✅ Page loaded successfully!")
#             print(f"   Title: {driver.title}")
#             return True
#         else:
#             print("❌ Unexpected page loaded")
#             return False
            
#     except Exception as e:
#         print(f"❌ Test failed: {e}")
#         return False
        
#     finally:
#         driver.quit()

# def debug_year_dropdown(driver, wait):
#     """Debug function to inspect the year dropdown in detail"""
    
#     print("🔍 DEBUGGING YEAR DROPDOWN...")
#     print("-" * 40)
    
#     try:
#         # Find the year dropdown element
#         year_element = wait.until(EC.presence_of_element_located((By.NAME, "narozeni_rok")))
#         print(f"✅ Year element found")
#         print(f"   Tag: {year_element.tag_name}")
#         print(f"   Type: {year_element.get_attribute('type')}")
#         print(f"   Enabled: {year_element.is_enabled()}")
#         print(f"   Displayed: {year_element.is_displayed()}")
#         print(f"   Current value: '{year_element.get_attribute('value')}'")
        
#         # Handle different element types
#         if year_element.tag_name.lower() == "select":
#             print("📋 This is a SELECT dropdown")
            
#             # Try to create Select object
#             year_select = Select(year_element)
#             print(f"✅ Select object created")
            
#             # Get all options
#             options = year_select.options
#             print(f"✅ Found {len(options)} options")
            
#             # Print first 10 and last 10 options
#             print("📋 First 10 options:")
#             for i, option in enumerate(options[:10]):
#                 value = option.get_attribute("value")
#                 text = option.text.strip()
#                 selected = option.is_selected()
#                 print(f"   [{i}] Value: '{value}' | Text: '{text}' | Selected: {selected}")
            
#             if len(options) > 20:
#                 print("...")
#                 print("📋 Last 10 options:")
#                 for i, option in enumerate(options[-10:], len(options)-10):
#                     value = option.get_attribute("value")
#                     text = option.text.strip()
#                     selected = option.is_selected()
#                     print(f"   [{i}] Value: '{value}' | Text: '{text}' | Selected: {selected}")
            
#             # Check if 2003 is in the options
#             print(f"\n🎯 Looking for year '2003':")
#             found_2003 = False
#             for i, option in enumerate(options):
#                 value = option.get_attribute("value")
#                 text = option.text.strip()
#                 if value == "2003" or text == "2003":
#                     print(f"   ✅ Found 2003 at index {i}: Value='{value}', Text='{text}'")
#                     found_2003 = True
#                     break
            
#             if not found_2003:
#                 print(f"   ❌ Year 2003 not found in dropdown options")
                
#                 # Find the range of years
#                 years = []
#                 for option in options:
#                     value = option.get_attribute("value")
#                     if value and value.isdigit():
#                         years.append(int(value))
                
#                 if years:
#                     years.sort()
#                     print(f"   📊 Year range: {min(years)} - {max(years)}")
#                     print(f"   📊 Total years available: {len(years)}")
                    
#                     # Find closest year to 2003
#                     closest_year = min(years, key=lambda x: abs(x - 2003))
#                     print(f"   🎯 Closest year to 2003: {closest_year}")
            
#         elif year_element.tag_name.lower() == "input":
#             print("⌨️  This is an INPUT field")
#             input_type = year_element.get_attribute("type")
#             placeholder = year_element.get_attribute("placeholder")
#             max_length = year_element.get_attribute("maxlength")
            
#             print(f"   Input type: {input_type}")
#             print(f"   Placeholder: {placeholder}")
#             print(f"   Max length: {max_length}")
            
#             # Test if we can type in it
#             print(f"\n🧪 Testing input capabilities:")
#             try:
#                 year_element.clear()
#                 year_element.send_keys("2003")
#                 current_value = year_element.get_attribute("value")
#                 print(f"   ✅ Successfully typed '2003', current value: '{current_value}'")
                
#                 # Clear it back
#                 year_element.clear()
#                 print(f"   ✅ Successfully cleared input")
                
#             except Exception as input_error:
#                 print(f"   ❌ Input test failed: {input_error}")
        
#         else:
#             print(f"❓ Unknown element type: {year_element.tag_name}")
        
#         return True
        
#     except Exception as e:
#         print(f"❌ Year dropdown debugging failed: {e}")
#         return False

# if __name__ == "__main__":
#     # Run the full test
#     print("Choose test to run:")
#     print("1. Full Astro-Seek scraper test (interactive)")
#     print("2. Simple connection test (headless)")
    
#     choice = input("Enter choice (1 or 2): ").strip()
    
#     if choice == "1":
#         test_astro_seek_birth_chart_scraper()
#     elif choice == "2":
#         test_astro_seek_scraper_simple()
#     else:
#         print("Running simple test by default...")
#         test_astro_seek_scraper_simple() 
"""
Fixed Astro-Seek birth chart web scraper
Addresses the main issues in the original code and improves reliability.

Key fixes:
1. Simplified year handling logic
2. Better error handling and fallbacks
3. Improved element selection strategies
4. More robust wait conditions
5. Cleaner code structure
6. Better debugging output
"""

import time
import logging
from typing import Optional, Dict, Any
from datetime import datetime

# Handle missing dependencies gracefully
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.keys import Keys
    from selenium.common.exceptions import TimeoutException, NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    
    SELENIUM_AVAILABLE = True
    
except ImportError as e:
    SELENIUM_AVAILABLE = False
    IMPORT_ERROR = str(e)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AstroSeekScraper:
    """
    Web scraper for Astro-Seek birth chart data
    """
    
    def __init__(self, headless: bool = False, timeout: int = 10):
        self.headless = headless
        self.timeout = timeout
        self.driver = None
        self.wait = None
        
    def setup_driver(self) -> bool:
        """Setup Chrome WebDriver with proper configuration"""
        
        if not SELENIUM_AVAILABLE:
            print(f"❌ Selenium not available: {IMPORT_ERROR}")
            print("Install with: pip install selenium webdriver-manager")
            return False
        
        print("🔧 Setting up browser driver...")
        
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Essential Chrome options
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.set_page_load_timeout(30)
                self.wait = WebDriverWait(self.driver, self.timeout)
                
                # Execute script to remove webdriver property
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                print("   ✅ ChromeDriver setup successful")
                return True
                
            except Exception as chrome_error:
                print(f"   ❌ ChromeDriver setup failed: {chrome_error}")
                self._print_installation_instructions()
                return False
        
        except Exception as e:
            print(f"❌ Failed to setup browser driver: {e}")
            return False
    
    def _print_installation_instructions(self):
        """Print Chrome installation instructions"""
        print("\n🔧 INSTALLATION INSTRUCTIONS:")
        print("=" * 50)
        print("To run this scraper, you need Google Chrome installed.")
        print("\n📥 Install Google Chrome:")
        print("1. Visit: https://www.google.com/chrome/")
        print("2. Download and install Chrome")
        print("3. Restart your terminal/IDE")
        print("\n🔄 Then install Python dependencies:")
        print("   pip install selenium webdriver-manager")
    
    def navigate_to_form(self) -> bool:
        """Navigate to the birth chart form page"""
        print("🌐 Navigating to birth chart form...")
        
        try:
            url = "https://horoscopes.astro-seek.com/birth-chart-horoscope-online"
            self.driver.get(url)
            
            # Wait for form to be present
            self.wait.until(EC.presence_of_element_located((By.NAME, "narozeni_den")))
            print("✅ Form page loaded successfully")
            time.sleep(2)  # Allow page to fully render
            return True
            
        except Exception as e:
            print(f"❌ Failed to navigate to form: {e}")
            return False
    
    def fill_birth_date(self, date_str: str) -> bool:
        """Fill birth date using dropdown selectors"""
        print(f"📅 Filling birth date: {date_str}")
        
        try:
            # Parse date (DD/MM/YYYY format)
            date_parts = date_str.split("/")
            if len(date_parts) != 3:
                raise ValueError("Date must be in DD/MM/YYYY format")
                
            day, month, year = date_parts
            
            # Fill day
            try:
                day_select = Select(self.wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_den"))))
                day_select.select_by_value(day)
                print(f"   ✅ Day selected: {day}")
            except Exception as e:
                print(f"   ❌ Error selecting day: {e}")
                return False
            
            # Fill month
            try:
                month_select = Select(self.wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_mesic"))))
                month_select.select_by_value(month)
                print(f"   ✅ Month selected: {month}")
            except Exception as e:
                print(f"   ❌ Error selecting month: {e}")
                return False
            
            # Fill year with improved handling
            if not self._fill_year(year):
                print(f"   ⚠️  Year selection had issues, but continuing...")
            
            return True
            
        except Exception as e:
            print(f"❌ Error filling birth date: {e}")
            return False
    
    def _fill_year(self, year: str) -> bool:
        """Handle year field with multiple fallback strategies"""
        print(f"📅 Setting year: {year}")
        
        try:
            year_element = self.wait.until(EC.presence_of_element_located((By.NAME, "narozeni_rok")))
            
            # Strategy 1: Normal select dropdown
            if year_element.tag_name.lower() == "select":
                try:
                    year_select = Select(year_element)
                    year_select.select_by_value(year)
                    print(f"   ✅ Year selected from dropdown: {year}")
                    return True
                except Exception as e:
                    print(f"   ⚠️  Dropdown selection failed: {e}")
                    
                    # Check if year is available in options
                    options = year_select.options
                    available_years = [opt.get_attribute("value") for opt in options if opt.get_attribute("value")]
                    
                    if year not in available_years and available_years:
                        # Find closest year
                        try:
                            year_nums = [int(y) for y in available_years if y.isdigit()]
                            if year_nums:
                                closest_year = min(year_nums, key=lambda x: abs(x - int(year)))
                                year_select.select_by_value(str(closest_year))
                                print(f"   ✅ Selected closest available year: {closest_year}")
                                return True
                        except:
                            pass
            
            # Strategy 2: Input field
            elif year_element.tag_name.lower() == "input":
                try:
                    year_element.clear()
                    year_element.send_keys(year)
                    print(f"   ✅ Year entered in input field: {year}")
                    return True
                except Exception as e:
                    print(f"   ⚠️  Input field entry failed: {e}")
            
            # Strategy 3: JavaScript fallback
            try:
                self.driver.execute_script("""
                    var element = arguments[0];
                    var year = arguments[1];
                    
                    element.value = year;
                    element.dispatchEvent(new Event('input', {bubbles: true}));
                    element.dispatchEvent(new Event('change', {bubbles: true}));
                """, year_element, year)
                print(f"   ✅ Year set via JavaScript: {year}")
                return True
            except Exception as e:
                print(f"   ⚠️  JavaScript fallback failed: {e}")
            
            return False
            
        except Exception as e:
            print(f"   ❌ Year field not found or accessible: {e}")
            return False
    
    def fill_birth_time(self, time_str: str) -> bool:
        """Fill birth time using dropdown selectors"""
        print(f"⏰ Filling birth time: {time_str}")
        
        try:
            # Parse time (HH:MM format)
            time_parts = time_str.split(":")
            if len(time_parts) != 2:
                raise ValueError("Time must be in HH:MM format")
                
            hour, minute = time_parts
            
            # Fill hour
            try:
                hour_select = Select(self.wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_hodina"))))
                hour_select.select_by_value(hour)
                print(f"   ✅ Hour selected: {hour}")
            except Exception as e:
                print(f"   ❌ Error selecting hour: {e}")
                return False
            
            # Fill minute
            try:
                minute_select = Select(self.wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_minuta"))))
                minute_select.select_by_value(minute)
                print(f"   ✅ Minute selected: {minute}")
            except Exception as e:
                print(f"   ❌ Error selecting minute: {e}")
                return False
            
            return True
            
        except Exception as e:
            print(f"❌ Error filling birth time: {e}")
            return False
    
    def fill_birth_city(self, city: str) -> bool:
        """Fill birth city and handle autocomplete"""
        print(f"🏙️  Filling birth city: {city}")
        
        try:
            city_field = self.wait.until(EC.element_to_be_clickable((By.NAME, "narozeni_city")))
            city_field.clear()
            city_field.send_keys(city)
            print(f"   ✅ City typed: {city}")
            
            # Wait for autocomplete dropdown
            time.sleep(3)
            
            # Try to select first autocomplete option
            autocomplete_selectors = [
                ".ui-autocomplete li:first-child a",
                ".ui-autocomplete li:first-child",
                ".autocomplete-suggestion:first-child",
                ".autocomplete-item:first-child"
            ]
            
            for selector in autocomplete_selectors:
                try:
                    first_option = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if first_option and first_option.is_displayed():
                        first_option.click()
                        print("   ✅ First autocomplete option selected")
                        return True
                except NoSuchElementException:
                    continue
            
            # If no autocomplete found, press Tab
            city_field.send_keys(Keys.TAB)
            print("   ✅ No autocomplete found, pressed Tab")
            return True
            
        except Exception as e:
            print(f"❌ Error filling city: {e}")
            return False
    
    def submit_form(self) -> bool:
        """Submit the birth chart form"""
        print("🧮 Submitting form...")
        
        try:
            # Find and click submit button
            submit_selectors = [
                "input[type='submit'][value*='Calculate']",
                "input[type='submit']",
                "button[type='submit']",
                ".submit-button"
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    
                    # Scroll into view
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                    time.sleep(1)
                    
                    submit_button.click()
                    print("   ✅ Form submitted successfully")
                    
                    # Wait for results page
                    time.sleep(5)
                    return True
                    
                except (TimeoutException, NoSuchElementException):
                    continue
            
            print("   ❌ Could not find submit button")
            return False
            
        except Exception as e:
            print(f"❌ Error submitting form: {e}")
            return False
    
    def extract_planetary_positions(self) -> Optional[str]:
        """Extract planetary positions from the results page"""
        print("🪐 Extracting planetary positions...")
        
        try:
            # First try to find a copy button
            copy_button = self._find_copy_button()
            if copy_button:
                copy_button.click()
                print("   ✅ Copy button clicked")
                time.sleep(2)
                
                # Handle any alert
                try:
                    alert = self.driver.switch_to.alert
                    alert.dismiss()
                    print("   ✅ Alert dismissed")
                except:
                    pass
            
            # Extract positions from page content
            positions_data = self._extract_positions_from_page()
            
            if positions_data:
                print("   ✅ Successfully extracted planetary positions")
                return positions_data
            else:
                print("   ⚠️  No planetary positions found")
                return None
                
        except Exception as e:
            print(f"❌ Error extracting positions: {e}")
            return None
    
    def _find_copy_button(self):
        """Find the copy positions button"""
        copy_selectors = [
            "//*[contains(text(), 'Copy positions')]",
            "//*[contains(text(), 'Copy')]",
            "input[value*='Copy']",
            ".copy-positions",
            "#copy-positions"
        ]
        
        for selector in copy_selectors:
            try:
                if selector.startswith("//"):
                    button = self.driver.find_element(By.XPATH, selector)
                else:
                    button = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if button and button.is_displayed():
                    return button
            except NoSuchElementException:
                continue
        
        return None
    
    def _extract_positions_from_page(self) -> Optional[str]:
        """Extract positions from page content"""
        
        # Try different content selectors
        content_selectors = [
            ".planets-table",
            ".positions-table",
            ".chart-data",
            "#positions",
            ".planetary-positions",
            "table"
        ]
        
        for selector in content_selectors:
            try:
                container = self.driver.find_element(By.CSS_SELECTOR, selector)
                text = container.text.strip()
                
                # Check if this looks like planetary data
                if any(planet in text.lower() for planet in ['sun', 'moon', 'mercury', 'venus', 'mars']):
                    return text
                    
            except NoSuchElementException:
                continue
        
        # Fallback: search page source for planetary data
        try:
            import re
            page_source = self.driver.page_source
            
            # Look for planetary positions pattern
            planet_pattern = r'(Sun|Moon|Mercury|Venus|Mars|Jupiter|Saturn|Uranus|Neptune|Pluto|North Node|South Node).*?(\d+°\d+\'.*?)'
            matches = re.findall(planet_pattern, page_source, re.IGNORECASE)
            
            if matches:
                positions = []
                for planet, position in matches:
                    positions.append(f"{planet}: {position}")
                return "\n".join(positions)
                
        except Exception as e:
            print(f"   ⚠️  Fallback extraction failed: {e}")
        
        return None
    
    def scrape_birth_chart(self, birth_data: Dict[str, str]) -> Optional[str]:
        """
        Main method to scrape birth chart data
        
        Args:
            birth_data: Dictionary with keys 'date', 'time', 'city'
                       date format: DD/MM/YYYY
                       time format: HH:MM
        
        Returns:
            Planetary positions data as string, or None if failed
        """
        
        print("🚀 Starting Astro-Seek Birth Chart Scraper")
        print("=" * 50)
        print(f"📊 Birth data:")
        print(f"   Date: {birth_data.get('date')}")
        print(f"   Time: {birth_data.get('time')}")
        print(f"   City: {birth_data.get('city')}")
        print()
        
        try:
            # Setup driver
            if not self.setup_driver():
                return None
            
            # Navigate to form
            if not self.navigate_to_form():
                return None
            
            # Fill form fields
            if not self.fill_birth_date(birth_data['date']):
                print("⚠️  Date filling failed, but continuing...")
            
            if not self.fill_birth_time(birth_data['time']):
                print("⚠️  Time filling failed, but continuing...")
            
            if not self.fill_birth_city(birth_data['city']):
                print("⚠️  City filling failed, but continuing...")
            
            # Submit form
            if not self.submit_form():
                return None
            
            # Extract results
            positions = self.extract_planetary_positions()
            
            if positions:
                print("\n🎯 EXTRACTED PLANETARY POSITIONS:")
                print("=" * 40)
                print(positions[:500] + ("..." if len(positions) > 500 else ""))
                print("=" * 40)
            
            print("\n✅ Scraping completed!")
            return positions
            
        except Exception as e:
            print(f"❌ Scraping failed: {e}")
            return None
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        if self.driver:
            try:
                self.driver.quit()
                print("🔧 Browser closed")
            except:
                pass

# Test functions
def test_astro_seek_scraper():
    """Test the scraper with sample data"""
    
    # Test data
    birth_data = {
        "date": "27/05/2003",
        "time": "06:45",
        "city": "Jhansi"
    }
    
    # Create scraper instance
    scraper = AstroSeekScraper(headless=False)  # Set to True for headless mode
    
    # Run scraping
    result = scraper.scrape_birth_chart(birth_data)
    
    if result:
        print("✅ Test successful!")
        return True
    else:
        print("❌ Test failed!")
        return False

def test_simple_connection():
    """Simple test to verify basic connectivity"""
    print("🧪 Running simple connection test...")
    
    scraper = AstroSeekScraper(headless=True)
    
    if not scraper.setup_driver():
        return False
    
    try:
        scraper.driver.get("https://horoscopes.astro-seek.com/birth-chart-horoscope-online")
        
        if "astro-seek" in scraper.driver.title.lower():
            print("✅ Connection test successful!")
            print(f"   Title: {scraper.driver.title}")
            return True
        else:
            print("❌ Unexpected page loaded")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False
        
    finally:
        scraper.cleanup()

if __name__ == "__main__":
    print("Choose test to run:")
    print("1. Full scraper test (interactive)")
    print("2. Simple connection test (headless)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        test_astro_seek_scraper()
    elif choice == "2":
        test_simple_connection()
    else:
        print("Running simple test by default...")
        test_simple_connection()