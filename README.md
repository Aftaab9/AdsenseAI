# AdsenseAI Campaign Risk Analyzer

A web-based campaign risk prediction and audience intelligence platform that implements the Theory of Planned Behaviour (TPB) framework to analyze multi-modal marketing content (text + images) for the Indian market.

## Overview

AdsenseAI predicts virality potential, backlash risk, and ad-fatigue by evaluating three key content characteristics:
- **Emotional-Moral Content (EMC)**: Affective cues and moral framing
- **Narrative Ambiguity (NAM)**: Interpretive openness and message clarity
- **Socio-Cultural Sensitivity (SCS)**: Alignment with Indian cultural norms

These characteristics influence **Perceived Intent**, which mediates audience behavioral responses through the TPB framework (Attitude, Subjective Norms, Perceived Control → Behavioral Intention).

## Features

### Campaign Risk Analysis
- 🎯 **TPB-Based Prediction**: Research-grounded framework for behavioral intention
- 🖼️ **Multi-Modal Analysis**: Text + image analysis using Google Gemini API
- 🇮🇳 **Indian Market Focus**: Cultural sensitivity detection for Indian context
- 📊 **Comprehensive Scoring**: Virality, backlash, and ad-fatigue predictions
- 🚦 **Actionable Recommendations**: Go/Caution/Stop decisions with reasoning
- 📅 **Festival Awareness**: Proximity alerts for major Indian festivals
- 🤖 **AI-Powered Suggestions**: Get specific tips to improve your campaign
- 📸 **Image-Only Analysis**: Analyze visual content without text using OCR
- 🎯 **Quick Examples**: Pre-loaded example campaigns for instant testing

### Audience Persona Testing
- 👥 **57 Pre-Built Personas**: Research-backed Indian market segments
- 🎭 **Multi-Persona Testing**: Test campaigns against multiple audiences simultaneously
- 📈 **Resonance Scoring**: Content-persona fit measurement (0-100)
- 💭 **Emotional Response Prediction**: Predict how each persona will feel
- 🎬 **Behavioral Prediction**: Predict actions (share, ignore, report)
- ⚠️ **Friction Point Analysis**: Identify content elements causing negative reactions
- ✨ **Opportunity Detection**: Find ways to improve content for specific personas
- 🎯 **AI Recommendations**: Get suggested target personas for your content
- 🗺️ **Audience Heatmap**: Visual comparison across all personas
- 🔧 **Custom Persona Builder**: Create your own audience segments

### Premium UI Design
- 🎨 **Glassmorphism Effects**: Modern, premium dark theme
- ✨ **Micro-Interactions**: Smooth animations and visual feedback
- 📱 **Fully Responsive**: Works beautifully on all devices
- ⚡ **Performance Optimized**: Minified CSS/JS for fast loading (70% size reduction)
- 🚀 **Smart Caching**: Instant results for repeated analyses

## Installation

### Prerequisites

- Python 3.9 or higher
- Google Gemini API key (free tier available)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd campaign-risk-analyzer
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download TextBlob corpora**
   ```bash
   python -m textblob.download_corpora
   ```

5. **Set up environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   
   # Edit .env and add your Gemini API key
   ```

6. **Get a Gemini API Key**
   - Visit: https://makersuite.google.com/app/apikey
   - Create a new API key
   - Add it to your `.env` file

## Usage

### Running the Application

**Quick Start:**
```bash
# Start the server (easiest method)
python start.py

# Or use uvicorn directly
uvicorn app.main:app --reload

