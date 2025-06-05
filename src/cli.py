# src/cli.py
"""
Complete Command Line Interface for Astrology AI Phase 1
Integrates document processing, rule extraction, and knowledge storage
Uses centralized configuration for all paths and settings
"""

import click
import json
import os
import sys
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Import configuration system
config_path = Path(__file__).parent.parent / "config"
sys.path.insert(0, str(config_path))

try:
    from settings import get_config, get_database_path, get_export_path, get_books_dir
except ImportError:
    # Fallback for when config system is not available
    def get_config():
        return None
    def get_database_path(db_type: str = "main"):
        return Path("data/astrology_rules.db")
    def get_export_path(filename: str):
        return Path("data") / filename
    def get_books_dir():
        return Path("data/books")

# Import our modules
from .document_processor import DocumentProcessor
from .rule_extractor import RuleExtractor
from .knowledge_base import KnowledgeBase
from .data_models import SourceInfo, AuthorityLevel

logger = logging.getLogger(__name__)

@click.group()
@click.version_option(version='1.0.0')
def cli():
    """🌌 Astrology AI - Ancient Wisdom meets Modern Intelligence
    
    Phase 1: Foundation & Rule Extraction System
    """
    pass


@cli.command()
@click.argument('pdf_path', type=click.Path(exists=True))
@click.option('--source-title', '-t', help='Title of the source book')
@click.option('--author', '-a', help='Author of the source')
@click.option('--authority', '-l', 
              type=click.Choice(['classical', 'traditional', 'modern', 'commentary']),
              default='modern', help='Authority level of the source')
@click.option('--extract-rules', '-r', is_flag=True, help='Extract rules and store in knowledge base')
@click.option('--show-samples', '-s', is_flag=True, help='Show sample sentences')
@click.option('--output', '-o', type=click.Path(), help='Output file for results')
def process_book(pdf_path, source_title, author, authority, extract_rules, show_samples, output):
    """Process an astrology book and optionally extract rules"""
    
    click.echo(f"📚 Processing: {Path(pdf_path).name}")
    
    # Initialize components
    processor = DocumentProcessor()
    
    try:
        # Process the PDF
        result = processor.process_document(pdf_path)
        
        # Display basic results
        click.echo(f"\n📊 Processing Results:")
        click.echo(f"   Document: {result.filename}")
        click.echo(f"   Total sentences: {len(result.sentences)}")
        click.echo(f"   Astrological sentences: {len(result.astrological_sentences)}")
        click.echo(f"   Content ratio: {len(result.astrological_sentences)/len(result.sentences)*100:.1f}%")
        
        if show_samples:
            click.echo(f"\n🔍 Sample astrological sentences:")
            for i, sentence in enumerate(result.astrological_sentences[:5]):
                click.echo(f"   {i+1}. {sentence[:100]}...")
        
        # Extract rules if requested
        if extract_rules:
            click.echo(f"\n🔄 Extracting rules...")
            
            # Create source info
            authority_map = {
                'classical': AuthorityLevel.CLASSICAL,
                'traditional': AuthorityLevel.TRADITIONAL, 
                'modern': AuthorityLevel.MODERN,
                'commentary': AuthorityLevel.COMMENTARY
            }
            
            source_info = SourceInfo(
                title=source_title or result.filename,
                author=author,
                authority_level=authority_map[authority]
            )
            
            # Extract rules
            extractor = RuleExtractor()
            rules = extractor.extract_rules_from_sentences(
                result.astrological_sentences, 
                source_info
            )
            
            click.echo(f"   Extracted {len(rules)} rules")
            
            # Store in knowledge base using configuration
            if rules:
                kb = KnowledgeBase()  # Uses configuration for database path
                stored_count = kb.store_rules_batch(rules)
                click.echo(f"   ✅ Stored {stored_count} rules in knowledge base")
                
                # Show rule samples
                click.echo(f"\n📝 Sample extracted rules:")
                for i, rule in enumerate(rules[:3]):
                    click.echo(f"   {i+1}. {rule.original_text[:80]}...")
                    click.echo(f"      Planet: {rule.conditions.planet}, House: {rule.conditions.house}")
                    click.echo(f"      Effects: {len(rule.effects)}, Confidence: {rule.confidence_score:.2f}")
        
        # Save results if requested
        if output:
            output_data = {
                'filename': result.filename,
                'processed_at': datetime.now().isoformat(),
                'total_sentences': len(result.sentences),
                'astrological_sentences': len(result.astrological_sentences),
                'sample_sentences': result.astrological_sentences[:10]
            }
            
            if extract_rules:
                output_data['extracted_rules'] = len(rules)
                output_data['stored_rules'] = stored_count if 'stored_count' in locals() else 0
            
            with open(output, 'w') as f:
                json.dump(output_data, f, indent=2)
            
            click.echo(f"💾 Results saved to: {output}")
        
        click.echo(f"\n✅ Processing complete!")
        
    except Exception as e:
        click.echo(f"❌ Error processing book: {e}")


