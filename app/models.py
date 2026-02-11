# AdsenseAI Campaign Risk Analyzer - Pydantic Models

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class CampaignRequest(BaseModel):
    """Request model for campaign analysis"""
    caption: Optional[str] = Field(None, description="Campaign text content (caption, ad copy, post) - optional if image is provided")
    platform: str = Field(..., description="Social media platform (Instagram, YouTube, TikTok, Twitter)")
    posting_date: Optional[str] = Field(None, description="Planned posting date (YYYY-MM-DD)")
    influencer: bool = Field(False, description="Whether this is an influencer partnership")
    image_base64: Optional[str] = Field(None, description="Base64 encoded campaign image")
    image_only: bool = Field(False, description="Flag indicating image-only analysis mode")

    class Config:
        json_schema_extra = {
            "example": {
                "caption": "Celebrating India's diversity this Diwali! 🪔",
                "platform": "Instagram",
                "posting_date": "2025-10-18",
                "influencer": True,
                "image_base64": None,
                "image_only": False
            }
        }


class EmotionalMoralContent(BaseModel):
    """Emotional-moral content analysis results"""
    emc_score: float = Field(..., description="Emotional-moral content score (0-100)")
    emotions: List[str] = Field(..., description="Detected emotions")
    moral_framing: bool = Field(..., description="Whether moral framing is present")
    arousal_level: float = Field(..., description="Emotional arousal level (0-1)")


class NarrativeAmbiguity(BaseModel):
    """Narrative ambiguity analysis results"""
    nam_score: float = Field(..., description="Narrative ambiguity score (0-100)")
    clarity: float = Field(..., description="Message clarity score (0-100)")
    interpretive_openness: float = Field(..., description="Interpretive openness score (0-100)")


class SocioCulturalSensitivity(BaseModel):
    """Socio-cultural sensitivity analysis results"""
    scs_score: float = Field(..., description="Socio-cultural sensitivity score (0-100)")
    triggers_found: int = Field(..., description="Number of cultural triggers detected")
    festival_proximity: Optional[Dict[str, Any]] = Field(None, description="Festival proximity alert")


class PerceivedIntent(BaseModel):
    """Perceived intent analysis results"""
    intent_score: float = Field(..., description="Perceived intent score (-100 to +100)")
    authenticity: float = Field(..., description="Authenticity score (0-100)")
    manipulation_risk: float = Field(..., description="Manipulation risk score (0-100)")
    interpretation: str = Field(..., description="Intent interpretation")


class TPBScores(BaseModel):
    """Theory of Planned Behaviour framework scores"""
    attitude: float = Field(..., description="Attitude toward behavior (0-100)")
    subjective_norms: float = Field(..., description="Subjective norms score (0-100)")
    perceived_control: float = Field(..., description="Perceived behavioral control (0-100)")
    behavioral_intention: float = Field(..., description="Behavioral intention (0-100)")


class SentimentAnalysis(BaseModel):
    """Sentiment analysis results"""
    polarity: float = Field(..., description="Sentiment polarity (-1 to +1)")
    subjectivity: float = Field(..., description="Subjectivity score (0 to 1)")
    positive: float = Field(..., description="Positive sentiment percentage")
    negative: float = Field(..., description="Negative sentiment percentage")
    neutral: float = Field(..., description="Neutral sentiment percentage")
    label: str = Field(..., description="Overall sentiment label")


class CulturalAlert(BaseModel):
    """Cultural sensitivity alert"""
    keyword: str = Field(..., description="Trigger keyword detected")
    category: str = Field(..., description="Alert category")
    severity: str = Field(..., description="Severity level (low, medium, high, critical)")
    risk_weight: int = Field(..., description="Risk weight value")
    message: str = Field(..., description="Alert message")


class Recommendation(BaseModel):
    """Campaign recommendation"""
    status: str = Field(..., description="Recommendation status (go, caution, stop)")
    action: str = Field(..., description="Recommended action")
    message: str = Field(..., description="Recommendation message")
    reasoning: List[str] = Field(..., description="Reasoning for recommendation")
    suggestions: List[str] = Field(..., description="Suggestions for improvement")


class SimilarCampaign(BaseModel):
    """Similar historical campaign"""
    brand: str = Field(..., description="Brand name")
    campaign: str = Field(..., description="Campaign name")
    outcome: str = Field(..., description="Campaign outcome")
    lesson: str = Field(..., description="Lesson learned")