# The application will be available at:
# http://localhost:8000
```

**Access Points:**
- **Web Interface**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc

### Using the Web Interface

1. **Quick Start with Examples**
   - Click one of the three example buttons:
     - ✅ **Safe: Diwali Celebration** - See a successful campaign
     - ⚠️ **Moderate: Festival Food** - Review a moderate-risk campaign
     - 🛑 **Risky: Colorism Content** - Understand what to avoid
   - Form auto-fills with example data
   - Click "Analyze Campaign" to see results

2. **Enter Your Own Campaign Details**
   - Type or paste your campaign caption
   - Select platform (Instagram, YouTube, TikTok, Twitter)
   - Choose posting date
   - Indicate if using influencer partnership
   - Optionally upload an image (or analyze image-only)

3. **Analyze**
   - Click "Analyze Campaign" button
   - Wait for results (< 2 seconds for text, < 5 seconds with image)
   - Cached results return instantly (<50ms)

4. **Review Results**
   - See recommendation (GO/CAUTION/STOP)
   - Check virality, backlash, and ad-fatigue scores
   - Review TPB framework breakdown
   - Read cultural alerts and AI-powered suggestions
   - View image analysis (if image provided)

5. **Test with Personas (Optional)**
   - Select target personas from the library
   - See how different audiences will respond
   - Get persona-specific recommendations
   - View audience heatmap for comparison

### API Endpoints

#### POST /api/analyze
Analyze campaign content for risk prediction.

**Request Body:**
```json
{
  "caption": "Celebrating India's diversity this Diwali! 🪔",
  "platform": "Instagram",
  "posting_date": "2025-10-18",
  "influencer": true,
  "image_base64": "data:image/jpeg;base64,...",
  "persona_ids": ["gen_z_metro", "millennial_professional"]
}
```

**Response:**
```json
{
  "emotional_moral_content": {
    "emc_score": 75,
    "emotions": ["joy", "pride"],
    "moral_framing": false
  },
  "tpb_scores": {
    "attitude": 82,
    "subjective_norms": 91,
    "perceived_control": 75,
    "behavioral_intention": 84
  },
  "virality_score": 88,
  "backlash_risk": 12,
  "ad_fatigue_risk": 25,
  "recommendation": {
    "status": "go",
    "action": "Good to Post",
    "message": "Content shows strong viral potential with minimal risk!"
  },
  "persona_analysis": {
    "persona_results": [...]
  }
}
```

#### GET /api/personas
Get list of all available personas.

**Query Parameters:**
- `category` (optional): Filter by category (e.g., "Generational", "Regional")

**Response:**
```json
[
  {
    "id": "gen_z_metro",
    "name": "Gen Z Metro",
    "category": "Generational",
    "age_range": "18-25",
    "description": "Urban Gen Z, digitally native..."
  }
]
```

#### GET /api/personas/{persona_id}
Get detailed information about a specific persona.

#### POST /api/analyze/personas
Analyze content against multiple personas.

#### GET /api/health
Check service health status.

## Project Structure

```
campaign-risk-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application & routes
│   ├── models.py                        # Pydantic request/response models
│   ├── analyzers/
│   │   ├── text_analyzer.py             # Text sentiment & emotion analysis
│   │   ├── cultural_sensitivity_detector.py  # Cultural sensitivity
│   │   ├── perceived_intent_calculator.py    # Perceived intent
│   │   ├── tpb_calculator.py            # TPB framework
│   │   ├── outcome_predictor.py         # Virality, backlash, ad-fatigue
│   │   ├── recommendation_engine.py     # Recommendation engine
│   │   ├── image_analyzer.py            # Gemini image analysis
│   │   ├── multimodal_fusion.py         # Text + image fusion
│   │   ├── persona_library.py           # Persona data management
│   │   ├── resonance_calculator.py      # Content-persona fit scoring
│   │   └── persona_tpb_modifier.py      # Persona-specific TPB
│   ├── data/
│   │   ├── data_loader.py               # Data loading utilities
│   │   ├── synthetic_data_generator.py  # Synthetic data generation
│   │   └── personas/                    # Persona JSON files
│   │       └── mvp_personas.json        # 57 pre-built personas
│   └── utils/
│       └── __init__.py
├── Data/                                # CSV datasets
│   ├── cultural_triggers.csv
│   ├── festival_calendar.csv
│   ├── historical_campaigns.csv
│   ├── Twitter_Data.csv
│   ├── Reddit_Data.csv
│   └── Instagram_Analytics.csv
├── templates/
│   └── index.html                       # Web interface
├── static/
│   ├── css/
│   │   └── styles.min.css               # Minified styles
│   ├── js/
│   │   ├── app.min.js                   # Minified main app
│   │   └── persona_testing.js           # Persona testing UI
│   └── examples/
│       └── images/                      # Sample campaign images
├── .kiro/
│   ├── specs/                           # Feature specifications
│   │   ├── campaign-risk-analyzer/
│   │   └── audience-persona-testing/
│   └── steering/                        # AI assistant guidance
├── .env.example                         # Environment variables template
├── .gitignore
├── requirements.txt
├── start.py                             # Server startup script
└── README.md
```

## Persona Categories

The system includes 57 research-backed personas across 11 categories:

| Category | Count | Examples |
|----------|-------|----------|
| **Generational** | 4 | Gen Z Metro, Millennial Professional, Gen X Parent, Boomer |
| **Regional** | 8 | North Urban, South Metro, East Traditional, West Business |
| **Lifestyle** | 5 | Achiever, Traditionalist, Explorer, Conscious Consumer |
| **Income/NCCS** | 5 | Premium Elite (A1), Upper Middle, Middle, Mass Market |
| **Digital Behavior** | 5 | Scroller, Engager, Creator, Skeptic, Impulse Buyer |
| **Values-Based** | 5 | Nationalist, Progressive, Pragmatist, Aspirational |
| **Family Stage** | 5 | Young Single, Newlywed, Young Parent, Empty Nester |
| **Health/Wellness** | 5 | Fitness Enthusiast, Ayurveda Believer, Modern Health |
| **Tech Adoption** | 5 | Early Adopter, Practical User, Digital Native |
| **Platform-Specific** | 5 | Instagram Aesthetic, YouTube Learner, Twitter Debater |
| **Rural** | 5 | Progressive Farmer, Rural Youth, Village Elder |

Each persona includes:
- Demographics (age, location, income)
- Psychographics (values, interests, personality traits)
- Digital behavior patterns
- Platform preferences
- Cultural sensitivities

## Technology Stack

- **Backend**: FastAPI, Python 3.9+, Uvicorn (ASGI server)
- **Text Analysis**: TextBlob, VADER Sentiment
- **Image Analysis**: Google Gemini API (gemini-1.5-flash)
- **Data Processing**: Pandas, NumPy
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **Fonts**: Space Grotesk, Inter (Google Fonts)

## Research Foundation

This system implements multiple research frameworks:

### Theory of Planned Behaviour (TPB)
- Ajzen, I. (1991). The theory of planned behavior. *Organizational Behavior and Human Decision Processes*, 50(2), 179-211.

### Audience Segmentation Frameworks
- **VALS Framework** (SRI International): Psychographic segmentation by values and lifestyles
- **Hofstede's Cultural Dimensions**: Cross-cultural behavior modeling
- **NCCS Classification**: Indian socioeconomic segmentation standard
- **Big Five Personality (OCEAN)**: Personality-based response prediction
- **McKinsey Consumer Decision Journey**: Purchase behavior modeling
- **Google Micro-Moments**: Intent-based targeting framework

### Hypotheses Tested

**Content Characteristics → Perceived Intent:**
- **H1**: Emotional-moral content influences perceived intent
- **H2**: Narrative ambiguity influences perceived intent
- **H3**: Socio-cultural sensitivity influences perceived intent

**Perceived Intent → Outcomes:**
- **H4a**: Perceived intent influences virality (positive intent → higher virality)
- **H4b**: Perceived intent influences backlash (negative intent → higher backlash)

**TPB Framework:**
- **H5**: TPB behavioral intention predicts virality
- **H6**: Cultural sensitivity violations predict backlash
- **H7**: Exposure intensity predicts ad-fatigue

**Persona-Specific:**
- **H8**: Content-persona resonance predicts engagement likelihood
- **H9**: Persona characteristics moderate TPB relationships
- **H10**: Friction points predict negative behavioral responses

## Data Sources

The system uses:
- **Provided Datasets**: Twitter_Data.csv, Reddit_Data.csv, Instagram_Analytics.csv, india_news_10000.csv
- **Synthetic Data**: Cultural triggers, festival calendar, historical campaigns (auto-generated)
- **Persona Library**: 57 research-backed Indian market personas (JSON format)

## Performance Targets

- **Text-only analysis**: < 2 seconds (first run), < 50ms (cached)
- **Text + image analysis**: < 5 seconds (includes Gemini API latency)
- **Multi-persona analysis (10 personas)**: < 1 second
- **Full persona library (57 personas)**: < 5 seconds
- **Page load time**: ~1.5 seconds (40% faster with optimizations)
- **File size savings**: 70% reduction in CSS, 60% in JavaScript

## Performance Optimizations

### Backend Caching
- **Response Cache**: Identical analyses return instantly (<50ms)
- **Sentiment Cache**: Text analysis results cached (>1000x speedup)
- **Data Loader**: CSV files loaded once and cached in memory
- **Persona Library**: Loaded at startup, cached for instant access

### Frontend Optimizations
- **Minified Assets**: CSS reduced from 50KB to 15KB, JS from 25KB to 10KB
- **DOM Caching**: Frequently accessed elements cached for faster manipulation
- **Lazy Loading**: Results section loaded only when needed
- **Chart Reuse**: Prevents memory leaks and improves performance

## Example Use Cases

### 1. Quick Testing with Examples
Try the pre-loaded examples to understand the system:
```
Click: "✅ Safe: Diwali Celebration"
Result: Green recommendation, high virality (80-90), low backlash (10-20)