@cli.command()
@click.argument('directory', type=click.Path(exists=True), required=False)
@click.option('--authority', '-l',
              type=click.Choice(['classical', 'traditional', 'modern', 'commentary']),
              default='modern', help='Default authority level for all books')
@click.option('--extract-rules', '-r', is_flag=True, help='Extract and store rules')
def batch_process(directory, authority, extract_rules):
    """Process all PDFs in a directory (uses books directory from config if not specified)"""
    
    # Use configured books directory if none specified
    if directory is None:
        directory = str(get_books_dir())
        click.echo(f"📁 Using configured books directory: {directory}")
    
    pdf_files = list(Path(directory).glob("*.pdf"))
    
    if not pdf_files:
        click.echo(f"❌ No PDF files found in {directory}")
        return
    
    click.echo(f"📚 Found {len(pdf_files)} PDF files")
    
    processor = DocumentProcessor()
    extractor = RuleExtractor() if extract_rules else None
    kb = KnowledgeBase() if extract_rules else None  # Uses configuration for database path
    
    total_rules = 0
    
    authority_map = {
        'classical': AuthorityLevel.CLASSICAL,
        'traditional': AuthorityLevel.TRADITIONAL,
        'modern': AuthorityLevel.MODERN,
        'commentary': AuthorityLevel.COMMENTARY
    }
    
    for pdf_file in pdf_files:
        click.echo(f"\n🔄 Processing: {pdf_file.name}")
        
        try:
            # Process document
            result = processor.process_document(str(pdf_file))
            click.echo(f"   📊 {len(result.astrological_sentences)} astrological sentences found")
            
            # Extract rules if requested
            if extract_rules and result.astrological_sentences:
                source_info = SourceInfo(
                    title=pdf_file.stem,
                    authority_level=authority_map[authority]
                )
                
                rules = extractor.extract_rules_from_sentences(
                    result.astrological_sentences,
                    source_info
                )
                
                if rules:
                    stored_count = kb.store_rules_batch(rules)
                    total_rules += stored_count
                    click.echo(f"   ✅ Extracted and stored {stored_count} rules")
            
        except Exception as e:
            click.echo(f"   ❌ Error: {e}")
    
    click.echo(f"\n📊 Batch processing complete!")
    if extract_rules:
        click.echo(f"🎯 Total rules extracted and stored: {total_rules}")


@cli.command()
@click.option('--planet', '-p', help='Filter by planet')
@click.option('--house', '-h', type=int, help='Filter by house (1-12)')
@click.option('--sign', '-s', help='Filter by zodiac sign')
@click.option('--source', help='Filter by source title')
@click.option('--min-confidence', '-c', type=float, default=0.0, help='Minimum confidence score')
@click.option('--limit', '-l', type=int, help='Limit number of results')
@click.option('--export', '-e', type=click.Path(), help='Export results to JSON file')
def search_rules(planet, house, sign, source, min_confidence, limit, export):
    """Search for rules in the knowledge base"""
    
    kb = KnowledgeBase()  # Uses configuration for database path
    
    try:
        rules = kb.search_rules(
            planet=planet,
            house=house, 
            sign=sign,
            source=source,
            min_confidence=min_confidence,
            limit=limit
        )
        
        click.echo(f"🔍 Found {len(rules)} matching rules")
        
        if rules:
            click.echo(f"\n📝 Rules:")
            for i, rule in enumerate(rules, 1):
                click.echo(f"\n{i}. {rule.original_text}")
                click.echo(f"   Planet: {rule.conditions.planet}, House: {rule.conditions.house}, Sign: {rule.conditions.sign}")
                click.echo(f"   Effects: {', '.join([e.description[:50] for e in rule.effects])}")
                click.echo(f"   Source: {rule.source.title}")
                click.echo(f"   Confidence: {rule.confidence_score:.2f}")
        
        if export:
            export_data = {
                'search_criteria': {
                    'planet': planet,
                    'house': house,
                    'sign': sign,
                    'source': source,
                    'min_confidence': min_confidence
                },
                'results_count': len(rules),
                'rules': [
                    {
                        'id': rule.id,
                        'text': rule.original_text,
                        'planet': rule.conditions.planet,
                        'house': rule.conditions.house,
                        'sign': rule.conditions.sign,
                        'effects': [e.description for e in rule.effects],
                        'source': rule.source.title,
                        'confidence': rule.confidence_score
                    }
                    for rule in rules
                ]
            }
            
            with open(export, 'w') as f:
                json.dump(export_data, f, indent=2)
            
            click.echo(f"💾 Search results exported to {export}")
        
    except Exception as e:
        click.echo(f"❌ Error searching rules: {e}")


