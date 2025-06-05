#!/usr/bin/env python3
"""
Personalized Astrological Report Generator for Devansh Yadav
Connects specific chart combinations to classical rules from knowledge base
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from knowledge_base import KnowledgeBase
from data_models import AstrologicalRule

class PersonalizedReportGenerator:
    """Generate detailed personalized reports connecting chart data to classical rules"""
    
    def __init__(self):
        self.kb = KnowledgeBase()
        self.report_sections = []
        
    def load_chart_data(self, chart_file: str) -> Dict[str, Any]:
        """Load chart data from JSON file"""
        try:
            with open(chart_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading chart: {e}")
            return None
    
    def find_matching_rules_for_combination(self, planet: str, house: int = None, 
                                          sign: str = None, min_confidence: float = 0.4) -> List[AstrologicalRule]:
        """Find rules matching specific planetary combinations"""
        try:
            rules = self.kb.search_rules(
                planet=planet,
                house=house,
                sign=sign,
                min_confidence=min_confidence,
                limit=50
            )
            return rules
        except Exception as e:
            print(f"Error searching rules for {planet}: {e}")
            return []
    
    def analyze_chart_combinations(self, chart_data: Dict[str, Any]) -> Dict[str, List]:
        """Analyze all significant combinations in the chart"""
        combinations = {
            'exalted_planets': [],
            'planets_in_own_signs': [],
            'house_concentrations': []
        }
        
        planets = chart_data.get('planets', {})
        
        # Analyze each planet
        for planet_name, planet_data in planets.items():
            sign = planet_data.get('sign')
            house = planet_data.get('house')
            sign_nature = planet_data.get('sign_nature', '')
            
            # Check for exaltation
            if sign_nature == "Exalted":
                combinations['exalted_planets'].append({
                    'planet': planet_name,
                    'sign': sign,
                    'house': house,
                    'significance': f"{planet_name} exalted in {sign} in {house}th house"
                })
        
        # Analyze house concentrations
        house_counts = {}
        for planet_name, planet_data in planets.items():
            house = planet_data.get('house')
            if house:
                house_counts[house] = house_counts.get(house, 0) + 1
        
        for house_num, planet_count in house_counts.items():
            if planet_count >= 2:
                planets_in_house = [p for p, data in planets.items() 
                                  if data.get('house') == house_num]
                combinations['house_concentrations'].append({
                    'house': house_num,
                    'planets': planets_in_house,
                    'count': planet_count,
                    'significance': f"{planet_count} planets in {house_num}th house: {', '.join(planets_in_house)}"
                })
        
        return combinations
    
    def format_rule_match(self, rule: AstrologicalRule, index: int) -> str:
        """Format a rule match for display"""
        effects_text = ""
        if hasattr(rule, 'effects') and rule.effects:
            if isinstance(rule.effects, list):
                effects_text = "; ".join(rule.effects[:2])
            else:
                effects_text = str(rule.effects)[:100]
        
        confidence_stars = "⭐" * min(5, int(rule.confidence * 5))
        
        return f"""
{index:2d}. 📜 {rule.original_text[:150]}{'...' if len(rule.original_text) > 150 else ''}
    🎯 Effects: {effects_text}
    📚 Source: {rule.source}
    ⭐ Confidence: {rule.confidence:.2f} {confidence_stars}