Click: "⚠️ Moderate: Festival Food"
Result: Yellow recommendation, moderate scores, timing warnings

Click: "🛑 Risky: Colorism Content"
Result: Red recommendation, high backlash (80-95), critical alerts
```

### 2. Pre-Launch Campaign Testing
Test your campaign before posting to avoid cultural missteps:
```
Input: "Get fair skin in 7 days! #FairSkin"
Output: STOP - High backlash risk (colorism trigger detected)
```

### 3. Festival Campaign Planning
Ensure your festival campaigns are culturally appropriate:
```
Input: "Happy Diwali! Enjoy our meat special 🍖"
Output: CAUTION - Festival proximity alert (avoid meat during Diwali)
```

### 4. Audience Targeting
Find the right personas for your content:
```
Input: "Sustainable fashion for conscious consumers"
Output: High resonance with: Conscious Consumer, Gen Z Metro, Progressive
```

### 5. Multi-Persona Testing
Test how different audiences will respond:
```
Input: "Traditional values meet modern lifestyle"
Output: 
- Traditionalist: 85% resonance (will share)
- Progressive: 45% resonance (will ignore)
- Pragmatist: 70% resonance (will engage)
```

### 6. Image-Only Analysis
Analyze visual content without text:
```
Upload: Image with text overlay
Output: OCR extracts text, analyzes visual elements, cultural symbols
```

## Troubleshooting

### Common Issues

**1. Server won't start**
```bash
# Check if port 8000 is already in use
# On Windows:
netstat -ano | findstr :8000