@cli.command()
@click.option('--output', '-o', help='Output file path (uses configured export directory if not specified)')
def export_knowledge(output):
    """Export all rules from the knowledge base to JSON"""
    
    try:
        kb = KnowledgeBase()  # Uses configuration for database path
        
        # Use configured export path if not specified
        if output is None:
            output = str(get_export_path('knowledge_export.json'))
        
        exported_path = kb.export_rules_json(output)
        
        stats = kb.get_database_stats()
        click.echo(f"✅ Exported {stats['total_rules']} rules to: {exported_path}")
        
    except Exception as e:
        click.echo(f"❌ Error exporting knowledge base: {e}")


@cli.command()
def stats():
    """Show knowledge base statistics"""
    
    try:
        kb = KnowledgeBase()  # Uses configuration for database path
        stats = kb.get_database_stats()
        
        click.echo(f"\n📊 Knowledge Base Statistics")
        click.echo(f"{'='*50}")
        click.echo(f"Total rules: {stats['total_rules']}")
        click.echo(f"Unique sources: {stats['unique_sources']}")
        click.echo(f"Average confidence: {stats['average_confidence']}")
        
        if stats['planet_distribution']:
            click.echo(f"\n🪐 Rules by planet:")
            for planet, count in stats['planet_distribution'].items():
                click.echo(f"   {planet}: {count}")
        
        if stats['house_distribution']:
            click.echo(f"\n🏠 Rules by house:")
            for house, count in stats['house_distribution'].items():
                click.echo(f"   House {house}: {count}")
        
        click.echo(f"\n✅ Statistics retrieved successfully")
        
    except Exception as e:
        click.echo(f"❌ Error retrieving statistics: {e}")


@cli.command()
@click.option('--confirm', is_flag=True, help='Skip confirmation prompt')
def clear_database(confirm):
    """Clear all rules from the database
    
    ⚠️  WARNING: This will permanently delete all rules!
    """
    
    try:
        kb = KnowledgeBase()  # Uses configuration for database path
        
        # Get current stats before clearing
        stats = kb.get_database_stats()
        total_rules = stats['total_rules']
        
        if total_rules == 0:
            click.echo("📭 Database is already empty - no rules to clear")
            return
        
        # Confirmation prompt unless --confirm flag is used
        if not confirm:
            click.echo(f"⚠️  WARNING: This will permanently delete {total_rules} rules from the database!")
            click.echo(f"   Database path: {kb.db_path}")
            
            if not click.confirm("\nAre you sure you want to proceed?"):
                click.echo("❌ Operation cancelled")
                return
        
        # Clear the database
        click.echo(f"\n🗑️  Clearing {total_rules} rules from database...")
        deleted_count = kb.clear_all_rules()
        
        click.echo(f"✅ Successfully cleared {deleted_count} rules from the database")
        click.echo(f"📭 Database is now empty and ready for fresh data")
        
    except Exception as e:
        click.echo(f"❌ Error clearing database: {e}")


