# AdsenseAI Campaign Risk Analyzer - Main FastAPI Application

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import base64
import logging
from dotenv import load_dotenv
from typing import Optional, List

# Import models
from app.models import (
    CampaignRequest, 
    AnalysisResponse,
    EmotionalMoralContent,
    NarrativeAmbiguity,
    SocioCulturalSensitivity,
    PerceivedIntent,
    TPBScores,
    SentimentAnalysis,
    CulturalAlert,
    Recommendation,
    SimilarCampaign,
    ImageAnalysis,
    PersonaAnalysisRequest,
    PersonaBasicInfo,
    MultiPersonaResult,
    PersonaAnalysisResult
)

# Import analyzers
from app.analyzers import (
    TextAnalyzer,
    CulturalSensitivityDetector,
    PerceivedIntentCalculator,
    TPBCalculator,
    OutcomePredictor,
    RecommendationEngine,
    ImageAnalyzer,
    fuse_text_and_image_analysis
)

# Import persona analyzers
from app.analyzers.persona_library import PersonaLibrary
from app.analyzers.resonance_calculator import ResonanceCalculator
from app.analyzers.persona_tpb_modifier import PersonaTPBModifier

# Import data loader
from app.data.data_loader import get_data_loader

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global instances
data_loader = None
text_analyzer = None
cultural_detector = None
intent_calculator = None
tpb_calculator = None
outcome_predictor = None
recommendation_engine = None
image_analyzer = None
persona_library = None
resonance_calculator = None
persona_tpb_modifier = None

# Response cache for frequently analyzed content
from functools import lru_cache
import hashlib
response_cache = {}