"""
    
    def generate_personalized_report(self, chart_file: str) -> str:
        """Generate comprehensive personalized report"""
        
        chart_data = self.load_chart_data(chart_file)
        if not chart_data:
            return "❌ Could not load chart data"
        
        name = chart_data.get('name', 'Unknown')
        birth_date = chart_data.get('birth_date', 'Unknown')
        birth_time = chart_data.get('birth_time', 'Unknown') 
        birth_location = chart_data.get('birth_location', 'Unknown')
        
        report = []
        report.append("🌟" * 25)
        report.append(f"   PERSONALIZED ASTROLOGICAL ANALYSIS")
        report.append(f"   Classical Rules Applied to {name}'s Birth Chart")
        report.append("🌟" * 25)
        report.append(f"\n📅 Birth Details:")
        report.append(f"   Name: {name}")
        report.append(f"   Date: {birth_date}")
        report.append(f"   Time: {birth_time}")
        report.append(f"   Location: {birth_location}")
        report.append(f"   Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        combinations = self.analyze_chart_combinations(chart_data)
        
        # Section 1: Major Planetary Strengths
        report.append(f"\n🌟 EXCEPTIONAL PLANETARY STRENGTHS")
        report.append("=" * 50)
        
        exalted_count = 0
        for exalted in combinations['exalted_planets']:
            planet = exalted['planet']
            sign = exalted['sign']
            house = exalted['house']
            
            report.append(f"\n✨ {planet} EXALTED IN {sign.upper()} ({house}th House)")
            report.append("-" * 50)
            
            rules = self.find_matching_rules_for_combination(planet, house, sign, 0.4)
            if rules:
                report.append(f"📚 Classical Rules Found: {len(rules)}")
                for i, rule in enumerate(rules[:3], 1):
                    report.append(self.format_rule_match(rule, i))
            else:
                report.append(f"💡 {planet} exalted in {sign} in {house}th house is an extremely powerful placement")
            
            exalted_count += 1
        
        # Section 2: House Concentrations
        report.append(f"\n🏠 PLANETARY CONCENTRATIONS & CONJUNCTIONS")
        report.append("=" * 50)
        
        for concentration in combinations['house_concentrations']:
            house_num = concentration['house']
            planets = concentration['planets']
            count = concentration['count']
            
            report.append(f"\n🔗 {count} PLANETS IN {house_num}th HOUSE: {', '.join(planets)}")
            report.append("-" * 50)
            
            house_rules = []
            for planet in planets:
                planet_rules = self.find_matching_rules_for_combination(planet, house_num, None, 0.3)
                house_rules.extend(planet_rules)
            
            if house_rules:
                house_rules.sort(key=lambda r: r.confidence, reverse=True)
                report.append(f"📚 Relevant Rules Found: {len(house_rules)}")
                for i, rule in enumerate(house_rules[:4], 1):
                    report.append(self.format_rule_match(rule, i))
        
        # Section 3: Specific Combinations
        report.append(f"\n🎯 SPECIFIC CHART COMBINATIONS")
        report.append("=" * 50)
        
        special_combos = [
            {
                'title': 'Sun + Rahu in 1st House (Taurus)',
                'planets': ['Sun', 'Rahu'],
                'house': 1,
            },
            {
                'title': 'Mercury + Venus in 12th House (Aries)', 
                'planets': ['Mercury', 'Venus'],
                'house': 12,
            },
            {
                'title': 'Mars Exalted in 9th House (Capricorn)',
                'planets': ['Mars'],
                'house': 9, 
            },
            {
                'title': 'Jupiter Exalted in 3rd House (Cancer)',
                'planets': ['Jupiter'],
                'house': 3,
            }
        ]
        
        for combo in special_combos:
            report.append(f"\n🎯 {combo['title']}")
            report.append("-" * 60)
            
            combo_rules = []
            for planet in combo['planets']:
                rules = self.find_matching_rules_for_combination(planet, combo['house'], None, 0.3)
                combo_rules.extend(rules)
            
            if combo_rules:
                combo_rules.sort(key=lambda r: r.confidence, reverse=True)
                report.append(f"📚 Classical References: {len(combo_rules)}")
                for i, rule in enumerate(combo_rules[:3], 1):
                    report.append(self.format_rule_match(rule, i))
        
        report.append("\n" + "="*70)
        report.append("📚 This analysis is based on classical Vedic astrology texts")
        report.append("="*70)
        
        return "\n".join(report)

def main():
    generator = PersonalizedReportGenerator()
    report = generator.generate_personalized_report("data/charts/Devansh_Yadav.json")
    
    output_dir = Path("data/output/personalized_reports")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"Devansh_Yadav_Personalized_Report_{timestamp}.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(report)
    print(f"\n💾 Report saved to: {output_file}")

if __name__ == "__main__":
    main() 