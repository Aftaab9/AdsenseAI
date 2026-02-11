# AdsenseAI User Guide

Complete guide to using the AdsenseAI Campaign Risk Analyzer for predicting campaign performance and audience reactions in the Indian market.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Quick Start with Examples](#quick-start-with-examples)
3. [Analyzing Your Campaign](#analyzing-your-campaign)
4. [Understanding Results](#understanding-results)
5. [Persona Testing](#persona-testing)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)
8. [Advanced Features](#advanced-features)

---

## Getting Started

### Prerequisites

Before using AdsenseAI, ensure you have:
- ✅ Server running at http://localhost:8000
- ✅ Google Gemini API key configured (for image analysis)
- ✅ Modern web browser (Chrome, Firefox, Safari, Edge)

### Accessing the Application

1. **Start the server** (if not already running):
   ```bash
   python start.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:8000
   ```

3. **You should see**:
   - Dark-themed interface with glassmorphism effects
   - Input form on the left
   - "How It Works" panel on the right with example buttons
   - Clean, modern design

---

## Quick Start with Examples

The fastest way to understand AdsenseAI is to try the pre-loaded examples.

### Example 1: ✅ Safe Campaign (Diwali Celebration)

**What it demonstrates**: A culturally appropriate, positive festival campaign

**Steps**:
1. Click the **"✅ Safe: Diwali Celebration"** button
2. Form auto-fills with:
   - Caption: "Celebrating India's diversity this Diwali! 🪔..."
   - Platform: Instagram
   - Date: Near Diwali
3. Click **"Analyze Campaign"**

**Expected Results**:
- 🟢 **Recommendation**: "Good to Post"
- **Virality Score**: 80-90 (High)
- **Backlash Risk**: 10-20 (Low)
- **Ad-Fatigue Risk**: 20-30 (Low)
- **Cultural Alerts**: None
- **Sentiment**: Positive (joy, pride, celebration)

**Key Takeaway**: Positive festival content with cultural respect performs well.

---

### Example 2: ⚠️ Moderate Risk (Festival Food)

**What it demonstrates**: Content that requires careful timing and context

**Steps**:
1. Click the **"⚠️ Moderate: Festival Food"** button
2. Form auto-fills with food promotion content
3. Click **"Analyze Campaign"**

**Expected Results**:
- 🟡 **Recommendation**: "Review Required"
- **Virality Score**: 40-60 (Moderate)
- **Backlash Risk**: 40-60 (Moderate)
- **Cultural Alerts**: Festival timing warnings
- **Suggestions**: Avoid non-veg during Hindu festivals

**Key Takeaway**: Commercial content needs careful timing around festivals.

---

### Example 3: 🛑 High Risk (Colorism Content)

**What it demonstrates**: Content that violates cultural norms and will cause backlash

**Steps**:
1. Click the **"🛑 Risky: Colorism Content"** button
2. Form auto-fills with problematic beauty standards
3. Click **"Analyze Campaign"**

**Expected Results**:
- 🔴 **Recommendation**: "Do Not Post"
- **Virality Score**: 20-40 (Low)
- **Backlash Risk**: 80-95 (Critical)
- **Cultural Alerts**: Critical colorism triggers
- **Perceived Intent**: Manipulative/harmful

**Key Takeaway**: Colorism and discriminatory content will cause severe backlash.

---

## Analyzing Your Campaign

### Step 1: Enter Campaign Content

#### Text Input
1. **Click in the caption field**
2. **Type or paste your campaign text**
   - Social media post
   - Ad copy
   - Marketing message
3. **Character counter** shows length in real-time
4. **Tips**:
   - Keep it concise (< 100 words for best results)
   - Include relevant hashtags
   - Use emojis naturally

#### Image Upload (Optional)
1. **Drag and drop** an image onto the upload area, OR
2. **Click "Choose File"** to browse
3. **Supported formats**: JPEG, PNG, GIF, WebP
4. **Max size**: 10MB
5. **Preview** appears after upload

**Image-Only Analysis**:
- You can analyze images without text
- System extracts text from image using OCR
- Visual elements analyzed for cultural sensitivity

---

### Step 2: Configure Campaign Settings

#### Platform Selection
Choose your target platform:
- **Instagram**: High social signaling, visual focus
- **YouTube**: Individual consumption, longer content
- **TikTok**: Trend-driven, high virality potential
- **Twitter**: Discourse-oriented, text-heavy

**Why it matters**: Platform affects subjective norms score in TPB framework.

#### Posting Date
1. **Click the date picker**
2. **Select your planned posting date**
3. **System checks**:
   - Festival proximity (within 7 days)
   - Seasonal sensitivity
   - Cultural timing

**Why it matters**: Posting near festivals requires extra cultural sensitivity.

#### Influencer Partnership
- **Check the box** if using influencer marketing
- **Adds +25 boost** to subjective norms score
- **Increases** virality potential

---

### Step 3: Run Analysis

1. **Click "Analyze Campaign"** button
2. **Loading animation** appears
3. **Wait time**:
   - Text-only: < 2 seconds (first run)
   - Text-only (cached): < 50ms
   - Text + image: < 5 seconds

4. **Results appear** with smooth animations

---

## Understanding Results

### Overall Recommendation

Your campaign receives one of three recommendations:

#### 🟢 Good to Post (Green)
**Criteria**:
- Backlash risk < 40%
- No critical cultural alerts
- Positive perceived intent
- Optional: High virality (>60%)

**Action**: Safe to proceed with campaign

**Example**: "Celebrating India's diversity this Diwali!"

---

#### 🟡 Review Required (Yellow)
**Criteria**:
- Backlash risk 40-69%
- Some cultural alerts present
- Neutral to slightly negative perceived intent

**Action**: Review suggestions and revise content

**Example**: "Festival food promotion" (timing-dependent)

---

#### 🔴 Do Not Post (Red)
**Criteria**:
- Backlash risk ≥ 70%
- Critical cultural alerts
- Negative perceived intent (<-50)

**Action**: Abandon or completely rework campaign

**Example**: "Fair skin is the key to beauty"

---

### Score Cards

#### Virality Score (0-100)
**What it measures**: Likelihood of voluntary sharing and amplification

**Factors**:
- TPB behavioral intention
- Emotional content strength
- Platform amplification factors
- Sentiment polarity

**Interpretation**:
- **80-100**: Highly viral potential
- **60-79**: Good sharing likelihood
- **40-59**: Moderate engagement
- **0-39**: Limited spread

---

#### Backlash Risk (0-100)
**What it measures**: Probability of negative collective reaction

**Factors**:
- Cultural trigger risk weights
- Negative perceived intent
- Sentiment negativity
- Content subjectivity

**Interpretation**:
- **70-100**: Critical risk - Do not post
- **40-69**: Moderate risk - Review required
- **20-39**: Low risk - Minor concerns
- **0-19**: Minimal risk - Safe

---

#### Ad-Fatigue Risk (0-100)
**What it measures**: Decreased attention from repetitive exposure

**Factors**:
- Content length
- Hashtag count
- Subjectivity level
- Exposure intensity

**Interpretation**:
- **70-100**: High fatigue - Content feels spammy
- **40-69**: Moderate fatigue - May annoy users
- **20-39**: Low fatigue - Acceptable
- **0-19**: Fresh content - Engaging

---

### TPB Framework Breakdown

The Theory of Planned Behaviour predicts behavioral intention through three components:

#### Attitude (40% weight)
**What it measures**: Emotional appeal and favorability

**Based on**:
- Sentiment polarity
- Emotional-moral content
- Perceived intent

**Score interpretation**:
- **80-100**: Highly favorable
- **60-79**: Positive attitude
- **40-59**: Neutral
- **0-39**: Negative attitude

---

#### Subjective Norms (35% weight)
**What it measures**: Social influence and acceptability

**Based on**:
- Platform multipliers
- Influencer boost
- Cultural alignment
- Pride/nostalgia emotions

**Score interpretation**:
- **80-100**: Strong social approval
- **60-79**: Positive social influence
- **40-59**: Neutral social context
- **0-39**: Social resistance

---

#### Perceived Control (25% weight)
**What it measures**: Ease of engagement

**Based on**:
- Message clarity
- Narrative ambiguity
- Sentiment positivity

**Score interpretation**:
- **80-100**: Very easy to engage
- **60-79**: Easy to understand
- **40-59**: Some effort required
- **0-39**: Confusing or difficult

---

#### Behavioral Intention (Combined)
**Formula**: Attitude (40%) + Subjective Norms (35%) + Perceived Control (25%)

**What it predicts**: Likelihood of sharing/engaging

**Score interpretation**:
- **80-100**: Very likely to share
- **60-79**: Likely to engage
- **40-59**: May engage
- **0-39**: Unlikely to engage

---

### Cultural Alerts

Cultural alerts flag potentially sensitive content:

#### Severity Levels

**🔴 Critical (35-40 points)**
- Immediate action required
- High backlash probability
- Examples: Beef, colorism, geopolitical issues

**🟠 High (25-30 points)**
- Significant concern
- Moderate backlash risk
- Examples: Pork, interfaith, alcohol

**🟡 Medium (15-20 points)**
- Caution advised
- Context-dependent risk
- Examples: Festival timing, regional sensitivity

**🟢 Low (5-10 points)**
- Minor concern
- Low risk with proper context
- Examples: Generic cultural references

#### Alert Details

Each alert shows:
- **Keyword**: The trigger word detected
- **Category**: Type of sensitivity (Religious, Colorism, Geopolitical, etc.)
- **Message**: Explanation of the concern
- **Risk Weight**: Numerical impact on backlash score

---

### Sentiment Analysis

#### Polarity (-1 to +1)
- **Positive (0.1 to 1.0)**: Optimistic, favorable
- **Neutral (-0.1 to 0.1)**: Factual, balanced
- **Negative (-1.0 to -0.1)**: Critical, unfavorable

#### Subjectivity (0 to 1)
- **Objective (0 to 0.3)**: Factual, informative
- **Balanced (0.3 to 0.7)**: Mix of fact and opinion
- **Subjective (0.7 to 1.0)**: Opinion-heavy, promotional

#### Emotions Detected
- **Joy**: Happiness, celebration
- **Pride**: National/cultural pride
- **Nostalgia**: Memories, tradition
- **Humor**: Comedy, lightheartedness
- **Anger**: Frustration, outrage
- **Fear**: Anxiety, concern
- **Inspiration**: Motivation, aspiration

---

### AI-Powered Suggestions

The system provides actionable recommendations:

#### Types of Suggestions

**1. Content Revisions**
- Remove problematic keywords
- Rephrase sensitive statements
- Add positive framing

**2. Timing Recommendations**
- Avoid specific festival periods
- Suggest better posting dates
- Seasonal considerations

**3. Audience Targeting**
- Recommended personas
- Demographic fit
- Platform suggestions

**4. Viral Potential Optimization**
- Add emotional storytelling
- Include trending hashtags
- Improve call-to-action

---

### Image Analysis (When Image Uploaded)

#### Visual Elements Detected
- **Emotions**: Joy, celebration, pride, etc.
- **Cultural Symbols**: Religious icons, national symbols
- **Text Overlays**: OCR-extracted text
- **Brand Elements**: Logos, products
- **Festival References**: Diwali diyas, Holi colors, etc.

#### Visual Sensitivity Flags
- Religious imagery
- Political references
- Colorism indicators
- Inappropriate content

#### Multi-Modal Fusion
- **Combined EMC**: Text (60%) + Visual (40%)
- **Combined SCS**: Maximum of text and visual scores
- **Unified Analysis**: Holistic content assessment

---

## Persona Testing

### What is Persona Testing?

Test your campaign against 57 research-backed Indian market personas to understand how different audiences will respond.

### Accessing Persona Testing

1. **Scroll down** after campaign analysis
2. **Find "Persona Testing"** section
3. **Click "Test with Personas"** button

### Selecting Personas

#### Option 1: Browse by Category
- **Generational**: Gen Z, Millennials, Gen X, Boomers
- **Regional**: North, South, East, West India
- **Lifestyle**: Achievers, Traditionalists, Explorers
- **Income**: Premium, Upper Middle, Middle, Mass Market
- **Digital Behavior**: Scrollers, Engagers, Creators
- **Values**: Nationalist, Progressive, Pragmatist
- **Family Stage**: Singles, Newlyweds, Parents
- **Health**: Fitness Enthusiasts, Ayurveda Believers
- **Tech**: Early Adopters, Digital Natives
- **Platform**: Instagram, YouTube, Twitter users
- **Rural**: Farmers, Rural Youth, Village Elders

#### Option 2: Quick Presets
- **Urban Youth**: Gen Z + Millennials + Digital Natives
- **Traditional**: Boomers + Traditionalists + Rural
- **Premium**: High income + Early Adopters + Achievers

#### Option 3: Select All
- Test against all 57 personas
- Takes ~5 seconds
- Comprehensive audience view

### Understanding Persona Results

#### Resonance Score (0-100)
**What it measures**: Content-persona fit

**Components**:
- Value alignment (25%)
- Tone match (20%)
- Interest relevance (20%)
- Cultural fit (15%)
- Platform fit (10%)
- Emotional resonance (10%)

**Interpretation**:
- **80-100**: Excellent fit - Will love it
- **60-79**: Good fit - Will engage
- **40-59**: Moderate fit - May engage
- **20-39**: Poor fit - Will ignore
- **0-19**: Very poor fit - May react negatively

---

#### Emotional Response Prediction

For each persona, see predicted emotions:
- **Primary Emotion**: Strongest feeling (joy, pride, anger, etc.)
- **Secondary Emotions**: Additional feelings
- **Intensity**: How strongly they'll feel

---

#### Behavioral Prediction

Predicted actions:
- **Share**: Will amplify content
- **Engage**: Will like/comment
- **Ignore**: Will scroll past
- **Report**: Will flag as inappropriate

---

#### Friction Points

Elements causing negative reactions:
- Specific words or phrases
- Cultural misalignment
- Tone mismatch
- Value conflicts

---

#### Opportunity Zones

Ways to improve for this persona:
- Add relevant themes
- Adjust tone
- Include specific interests
- Cultural adaptations

---

### Audience Heatmap

Visual comparison across all tested personas:

**Color Coding**:
- 🟢 **Green (80-100)**: Excellent resonance
- 🟡 **Yellow (60-79)**: Good resonance
- 🟠 **Orange (40-59)**: Moderate resonance
- 🔴 **Red (0-39)**: Poor resonance

**Use Cases**:
- Identify best-fit personas
- Spot problematic segments
- Compare across categories
- Optimize targeting

---

## Best Practices

### Content Creation

#### DO ✅
- **Use positive, inclusive language**
- **Respect cultural and religious diversity**
- **Time content appropriately around festivals**
- **Include authentic emotional storytelling**
- **Show diverse representation**
- **Focus on values and benefits**
- **Use natural, conversational tone**

#### DON'T ❌
- **Use colorism language** (fair, whitening, gora)
- **Reference geopolitical conflicts** (Pakistan, Kashmir)
- **Compare religions or castes**
- **Promote alcohol/beef insensitively**
- **Use manipulative emotional tactics**
- **Post controversial content during festivals**
- **Make unrealistic claims**

---

### Festival Marketing

#### Major Indian Festivals

**Diwali (October/November)**
- ✅ DO: Celebrate light, prosperity, family
- ❌ DON'T: Promote alcohol, meat, negative themes

**Eid (Varies)**
- ✅ DO: Inclusive celebration, peace messages
- ❌ DON'T: Pork, alcohol, insensitive imagery

**Holi (March)**
- ✅ DO: Colors, joy, celebration
- ❌ DON'T: Non-consensual themes, harassment

**Independence Day (August 15)**
- ✅ DO: Patriotism, unity, national pride
- ❌ DON'T: Political controversy, Pakistan references

**Republic Day (January 26)**
- ✅ DO: Constitutional values, democracy
- ❌ DON'T: Political debates, divisive content

---

### Platform-Specific Tips

#### Instagram
- **Visual-first**: High-quality images essential
- **Hashtags**: 5-10 relevant hashtags
- **Tone**: Aspirational, aesthetic
- **Best for**: Lifestyle, fashion, food, travel

#### YouTube
- **Long-form**: Detailed, informative content
- **Educational**: How-to, tutorials, reviews
- **Tone**: Authentic, conversational
- **Best for**: Education, entertainment, reviews

#### TikTok
- **Trend-driven**: Follow current trends
- **Short-form**: Quick, engaging content
- **Tone**: Fun, energetic, creative
- **Best for**: Entertainment, challenges, viral content

#### Twitter
- **Text-heavy**: Strong copy essential
- **Discourse**: Engage in conversations
- **Tone**: Witty, informative, timely
- **Best for**: News, opinions, real-time updates

---

### Persona Targeting

#### Urban Youth (Gen Z + Millennials)
- **Values**: Authenticity, diversity, sustainability
- **Interests**: Technology, social causes, entertainment
- **Tone**: Casual, relatable, meme-friendly
- **Platforms**: Instagram, TikTok, Twitter

#### Traditional Audiences (Boomers + Gen X)
- **Values**: Family, tradition, respect
- **Interests**: Health, family, spirituality
- **Tone**: Respectful, formal, value-driven
- **Platforms**: YouTube, Facebook

#### Premium Segment
- **Values**: Quality, exclusivity, innovation
- **Interests**: Luxury, travel, technology
- **Tone**: Sophisticated, aspirational
- **Platforms**: Instagram, LinkedIn

---

## Troubleshooting

### Analysis Issues

**Problem**: Analysis takes too long
- **Solution**: First analysis may take 2-5 seconds (normal)
- **Solution**: Subsequent identical analyses return in <50ms (cached)
- **Solution**: Check internet connection for image analysis

**Problem**: "API Error" message
- **Solution**: Verify Gemini API key in `.env` file
- **Solution**: Check API quota at https://makersuite.google.com
- **Solution**: Restart server: `python start.py`

**Problem**: Unexpected results
- **Solution**: Review cultural alerts for explanations
- **Solution**: Check if content matches Indian cultural context
- **Solution**: Try example campaigns to verify system working

---

### Interface Issues

**Problem**: Example buttons not working
- **Solution**: Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
- **Solution**: Check browser console (F12) for errors
- **Solution**: Ensure JavaScript enabled

**Problem**: Styling looks broken
- **Solution**: Clear browser cache
- **Solution**: Verify minified files exist: `static/css/styles.min.css`
- **Solution**: Try different browser

**Problem**: Image upload fails
- **Solution**: Check file size (max 10MB)
- **Solution**: Verify file format (JPEG, PNG, GIF, WebP)
- **Solution**: Try different image

---

### Persona Testing Issues

**Problem**: Personas not loading
- **Solution**: Check `app/data/personas/mvp_personas.json` exists
- **Solution**: Verify JSON file is valid
- **Solution**: Restart server

**Problem**: Slow persona analysis
- **Solution**: Testing all 57 personas takes ~5 seconds (normal)
- **Solution**: Select fewer personas for faster results
- **Solution**: Use quick presets for common segments

---

## Advanced Features

### API Access

Use the REST API for programmatic access:

```bash
# Analyze campaign
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Your campaign text",
    "platform": "Instagram",
    "posting_date": "2025-10-20",
    "influencer": true
  }'

# Get personas
curl http://localhost:8000/api/personas

# Get specific persona
curl http://localhost:8000/api/personas/gen_z_metro
```

**Documentation**: http://localhost:8000/docs

---

### Caching System

The system automatically caches results for performance:

**What's cached**:
- Text-only analysis results
- Sentiment analysis
- Emotion detection
- Persona library

**Cache duration**: Until server restart

**Clear cache**: Restart server with `python start.py`

---

### Export Results

**Coming Soon**:
- PDF report generation
- JSON data export
- Shareable result links
- Campaign history tracking

---

## Getting Help

### Resources

- **API Documentation**: http://localhost:8000/docs
- **Example Campaigns**: `static/examples/EXAMPLE_CAMPAIGNS.md`
- **Image Guide**: `static/examples/HOW_TO_ADD_IMAGES.md`
- **Sample Images**: `static/examples/SAMPLE_IMAGES_DOCUMENTATION.md`

### Support

- Check server logs for errors
- Review browser console (F12) for frontend issues
- Verify environment variables in `.env`
- Ensure all dependencies installed: `pip install -r requirements.txt`

---

## Conclusion

AdsenseAI helps you create culturally appropriate, engaging campaigns for the Indian market. By combining TPB framework analysis, cultural sensitivity detection, and persona testing, you can:

✅ Avoid cultural missteps and backlash
✅ Optimize content for virality
✅ Target the right audiences
✅ Make data-driven decisions
✅ Save time and resources

**Start with the examples, then analyze your own campaigns!**

---

*Last Updated: January 2026*
*Version: 1.0*
*For questions or issues, check the troubleshooting section or review server logs.*