class ImageAnalysis(BaseModel):
    """Image analysis results"""
    visual_emotions: List[str] = Field(..., description="Visual emotions detected")
    cultural_symbols: List[str] = Field(..., description="Cultural symbols identified")
    sensitivity_flags: List[str] = Field(..., description="Sensitivity flags")
    text_overlay: str = Field(..., description="Text overlay detected in image")
    visual_emc_score: float = Field(..., description="Visual EMC score")


# ============================================================================
# PERSONA TESTING MODELS (Forward declarations for AnalysisResponse)
# Added for Audience Persona Testing Feature
# Requirements: 1.2, 2.1-2.4
# ============================================================================

from enum import Enum
from typing import Tuple


class PersonaCategory(str, Enum):
    """MVP persona categories (6 categories for initial release)"""
    GENERATIONAL = "generational"      # Gen Z, Millennials, Gen X, Boomers
    REGIONAL = "regional"              # North, South, East, West, Northeast
    LIFESTYLE = "lifestyle"            # Achiever, Traditionalist, Explorer
    INCOME = "income"                  # NCCS A1-E segments
    DIGITAL = "digital"                # Scroller, Engager, Creator, Skeptic
    VALUES = "values"                  # Nationalist, Progressive, Pragmatist


class PersonaAnalysisResult(BaseModel):
    """Result of analyzing content against a single persona"""
    persona_id: str
    persona_name: str
    avatar_emoji: Optional[str] = Field(None, description="Persona avatar emoji")
    tagline: Optional[str] = Field(None, description="Persona tagline")
    
    # Core Scores (0-100)
    resonance_score: float = Field(..., ge=0, le=100, description="Overall content-persona fit")
    engagement_likelihood: float = Field(..., ge=0, le=100, description="Probability of engagement")
    share_likelihood: float = Field(..., ge=0, le=100, description="Probability of sharing")
    
    # Emotional Response Prediction
    predicted_emotions: Dict[str, float] = Field(
        default_factory=dict,
        description="Emotion scores: {'joy': 0.7, 'interest': 0.5}"
    )
    dominant_emotion: str = Field(..., description="Primary predicted emotion")
    emotional_intensity: float = Field(..., ge=0, le=100, description="Strength of emotional response")
    
    # Behavioral Prediction
    predicted_actions: Dict[str, float] = Field(
        default_factory=dict,
        description="Action probabilities: {'like': 0.6, 'share': 0.3, 'ignore': 0.3}"
    )
    most_likely_action: str = Field(..., description="Most likely action")
    
    # Content-Persona Alignment Details
    value_alignment: float = Field(..., ge=0, le=100, description="Content-values alignment")
    tone_match: float = Field(..., ge=0, le=100, description="Tone-preference match")
    relevance_score: float = Field(..., ge=0, le=100, description="Content relevance to interests")


class MultiPersonaResult(BaseModel):
    """
    Comparative results across multiple personas
    
    Provides aggregate insights and persona-specific results for multi-persona testing
    """
    # Individual Persona Results
    persona_results: List[PersonaAnalysisResult] = Field(
        default_factory=list,
        description="Analysis results for each tested persona"
    )
    
    # Comparative Analysis
    best_fit_personas: List[str] = Field(
        default_factory=list,
        description="Top 3 persona IDs with highest resonance"
    )
    worst_fit_personas: List[str] = Field(
        default_factory=list,
        description="Bottom 3 persona IDs with lowest resonance"
    )
    
    # Aggregate Insights
    average_resonance: float = Field(0.0, ge=0, le=100, description="Average resonance across all personas")
    resonance_variance: float = Field(0.0, ge=0, description="Variance in resonance scores")
    universal_appeal_score: float = Field(0.0, ge=0, le=100, description="Content appeal across all personas")


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    # Analysis Type
    analysis_type: str = Field("text_only", description="Type of analysis: 'text_only', 'image_only', or 'multimodal'")
    
    # Content Characteristics
    emotional_moral_content: EmotionalMoralContent
    narrative_ambiguity: NarrativeAmbiguity
    socio_cultural_sensitivity: SocioCulturalSensitivity
    
    # Mediator
    perceived_intent: PerceivedIntent
    
    # TPB Framework
    tpb_scores: TPBScores
    
    # Outcomes
    virality_score: int = Field(..., description="Virality prediction (0-100)")
    backlash_risk: int = Field(..., description="Backlash risk (0-100)")
    ad_fatigue_risk: int = Field(..., description="Ad-fatigue risk (0-100)")
    exposure_intensity: int = Field(..., description="Exposure intensity (0-100)")
    
    # Alerts & Recommendations
    cultural_alerts: List[CulturalAlert]
    sentiment: SentimentAnalysis
    recommendation: Recommendation
    similar_campaigns: List[SimilarCampaign]
    
    # Multi-modal
    image_analysis: Optional[ImageAnalysis] = None
    
    # OCR extracted text (for image-only analysis)
    extracted_text: Optional[str] = Field(None, description="Text extracted from image via OCR (for image-only analysis)")
    
    # Persona Testing (NEW - MVP Feature)
    persona_analysis: Optional[MultiPersonaResult] = Field(
        None,
        description="Multi-persona analysis results (if persona_ids provided)"
    )
    
    # Real Audience Analysis (NEW - Research Data Based)
    real_audience_analysis: Optional[Any] = Field(
        None,
        description="Real audience predictions based on 156 participant survey data"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "analysis_type": "multimodal",
                "emotional_moral_content": {
                    "emc_score": 75,
                    "emotions": ["joy", "pride", "nostalgia"],
                    "moral_framing": False,
                    "arousal_level": 0.7
                },
                "virality_score": 88,
                "backlash_risk": 12,
                "recommendation": {
                    "status": "go",
                    "action": "Good to Post",
                    "message": "Content shows strong viral potential with minimal risk!"
                }
            }
        }