def initialize_system():
    """Initialize data and analyzers"""
    global data_loader, text_analyzer, cultural_detector, intent_calculator
    global tpb_calculator, outcome_predictor, recommendation_engine, image_analyzer
    global persona_library, resonance_calculator, persona_tpb_modifier
    
    try:
        logger.info("Initializing AdsenseAI system...")
        
        # Initialize data loader
        data_loader = get_data_loader()
        logger.info("Data loader initialized")
        
        # Load core data
        data_loader.load_all_core_data(use_synthetic_fallback=True)
        logger.info("Core data loaded")
        
        # Initialize analyzers
        text_analyzer = TextAnalyzer()
        cultural_detector = CulturalSensitivityDetector()
        intent_calculator = PerceivedIntentCalculator()
        tpb_calculator = TPBCalculator()
        outcome_predictor = OutcomePredictor()
        recommendation_engine = RecommendationEngine(data_loader)
        
        # Initialize image analyzer if API key is available
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        if gemini_api_key:
            image_analyzer = ImageAnalyzer(gemini_api_key)
            logger.info("Image analyzer initialized with Gemini API")
        else:
            logger.warning("GEMINI_API_KEY not found - image analysis will be unavailable")
        
        # Initialize persona testing components
        try:
            persona_library = PersonaLibrary()
            resonance_calculator = ResonanceCalculator()
            persona_tpb_modifier = PersonaTPBModifier()
            logger.info("Persona testing components initialized")
        except Exception as e:
            logger.warning(f"Persona testing initialization failed: {str(e)}")
            # Continue without persona testing
        
        logger.info("AdsenseAI system initialized successfully")
        
    except Exception as e:
        logger.error(f"Error during initialization: {str(e)}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    initialize_system()
    yield
    # Shutdown (if needed)
    logger.info("Shutting down AdsenseAI system...")


# Initialize FastAPI application
app = FastAPI(
    title="AdsenseAI Campaign Risk Analyzer",
    description="TPB-based campaign risk prediction system for the Indian market",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


# Root endpoint - Serve HTML interface
@app.get("/")
async def root():
    """Serve the HTML interface"""
    from fastapi.responses import FileResponse
    import os
    
    html_path = os.path.join("templates", "index.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    else:
        # Fallback to API information
        return {
            "name": "AdsenseAI Campaign Risk Analyzer",
            "version": "1.0.0",
            "description": "TPB-based campaign risk prediction for Indian market",
            "endpoints": {
                "docs": "/docs",
                "health": "/api/health",
                "analyze": "/api/analyze (POST)"
            }
        }


# Health check endpoint
@app.get("/api/health")
async def health_check():
    """
    Health check endpoint
    
    Returns service status and data loading status
    
    Requirements: System health
    """
    try:
        # Check if data loader is initialized
        if data_loader is None:
            return {
                "status": "unhealthy",
                "service": "AdsenseAI Campaign Risk Analyzer",
                "version": "1.0.0",
                "error": "Data loader not initialized"
            }
        
        # Check data loading status
        cultural_triggers = data_loader.load_cultural_triggers()
        festival_calendar = data_loader.load_festival_calendar()
        historical_campaigns = data_loader.load_historical_campaigns()
        
        data_status = {
            "cultural_triggers": len(cultural_triggers),
            "festival_calendar": len(festival_calendar),
            "historical_campaigns": len(historical_campaigns)
        }
        
        # Check if analyzers are initialized
        analyzers_status = {
            "text_analyzer": text_analyzer is not None,
            "cultural_detector": cultural_detector is not None,
            "intent_calculator": intent_calculator is not None,
            "tpb_calculator": tpb_calculator is not None,
            "outcome_predictor": outcome_predictor is not None,
            "recommendation_engine": recommendation_engine is not None,
            "image_analyzer": image_analyzer is not None
        }
        
        return {
            "status": "healthy",
            "service": "AdsenseAI Campaign Risk Analyzer",
            "version": "1.0.0",
            "data_loaded": data_status,
            "analyzers_initialized": analyzers_status
        }
        
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "AdsenseAI Campaign Risk Analyzer",
            "version": "1.0.0",
            "error": str(e)
        }


@app.get("/api/personas", response_model=List[PersonaBasicInfo])
async def get_personas():
    """
    Get list of all available personas
    
    Returns basic information for all 12 MVP personas including:
    - id, name, category, tagline
    - avatar_emoji, color_theme
    - market_size_percent
    
    Requirements: 1.1
    """
    try:
        if persona_library is None:
            raise HTTPException(
                status_code=503,
                detail="Persona library not initialized"
            )
        
        logger.info("Fetching all personas...")
        
        # Get all personas from library
        all_personas = persona_library.get_all_personas()
        
        # Convert to basic info format
        personas_basic = [
            PersonaBasicInfo(
                id=persona.id,
                name=persona.name,
                category=persona.category,
                tagline=persona.tagline,
                avatar_emoji=persona.avatar_emoji,
                color_theme=persona.color_theme,
                market_size_percent=persona.market_size_percent
            )
            for persona in all_personas
        ]
        
        logger.info(f"Returning {len(personas_basic)} personas")
        return personas_basic
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching personas: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching personas: {str(e)}"
        )


@app.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_campaign(request: PersonaAnalysisRequest):
    """
    Main campaign analysis endpoint (with optional persona testing)
    
    Orchestrates all analysis modules to provide comprehensive risk assessment.
    If persona_ids are provided, also performs persona-specific analysis.
    
    Supports three analysis modes:
    - text_only: Only caption provided
    - image_only: Only image provided (uses OCR to extract text)
    - multimodal: Both caption and image provided
    
    Args:
        request: PersonaAnalysisRequest with caption, platform, posting_date, influencer, 
                 image_base64, and optional persona_ids
        
    Returns:
        AnalysisResponse with complete TPB-based analysis and optional persona results
        
    Requirements: All, 3.1, 12.1, 15.1, 15.2, 15.3, 15.4, 15.5
    """
    try:
        # Validate input - at least one of caption or image must be provided
        has_caption = request.caption and request.caption.strip()
        has_image = request.image_base64 is not None
        
        if not has_caption and not has_image:
            raise HTTPException(
                status_code=400, 
                detail="At least one of caption or image must be provided"
            )
        
        if request.platform not in ["Instagram", "YouTube", "TikTok", "Twitter"]:
            raise HTTPException(
                status_code=400, 
                detail="Platform must be one of: Instagram, YouTube, TikTok, Twitter"
            )
        
        # Generate cache key for text-only analysis (excluding image for cache efficiency)
        cache_key = None
        if has_caption and not has_image and not request.persona_ids:
            # Only cache simple text-only analyses without personas
            cache_data = f"{request.caption}|{request.platform}|{request.posting_date}|{request.influencer}"
            cache_key = hashlib.md5(cache_data.encode()).hexdigest()
            
            # Check cache
            if cache_key in response_cache:
                logger.info(f"Returning cached result for key: {cache_key[:8]}...")
                return response_cache[cache_key]
        
        # Determine analysis type
        if has_caption and has_image:
            analysis_type = "multimodal"
        elif has_image:
            analysis_type = "image_only"
        else:
            analysis_type = "text_only"
        
        logger.info(f"Analyzing campaign for platform: {request.platform}, type: {analysis_type}")
        
        # Initialize variables
        caption_text = request.caption.strip() if has_caption else ""
        extracted_text = None
        image_analysis_result = None
        
        # Step 0: For image-only analysis, extract text from image first
        if analysis_type == "image_only" and image_analyzer:
            try:
                logger.info("Step 0: Extracting text from image (OCR)...")
                ocr_result = image_analyzer.extract_text_from_image(request.image_base64)
                
                if ocr_result.get('extracted_text'):
                    extracted_text = ocr_result['extracted_text']
                    caption_text = extracted_text  # Use extracted text for analysis
                    logger.info(f"OCR extracted text: {extracted_text[:100]}..." if len(extracted_text) > 100 else f"OCR extracted text: {extracted_text}")
                else:
                    logger.info("No text found in image, proceeding with visual-only analysis")
                    # Use a minimal placeholder for text analysis
                    caption_text = "Image content"
                    
            except Exception as e:
                logger.error(f"OCR extraction error: {str(e)}")
                caption_text = "Image content"
        
        # Step 1: Text Analysis
        logger.info("Step 1: Performing text analysis...")
        text_analysis = text_analyzer.analyze_text(caption_text)
        
        # Extract components
        sentiment = text_analysis['sentiment']
        emotions = text_analysis['emotions']
        
        # Calculate EMC and NAM scores
        emc_result = text_analyzer.calculate_emc_score(caption_text)
        nam_result = text_analyzer.calculate_nam_score(caption_text)
        
        # Step 2: Cultural Sensitivity Detection
        logger.info("Step 2: Detecting cultural sensitivity issues...")
        cultural_result = cultural_detector.calculate_scs_score(
            text=caption_text,
            posting_date=request.posting_date
        )
        
        # Step 3: Image Analysis (if image provided)
        if has_image and image_analyzer:
            try:
                logger.info("Step 3: Analyzing image content...")
                
                # Pass the base64 string directly - analyze_image handles the parsing
                image_analysis_result = image_analyzer.analyze_image(request.image_base64)
                
                # Check if there was an error in the analysis
                if image_analysis_result.get('error'):
                    logger.warning(f"Image analysis returned error: {image_analysis_result.get('error')}")
                else:
                    logger.info("Image analysis complete")
                
            except Exception as e:
                logger.error(f"Image analysis error: {str(e)}")
                # Continue without image analysis
                image_analysis_result = None
        
        # Step 4: Multi-modal Fusion (if image was analyzed)
        if image_analysis_result and not image_analysis_result.get('error'):
            logger.info("Step 4: Fusing text and image analysis...")
            
            # Prepare text analysis for fusion
            text_for_fusion = {
                'emc_score': emc_result['emc_score'],
                'scs_score': cultural_result['scs_score'],
                'emotions': emotions
            }
            
            fused_result = fuse_text_and_image_analysis(
                text_analysis=text_for_fusion,
                image_analysis=image_analysis_result
            )
            
            # Update with fused results
            emc_result['emc_score'] = fused_result['emc_score']
            cultural_result['scs_score'] = fused_result['scs_score']
            emotions = fused_result['emotions']
        
        # Step 5: Perceived Intent Calculation
        logger.info("Step 5: Calculating perceived intent...")
        intent_result = intent_calculator.calculate_perceived_intent(
            emc_score=emc_result['emc_score'],
            nam_score=nam_result['nam_score'],
            scs_score=cultural_result['scs_score'],
            sentiment=sentiment,
            text=caption_text  # CRITICAL FIX 2: Pass text for manipulation detection
        )
        
        # Step 6: TPB Framework Calculation
        logger.info("Step 6: Calculating TPB framework scores...")
        tpb_result = tpb_calculator.calculate_tpb_scores(
            sentiment=sentiment,
            emc_score=emc_result['emc_score'],
            perceived_intent=intent_result['intent_score'],
            nam_score=nam_result['nam_score'],
            emotions=emotions,
            platform=request.platform,
            influencer=request.influencer
        )
        
        # Step 7: Outcome Prediction
        logger.info("Step 7: Predicting outcomes...")
        outcomes = outcome_predictor.predict_all_outcomes(
            behavioral_intention=tpb_result['behavioral_intention'],
            emotions=emotions,
            sentiment=sentiment,
            platform=request.platform,
            perceived_intent=intent_result['intent_score'],
            scs_score=cultural_result['scs_score'],
            cultural_alerts=cultural_result['detected_triggers'] + cultural_result['festival_proximity'],
            caption=caption_text,
            emc_score=emc_result['emc_score']  # CRITICAL FIX 4: Pass EMC score for backlash calculation
        )
        
        # Step 8: Generate Recommendations
        logger.info("Step 8: Generating recommendations...")
        recommendation = recommendation_engine.generate_recommendation(
            virality_score=outcomes['virality_score'],
            backlash_risk=outcomes['backlash_risk'],
            cultural_alerts=(cultural_result['detected_triggers'] + cultural_result['festival_proximity']),
            perceived_intent=intent_result['intent_score'],
            tpb_scores=tpb_result,
            sentiment=sentiment,
            platform=request.platform
        )
        
        # Step 8.5: Real Audience Analysis (based on 156 participant survey data)
        real_audience_result = None
        try:
            logger.info("Step 8.5: Analyzing against real audience data...")
            from app.analyzers.real_audience_analyzer import get_real_audience_analyzer
            
            real_audience_analyzer = get_real_audience_analyzer()
            real_audience_result = real_audience_analyzer.predict_audience_reaction(
                emc_score=emc_result['emc_score'],
                nam_score=nam_result['nam_score'],
                scs_score=cultural_result['scs_score'],
                perceived_intent=intent_result['intent_score']
            )
            logger.info("Real audience analysis complete")
        except Exception as e:
            logger.warning(f"Real audience analysis failed: {str(e)}")
            # Continue without real audience analysis
        
        # Step 9: Persona Analysis (if persona_ids provided)
        persona_analysis_result = None
        if request.persona_ids and persona_library and resonance_calculator and persona_tpb_modifier:
            try:
                logger.info(f"Step 9: Performing persona analysis for {len(request.persona_ids)} personas...")
                
                # Get selected personas
                selected_personas = []
                for persona_id in request.persona_ids:
                    persona = persona_library.get_persona_by_id(persona_id)
                    if persona:
                        selected_personas.append(persona)
                    else:
                        logger.warning(f"Persona not found: {persona_id}")
                
                if selected_personas:
                    # Analyze each persona
                    persona_results = []
                    
                    for persona in selected_personas:
                        # Calculate resonance score
                        resonance_result = resonance_calculator.calculate_resonance(
                            content_analysis={
                                'text': caption_text,
                                'sentiment': sentiment,
                                'emotions': emotions,
                                'emc_score': emc_result['emc_score'],
                                'scs_score': cultural_result['scs_score'],
                                'platform': request.platform
                            },
                            persona=persona
                        )
                        
                        # Create persona analysis result
                        persona_result = PersonaAnalysisResult(
                            persona_id=persona.id,
                            persona_name=persona.name,
                            avatar_emoji=persona.avatar_emoji,
                            tagline=persona.tagline,
                            resonance_score=resonance_result['resonance_score'],
                            engagement_likelihood=resonance_result['engagement_likelihood'],
                            share_likelihood=resonance_result['share_likelihood'],
                            predicted_emotions=resonance_result['predicted_emotions'],
                            dominant_emotion=resonance_result['dominant_emotion'],
                            emotional_intensity=resonance_result['emotional_intensity'],
                            predicted_actions=resonance_result['predicted_actions'],
                            most_likely_action=resonance_result['most_likely_action'],
                            value_alignment=resonance_result['value_alignment'],
                            tone_match=resonance_result['tone_match'],
                            relevance_score=resonance_result['relevance_score']
                        )
                        
                        persona_results.append(persona_result)
                    
                    # Calculate comparative metrics
                    if persona_results:
                        resonance_scores = [p.resonance_score for p in persona_results]
                        avg_resonance = sum(resonance_scores) / len(resonance_scores)
                        
                        # Calculate variance
                        variance = sum((score - avg_resonance) ** 2 for score in resonance_scores) / len(resonance_scores)
                        
                        # Universal appeal: inverse of variance, normalized
                        universal_appeal = max(0, 100 - (variance / 10))
                        
                        # Sort by resonance score
                        sorted_results = sorted(persona_results, key=lambda x: x.resonance_score, reverse=True)
                        
                        # Get best and worst fit personas
                        best_fit = [p.persona_id for p in sorted_results[:3]]
                        worst_fit = [p.persona_id for p in sorted_results[-3:]]
                        
                        # Create multi-persona result
                        persona_analysis_result = MultiPersonaResult(
                            persona_results=persona_results,
                            best_fit_personas=best_fit,
                            worst_fit_personas=worst_fit,
                            average_resonance=avg_resonance,
                            resonance_variance=variance,
                            universal_appeal_score=universal_appeal
                        )
                        
                        logger.info(f"Persona analysis complete. Average resonance: {avg_resonance:.1f}")
                
            except Exception as e:
                logger.error(f"Persona analysis error: {str(e)}")
                # Continue without persona analysis
                persona_analysis_result = None
        
        # Build response
        logger.info("Building response...")
        response = AnalysisResponse(
            # Analysis Type
            analysis_type=analysis_type,
            
            # Content Characteristics
            emotional_moral_content=EmotionalMoralContent(
                emc_score=emc_result['emc_score'],
                emotions=emotions,
                moral_framing=emc_result['moral_framing'].get('has_moral_framing', False),
                arousal_level=emc_result['emotional_intensity'].get('arousal_level', 0.0)
            ),
            narrative_ambiguity=NarrativeAmbiguity(
                nam_score=nam_result['nam_score'],
                clarity=nam_result['clarity_metrics'].get('clarity_score', 100.0),
                interpretive_openness=nam_result['openness_metrics'].get('openness_score', 0.0)
            ),
            socio_cultural_sensitivity=SocioCulturalSensitivity(
                scs_score=cultural_result['scs_score'],
                triggers_found=cultural_result['triggers_found'],
                festival_proximity=cultural_result['festival_proximity'][0] if cultural_result['festival_proximity'] else None
            ),
            
            # Mediator
            perceived_intent=PerceivedIntent(
                intent_score=intent_result['intent_score'],
                authenticity=intent_result['authenticity'],
                manipulation_risk=intent_result['manipulation_risk'],
                interpretation=intent_result['interpretation']
            ),
            
            # TPB Framework
            tpb_scores=TPBScores(
                attitude=tpb_result['attitude'],
                subjective_norms=tpb_result['subjective_norms'],
                perceived_control=tpb_result['perceived_control'],
                behavioral_intention=tpb_result['behavioral_intention']
            ),
            
            # Outcomes
            virality_score=int(outcomes['virality_score']),
            backlash_risk=int(outcomes['backlash_risk']),
            ad_fatigue_risk=int(outcomes['ad_fatigue_risk']),
            exposure_intensity=int(outcomes['exposure_intensity']),
            
            # Alerts & Recommendations
            cultural_alerts=[
                CulturalAlert(
                    keyword=alert.get('keyword', alert.get('festival', 'Unknown')),
                    category=alert.get('category', 'Festival'),
                    severity=alert['severity'],
                    risk_weight=alert['risk_weight'],
                    message=alert['message']
                )
                for alert in (cultural_result['detected_triggers'] + cultural_result['festival_proximity'])
            ],
            sentiment=SentimentAnalysis(
                polarity=sentiment['polarity'],
                subjectivity=sentiment['subjectivity'],
                positive=sentiment['positive'],
                negative=sentiment['negative'],
                neutral=sentiment['neutral'],
                label=sentiment['label']
            ),
            recommendation=Recommendation(
                status=recommendation['status'],
                action=recommendation['action'],
                message=recommendation['message'],
                reasoning=recommendation['reasoning'],
                suggestions=recommendation['suggestions']
            ),
            similar_campaigns=[
                SimilarCampaign(
                    brand=campaign['brand'],
                    campaign=campaign['campaign'],
                    outcome=campaign['outcome'],
                    lesson=campaign['lesson']
                )
                for campaign in recommendation['similar_campaigns']
            ],
            
            # Multi-modal
            image_analysis=ImageAnalysis(
                visual_emotions=image_analysis_result['visual_emotions'],
                cultural_symbols=image_analysis_result['cultural_symbols'],
                sensitivity_flags=image_analysis_result['sensitivity_flags'],
                text_overlay=image_analysis_result['text_overlay'],
                visual_emc_score=image_analysis_result['visual_emc_score']
            ) if image_analysis_result and not image_analysis_result.get('error') else None,
            
            # OCR extracted text (for image-only analysis)
            extracted_text=extracted_text,
            
            # Persona Testing (NEW - MVP Feature)
            persona_analysis=persona_analysis_result,
            
            # Real Audience Analysis (NEW - Research Data Based)
            real_audience_analysis=real_audience_result
        )
        
        logger.info(f"Analysis complete (type: {analysis_type})")
        
        # Cache the response if applicable (text-only, no personas, cache size < 100)
        if cache_key and len(response_cache) < 100:
            response_cache[cache_key] = response
            logger.info(f"Cached result for key: {cache_key[:8]}...")
        
        return response
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error during analysis: {str(e)}"
        )


