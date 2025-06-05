# 🤝 Contributing to Astrology AI

Thank you for your interest in contributing to **Astrology AI**! This project aims to bridge ancient Vedic wisdom with modern AI technology, and we welcome contributions from developers, astrologers, and enthusiasts.

## 🎯 **How You Can Contribute**

### 📝 **Code Contributions**
- **Bug fixes** - Help us improve stability and reliability
- **Feature development** - Implement new functionality from our roadmap
- **Performance optimization** - Enhance processing speed and memory usage
- **Documentation** - Improve code documentation and user guides

### 📚 **Knowledge Contributions**
- **Classical texts** - Help us expand our source material
- **Rule validation** - Verify extracted rules against traditional sources
- **Translation assistance** - Help with Sanskrit-English translations
- **Test data** - Provide birth charts for testing and validation

### 🔍 **Quality Assurance**
- **Testing** - Write tests for new functionality
- **Bug reporting** - Identify issues and edge cases
- **Code review** - Review pull requests from other contributors
- **Performance testing** - Benchmark and profile code

---

## 🚀 **Getting Started**

### **1. Fork and Clone**
```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/astrology-ai.git
cd astrology-ai

# Add upstream remote
git remote add upstream https://github.com/original-owner/astrology-ai.git
```

### **2. Set Up Development Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Create necessary directories
mkdir -p data/{books,rules,charts,exports,logs,cache,backup,temp}
mkdir -p config
```

### **3. Initialize the System**
```bash
# Test the setup
python main.py cli --help
python main.py config

# Initialize database
python main.py cli init-db
python main.py cli stats
```

### **4. Run Tests**
```bash
# Run the full test suite
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
```

---

## 📋 **Development Workflow**

### **1. Create a Feature Branch**
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
# or  
git checkout -b docs/documentation-improvement
```