# ============================================================================
# ADDITIONAL PERSONA TESTING MODELS
# ============================================================================


class Demographics(BaseModel):
    """Demographic characteristics of a persona"""
    age_range: Tuple[int, int] = Field(..., description="Age range (min, max)")
    gender: str = Field(..., description="Gender: 'all', 'male', 'female'")
    location_type: str = Field(..., description="Location: 'metro', 'tier2', 'tier3', 'rural'")
    region: Optional[str] = Field(None, description="Region: 'north', 'south', 'east', 'west', 'northeast'")
    income_level: str = Field(..., description="NCCS category: A1, A2, A3, B1, B2, C, D, E")
    education: str = Field(..., description="Education: 'school', 'graduate', 'postgrad', 'professional'")
    occupation: List[str] = Field(default_factory=list, description="Occupations: ['professional', 'student', 'homemaker']")
    language_primary: str = Field(..., description="Primary language: 'english', 'hindi', 'regional'")
    urban_rural: str = Field(..., description="Urban/rural: 'urban', 'semi-urban', 'rural'")


class Psychographics(BaseModel):
    """Psychographic profile based on VALS + Big Five (OCEAN)"""
    # VALS Framework
    primary_motivation: str = Field(..., description="VALS motivation: 'achievement', 'ideals', 'self-expression'")
    resources_level: str = Field(..., description="Resources: 'high', 'medium', 'low'")
    
    # Big Five Personality (OCEAN) - scores 0-100
    openness: float = Field(..., ge=0, le=100, description="Curiosity, creativity, new experiences")
    conscientiousness: float = Field(..., ge=0, le=100, description="Organization, dependability, discipline")
    extraversion: float = Field(..., ge=0, le=100, description="Sociability, assertiveness, energy")
    agreeableness: float = Field(..., ge=0, le=100, description="Cooperation, trust, empathy")
    neuroticism: float = Field(..., ge=0, le=100, description="Emotional instability, anxiety")
    
    # Values and Interests
    core_values: List[str] = Field(default_factory=list, description="Core values: ['family', 'success', 'tradition']")
    interests: List[str] = Field(default_factory=list, description="Interests: ['technology', 'fashion', 'sports']")
    lifestyle_descriptors: List[str] = Field(default_factory=list, description="Lifestyle: ['urban', 'health-conscious']")
    
    # Decision Making Style
    decision_style: str = Field(..., description="Decision style: 'impulsive', 'deliberate', 'social-proof', 'expert-driven'")
    risk_tolerance: str = Field(..., description="Risk tolerance: 'risk-averse', 'moderate', 'risk-seeking'")