@cli.command()
def test_setup():
    """Test if the setup is working correctly"""
    
    click.echo("🧪 Testing Astrology AI setup...")
    
    # Test configuration
    try:
        config = get_config()
        if config:
            click.echo("✅ Configuration system loaded")
            
            # Validate setup
            validation = config.validate_setup()
            click.echo("\n📊 Configuration validation:")
            for check, result in validation.items():
                status = "✅" if result else "❌"
                click.echo(f"   {status} {check}: {result}")
        else:
            click.echo("⚠️  Using fallback configuration")
    except Exception as e:
        click.echo(f"❌ Configuration error: {e}")
    
    # Test imports
    try:
        import PyPDF2
        import pdfplumber
        import spacy
        click.echo("✅ Required packages imported successfully")
    except ImportError as e:
        click.echo(f"❌ Missing package: {e}")
        return
    
    # Test directories using configuration
    try:
        config = get_config()
        if config:
            required_dirs = [
                ('Books', config.directories.books_dir),
                ('Rules', config.directories.rules_dir), 
                ('Charts', config.directories.charts_dir),
                ('Exports', config.directories.exports_dir)
            ]
        else:
            # Fallback directories
            required_dirs = [
                ('Books', Path('data/books')),
                ('Rules', Path('data/rules')),
                ('Charts', Path('data/charts'))
            ]
        
        for name, dir_path in required_dirs:
            if dir_path.exists():
                click.echo(f"✅ {name} directory exists: {dir_path}")
            else:
                click.echo(f"❌ {name} directory missing: {dir_path}")
                dir_path.mkdir(parents=True, exist_ok=True)
                click.echo(f"✅ Created {name} directory: {dir_path}")
    except Exception as e:
        click.echo(f"❌ Directory setup error: {e}")
    
    # Test components
    try:
        processor = DocumentProcessor()
        extractor = RuleExtractor()
        kb = KnowledgeBase()  # Uses configuration for database path
        click.echo("✅ All components initialized successfully")
    except Exception as e:
        click.echo(f"❌ Component initialization error: {e}")
        return
    
    # Test rule extraction
    test_sentence = "Mars in the 7th house causes conflicts in marriage"
    if processor.contains_astrological_content(test_sentence):
        click.echo("✅ Astrological content detection working")
    else:
        click.echo("❌ Astrological content detection failed")
    
    click.echo(f"\n🎉 Setup test complete! Ready to process astrology books.")
    click.echo(f"\n🚀 Next steps:")
    
    try:
        books_dir = get_books_dir()
        click.echo(f"   1. Add PDF books to {books_dir}")
        click.echo(f"   2. Run: python cli.py process-book {books_dir}/your_book.pdf --extract-rules")
    except:
        click.echo(f"   1. Add PDF books to data/books/")
        click.echo(f"   2. Run: python cli.py process-book data/books/your_book.pdf --extract-rules")
    
    click.echo(f"   3. View results: python cli.py stats")


@cli.command()
def config_info():
    """Show current configuration information"""
    
    try:
        config = get_config()
        if not config:
            click.echo("⚠️  Configuration system not available, using fallbacks")
            return
        
        click.echo("🔧 Current Configuration")
        click.echo("=" * 50)
        
        click.echo(f"Project Root: {config.directories.project_root}")
        click.echo(f"Data Directory: {config.directories.data_dir}")
        
        click.echo(f"\n📁 Directory Structure:")
        click.echo(f"   Books: {config.directories.books_dir}")
        click.echo(f"   Rules: {config.directories.rules_dir}")
        click.echo(f"   Charts: {config.directories.charts_dir}")
        click.echo(f"   Exports: {config.directories.exports_dir}")
        click.echo(f"   Logs: {config.directories.logs_dir}")
        click.echo(f"   Cache: {config.directories.cache_dir}")
        
        click.echo(f"\n🗄️  Database Paths:")
        click.echo(f"   Main: {config.get_database_path('main')}")
        click.echo(f"   Test: {config.get_database_path('test')}")
        
        click.echo(f"\n⚙️  Processing Settings:")
        click.echo(f"   Min sentence length: {config.processing.min_sentence_length}")
        click.echo(f"   Max sentence length: {config.processing.max_sentence_length}")
        click.echo(f"   Min confidence threshold: {config.processing.min_confidence_threshold}")
        click.echo(f"   OCR correction: {config.processing.enable_ocr_correction}")
        
    except Exception as e:
        click.echo(f"❌ Error getting configuration info: {e}")


@cli.group()
def chart():
    """Phase 2: File-based chart data management and analysis"""
    pass

@chart.command("create-template")
@click.option("--format", "output_format", default="json", 
              type=click.Choice(["json", "yaml", "txt"]), 
              help="Template format")
@click.option("--name", default="my_chart", help="Template filename")
def create_template(output_format, name):
    """Create a chart data template file for manual input"""
    
    from .chart_data_manager import ChartDataManager
    
    try:
        manager = ChartDataManager()
        
        # Get template from templates directory
        template_file = f"chart_template.{output_format}"
        template_path = manager.templates_dir / template_file
        
        if not template_path.exists():
            click.echo(f"❌ Template {template_file} not found")
            return
        
        # Copy template to main charts directory with new name
        output_path = manager.charts_dir / f"{name}.{output_format}"
        
        if output_path.exists():
            if not click.confirm(f"File {output_path.name} already exists. Overwrite?"):
                return
        
        import shutil
        shutil.copy2(template_path, output_path)
        
        click.echo(f"✅ Created chart template: {output_path}")
        click.echo(f"\n📝 Next steps:")
        click.echo(f"   1. Edit {output_path}")
        click.echo(f"   2. Fill in your birth chart details")
        click.echo(f"   3. Use: python main.py chart load {name}.{output_format}")
        
        if output_format == "txt":
            click.echo(f"\n💡 Text format is simple - just edit with any text editor!")
        else:
            click.echo(f"\n💡 Use a text editor that supports {output_format.upper()} syntax highlighting")
            
    except Exception as e:
        click.echo(f"❌ Failed to create template: {e}")

