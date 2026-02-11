# AdsenseAI Campaign Risk Analyzer - Perceived Intent Calculator Module
# Calculates audience attribution of creator motives (mediating variable in TPB)

from typing import Dict, List


class PerceivedIntentCalculator:
    """
    Calculates perceived intent based on content characteristics.
    Perceived intent mediates the relationship between content characteristics
    and behavioral outcomes (virality and backlash).
    """
    
    def __init__(self):
        """Initialize the perceived intent calculator"""
        
        # CRITICAL FIX 2: Manipulation pattern detection
        # Detects manipulative framing even with positive sentiment
        self.MANIPULATION_PATTERNS = {
            'insecurity_exploitation': {
                'triggers': ['dont let', 'stop letting', 'hold you back', 'holding you back',
                           'problem', 'issue', 'struggle', 'suffering'],
                'promises': ['transform', 'change', 'finally', 'guaranteed', 'secret',
                           'solution', 'answer', 'fix', 'cure'],
                'penalty': 40
            },
            'fear_based_selling': {
                'triggers': ['miss out', 'left behind', 'before its too late', 'running out',
                           'limited', 'last chance', 'dont wait', 'act now'],
                'urgency': ['now', 'today', 'hurry', 'quick', 'fast', 'immediate'],
                'penalty': 35
            },
            'shame_based_marketing': {
                'triggers': ['embarrassed', 'ashamed', 'hide', 'ugly', 'unattractive',
                           'disgusting', 'gross', 'inferior'],
                'solutions': ['finally', 'no more', 'say goodbye', 'never again', 'transform'],
                'penalty': 45
            },
            'false_causation': {
                'claims': ['because of your', 'due to your', 'your X is why', 'reason you',
                          'thats why you', 'if only you'],
                'areas': ['job', 'career', 'marriage', 'success', 'failure', 'rejection',
                         'relationship', 'money', 'wealth'],
                'penalty': 50
            }
        }
    
    def calculate_authenticity_score(self, sentiment: Dict, scs_score: float, 
                                    emc_score: float) -> float:
        """
        Calculate authenticity score based on positive sentiment,
        low cultural sensitivity issues, and appropriate EMC.
        
        Formula: Authenticity = (pos_sentiment * 30) + ((100 - scs) * 40) + (emc_appropriate * 30)
        
        Args:
            sentiment: Sentiment analysis dictionary
            scs_score: Socio-cultural sensitivity score (0-100)
            emc_score: Emotional-moral content score (0-100)
            
        Returns:
            Authenticity score (0-100)
            
        Requirements: 4.1, 4.2
        """
        # Component 1: Positive sentiment (0-30 points)
        polarity = sentiment.get('polarity', 0.0)  # -1 to +1
        # Convert polarity to 0-100 scale, then apply weight
        positive_sentiment = ((polarity + 1) / 2) * 100  # 0-100
        sentiment_component = positive_sentiment * 0.30
        
        # Component 2: Low SCS (0-40 points)
        # Lower SCS = higher authenticity
        low_scs_component = (100 - scs_score) * 0.40
        
        # Component 3: Appropriate EMC (0-30 points)
        # EMC in 40-70 range is considered appropriate (authentic but engaging)
        # Too low = boring, too high = manipulative
        if 40 <= emc_score <= 70:
            emc_appropriateness = 100  # Ideal range
        elif emc_score < 40:
            # Too low - scale from 0 to 100
            emc_appropriateness = (emc_score / 40) * 100
        else:  # emc_score > 70
            # Too high - scale from 100 down to 0
            emc_appropriateness = max(0, 100 - ((emc_score - 70) / 30) * 100)
        
        emc_component = emc_appropriateness * 0.30
        
        # Calculate total authenticity score
        authenticity = sentiment_component + low_scs_component + emc_component
        authenticity = min(max(authenticity, 0), 100)  # Clamp to 0-100
        
        return round(authenticity, 2)
    
    def detect_manipulation_patterns(self, text: str, scs_score: float, 
                                    sentiment: Dict) -> Dict:
        """
        CRITICAL FIX 2: Detect manipulation patterns even with positive sentiment.
        
        Identifies manipulative framing that exploits insecurities, uses fear/shame,
        or makes false causal claims.
        
        Args:
            text: Text content to analyze
            scs_score: Socio-cultural sensitivity score
            sentiment: Sentiment analysis dictionary
            
        Returns:
            Dictionary with manipulation detection results
        """
        if not text or not text.strip():
            return {
                'manipulation_detected': False,
                'patterns_found': [],
                'total_penalty': 0
            }
        
        text_lower = text.lower()
        patterns_found = []
        total_penalty = 0
        
        # Check each manipulation pattern
        for pattern_name, pattern_def in self.MANIPULATION_PATTERNS.items():
            pattern_detected = False
            matched_elements = []
            
            if pattern_name == 'insecurity_exploitation':
                # Check for triggers + promises combination
                triggers = [t for t in pattern_def['triggers'] if t in text_lower]
                promises = [p for p in pattern_def['promises'] if p in text_lower]
                
                if triggers and promises:
                    pattern_detected = True
                    matched_elements = triggers + promises
                    
            elif pattern_name == 'fear_based_selling':
                # Check for triggers + urgency combination
                triggers = [t for t in pattern_def['triggers'] if t in text_lower]
                urgency = [u for u in pattern_def['urgency'] if u in text_lower]
                
                if triggers and urgency:
                    pattern_detected = True
                    matched_elements = triggers + urgency
                    
            elif pattern_name == 'shame_based_marketing':
                # Check for triggers + solutions combination
                triggers = [t for t in pattern_def['triggers'] if t in text_lower]
                solutions = [s for s in pattern_def['solutions'] if s in text_lower]
                
                if triggers and solutions:
                    pattern_detected = True
                    matched_elements = triggers + solutions
                    
            elif pattern_name == 'false_causation':
                # Check for claims + areas combination
                claims = [c for c in pattern_def['claims'] if c in text_lower]
                areas = [a for a in pattern_def['areas'] if a in text_lower]
                
                if claims and areas:
                    pattern_detected = True
                    matched_elements = claims + areas
            
            if pattern_detected:
                patterns_found.append({
                    'pattern': pattern_name,
                    'penalty': pattern_def['penalty'],
                    'matched': matched_elements[:5]  # Limit to 5 for brevity
                })
                total_penalty += pattern_def['penalty']
        
        # SPECIAL RULE: High SCS + Positive Sentiment = Likely Manipulation
        # Positive framing of harmful content is manipulative
        polarity = sentiment.get('polarity', 0.0)
        if scs_score > 50 and polarity > 0.3:
            patterns_found.append({
                'pattern': 'positive_harmful_framing',
                'penalty': 25,
                'matched': ['high_scs_positive_sentiment']
            })
            total_penalty += 25
        
        return {
            'manipulation_detected': len(patterns_found) > 0,
            'patterns_found': patterns_found,
            'total_penalty': total_penalty
        }
    
    def calculate_manipulation_risk(self, scs_score: float, emc_score: float,
                                   sentiment: Dict) -> float:
        """
        Calculate manipulation risk score based on high SCS,
        excessive EMC, and high subjectivity.
        
        Formula: Manipulation = (scs * 40) + (excessive_emc * 30) + (subjectivity * 30)
        
        Args:
            scs_score: Socio-cultural sensitivity score (0-100)
            emc_score: Emotional-moral content score (0-100)
            sentiment: Sentiment analysis dictionary
            
        Returns:
            Manipulation risk score (0-100)
            
        Requirements: 4.3
        """
        # Component 1: High SCS (0-40 points)
        # Higher SCS = higher manipulation risk
        scs_component = scs_score * 0.40
        
        # Component 2: Excessive EMC (0-30 points)
        # EMC > 70 is considered excessive (trying too hard)
        if emc_score <= 70:
            excessive_emc = 0
        else:
            # Scale from 0 to 100 for EMC 70-100
            excessive_emc = ((emc_score - 70) / 30) * 100
        
        emc_component = excessive_emc * 0.30
        
        # Component 3: High subjectivity (0-30 points)
        # High subjectivity suggests opinion/sales rather than facts
        subjectivity = sentiment.get('subjectivity', 0.0)  # 0 to 1
        subjectivity_score = subjectivity * 100  # Convert to 0-100
        subjectivity_component = subjectivity_score * 0.30
        
        # Calculate total manipulation risk
        manipulation = scs_component + emc_component + subjectivity_component
        manipulation = min(max(manipulation, 0), 100)  # Clamp to 0-100
        
        return round(manipulation, 2)
    
    def calculate_perceived_intent(self, emc_score: float, nam_score: float,
                                  scs_score: float, sentiment: Dict, text: str = "") -> Dict:
        """
        Calculate perceived intent score representing audience attribution
        of creator motives.
        
        Combines authenticity and manipulation scores to determine if content
        is likely perceived as genuine, values-aligned, manipulative, or insensitive.
        
        Args:
            emc_score: Emotional-moral content score (0-100)
            nam_score: Narrative ambiguity measure score (0-100)
            scs_score: Socio-cultural sensitivity score (0-100)
            sentiment: Sentiment analysis dictionary
            text: Text content for manipulation detection (optional)
            
        Returns:
            Dictionary containing perceived intent analysis
            
        Requirements: 4.4, 4.5
        """
        # Calculate authenticity and manipulation scores
        authenticity = self.calculate_authenticity_score(sentiment, scs_score, emc_score)
        manipulation = self.calculate_manipulation_risk(scs_score, emc_score, sentiment)
        
        # CRITICAL FIX 2: Detect manipulation patterns
        manipulation_detection = self.detect_manipulation_patterns(text, scs_score, sentiment)
        
        # Apply manipulation penalty if patterns detected
        if manipulation_detection['manipulation_detected']:
            manipulation += manipulation_detection['total_penalty']
            manipulation = min(manipulation, 100)  # Cap at 100
        
        # Calculate perceived intent score (-100 to +100)
        # Positive = authentic, Negative = manipulative
        intent_score = authenticity - manipulation
        intent_score = max(min(intent_score, 100), -100)  # Clamp to -100 to +100
        
        # Determine interpretation based on score
        if intent_score >= 50:
            interpretation = "Highly Authentic - Likely perceived as genuine and values-aligned"
            category = "authentic"
        elif intent_score >= 20:
            interpretation = "Moderately Authentic - Generally perceived as sincere"
            category = "authentic"
        elif intent_score >= -20:
            interpretation = "Neutral - Mixed signals, interpretation varies by audience"
            category = "neutral"
        elif intent_score >= -50:
            interpretation = "Moderately Manipulative - May be perceived as sales-focused"
            category = "manipulative"
        else:
            interpretation = "Highly Manipulative - Likely perceived as insincere or exploitative"
            category = "manipulative"
        
        # Factor in narrative ambiguity
        # High ambiguity increases interpretive uncertainty
        ambiguity_factor = "low"
        if nam_score > 60:
            ambiguity_factor = "high"
            interpretation += " (High ambiguity may lead to varied interpretations)"
        elif nam_score > 30:
            ambiguity_factor = "medium"
        
        # Check for cultural insensitivity
        if scs_score > 50:
            interpretation += " ⚠️ Cultural sensitivity concerns present"
        
        # Add manipulation warning if detected
        if manipulation_detection['manipulation_detected']:
            interpretation += f" ⚠️ {len(manipulation_detection['patterns_found'])} manipulation pattern(s) detected"
        
        return {
            'intent_score': round(intent_score, 2),
            'authenticity': authenticity,
            'manipulation_risk': manipulation,
            'interpretation': interpretation,
            'category': category,
            'ambiguity_factor': ambiguity_factor,
            'confidence': self._calculate_confidence(nam_score, scs_score),
            'manipulation_patterns': manipulation_detection  # NEW: Include pattern details
        }
    
    def _calculate_confidence(self, nam_score: float, scs_score: float) -> str:
        """
        Calculate confidence level in perceived intent assessment.
        
        High ambiguity or high SCS reduces confidence.
        
        Args:
            nam_score: Narrative ambiguity score
            scs_score: Cultural sensitivity score
            
        Returns:
            Confidence level string
        """
        # Lower confidence if high ambiguity or high cultural sensitivity
        uncertainty = (nam_score * 0.6) + (scs_score * 0.4)
        
        if uncertainty < 30:
            return "high"
        elif uncertainty < 60:
            return "medium"
        else:
            return "low"
    
    def get_intent_recommendations(self, intent_result: Dict) -> List[str]:
        """
        Generate recommendations based on perceived intent analysis.
        
        Args:
            intent_result: Result from calculate_perceived_intent()
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        intent_score = intent_result.get('intent_score', 0)
        authenticity = intent_result.get('authenticity', 0)
        manipulation = intent_result.get('manipulation_risk', 0)
        ambiguity = intent_result.get('ambiguity_factor', 'low')
        
        # Recommendations based on intent score
        if intent_score < -20:
            recommendations.append("⚠️ Content may be perceived as manipulative or insincere")
            recommendations.append("Consider reducing emotional intensity and sales language")
            recommendations.append("Focus on authentic storytelling and value delivery")
        
        # Recommendations based on authenticity
        if authenticity < 40:
            recommendations.append("Increase authenticity by aligning with cultural values")
            recommendations.append("Use more genuine, relatable language")
        
        # Recommendations based on manipulation risk
        if manipulation > 60:
            recommendations.append("⚠️ High manipulation risk detected")
            recommendations.append("Reduce excessive emotional appeals")
            recommendations.append("Avoid culturally sensitive topics or handle with care")
        
        # Recommendations based on ambiguity
        if ambiguity == "high":
            recommendations.append("Message clarity could be improved")
            recommendations.append("Reduce abstract language and open-ended statements")
            recommendations.append("Be more specific and direct in messaging")
        
        # Positive reinforcement
        if intent_score > 50 and authenticity > 70:
            recommendations.append("✅ Strong authentic messaging - maintain this approach")
        
        return recommendations
