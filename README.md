# Narrative Analyzer

An AI-powered web application that helps users distinguish between facts, claims, opinions, emotional language, missing context, and questions for further verification in articles, social media posts, opinion pieces, and other written content.

## Overview

**Narrative Analyzer** provides critical thinking tools for content analysis by breaking down text into distinct categories:
- **Facts**: Verifiable statements about objective reality
- **Claims**: Assertions that may require evidence
- **Opinions**: Subjective interpretations and perspectives
- **Emotional Language**: Language designed to evoke emotional responses
- **Missing Context**: Gaps in information or perspective
- **Questions for Further Verification**: Topics requiring additional investigation

This tool is designed for journalists, researchers, educators, students, and anyone seeking to critically evaluate written content.

## Features (Planned)

### Phase 1: MVP Foundation
- ✅ Text input interface with character counter
- ✅ File upload support (TXT, Markdown)
- ✅ Expandable UI sections for analysis categories
- ⏳ Mock data for demonstration
- ⏳ Clean, responsive Streamlit interface

### Phase 2: AI Integration
- ⏳ OpenAI-powered text analysis
- ⏳ Real-time categorization
- ⏳ Confidence scoring for each category
- ⏳ Explanation generation for identified elements

### Phase 3: Enhanced Features
- ⏳ Batch file processing
- ⏳ Analysis history and saved reports
- ⏳ Export analysis results (JSON, PDF)
- ⏳ Comparative analysis across multiple texts

### Phase 4: Production Deployment
- ⏳ Performance optimization
- ⏳ Caching and rate limiting
- ⏳ User authentication
- ⏳ Analytics and logging

## Folder Structure

```
narrative-analyzer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
├── config/               # Configuration files (Phase 2)
├── services/             # Business logic and AI services (Phase 2)
├── utils/                # Helper functions and utilities (Phase 2)
├── components/           # Reusable UI components (Phase 2)
├── tests/                # Unit and integration tests (Phase 3)
├── data/                 # Sample data and test files (Phase 3)
└── docs/                 # Extended documentation (Phase 3)
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend Framework** | Streamlit |
| **LLM API** | OpenAI (GPT-4 / GPT-3.5-turbo) |
| **Language** | Python 3.9+ |
| **Data Validation** | Pydantic |
| **Environment Management** | python-dotenv |
| **Version Control** | Git / GitHub |

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- OpenAI API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yuliahartati/narrative-analyzer.git
   cd narrative-analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

The application will open at `http://localhost:8501`

## Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_api_key_here

# Optional: Model configuration (Phase 2)
# OPENAI_MODEL=gpt-4
# ANALYSIS_TEMPERATURE=0.3
```

**Important**: Never commit `.env` files to version control. Use `.env.example` as a template.

## Usage

### Basic Text Analysis
1. Enter or paste text into the input area
2. (Phase 2) Click "Analyze" to process
3. Review categorized results in expandable sections
4. (Phase 3) Export or save results as needed

### File Upload
1. Click "Upload File" and select a TXT or Markdown file
2. Content automatically populates the text area
3. (Phase 2) Proceed with analysis

## Roadmap

### Q1 2026: MVP Release
- [x] Project scaffolding and structure
- [ ] Streamlit UI implementation
- [ ] Mock data layer
- [ ] Basic file handling

### Q2 2026: AI Integration
- [ ] OpenAI API integration
- [ ] Text categorization pipeline
- [ ] Confidence scoring
- [ ] Error handling and logging

### Q3 2026: Feature Enhancement
- [ ] Batch processing
- [ ] Analysis caching
- [ ] Export functionality
- [ ] Performance optimization

### Q4 2026: Production Ready
- [ ] User authentication
- [ ] Database integration
- [ ] Rate limiting
- [ ] Deployment pipeline

## API Integration (Phase 2)

This project uses OpenAI's API for text analysis. Ensure you have:
- A valid OpenAI API key
- Sufficient API credits
- Understanding of [OpenAI's usage policies](https://platform.openai.com/docs/guides/usage)

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Screenshots

*Screenshots will be added in Phase 2 after UI implementation*

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

**Author**: Yulia Hartati  
**Email**: [Your email]  
**GitHub**: [@yuliahartati](https://github.com/yuliahartati)

## Disclaimer

This tool is designed to assist in critical analysis. It should not be the sole basis for fact-checking or verification. Always cross-reference with authoritative sources for important claims.

---

**Last Updated**: September 2026  
**Status**: Phase 1 - MVP Foundation