@chart.command("load")
@click.argument("filename")
@click.option("--format", "output_format", default="display", 
              type=click.Choice(["display", "json", "yaml"]), 
              help="Output format")
def load_chart(filename, output_format):
    """Load and display a chart from file"""
    
    from .chart_data_manager import ChartDataManager
    
    try:
        manager = ChartDataManager()
        
        chart_data = manager.load_chart(filename)
        if not chart_data:
            click.echo(f"❌ Chart file not found: {filename}")
            available = manager.list_available_charts()
            if available:
                click.echo(f"\n📂 Available charts: {', '.join(available)}")
            else:
                click.echo(f"\n💡 Create a chart with: python main.py chart create-template")
            return
        
        if output_format == "display":
            click.echo(manager.display_chart_summary(chart_data))
        elif output_format == "json":
            import json
            click.echo(json.dumps(chart_data.to_dict(), indent=2))
        elif output_format == "yaml":
            import yaml
            click.echo(yaml.dump(chart_data.to_dict(), default_flow_style=False))
            
    except Exception as e:
        click.echo(f"❌ Failed to load chart: {e}")

@chart.command("list")
def list_charts():
    """List all available chart files"""
    
    from .chart_data_manager import ChartDataManager
    
    try:
        manager = ChartDataManager()
        charts = manager.list_available_charts()
        
        if not charts:
            click.echo("📂 No chart files found")
            click.echo("\n💡 Create your first chart:")
            click.echo("   python main.py chart create-template --name my_chart")
            return
        
        click.echo("📂 Available chart files:")
        click.echo("=" * 40)
        
        for chart_file in charts:
            try:
                chart_data = manager.load_chart(chart_file)
                if chart_data:
                    click.echo(f"📄 {chart_file}")
                    click.echo(f"   Name: {chart_data.name}")
                    click.echo(f"   Birth: {chart_data.birth_date} at {chart_data.birth_time}")
                    click.echo(f"   Location: {chart_data.birth_location}")
                    click.echo("")
                else:
                    click.echo(f"⚠️  {chart_file} (error loading)")
            except Exception:
                click.echo(f"❌ {chart_file} (corrupted)")
        
        click.echo(f"💡 Load a chart with: python main.py chart load <filename>")
        
    except Exception as e:
        click.echo(f"❌ Failed to list charts: {e}")

