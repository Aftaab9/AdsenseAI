# AdsenseAI Campaign Risk Analyzer - TPB Framework Calculator Module
# Implements Theory of Planned Behaviour (TPB) framework to predict behavioral intention

from typing import Dict, List


class TPBCalculator:
    """
    Implements Theory of Planned Behaviour (TPB) framework to predict
    behavioral intention (likelihood of sharing/engaging with content).
    
    TPB Components:
    - Attitude: Evaluation of the behavior (sharing/engaging)
    - Subjective Norms: Perceived social pressure to perform behavior
    - Perceived Control: Perceived ease of performing behavior
    - Behavioral Intention: Likelihood of performing behavior (outcome)
    
    Based on Ajzen (1991) TPB framework adapted for Indian social media context.
    """
    
    def __init__(self):
        """Initialize the TPB calculator with platform-specific parameters"""
        # Platform multipliers for subjective norms
        # Based on social signaling strength of each platform
        self.platform_multipliers = {
            'instagram': 1.3,   # High social signaling, visual sharing
            'tiktok': 1.4,      # Trend-driven, high peer influence
            'youtube': 1.0,     # Individual consumption, lower social pressure
            'twitter': 1.2,     # Discourse-oriented, moderate social influence
            'facebook': 1.2,    # Social network, moderate influence
            'linkedin': 1.1     # Professional context, lower emotional sharing
        }
        
        # Emotion weights for Indian cultural context
        self.indian_emotion_boosts = {
            'pride': 10,        # National/cultural pride resonates strongly
            'nostalgia': 10     # Cultural heritage and tradition valued
        }
    
    def calculate_attitude(self, sentiment: Dict, emc_score: float,
                          perceived_intent: float, emotions: List[str]) -> Dict:
        """
        Calculate attitude toward the behavior (sharing/engaging with content).
        
        Attitude is based on:
        - Sentiment polarity (positive content = positive attitude)
        - Emotional-moral content (engaging content = positive attitude)
        - Perceived intent (authentic content = positive attitude)
        - Emotion boosters for Indian context (pride/nostalgia)
        
        Formula: Attitude = ((polarity + 1) / 2 * 100) * 0.5 + (emc * 0.3) + ((intent + 100) / 2 * 0.2)
        
        Args:
            sentiment: Sentiment analysis dictionary with polarity
            emc_score: Emotional-moral content score (0-100)
            perceived_intent: Perceived intent score (-100 to +100)
            emotions: List of detected emotions
            
        Returns:
            Dictionary containing attitude score and breakdown
            
        Requirements: 5.1
        """
        # Get sentiment polarity (-1 to +1)
        polarity = sentiment.get('polarity', 0.0)
        
        # Component 1: Sentiment polarity (0-50 points)
        # Convert polarity from -1..+1 to 0..100, then apply 50% weight
        sentiment_normalized = ((polarity + 1) / 2) * 100  # 0-100
        sentiment_component = sentiment_normalized * 0.5
        
        # Component 2: EMC score (0-30 points)
        # Higher EMC = more engaging = more positive attitude
        emc_component = emc_score * 0.3
        
        # Component 3: Perceived intent (0-20 points)
        # Convert intent from -100..+100 to 0..100, then apply 20% weight
        intent_normalized = (perceived_intent + 100) / 2  # 0-100
        intent_component = intent_normalized * 0.2
        
        # Calculate base attitude score
        attitude_base = sentiment_component + emc_component + intent_component
        
        # Apply emotion boosters for Indian context
        emotion_boost = 0
        for emotion in emotions:
            if emotion in self.indian_emotion_boosts:
                emotion_boost += self.indian_emotion_boosts[emotion]
        
        # Add general positive emotion boost (+5 per positive emotion)
        positive_emotions = ['joy', 'inspiration', 'humor']
        for emotion in emotions:
            if emotion in positive_emotions and emotion not in self.indian_emotion_boosts:
                emotion_boost += 5
        
        # Calculate final attitude score
        attitude_score = attitude_base + emotion_boost
        attitude_score = min(attitude_score, 100)  # Cap at 100
        
        return {
            'attitude': round(attitude_score, 2),
            'sentiment_component': round(sentiment_component, 2),
            'emc_component': round(emc_component, 2),
            'intent_component': round(intent_component, 2),
            'emotion_boost': emotion_boost,
            'breakdown': f"Sentiment: {sentiment_component:.1f} + EMC: {emc_component:.1f} + Intent: {intent_component:.1f} + Emotions: {emotion_boost}"
        }

    def calculate_subjective_norms(self, platform: str, influencer: bool,
                                   emotions: List[str]) -> Dict:
        """
        Calculate subjective norms (perceived social pressure to share/engage).
        
        Subjective norms are influenced by:
        - Platform (different platforms have different social signaling strength)
        - Influencer partnership (increases social pressure)
        - Pride emotion (collective identity in Indian context)
        
        Formula: Norms = (base + influencer_boost + emotion_boost) * platform_multiplier
        
        Args:
            platform: Social media platform name
            influencer: Whether this is an influencer partnership
            emotions: List of detected emotions
            
        Returns:
            Dictionary containing subjective norms score and breakdown
            
        Requirements: 5.2
        """
        # Base subjective norms score
        base_score = 50
        
        # Influencer boost (+25 points)
        # Influencer partnerships increase social pressure to engage
        influencer_boost = 25 if influencer else 0
        
        # Pride emotion boost (+10 points)
        # Pride triggers collective identity and social sharing in Indian context
        pride_boost = 10 if 'pride' in emotions else 0
        
        # Calculate pre-multiplier score
        pre_multiplier_score = base_score + influencer_boost + pride_boost
        
        # Apply platform multiplier
        platform_lower = platform.lower()
        platform_multiplier = self.platform_multipliers.get(platform_lower, 1.0)
        
        # Calculate final subjective norms score
        norms_score = pre_multiplier_score * platform_multiplier
        norms_score = min(norms_score, 100)  # Cap at 100
        
        return {
            'subjective_norms': round(norms_score, 2),
            'base_score': base_score,
            'influencer_boost': influencer_boost,
            'pride_boost': pride_boost,
            'platform_multiplier': platform_multiplier,
            'platform': platform,
            'breakdown': f"Base: {base_score} + Influencer: {influencer_boost} + Pride: {pride_boost} × Platform: {platform_multiplier}"
        }

    def calculate_perceived_control(self, sentiment: Dict, nam_score: float) -> Dict:
        """
        Calculate perceived behavioral control (perceived ease of engaging/sharing).
        
        Perceived control is influenced by:
        - Base ease of social media engagement (high - it's easy to share)
        - Subjectivity (high subjectivity = seems salesy = reduces control)
        - Ambiguity (high ambiguity = confusing = reduces control)
        - Negative sentiment (negative content = less comfortable sharing)
        
        Formula: Control = base - subjectivity_penalty - ambiguity_penalty - sentiment_penalty
        
        Args:
            sentiment: Sentiment analysis dictionary
            nam_score: Narrative ambiguity measure score (0-100)
            
        Returns:
            Dictionary containing perceived control score and breakdown
            
        Requirements: 5.3
        """
        # Base perceived control score (70 - social media is easy to use)
        base_score = 70
        
        # Penalty 1: High subjectivity (-10 points if > 0.7)
        # High subjectivity suggests opinion/sales rather than facts
        # Makes people less comfortable sharing
        subjectivity = sentiment.get('subjectivity', 0.0)
        subjectivity_penalty = 10 if subjectivity > 0.7 else 0
        
        # Penalty 2: High ambiguity (-15 points if NAM > 50)
        # Confusing content reduces perceived control
        # People don't share what they don't understand
        ambiguity_penalty = 15 if nam_score > 50 else 0
        
        # Penalty 3: Negative sentiment (-20 points if polarity < -0.2)
        # People are less comfortable sharing negative content
        polarity = sentiment.get('polarity', 0.0)
        sentiment_penalty = 20 if polarity < -0.2 else 0
        
        # Calculate final perceived control score
        control_score = base_score - subjectivity_penalty - ambiguity_penalty - sentiment_penalty
        control_score = max(control_score, 0)  # Floor at 0
        
        return {
            'perceived_control': round(control_score, 2),
            'base_score': base_score,
            'subjectivity_penalty': subjectivity_penalty,
            'ambiguity_penalty': ambiguity_penalty,
            'sentiment_penalty': sentiment_penalty,
            'breakdown': f"Base: {base_score} - Subjectivity: {subjectivity_penalty} - Ambiguity: {ambiguity_penalty} - Sentiment: {sentiment_penalty}"
        }

    def calculate_behavioral_intention(self, attitude: float, subjective_norms: float,
                                       perceived_control: float) -> Dict:
        """
        Calculate behavioral intention (likelihood of sharing/engaging).
        
        This is the key outcome of the TPB framework, predicting the likelihood
        that audiences will share or engage with the content.
        
        Based on Ajzen (1991) TPB formula with weights adapted for Indian context:
        - Attitude: 40% (primary driver in collectivist context)
        - Subjective Norms: 35% (strong social influence in Indian culture)
        - Perceived Control: 25% (lower weight as social media is easy)
        
        Formula: Intention = (Attitude * 0.40) + (Subjective_Norms * 0.35) + (Perceived_Control * 0.25)
        
        Args:
            attitude: Attitude score (0-100)
            subjective_norms: Subjective norms score (0-100)
            perceived_control: Perceived control score (0-100)
            
        Returns:
            Dictionary containing behavioral intention score and breakdown
            
        Requirements: 5.4, 5.5
        """
        # Apply TPB weights
        attitude_component = attitude * 0.40
        norms_component = subjective_norms * 0.35
        control_component = perceived_control * 0.25
        
        # Calculate behavioral intention
        intention_score = attitude_component + norms_component + control_component
        intention_score = min(max(intention_score, 0), 100)  # Clamp to 0-100
        
        # Determine interpretation
        if intention_score >= 75:
            interpretation = "Very High - Strong likelihood of sharing and engagement"
            category = "very_high"
        elif intention_score >= 60:
            interpretation = "High - Good likelihood of sharing and engagement"
            category = "high"
        elif intention_score >= 45:
            interpretation = "Moderate - Some sharing and engagement expected"
            category = "moderate"
        elif intention_score >= 30:
            interpretation = "Low - Limited sharing and engagement expected"
            category = "low"
        else:
            interpretation = "Very Low - Minimal sharing and engagement expected"
            category = "very_low"
        
        return {
            'behavioral_intention': round(intention_score, 2),
            'attitude_component': round(attitude_component, 2),
            'norms_component': round(norms_component, 2),
            'control_component': round(control_component, 2),
            'interpretation': interpretation,
            'category': category,
            'breakdown': f"Attitude: {attitude_component:.1f} (40%) + Norms: {norms_component:.1f} (35%) + Control: {control_component:.1f} (25%)"
        }
    
    def calculate_tpb_scores(self, sentiment: Dict, emc_score: float,
                            perceived_intent: float, nam_score: float,
                            emotions: List[str], platform: str,
                            influencer: bool) -> Dict:
        """
        Calculate all TPB framework scores in one call.
        
        This is the main entry point for TPB analysis, calculating all four
        components: attitude, subjective norms, perceived control, and behavioral intention.
        
        Args:
            sentiment: Sentiment analysis dictionary
            emc_score: Emotional-moral content score (0-100)
            perceived_intent: Perceived intent score (-100 to +100)
            nam_score: Narrative ambiguity measure score (0-100)
            emotions: List of detected emotions
            platform: Social media platform name
            influencer: Whether this is an influencer partnership
            
        Returns:
            Dictionary containing all TPB scores and breakdowns
            
        Requirements: 5.1, 5.2, 5.3, 5.4, 5.5
        """
        # Calculate each TPB component
        attitude_result = self.calculate_attitude(sentiment, emc_score, perceived_intent, emotions)
        norms_result = self.calculate_subjective_norms(platform, influencer, emotions)
        control_result = self.calculate_perceived_control(sentiment, nam_score)
        
        # Calculate behavioral intention from the three components
        intention_result = self.calculate_behavioral_intention(
            attitude_result['attitude'],
            norms_result['subjective_norms'],
            control_result['perceived_control']
        )
        
        return {
            'attitude': attitude_result['attitude'],
            'subjective_norms': norms_result['subjective_norms'],
            'perceived_control': control_result['perceived_control'],
            'behavioral_intention': intention_result['behavioral_intention'],
            'attitude_breakdown': attitude_result,
            'norms_breakdown': norms_result,
            'control_breakdown': control_result,
            'intention_breakdown': intention_result
        }