### **2. Make Your Changes**
- Follow our [coding standards](#-coding-standards)
- Write tests for new functionality
- Update documentation as needed
- Commit regularly with clear messages

### **3. Test Your Changes**
```bash
# Run all tests
pytest tests/ -v

# Check code quality
flake8 src/
black --check src/
mypy src/

# Run security checks
bandit -r src/
safety check
```

### **4. Submit a Pull Request**
- Push your branch to your fork
- Create a pull request with a clear description
- Link any related issues
- Wait for review and feedback

---

## 📐 **Coding Standards**

### **Python Style Guidelines**
- **Follow PEP 8** with 88-character line limit (Black formatting)
- **Use type hints** for all function signatures and class attributes
- **Write docstrings** for all public classes and functions
- **Prefer descriptive names** over abbreviated ones

### **Code Example**
```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class AstrologicalRule:
    """Represents an extracted astrological rule from classical texts.
    
    Attributes:
        id: Unique identifier for the rule
        text: Original rule text from source
        conditions: Planetary conditions (planet, house, sign, etc.)
        effects: Predicted outcomes
        source: Source book title
        confidence: Extraction confidence (0.0-1.0)
    """
    id: str
    text: str
    conditions: Dict[str, Any]
    effects: List[str]
    source: str
    confidence: float
    
    def __post_init__(self) -> None:
        """Validate rule data after initialization."""
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(f"Confidence must be between 0.0 and 1.0, got {self.confidence}")

def extract_planetary_rules(
    text: str, 
    min_confidence: float = 0.4,
    source_title: Optional[str] = None
) -> List[AstrologicalRule]:
    """Extract planetary placement rules from astrological text.
    
    Args:
        text: Input text containing astrological content
        min_confidence: Minimum confidence threshold for rule acceptance
        source_title: Name of the source book/document
        
    Returns:
        List of extracted astrological rules meeting confidence threshold
        
    Raises:
        ValueError: If min_confidence is not between 0.0 and 1.0
        ExtractionError: If text processing fails
        
    Example:
        >>> text = "Mars in the 7th house causes conflicts in marriage"
        >>> rules = extract_planetary_rules(text, min_confidence=0.5)
        >>> print(f"Extracted {len(rules)} rules")
    """
    if not 0.0 <= min_confidence <= 1.0:
        raise ValueError(f"min_confidence must be between 0.0 and 1.0")
    
    logger.info(f"Extracting rules from text with {min_confidence} confidence threshold")
    
    try:
        # Implementation here...
        rules = []
        # ... processing logic ...
        
        logger.info(f"Successfully extracted {len(rules)} rules")
        return rules
        
    except Exception as e:
        logger.error(f"Rule extraction failed: {e}")
        raise ExtractionError(f"Failed to extract rules: {e}") from e
```

### **Error Handling**
```python
# Custom exceptions for specific error types
class AstrologyAIError(Exception):
    """Base exception for Astrology AI errors."""
    pass

class ExtractionError(AstrologyAIError):
    """Raised when rule extraction fails."""
    pass

class ConfigurationError(AstrologyAIError):
    """Raised when configuration is invalid."""
    pass

# Use specific exception types
def process_pdf(pdf_path: str) -> ProcessingResult:
    try:
        # Processing logic
        return ProcessingResult.success()
    except FileNotFoundError:
        raise ExtractionError(f"PDF file not found: {pdf_path}")
    except PermissionError:
        raise ExtractionError(f"Permission denied reading: {pdf_path}")
```

### **Documentation Standards**
```python
class DocumentProcessor:
    """Processes PDF documents and extracts clean text for rule extraction.
    
    This class handles various PDF formats, applies OCR correction,
    and filters content for astrological relevance.
    
    Attributes:
        ocr_correction_enabled: Whether to apply OCR error correction
        min_text_length: Minimum text length for processing
        
    Example:
        >>> processor = DocumentProcessor(ocr_correction_enabled=True)
        >>> result = processor.process_pdf("classical_text.pdf")
        >>> if result.success:
        ...     print(f"Extracted {len(result.data)} characters")
    """
    
    def process_pdf(self, pdf_path: str, source_info: SourceInfo) -> ProcessingResult:
        """Process a PDF file and extract clean text.
        
        Args:
            pdf_path: Path to the PDF file to process
            source_info: Information about the source book
            
        Returns:
            ProcessingResult containing extracted text or error information
            
        Raises:
            ExtractionError: If PDF processing fails
            ConfigurationError: If processor is not properly configured
        """
```

---

## 🧪 **Testing Guidelines**

### **Test Structure**
```
tests/
├── unit/                   # Unit tests for individual components
│   ├── test_rule_extractor.py
│   ├── test_document_processor.py
│   └── test_knowledge_base.py
├── integration/            # Integration tests
│   ├── test_full_pipeline.py
│   └── test_cli_commands.py
├── fixtures/              # Test data and fixtures
│   ├── sample_texts.py
│   └── test_charts.json
└── conftest.py            # Pytest configuration
```

### **Writing Tests**
```python
import pytest
from unittest.mock import Mock, patch
from src.rule_extractor import RuleExtractor
from src.data_models import SourceInfo, AuthorityLevel

class TestRuleExtractor:
    """Test suite for RuleExtractor class."""
    
    @pytest.fixture
    def extractor(self):
        """Create a RuleExtractor instance for testing."""
        return RuleExtractor()
    
    @pytest.fixture
    def sample_source(self):
        """Create sample source information."""
        return SourceInfo(
            title="Test Classical Text",
            authority_level=AuthorityLevel.CLASSICAL
        )
    
    def test_extract_planet_from_simple_text(self, extractor):
        """Test planet extraction from straightforward text."""
        text = "Mars in the 7th house causes conflicts"
        planet = extractor.extract_planet_advanced(text)
        assert planet == "Mars"
    
    def test_extract_multiple_rules(self, extractor, sample_source):
        """Test extraction of multiple rules from text."""
        text = """
        Mars in the 7th house causes conflicts in marriage.
        Jupiter in the 5th house blesses with children.
        Saturn in the 10th house gives career success through hard work.
        """
        
        rules = extractor.extract_rules_from_text(text, sample_source)
        
        assert len(rules) >= 3
        assert any("Mars" in rule.conditions.get("planet", "") for rule in rules)
        assert any("Jupiter" in rule.conditions.get("planet", "") for rule in rules)
        assert any("Saturn" in rule.conditions.get("planet", "") for rule in rules)
    
    @patch('src.rule_extractor.logger')
    def test_extraction_logging(self, mock_logger, extractor, sample_source):
        """Test that extraction events are properly logged."""
        text = "Mars in the 7th house causes conflicts"
        extractor.extract_rules_from_text(text, sample_source)
        
        mock_logger.info.assert_called()
        
    def test_low_confidence_rules_filtered(self, extractor, sample_source):
        """Test that low confidence rules are properly filtered."""
        # Text that should produce low confidence
        text = "Some unclear text about planets maybe"
        
        rules = extractor.extract_rules_from_text(
            text, 
            sample_source, 
            min_confidence=0.7
        )
        
        assert all(rule.confidence >= 0.7 for rule in rules)
```

### **Integration Testing**
```python
def test_full_extraction_pipeline(tmp_path):
    """Test the complete pipeline from PDF to stored rules."""
    # Create test environment
    pdf_path = tmp_path / "test.pdf"
    create_test_pdf(pdf_path, sample_astrological_text)
    
    # Initialize components
    processor = DocumentProcessor()
    extractor = RuleExtractor()
    kb = KnowledgeBase(":memory:")
    
    # Run pipeline
    processing_result = processor.process_pdf(str(pdf_path))
    assert processing_result.success
    
    source = SourceInfo(title="Test", authority_level=AuthorityLevel.CLASSICAL)
    rules = extractor.extract_rules_from_text(processing_result.data, source)
    assert len(rules) > 0
    
    stored_count = kb.store_rules_batch(rules)
    assert stored_count == len(rules)
    
    # Verify storage
    retrieved_rules = kb.search_rules()
    assert len(retrieved_rules) == stored_count
```

---

## 📊 **Astrology Domain Guidelines**

### **Source Authority Hierarchy**
When contributing astrological content, respect the traditional authority hierarchy:

1. **Classical Texts (Highest Authority)**
   - Brihat Parashara Hora Shastra
   - Saravali by Kalyana Varma
   - Jataka Parijata by Vaidyanatha Dikshita
   - Phaladeepika by Mantreshwar

2. **Traditional Authorities**
   - Established commentaries on classical texts
   - Works by B.V. Raman
   - Regional traditional texts

3. **Modern Interpretations**
   - Contemporary synthesis works
   - Modern research and interpretation

### **Rule Extraction Guidelines**
```python
# Good - Specific, source-attributed rule
{
    "text": "Mars exalted in the 9th house makes the native fortunate in foreign lands",
    "conditions": {
        "planet": "Mars",
        "house": 9,
        "strength": "exalted"
    },
    "effects": ["fortune in foreign lands", "success abroad"],
    "source": "Brihat Parashara Hora Shastra 42.15",
    "confidence": 0.85
}

# Avoid - Vague or unsourced interpretations
{
    "text": "Mars might cause some issues maybe",
    "conditions": {"planet": "Mars"},
    "effects": ["possible problems"],
    "source": "Unknown",
    "confidence": 0.2
}
```

### **Terminology Standards**
- **Use Sanskrit terms** with English translations: "Lagna (Ascendant)"
- **Consistent planet names**: Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu
- **House numbering**: 1-12 (not Roman numerals)
- **Sign names**: Use English names (Aries, Taurus, etc.) with Sanskrit equivalents in metadata

---

## 🔄 **Development Phases**

### **Phase 1: Foundation (Current)**
- Document processing and rule extraction
- Knowledge base management
- CLI interface
- Source attribution system

**How to Contribute:**
- Improve extraction accuracy
- Add new source texts
- Enhance search capabilities
- Write comprehensive tests

### **Phase 2: AI Enhancement (Next)**
- Local AI integration
- Advanced interpretation engine
- Multiple output formats
- Context-aware rule matching

**How to Contribute:**
- AI prompt engineering
- Output quality evaluation
- Performance optimization
- User experience design

### **Phase 3: Advanced Features (Future)**
- Web interface
- Chart calculation
- Transit analysis
- Community features

---

## 🐛 **Bug Reports**

### **Before Reporting**
1. **Search existing issues** to avoid duplicates
2. **Test with latest version** from main branch
3. **Gather system information** (OS, Python version, dependencies)

### **Bug Report Template**
```markdown
## Bug Description
Clear description of what's happening vs. what should happen

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should have happened

## Actual Behavior
What actually happened

## Environment
- OS: [e.g., macOS 13.0, Ubuntu 22.04]
- Python: [e.g., 3.10.8]
- Astrology AI Version: [e.g., 1.0.0]

## Additional Context
- Error messages (full stack trace)
- Sample data that triggers the bug
- Screenshots if applicable

## Sample Data
If possible, provide minimal test data that reproduces the issue
```

---

## 💡 **Feature Requests**

### **Feature Request Template**
```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Why is this feature needed? What problem does it solve?

## Proposed Solution
How should this feature work?

## Alternative Solutions
Any alternative approaches considered?

## Implementation Notes
Technical considerations or suggestions

## Priority
- [ ] Critical (blocks current functionality)
- [ ] High (significant improvement)
- [ ] Medium (nice to have)
- [ ] Low (future enhancement)
```

---

## 🎓 **Learning Resources**

### **Vedic Astrology Fundamentals**
- **Planets (Grahas)**: Understanding planetary influences
- **Houses (Bhavas)**: Life areas and their meanings
- **Signs (Rashis)**: Zodiacal characteristics
- **Aspects (Drishti)**: Planetary influences between positions

### **Technical Resources**
- **Python Packaging**: [Python.org packaging guide](https://packaging.python.org/)
- **SQLite Documentation**: [SQLite.org](https://sqlite.org/docs.html)
- **Natural Language Processing**: [spaCy documentation](https://spacy.io/)
- **Type Hints**: [Python typing module](https://docs.python.org/3/library/typing.html)

### **Classical Texts (Public Domain)**
- Brihat Parashara Hora Shastra translations
- Saravali by Kalyana Varma
- Jataka Parijata translations
- Various commentary works

---

## ✅ **Pull Request Checklist**

Before submitting your pull request, ensure:

- [ ] **Code follows style guidelines** (Black, flake8, mypy pass)
- [ ] **All tests pass** (`pytest tests/ -v`)
- [ ] **New functionality has tests** (aim for >80% coverage)
- [ ] **Documentation is updated** (docstrings, README, etc.)
- [ ] **Classical accuracy maintained** (astrological content verified)
- [ ] **Source attribution included** (for any astrological interpretations)
- [ ] **Commit messages are clear** and follow conventional format
- [ ] **Branch is up to date** with main branch
- [ ] **No debugging code** or commented-out sections remain

### **Commit Message Format**
```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `perf`: Performance improvements

**Examples:**
```
feat(extractor): add Sanskrit term recognition

Implement pattern matching for Sanskrit astrological terms
alongside English equivalents for better rule extraction
from classical texts.

Closes #123
```

```
fix(knowledge_base): resolve duplicate rule detection

Fixed issue where rules with identical text but different
sources were incorrectly flagged as duplicates.

Fixes #456
```

---

## 🏆 **Recognition**

We value all contributions and maintain a contributors list in our documentation. Significant contributions will be acknowledged in:

- **README.md** contributors section
- **Documentation** author credits
- **Release notes** for major contributions
- **Classical text acknowledgments** for source material contributions

---

## ❓ **Questions?**

- **GitHub Discussions**: For general questions and community discussion
- **GitHub Issues**: For bug reports and feature requests
- **Email**: Contact maintainers directly for sensitive issues

---

**Thank you for helping us bridge ancient wisdom with modern technology! 🌟**

Every contribution, no matter how small, helps make Astrology AI more accurate, accessible, and valuable for the global community of astrology enthusiasts.

*May your code be bug-free and your interpretations be accurate!* ✨ 