@chart.command("interpret")
@click.argument("filename")
@click.option("--category", help="Focus on specific category (health, wealth, marriage, career)")
@click.option("--min-confidence", type=float, default=0.5, help="Minimum rule confidence")
@click.option("--detailed", is_flag=True, help="Show detailed rule matches")
@click.option("--save-output", is_flag=True, default=True, help="Save interpretation to file (default: True)")
def interpret_chart(filename, category, min_confidence, detailed, save_output):
    """Interpret a chart using extracted astrological rules"""
    
    from .chart_data_manager import ChartDataManager
    from .interpreter import ChartInterpreter
    
    try:
        # Load chart
        manager = ChartDataManager()
        simple_chart = manager.load_chart(filename)
        
        if not simple_chart:
            click.echo(f"❌ Chart file not found: {filename}")
            return
        
        # Convert to BirthChart format
        birth_chart = manager.convert_to_birth_chart(simple_chart)
        
        # Initialize interpreter
        click.echo(f"🔮 Interpreting chart for {simple_chart.name}...")
        click.echo("=" * 50)
        
        interpreter = ChartInterpreter()
        
        # Generate interpretation
        interpretation = interpreter.interpret_chart(
            birth_chart, 
            min_confidence=min_confidence
        )
        
        if not interpretation:
            click.echo("❌ No interpretation could be generated")
            return
        
        # Prepare output content
        output_lines = []
        output_lines.append(f"🌟 CHART INTERPRETATION: {simple_chart.name}")
        output_lines.append("=" * 60)
        output_lines.append(f"📅 Birth: {simple_chart.birth_date} at {simple_chart.birth_time}")
        output_lines.append(f"📍 Location: {simple_chart.birth_location}")
        output_lines.append(f"🕐 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("")
        
        # Filter by category if specified
        if category:
            relevant_matches = interpretation.get_rules_by_category(category)
            output_lines.append(f"🎯 {category.upper()} ANALYSIS:")
            output_lines.append("-" * 30)
            
            if not relevant_matches:
                output_lines.append(f"No specific rules found for {category}")
                click.echo(f"No specific rules found for {category}")
            else:
                for i, match in enumerate(relevant_matches, 1):
                    line = f"{i:2d}. {match}"
                    output_lines.append(line)
                    click.echo(line)
        else:
            # Show overall interpretation
            output_lines.append("📋 OVERALL SUMMARY:")
            output_lines.append(interpretation.overall_summary)
            output_lines.append("")
            
            output_lines.append(f"📊 RULE MATCHES: {len(interpretation.matched_rules)} total")
            output_lines.append("-" * 30)
            
            # Show top matches (simplified - just show first 10)
            top_matches = interpretation.matched_rules[:10]
            
            for i, match in enumerate(top_matches, 1):
                line = f"{i:2d}. {match}"
                output_lines.append(line)
                if detailed:
                    detail_line = f"    Source: Classical Vedic Astrology"
                    output_lines.append(detail_line)
                    output_lines.append("")
            
            if len(interpretation.matched_rules) > 10:
                remaining = len(interpretation.matched_rules) - 10
                remaining_line = f"    ... and {remaining} more matches"
                output_lines.append(remaining_line)
            
            # Display to console
            click.echo("📋 OVERALL SUMMARY:")
            click.echo(interpretation.overall_summary)
            click.echo("")
            
            click.echo(f"📊 RULE MATCHES: {len(interpretation.matched_rules)} total")
            click.echo("-" * 30)
            
            for i, match in enumerate(top_matches, 1):
                click.echo(f"{i:2d}. {match}")
                if detailed:
                    click.echo(f"    Source: Classical Vedic Astrology")
                    click.echo("")
            
            if len(interpretation.matched_rules) > 10:
                remaining = len(interpretation.matched_rules) - 10
                click.echo(f"    ... and {remaining} more matches")
        
        confidence_line = f"\n💡 Generated with confidence level: {interpretation.confidence_level}"
        output_lines.append(confidence_line)
        click.echo(confidence_line)
        
        # Save to file if requested
        if save_output:
            # Create output directory
            output_dir = Path("data/output/interpretations")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            chart_name = simple_chart.name.replace(" ", "_")
            category_suffix = f"_{category}" if category else ""
            detail_suffix = "_detailed" if detailed else ""
            
            output_filename = f"{chart_name}_{timestamp}{category_suffix}{detail_suffix}.txt"
            output_path = output_dir / output_filename
            
            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(output_lines))
            
            click.echo(f"\n💾 Interpretation saved to: {output_path}")
                
    except Exception as e:
        click.echo(f"❌ Interpretation failed: {e}")
        import traceback
        traceback.print_exc()

@chart.command("demo")
def demo_chart():
    """Demo chart loading with sample data"""
    
    from .chart_data_manager import ChartDataManager
    
    try:
        manager = ChartDataManager()
        
        # Check if sample chart exists
        sample_file = "chart_template.json"
        template_path = manager.templates_dir / sample_file
        
        if template_path.exists():
            chart_data = manager._load_json_chart(template_path)
            click.echo("🎯 Demo Chart Data:")
            click.echo("=" * 40)
            click.echo(manager.display_chart_summary(chart_data))
            
            click.echo(f"\n💡 This is sample data from: {template_path}")
            click.echo(f"📝 Create your own chart:")
            click.echo(f"   python main.py chart create-template --name my_chart")
        else:
            click.echo("❌ Sample chart template not found")
            
    except Exception as e:
        click.echo(f"❌ Demo failed: {e}")

@chart.command("validate")
@click.argument("filename")
def validate_chart(filename):
    """Validate chart data format and completeness"""
    
    from .chart_data_manager import ChartDataManager
    
    try:
        manager = ChartDataManager()
        chart_data = manager.load_chart(filename)
        
        if not chart_data:
            click.echo(f"❌ Chart file not found: {filename}")
            return
        
        click.echo(f"🔍 Validating chart: {filename}")
        click.echo("=" * 40)
        
        errors = []
        warnings = []
        
        # Basic validation
        if not chart_data.name.strip():
            errors.append("Name is empty")
        
        if not chart_data.birth_date:
            errors.append("Birth date is missing")
        
        if not chart_data.birth_time:
            errors.append("Birth time is missing")
        
        if not chart_data.birth_location:
            warnings.append("Birth location is missing")
        
        # Planet validation
        required_planets = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Rahu', 'Ketu']
        missing_planets = []
        
        for planet in required_planets:
            if planet not in chart_data.planets:
                missing_planets.append(planet)
            else:
                planet_data = chart_data.planets[planet]
                if 'house' not in planet_data or not (1 <= planet_data.get('house', 0) <= 12):
                    errors.append(f"{planet} has invalid house number")
                if 'sign' not in planet_data or not planet_data.get('sign'):
                    errors.append(f"{planet} is missing sign")
        
        if missing_planets:
            errors.append(f"Missing planets: {', '.join(missing_planets)}")
        
        # House validation
        for house_num in range(1, 13):
            if house_num not in chart_data.houses:
                warnings.append(f"House {house_num} data is missing")
        
        # Report results
        if errors:
            click.echo("❌ ERRORS:")
            for error in errors:
                click.echo(f"   • {error}")
        
        if warnings:
            click.echo("⚠️  WARNINGS:")
            for warning in warnings:
                click.echo(f"   • {warning}")
        
        if not errors and not warnings:
            click.echo("✅ Chart validation passed!")
            click.echo("📊 Chart summary:")
            click.echo(f"   • Name: {chart_data.name}")
            click.echo(f"   • Planets: {len(chart_data.planets)}/9")
            click.echo(f"   • Houses: {len(chart_data.houses)}/12")
        elif not errors:
            click.echo("✅ Chart is valid (with warnings)")
        else:
            click.echo("❌ Chart has errors that need fixing")
        
    except Exception as e:
        click.echo(f"❌ Validation failed: {e}")