class CulturalProfile(BaseModel):
    """Cultural dimensions based on Hofstede + India-specific factors"""
    # Hofstede Dimensions (0-100 scale)
    individualism: float = Field(..., ge=0, le=100, description="Low = collectivist, High = individualist")
    power_distance: float = Field(..., ge=0, le=100, description="Acceptance of hierarchy")
    uncertainty_avoidance: float = Field(..., ge=0, le=100, description="Comfort with ambiguity")
    masculinity: float = Field(..., ge=0, le=100, description="Achievement vs nurturing orientation")
    long_term_orientation: float = Field(..., ge=0, le=100, description="Tradition vs pragmatism")
    indulgence: float = Field(..., ge=0, le=100, description="Restraint vs gratification")
    
    # India-Specific Cultural Factors
    traditionalism: float = Field(..., ge=0, le=100, description="Adherence to traditions")
    religious_sensitivity: float = Field(..., ge=0, le=100, description="Sensitivity to religious content")
    regional_identity_strength: float = Field(..., ge=0, le=100, description="Pride in regional culture")
    family_orientation: float = Field(..., ge=0, le=100, description="Family-centric decision making")
    status_consciousness: float = Field(..., ge=0, le=100, description="Importance of social status")
    
    # Language & Communication
    language_preference: str = Field(..., description="Language: 'english', 'hindi', 'hinglish', 'regional'")
    humor_style: List[str] = Field(default_factory=list, description="Humor: ['sarcasm', 'slapstick', 'wordplay']")
    communication_formality: str = Field(..., description="Formality: 'formal', 'casual', 'mixed'")


class MediaBehavior(BaseModel):
    """Digital behavior patterns based on Meta/Google research"""
    # Platform Preferences (0-1 affinity scores)
    platform_affinity: Dict[str, float] = Field(
        default_factory=dict,
        description="Platform affinity scores: {'instagram': 0.9, 'youtube': 0.7}"
    )
    
    # Content Preferences
    content_formats: List[str] = Field(
        default_factory=list,
        description="Formats: ['short_video', 'stories', 'long_form', 'images']"
    )
    content_topics: List[str] = Field(
        default_factory=list,
        description="Topics: ['entertainment', 'education', 'news', 'lifestyle']"
    )
    
    # Consumption Patterns
    daily_screen_time: str = Field(..., description="Screen time: 'low' (<2h), 'medium' (2-5h), 'high' (>5h)")
    peak_activity_times: List[str] = Field(
        default_factory=list,
        description="Peak times: ['morning', 'lunch', 'evening', 'late_night']"
    )
    content_discovery: str = Field(..., description="Discovery: 'algorithm', 'search', 'social', 'influencer'")
    
    # Engagement Behavior
    engagement_style: str = Field(..., description="Style: 'passive', 'reactive', 'proactive', 'creator'")
    sharing_propensity: str = Field(..., description="Sharing: 'never', 'selective', 'frequent', 'viral'")
    comment_likelihood: str = Field(..., description="Commenting: 'never', 'rare', 'sometimes', 'often'")
    
    # Ad Response
    ad_receptivity: str = Field(..., description="Ad response: 'ad_blocker', 'tolerant', 'receptive', 'engaged'")
    influencer_trust: str = Field(..., description="Influencer trust: 'skeptical', 'neutral', 'trusting', 'fan'")
    brand_loyalty: str = Field(..., description="Brand loyalty: 'switcher', 'neutral', 'loyal', 'advocate'")


class BehavioralTriggers(BaseModel):
    """Content elements that drive specific responses"""
    # Positive Triggers (increase engagement)
    engagement_triggers: List[str] = Field(
        default_factory=list,
        description="Engagement triggers: ['humor', 'nostalgia', 'aspiration', 'deals']"
    )
    share_triggers: List[str] = Field(
        default_factory=list,
        description="Share triggers: ['relatable', 'informative', 'emotional', 'funny']"
    )
    purchase_triggers: List[str] = Field(
        default_factory=list,
        description="Purchase triggers: ['discount', 'scarcity', 'social_proof', 'quality']"
    )
    
    # Negative Triggers (cause friction/backlash)
    friction_triggers: List[str] = Field(
        default_factory=list,
        description="Friction triggers: ['pushy_sales', 'inauthentic', 'offensive']"
    )
    ignore_triggers: List[str] = Field(
        default_factory=list,
        description="Ignore triggers: ['irrelevant', 'boring', 'too_long', 'seen_before']"
    )
    report_triggers: List[str] = Field(
        default_factory=list,
        description="Report triggers: ['offensive', 'misleading', 'spam', 'inappropriate']"
    )
    
    # Emotional Response Patterns
    emotional_triggers: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Emotional triggers: {'joy': ['family', 'success'], 'anger': ['injustice']}"
    )
    
    # Call-to-Action Effectiveness
    effective_ctas: List[str] = Field(
        default_factory=list,
        description="Effective CTAs: ['learn_more', 'shop_now', 'share', 'comment']"
    )
    ineffective_ctas: List[str] = Field(
        default_factory=list,
        description="Ineffective CTAs: ['buy_now', 'limited_time', 'act_fast']"
    )