@app.get("/api/audience/segments")
async def get_audience_segments():
    """
    Get insights about real audience segments from survey data.
    
    Returns segment profiles based on 156 participant responses.
    """
    try:
        from app.analyzers.real_audience_analyzer import get_real_audience_analyzer
        
        analyzer = get_real_audience_analyzer()
        insights = analyzer.get_segment_insights()
        
        return insights
        
    except Exception as e:
        logger.error(f"Error getting audience segments: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving audience segments: {str(e)}"
        )


@app.post("/api/audience/predict")
async def predict_audience_reaction(
    emc_score: float,
    nam_score: float,
    scs_score: float,
    perceived_intent: float
):
    """
    Predict how real audience segments will react to content.
    
    Uses survey data from 156 respondents to predict reactions
    based on content characteristics.
    
    Args:
        emc_score: Emotional-Moral Content score (0-100)
        nam_score: Narrative Ambiguity score (0-100)
        scs_score: Socio-Cultural Sensitivity score (0-100)
        perceived_intent: Perceived Intent score (-100 to 100)
    
    Returns:
        Predicted reactions by audience segment
    """
    try:
        from app.analyzers.real_audience_analyzer import get_real_audience_analyzer
        
        analyzer = get_real_audience_analyzer()
        predictions = analyzer.predict_audience_reaction(
            emc_score=emc_score,
            nam_score=nam_score,
            scs_score=scs_score,
            perceived_intent=perceived_intent
        )
        
        return predictions
        
    except Exception as e:
        logger.error(f"Error predicting audience reaction: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error predicting audience reaction: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True
    )