@chart.command("convert")
@click.argument("filename")
@click.option("--to-format", required=True, 
              type=click.Choice(["json", "yaml", "txt"]), 
              help="Target format")
@click.option("--output-name", help="Output filename (without extension)")
def convert_chart(filename, to_format, output_name):
    """Convert chart between different file formats"""
    
    from .chart_data_manager import ChartDataManager
    
    try:
        manager = ChartDataManager()
        chart_data = manager.load_chart(filename)
        
        if not chart_data:
            click.echo(f"❌ Chart file not found: {filename}")
            return
        
        # Determine output filename
        if output_name:
            output_file = f"{output_name}.{to_format}"
        else:
            # Use original name but change extension
            from pathlib import Path
            base_name = Path(filename).stem
            output_file = f"{base_name}.{to_format}"
        
        # Save in new format
        if to_format in ['json', 'yaml']:
            output_path = manager.save_chart(chart_data, Path(output_file).stem, to_format)
            click.echo(f"✅ Converted to {to_format.upper()}: {output_path}")
        else:  # txt format
            # For text format, we need to write manually
            output_path = manager.charts_dir / output_file
            with open(output_path, 'w') as f:
                f.write(f"# Chart Data for {chart_data.name}\n\n")
                f.write(f"Name: {chart_data.name}\n")
                f.write(f"Birth Date: {chart_data.birth_date}\n")
                f.write(f"Birth Time: {chart_data.birth_time}\n")
                f.write(f"Birth Location: {chart_data.birth_location}\n\n")
                
                f.write("# Planetary Positions (Planet: Sign, House, Degree)\n")
                for planet, data in chart_data.planets.items():
                    retrograde_indicator = " (R)" if data.get('retrograde', False) else ""
                    f.write(f"{planet}: {data['sign']}, {data['house']}, {data.get('degree', 0.0)}{retrograde_indicator}\n")
                
                f.write("\n# House Signs (House: Sign, Lord)\n")
                for house_num, data in chart_data.houses.items():
                    f.write(f"{house_num}: {data['sign']}, {data['lord']}\n")
                
                f.write(f"\n# Basic Info\n")
                f.write(f"Ascendant: {chart_data.ascendant}\n")
                f.write(f"Moon Sign: {chart_data.moon_sign}\n")
                f.write(f"Sun Sign: {chart_data.sun_sign}\n")
                
                if chart_data.notes:
                    f.write(f"\n# Notes\n")
                    f.write(f"Notes: {chart_data.notes}\n")
            
            click.echo(f"✅ Converted to TXT: {output_path}")
        
    except Exception as e:
        click.echo(f"❌ Conversion failed: {e}")

@chart.command("import")
@click.option("--file", "import_file", type=click.Path(exists=True), help="Import from text file")
@click.option("--text", help="Import from direct text input")
@click.option("--name", required=True, help="Chart name")
@click.option("--birth-date", help="Birth date (YYYY-MM-DD)")
@click.option("--birth-time", help="Birth time (HH:MM)")
@click.option("--birth-location", help="Birth location")
@click.option("--format", "output_format", default="json", 
              type=click.Choice(["json", "yaml"]), 
              help="Output format for saved chart")
