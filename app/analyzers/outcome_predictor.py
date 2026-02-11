# AdsenseAI Campaign Risk Analyzer - Outcome Predictor Module
# Predicts virality, backlash, exposure intensity, and ad-fatigue based on TPB and content characteristics

from typing import Dict, List


class OutcomePredictor:
    """
    Predicts campaign outcomes based on TPB framework and content characteristics.
    
    Outcomes predicted:
    - Virality Score: Likelihood of voluntary content sharing and amplification (0-100)
    - Backlash Risk: Likelihood of negative collective reaction (0-100)
    - Exposure Intensity: Frequency and magnitude of audience exposure (0-100)
    - Ad-Fatigue Risk: Decreased attention from repetitive exposure (0-100)
    
    Based on research hypotheses H4a, H4b, H5, H6, H7 from the design document.
    """
    
    def __init__(self):
        """Initialize the outcome predictor with platform-specific parameters"""
        # Platform multipliers for virality
        # Based on content amplification characteristics of each platform
        self.virality_platform_multipliers = {
            'instagram': 1.05,  # Visual content, moderate viral potential
            'tiktok': 1.10,     # Algorithm-driven, high viral potential
            'youtube': 1.00,    # Individual consumption, baseline
            'twitter': 1.05,    # Retweet mechanism, moderate viral potential
            'facebook': 1.03,   # Share mechanism, moderate viral potential
            'linkedin': 0.95    # Professional context, lower viral potential
        }
    
    def predict_virality(self, behavioral_intention: float, emotions: List[str],
                        sentiment: Dict, platform: str) -> Dict:
        """
        Predict virality score (likelihood of voluntary content sharing and amplification).
        
        Virality is based on:
        - Behavioral intention (TPB outcome - primary driver, scaled down)
        - Emotion count (moderate boost per emotion)
        - High polarity (strong sentiment = more shareable)
        - Positive sentiment boost (positive content is more viral)
        - Platform characteristics (some platforms amplify better)
        
        Formula:
        Virality = (behavioral_intention * 0.7 + emotion_boost + polarity_boost + positive_boost) * platform_multiplier
        
        Args:
            behavioral_intention: TPB behavioral intention score (0-100)
            emotions: List of detected emotions
            sentiment: Sentiment analysis dictionary with polarity
            platform: Social media platform name
            
        Returns:
            Dictionary containing virality score and breakdown
            
        Requirements: 6.1, 6.3
        """
        # Base score: behavioral intention (scaled to 70% to prevent always hitting 100)
        base_score = behavioral_intention * 0.7
        
        # Boost 1: Emotion count (+3 per emotion, capped at 15)
        # More emotions = more engaging = more likely to be shared
        emotion_count = len(emotions)
        emotion_boost = min(emotion_count * 3, 15)
        
        # Boost 2: High polarity (+8 if |polarity| > 0.5)
        # Strong sentiment (positive or negative) is more shareable
        polarity = sentiment.get('polarity', 0.0)
        polarity_boost = 8 if abs(polarity) > 0.5 else 0
        
        # Boost 3: Positive sentiment bonus (scaled down)
        # Positive content is more viral than negative
        positive_boost = 0
        if polarity > 0.3:  # Positive sentiment
            positive_boost = 8
            # Extra boost for very positive content
            if polarity > 0.6:
                positive_boost = 12
        
        # Penalty for negative sentiment (negative content less viral)
        negative_penalty = 0
        if polarity < -0.3:
            negative_penalty = 10
            if polarity < -0.6:
                negative_penalty = 18
        
        # Calculate pre-multiplier score
        pre_multiplier_score = base_score + emotion_boost + polarity_boost + positive_boost - negative_penalty
        
        # Apply platform multiplier
        platform_lower = platform.lower()
        platform_multiplier = self.virality_platform_multipliers.get(platform_lower, 1.0)
        
        # Calculate final virality score
        virality_score = pre_multiplier_score * platform_multiplier
        virality_score = max(min(virality_score, 100), 0)  # Cap between 0-100
        
        # Determine interpretation
        if virality_score >= 75:
            interpretation = "Very High - Strong viral potential"
            category = "very_high"
        elif virality_score >= 60:
            interpretation = "High - Good viral potential"
            category = "high"
        elif virality_score >= 45:
            interpretation = "Moderate - Some viral potential"
            category = "moderate"
        elif virality_score >= 30:
            interpretation = "Low - Limited viral potential"
            category = "low"
        else:
            interpretation = "Very Low - Minimal viral potential"
            category = "very_low"
        
        return {
            'virality_score': round(virality_score, 2),
            'base_score': round(base_score, 2),
            'emotion_boost': emotion_boost,
            'emotion_count': emotion_count,
            'polarity_boost': polarity_boost,
            'positive_boost': positive_boost,
            'negative_penalty': negative_penalty,
            'platform_multiplier': platform_multiplier,
            'platform': platform,
            'interpretation': interpretation,
            'category': category,
            'breakdown': f"Intention: {base_score:.1f} + Emotions: {emotion_boost} + Polarity: {polarity_boost} + Positive: {positive_boost} - Negative: {negative_penalty} × Platform: {platform_multiplier}"
        }

    def predict_backlash(self, perceived_intent: float, scs_score: float,
                        cultural_alerts: List[Dict], sentiment: Dict, emc_score: float = 0) -> Dict:
        """
        Predict backlash risk (likelihood of negative collective reaction).
        
        CRITICAL FIX 4: Restructured to properly weight Perceived Intent as mediator.
        Research: "backlash is aroused when viewers perceive manipulative, insensitive, 
        or opportunistic intention"
        
        New Formula (Intent-Centered):
        Backlash = (Cultural_Component × 0.30) + 
                   (Intent_Component × 0.40) +     // PRIMARY MEDIATOR
                   (EMC_Component × 0.15) + 
                   (Sentiment_Component × 0.15)
        
        Compound Effect: When 3+ risk factors present, multiply by 1.3
        
        Args:
            perceived_intent: Perceived intent score (-100 to +100) - PRIMARY MEDIATOR
            scs_score: Socio-cultural sensitivity score (0-100)
            cultural_alerts: List of cultural alert dictionaries with risk_weight
            sentiment: Sentiment analysis dictionary
            emc_score: Emotional-moral content score (optional, for compound detection)
            
        Returns:
            Dictionary containing backlash risk score and breakdown
            
        Requirements: 6.2, 6.4
        """
        # Component 1: Cultural Sensitivity (0-30 points) - 30% weight
        # Sum all risk weights from cultural alerts
        cultural_risk = sum(alert.get('risk_weight', 0) for alert in cultural_alerts)
        
        # Apply severity multiplier for critical/high severity alerts
        critical_count = sum(1 for alert in cultural_alerts if alert.get('severity') == 'critical')
        high_count = sum(1 for alert in cultural_alerts if alert.get('severity') == 'high')
        
        severity_multiplier = 1.0
        if critical_count > 0:
            severity_multiplier = 1.5
        elif high_count > 0:
            severity_multiplier = 1.3
        
        cultural_risk = cultural_risk * severity_multiplier
        # Normalize to 0-100 scale (assume max 150 with multiplier)
        cultural_component = min((cultural_risk / 150.0) * 100, 100) * 0.30
        
        # Component 2: Perceived Intent (0-40 points) - 40% weight - PRIMARY MEDIATOR
        # CRITICAL FIX 4: Intent is now the PRIMARY driver of backlash
        # Convert intent from -100..+100 to backlash contribution 0..100
        if perceived_intent < -50:
            # Highly manipulative: 100 points
            intent_contribution = 100
        elif perceived_intent < -20:
            # Moderately manipulative: 80 points
            intent_contribution = 80
        elif perceived_intent < 0:
            # Slightly manipulative: 60 points
            intent_contribution = 60
        elif perceived_intent < 20:
            # Neutral/slightly authentic: 40 points
            intent_contribution = 40
        else:
            # Authentic: 20 points (minimum)
            intent_contribution = 20
        
        intent_component = intent_contribution * 0.40
        
        # Component 3: EMC (0-15 points) - 15% weight
        # High EMC can contribute to backlash if perceived as manipulative
        if emc_score > 70:
            emc_contribution = ((emc_score - 70) / 30) * 100  # 70-100 -> 0-100
        else:
            emc_contribution = 0
        emc_component = emc_contribution * 0.15
        
        # Component 4: Negative Sentiment (0-15 points) - 15% weight
        # Negative content is more likely to trigger backlash
        polarity = sentiment.get('polarity', 0.0)
        if polarity < 0:
            sentiment_contribution = abs(polarity) * 100  # -1..0 -> 100..0
        else:
            sentiment_contribution = 0
        sentiment_component = sentiment_contribution * 0.15
        
        # Calculate base backlash risk
        backlash_risk = cultural_component + intent_component + emc_component + sentiment_component
        
        # CRITICAL FIX 4: Compound Effect Detection
        # When 3+ risk factors present, multiply by 1.3
        risk_factors = 0
        if cultural_risk > 30: risk_factors += 1
        if perceived_intent < -20: risk_factors += 1
        if emc_score > 70: risk_factors += 1
        if polarity < -0.3: risk_factors += 1
        if critical_count > 0: risk_factors += 1
        
        if risk_factors >= 3:
            backlash_risk = backlash_risk * 1.3
            compound_effect = True
        else:
            compound_effect = False
        
        backlash_risk = min(backlash_risk, 100)  # Cap at 100
        
        # Determine interpretation
        if backlash_risk >= 70:
            interpretation = "Critical - High likelihood of backlash"
            category = "critical"
        elif backlash_risk >= 50:
            interpretation = "High - Significant backlash risk"
            category = "high"
        elif backlash_risk >= 30:
            interpretation = "Moderate - Some backlash risk"
            category = "moderate"
        elif backlash_risk >= 15:
            interpretation = "Low - Minimal backlash risk"
            category = "low"
        else:
            interpretation = "Very Low - Negligible backlash risk"
            category = "very_low"
        
        return {
            'backlash_risk': round(backlash_risk, 2),
            'cultural_component': round(cultural_component, 2),
            'intent_component': round(intent_component, 2),
            'emc_component': round(emc_component, 2),
            'sentiment_component': round(sentiment_component, 2),
            'severity_multiplier': severity_multiplier,
            'compound_effect': compound_effect,
            'risk_factors': risk_factors,
            'critical_alerts': critical_count,
            'high_alerts': high_count,
            'alert_count': len(cultural_alerts),
            'interpretation': interpretation,
            'category': category,
            'breakdown': f"Cultural: {cultural_component:.1f} (30%) + Intent: {intent_component:.1f} (40%) + EMC: {emc_component:.1f} (15%) + Sentiment: {sentiment_component:.1f} (15%)" + (" × 1.3 (compound)" if compound_effect else "")
        }

    def calculate_exposure_intensity(self, virality_score: float,
                                     backlash_risk: float) -> Dict:
        """
        Calculate exposure intensity (frequency and magnitude of audience exposure).
        
        Exposure intensity represents how much audiences will be exposed to the content
        following initial diffusion. Both viral content and controversial content
        generate high exposure, but through different mechanisms:
        - Virality: Voluntary sharing and amplification
        - Backlash: Sustained negative discussion and controversy
        
        Formula:
        Exposure = (virality * 0.6) + (backlash * 0.4)
        
        Rationale: Viral content spreads more widely than controversial content,
        but controversial content can also generate sustained exposure through debate.
        
        Args:
            virality_score: Virality prediction score (0-100)
            backlash_risk: Backlash risk score (0-100)
            
        Returns:
            Dictionary containing exposure intensity score and breakdown
            
        Requirements: 6.5, 7.1, 7.2
        """
        # Calculate exposure intensity
        # Virality contributes 60% (primary driver of exposure)
        # Backlash contributes 40% (controversial content also gets exposure)
        virality_component = virality_score * 0.6
        backlash_component = backlash_risk * 0.4
        
        exposure_intensity = virality_component + backlash_component
        exposure_intensity = min(exposure_intensity, 100)  # Cap at 100
        
        # Determine interpretation
        if exposure_intensity >= 75:
            interpretation = "Very High - Massive audience exposure expected"
            category = "very_high"
        elif exposure_intensity >= 60:
            interpretation = "High - Significant audience exposure expected"
            category = "high"
        elif exposure_intensity >= 45:
            interpretation = "Moderate - Moderate audience exposure expected"
            category = "moderate"
        elif exposure_intensity >= 30:
            interpretation = "Low - Limited audience exposure expected"
            category = "low"
        else:
            interpretation = "Very Low - Minimal audience exposure expected"
            category = "very_low"
        
        # Determine exposure pattern
        if virality_score > 60 and backlash_risk > 60:
            pattern = "controversial_viral"
            pattern_description = "Controversial viral content - high sharing AND high backlash"
        elif virality_score > 60:
            pattern = "positive_viral"
            pattern_description = "Positive viral content - high sharing, low backlash"
        elif backlash_risk > 60:
            pattern = "controversial"
            pattern_description = "Controversial content - high backlash, limited sharing"
        else:
            pattern = "normal"
            pattern_description = "Normal content - moderate exposure"
        
        return {
            'exposure_intensity': round(exposure_intensity, 2),
            'virality_component': round(virality_component, 2),
            'backlash_component': round(backlash_component, 2),
            'interpretation': interpretation,
            'category': category,
            'pattern': pattern,
            'pattern_description': pattern_description,
            'breakdown': f"Virality: {virality_component:.1f} (60%) + Backlash: {backlash_component:.1f} (40%)"
        }

    def predict_ad_fatigue(self, exposure_intensity: float, caption: str,
                          sentiment: Dict) -> Dict:
        """
        Predict ad-fatigue risk (decreased attention and increased irritation from repetitive exposure).
        
        Ad-fatigue is based on:
        - Exposure intensity (more exposure = more fatigue)
        - Content length (longer content = more fatigue)
        - Hashtag count (excessive hashtags = more fatigue)
        - High subjectivity (salesy content = more fatigue)
        
        Formula:
        Fatigue = base + length_penalty + hashtag_penalty + subjectivity_penalty + (exposure * 0.3)
        
        Args:
            exposure_intensity: Exposure intensity score (0-100)
            caption: Campaign text content
            sentiment: Sentiment analysis dictionary with subjectivity
            
        Returns:
            Dictionary containing ad-fatigue risk score and breakdown
            
        Requirements: 7.3, 7.4, 7.5
        """
        # Base ad-fatigue risk
        base_risk = 30
        
        # Penalty 1: Content length
        # Count words in caption
        word_count = len(caption.split())
        
        if word_count > 100:
            # Very long content: +25 total
            length_penalty = 25
        elif word_count > 50:
            # Long content: +15
            length_penalty = 15
        else:
            # Normal length: no penalty
            length_penalty = 0
        
        # Penalty 2: Hashtag count
        # Count hashtags in caption
        hashtag_count = caption.count('#')
        
        if hashtag_count > 5:
            # Excessive hashtags: +2 per hashtag over 5
            hashtag_penalty = (hashtag_count - 5) * 2
        else:
            # Normal hashtag usage: no penalty
            hashtag_penalty = 0
        
        # Penalty 3: High subjectivity
        # High subjectivity suggests salesy/opinion content
        subjectivity = sentiment.get('subjectivity', 0.0)
        
        if subjectivity > 0.7:
            # High subjectivity: +20
            subjectivity_penalty = 20
        else:
            # Normal subjectivity: no penalty
            subjectivity_penalty = 0
        
        # Factor 4: Exposure intensity
        # Higher exposure = more repetition = more fatigue
        exposure_factor = exposure_intensity * 0.3
        
        # Calculate total ad-fatigue risk
        fatigue_risk = base_risk + length_penalty + hashtag_penalty + subjectivity_penalty + exposure_factor
        fatigue_risk = min(fatigue_risk, 100)  # Cap at 100
        
        # Determine interpretation
        if fatigue_risk >= 70:
            interpretation = "Critical - High ad-fatigue risk, content may irritate audiences"
            category = "critical"
        elif fatigue_risk >= 55:
            interpretation = "High - Significant ad-fatigue risk"
            category = "high"
        elif fatigue_risk >= 40:
            interpretation = "Moderate - Some ad-fatigue risk"
            category = "moderate"
        elif fatigue_risk >= 25:
            interpretation = "Low - Minimal ad-fatigue risk"
            category = "low"
        else:
            interpretation = "Very Low - Negligible ad-fatigue risk"
            category = "very_low"
        
        return {
            'ad_fatigue_risk': round(fatigue_risk, 2),
            'base_risk': base_risk,
            'length_penalty': length_penalty,
            'hashtag_penalty': hashtag_penalty,
            'subjectivity_penalty': subjectivity_penalty,
            'exposure_factor': round(exposure_factor, 2),
            'word_count': word_count,
            'hashtag_count': hashtag_count,
            'interpretation': interpretation,
            'category': category,
            'breakdown': f"Base: {base_risk} + Length: {length_penalty} + Hashtags: {hashtag_penalty} + Subjectivity: {subjectivity_penalty} + Exposure: {exposure_factor:.1f}"
        }
    
    def predict_all_outcomes(self, behavioral_intention: float, emotions: List[str],
                            sentiment: Dict, platform: str, perceived_intent: float,
                            scs_score: float, cultural_alerts: List[Dict],
                            caption: str, emc_score: float = 0) -> Dict:
        """
        Predict all outcomes in one call.
        
        This is the main entry point for outcome prediction, calculating:
        - Virality score
        - Backlash risk (CRITICAL FIX 4: Now properly weights Intent as mediator)
        - Exposure intensity
        - Ad-fatigue risk
        
        Args:
            behavioral_intention: TPB behavioral intention score (0-100)
            emotions: List of detected emotions
            sentiment: Sentiment analysis dictionary
            platform: Social media platform name
            perceived_intent: Perceived intent score (-100 to +100)
            scs_score: Socio-cultural sensitivity score (0-100)
            cultural_alerts: List of cultural alert dictionaries
            caption: Campaign text content
            emc_score: Emotional-moral content score (for backlash calculation)
            
        Returns:
            Dictionary containing all outcome predictions
            
        Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5
        """
        # Predict virality
        virality_result = self.predict_virality(behavioral_intention, emotions, sentiment, platform)
        
        # Predict backlash (CRITICAL FIX 4: Pass emc_score)
        backlash_result = self.predict_backlash(
            perceived_intent, scs_score, cultural_alerts, sentiment, emc_score
        )
        
        # Calculate exposure intensity
        exposure_result = self.calculate_exposure_intensity(
            virality_result['virality_score'],
            backlash_result['backlash_risk']
        )
        
        # Predict ad-fatigue
        fatigue_result = self.predict_ad_fatigue(
            exposure_result['exposure_intensity'],
            caption,
            sentiment
        )
        
        return {
            'virality_score': int(round(virality_result['virality_score'])),
            'backlash_risk': int(round(backlash_result['backlash_risk'])),
            'exposure_intensity': int(round(exposure_result['exposure_intensity'])),
            'ad_fatigue_risk': int(round(fatigue_result['ad_fatigue_risk'])),
            'virality_breakdown': virality_result,
            'backlash_breakdown': backlash_result,
            'exposure_breakdown': exposure_result,
            'fatigue_breakdown': fatigue_result
        }