# Kill the process or use a different port:
uvicorn app.main:app --port 8001
```

**2. Gemini API errors**
- Verify your API key in `.env` file
- Check API quota at https://makersuite.google.com
- Ensure you're using the free tier model: `gemini-1.5-flash`

**3. Persona library not loading**
- Check that `app/data/personas/mvp_personas.json` exists
- Verify JSON file is valid
- Check server logs for initialization errors

**4. Slow performance**
- First analysis may take 2-5 seconds (normal)
- Subsequent identical analyses return in <50ms (cached)
- Clear cache by restarting server if needed
- Consider upgrading to paid Gemini API tier for faster image analysis

**5. Example buttons not working**
- Check browser console (F12) for JavaScript errors
- Ensure server is running
- Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

**6. CSS/styling issues**
- Hard refresh to clear browser cache
- Verify minified files exist: `static/css/styles.min.css`, `static/js/app.min.js`
- Check browser console for 404 errors

## Testing

Run the comprehensive test suite:
```bash
# Run all tests
python -m pytest -v

# Run specific test file
python -m pytest test_comprehensive_e2e.py -v

# Run with coverage
python -m pytest --cov=app tests/
```

## Deployment

### Production Checklist
- [ ] Set `DEBUG=False` in environment
- [ ] Use production ASGI server (Gunicorn + Uvicorn workers)
- [ ] Enable HTTPS
- [ ] Set up rate limiting
- [ ] Configure CORS for your domain
- [ ] Set up monitoring and logging
- [ ] Use environment variables for all secrets
- [ ] Enable response caching
- [ ] Set up CDN for static files

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

This is a research-based implementation. For questions or contributions, please refer to the design and requirements documents in `.kiro/specs/campaign-risk-analyzer/`.

## License

[Add your license here]

## Acknowledgments

- Theory of Planned Behaviour framework by Icek Ajzen
- Indian market cultural sensitivity research
- Google Gemini API for multi-modal analysis