def import_chart(import_file, text, name, birth_date, birth_time, birth_location, output_format):
    """Import chart from specific text format (Planet,Sign,Degree°Minute')"""
    
    from .chart_data_manager import ChartDataManager
    
    try:
        manager = ChartDataManager()
        
        # Get chart text from file or direct input
        if import_file:
            with open(import_file, 'r') as f:
                chart_text = f.read()
            click.echo(f"📄 Importing from file: {import_file}")
        elif text:
            chart_text = text
            click.echo("📝 Importing from direct text input")
        else:
            click.echo("❌ Please provide either --file or --text option")
            return
        
        # Parse the chart
        click.echo("🔍 Parsing chart data...")
        
        chart_data = manager.parse_chart_from_text_format(
            chart_text=chart_text,
            name=name,
            birth_date=birth_date or "",
            birth_time=birth_time or "",
            birth_location=birth_location or ""
        )
        
        # Save the chart
        output_path = manager.save_chart(chart_data, name, output_format)
        
        click.echo(f"✅ Chart imported successfully!")
        click.echo(f"💾 Saved as: {output_path}")
        
        # Display summary
        click.echo("\n📊 Import Summary:")
        click.echo(f"   Name: {chart_data.name}")
        click.echo(f"   Ascendant: {chart_data.ascendant}")
        click.echo(f"   Planets found: {len(chart_data.planets)}")
        click.echo(f"   Houses: {len(chart_data.houses)}")
        
        # Show planetary positions
        if chart_data.planets:
            click.echo("\n🪐 Imported Planets:")
            for planet, data in chart_data.planets.items():
                retrograde_indicator = " (R)" if data.get('retrograde', False) else ""
                click.echo(f"   {planet:8}: {data['sign']:12} | House {data['house']:2} | {data['degree']:6.1f}°{retrograde_indicator}")
        
        click.echo(f"\n💡 Load your chart with:")
        click.echo(f"   python main.py chart load {name}.{output_format}")
        
    except Exception as e:
        click.echo(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()

@chart.command("outputs")
@click.option("--chart-name", help="Filter by chart name")
@click.option("--category", help="Filter by category")
@click.option("--detailed", is_flag=True, help="Show detailed file info")
def list_outputs(chart_name, category, detailed):
    """List all saved interpretation output files"""
    
    output_dir = Path("data/output/interpretations")
    
    if not output_dir.exists():
        click.echo("📂 No output directory found")
        click.echo("💡 Run some chart interpretations first!")
        return
    
    # Get all txt files
    files = list(output_dir.glob("*.txt"))
    
    if not files:
        click.echo("📂 No interpretation files found")
        click.echo("💡 Run: python main.py cli chart interpret <chart_file>")
        return
    
    # Filter files
    if chart_name:
        files = [f for f in files if chart_name.lower() in f.name.lower()]
    
    if category:
        files = [f for f in files if f"_{category}_" in f.name or f.name.endswith(f"_{category}.txt")]
    
    if not files:
        click.echo(f"📂 No files found matching filters")
        return
    
    # Sort by modification time (newest first)
    files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    
    click.echo(f"📊 Found {len(files)} interpretation files:")
    click.echo("=" * 60)
    
    for i, file_path in enumerate(files, 1):
        file_stats = file_path.stat()
        file_size = file_stats.st_size
        mod_time = datetime.fromtimestamp(file_stats.st_mtime)
        
        # Parse filename components
        filename = file_path.stem
        parts = filename.split('_')
        
        if len(parts) >= 3:
            chart_name_part = parts[0]
            date_part = parts[1] if len(parts) > 1 else "unknown"
            time_part = parts[2] if len(parts) > 2 else "unknown"
            category_part = parts[3] if len(parts) > 3 and not parts[3] == "detailed" else "complete"
            detail_part = "detailed" if "detailed" in parts else "standard"
        else:
            chart_name_part = filename
            date_part = "unknown"
            time_part = "unknown"
            category_part = "complete"
            detail_part = "standard"
        
        click.echo(f"{i:2d}. 📄 {file_path.name}")
        click.echo(f"    📊 Chart: {chart_name_part}")
        click.echo(f"    🎯 Type: {category_part} ({detail_part})")
        click.echo(f"    📅 Generated: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
        click.echo(f"    📏 Size: {file_size} bytes")
        
        if detailed:
            # Read first few lines to show content preview
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if len(lines) > 3:
                        preview = "".join(lines[1:4]).strip()  # Skip header, show next 3 lines
                        if len(preview) > 100:
                            preview = preview[:100] + "..."
                        click.echo(f"    📝 Preview: {preview}")
            except Exception:
                pass
        
        click.echo("")
    
    click.echo(f"💡 View a file with: cat data/output/interpretations/<filename>")
    click.echo(f"📁 Output directory: {output_dir.absolute()}")

# Add the chart group to main CLI
cli.add_command(chart)

if __name__ == '__main__':
    cli()