class Persona(BaseModel):
    """
    Core persona data structure based on research frameworks
    
    Represents a consumer segment with defined demographic, psychographic,
    and behavioral characteristics for audience testing.
    """
    id: str = Field(..., description="Unique identifier (e.g., 'gen_z_metro')")
    name: str = Field(..., description="Display name (e.g., 'The Digital Native')")
    tagline: str = Field(..., description="Short description")
    category: PersonaCategory = Field(..., description="Persona category")
    subcategory: str = Field(..., description="Specific segment within category")
    
    # Core Components
    demographics: Demographics
    psychographics: Psychographics
    cultural_profile: CulturalProfile
    media_behavior: MediaBehavior
    behavioral_triggers: BehavioralTriggers
    
    # Research Framework References
    framework_basis: List[str] = Field(
        default_factory=list,
        description="Research frameworks: ['VALS', 'NCCS', 'Hofstede', 'OCEAN']"
    )
    
    # Visual representation
    avatar_emoji: str = Field(..., description="Avatar emoji: 👨‍💼, 👩‍🎓, etc.")
    color_theme: str = Field(..., description="Hex color for UI")
    
    # Market size estimate
    market_size_percent: float = Field(..., ge=0, le=100, description="Estimated % of Indian market")


class PersonaAnalysisRequest(BaseModel):
    """
    Extended request model for persona analysis
    
    Adds optional persona_ids field to enable persona testing
    """
    # Content (same as CampaignRequest)
    caption: Optional[str] = Field(None, description="Campaign text content (caption, ad copy, post) - optional if image is provided")
    platform: str = Field(..., description="Social media platform (Instagram, YouTube, TikTok, Twitter)")
    posting_date: Optional[str] = Field(None, description="Planned posting date (YYYY-MM-DD)")
    influencer: bool = Field(False, description="Whether this is an influencer partnership")
    image_base64: Optional[str] = Field(None, description="Base64 encoded campaign image")
    image_only: bool = Field(False, description="Flag indicating image-only analysis mode")
    
    # Persona Selection (optional)
    persona_ids: Optional[List[str]] = Field(
        None,
        description="List of persona IDs to test against (e.g., ['gen_z_metro', 'millennial_professional'])"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "caption": "Celebrating India's diversity this Diwali! 🪔",
                "platform": "Instagram",
                "posting_date": "2025-10-18",
                "influencer": True,
                "image_base64": None,
                "image_only": False,
                "persona_ids": ["gen_z_metro", "millennial_professional", "boomer_traditional"]
            }
        }


class PersonaBasicInfo(BaseModel):
    """
    Basic persona information for listing
    
    Lightweight model for GET /api/personas endpoint
    """
    id: str = Field(..., description="Unique persona identifier")
    name: str = Field(..., description="Display name")
    category: PersonaCategory = Field(..., description="Persona category")
    tagline: str = Field(..., description="Short description")
    avatar_emoji: str = Field(..., description="Avatar emoji")
    color_theme: str = Field(..., description="Hex color for UI")
    market_size_percent: float = Field(..., description="Estimated % of Indian market")


# ============================================================================
# REAL AUDIENCE ANALYSIS MODELS
# Based on 156 participant survey data
# ============================================================================

class AudienceSegmentProfile(BaseModel):
    """Profile of a real audience segment from survey data"""
    name: str = Field(..., description="Segment name")
    size: int = Field(..., description="Number of respondents in segment")
    percentage: float = Field(..., description="Percentage of total audience")
    characteristics: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="Construct averages: {'EMC': {'mean': 3.5, 'std': 0.8}}"
    )


class SegmentReaction(BaseModel):
    """Predicted reaction for a specific segment"""
    segment_name: str
    size: int
    percentage: float
    characteristics: Dict[str, Dict[str, float]]
    predicted_reactions: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Predicted outcomes: {'virality': {'score': 3.5, 'likelihood': 'High'}}"
    )


class RealAudienceAnalysis(BaseModel):
    """
    Real audience analysis based on survey data
    
    Provides predictions based on actual participant responses
    from 156 respondents who rated content on EMC, NAM, SCS, and outcomes.
    """
    total_respondents: int = Field(..., description="Total survey respondents")
    segments: List[SegmentReaction] = Field(
        default_factory=list,
        description="Segment-specific predictions"
    )
    overall_prediction: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Weighted overall prediction across all segments"
    )


class AudienceInsights(BaseModel):
    """Insights about audience segments"""
    total_respondents: int
    segments: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Segment profiles with characteristics"
    )
