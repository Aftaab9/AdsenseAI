"""
Resonance Calculator

Calculates how well campaign content resonates with specific audience personas.
Implements research-backed scoring algorithms combining value alignment,
tone matching, interest relevance, and cultural fit.

Requirements: 4.1, 4.3
"""

from typing import Dict, List, Optional
import re

from app.models import Persona


class ResonanceCalculator:
    """
    Calculates resonance scores between campaign content and audience personas.
    
    Resonance Score Formula:
    Resonance = (Value_Alignment × 0.25 + Tone_Match × 0.20 + 
                 Interest_Relevance × 0.20 + Cultural_Fit × 0.15 + 
                 Platform_Fit × 0.10 + Emotional_Resonance × 0.10) × Personality_Modifier
    
    All component scores are normalized to 0-100 scale.
    """
    
    def __init__(self):
        """Initialize the resonance calculator"""
        pass
    
    def calculate_resonance(
        self,
        content_analysis: Dict,
        persona: Persona,
        platform: str = "instagram"
    ) -> Dict:
        """
        Calculate overall resonance score between content and persona.
        
        Args:
            content_analysis: Dictionary containing text analysis results
                Expected keys: sentiment, emotions, moral_framing, emc_score, etc.
            persona: Persona object to test against
            platform: Platform name (default: "instagram")
        
        Returns:
            Dictionary containing resonance score and component breakdowns
        
        Requirements: 4.1, 4.3
        """
        # Extract content text for analysis
        content_text = content_analysis.get('cleaned_text', content_analysis.get('text', ''))
        
        # Calculate each component (0-100 scale)
        value_alignment = self._calculate_value_alignment(content_analysis, persona)
        tone_match = self._calculate_tone_match(content_analysis, persona)
        interest_relevance = self._calculate_interest_relevance(content_text, persona)
        cultural_fit = self._calculate_cultural_fit(content_analysis, persona)
        platform_fit = self._calculate_platform_fit(platform, persona)
        emotional_resonance = self._calculate_emotional_resonance(content_analysis, persona)
        
        # Apply weighted formula
        weighted_sum = (
            value_alignment * 0.25 +
            tone_match * 0.20 +
            interest_relevance * 0.20 +
            cultural_fit * 0.15 +
            platform_fit * 0.10 +
            emotional_resonance * 0.10
        )
        
        # Apply personality modifier based on OCEAN traits
        personality_modifier = self._calculate_personality_modifier(
            content_analysis, persona.psychographics
        )
        
        # Calculate final resonance score
        resonance_score = weighted_sum * personality_modifier
        resonance_score = min(max(resonance_score, 0), 100)  # Clamp to 0-100
        
        # Predict emotional response
        emotion_prediction = self.predict_emotion(content_analysis, persona)
        
        # Predict behavioral actions
        action_prediction = self.predict_actions(content_analysis, persona, resonance_score)
        
        # Calculate engagement and share likelihood based on persona behavior
        engagement_base = resonance_score
        if persona.media_behavior.engagement_style == 'proactive':
            engagement_likelihood = min(engagement_base * 1.2, 100)
        elif persona.media_behavior.engagement_style == 'reactive':
            engagement_likelihood = engagement_base
        elif persona.media_behavior.engagement_style == 'passive':
            engagement_likelihood = engagement_base * 0.7
        else:  # creator
            engagement_likelihood = min(engagement_base * 1.3, 100)
        
        # Calculate share likelihood based on sharing propensity
        share_base = resonance_score * 0.8
        if persona.media_behavior.sharing_propensity == 'viral':
            share_likelihood = min(share_base * 1.5, 100)
        elif persona.media_behavior.sharing_propensity == 'frequent':
            share_likelihood = min(share_base * 1.2, 100)
        elif persona.media_behavior.sharing_propensity == 'selective':
            share_likelihood = share_base
        else:  # never
            share_likelihood = share_base * 0.3
        
        return {
            'resonance_score': round(resonance_score, 2),
            'value_alignment': round(value_alignment, 2),
            'tone_match': round(tone_match, 2),
            'interest_relevance': round(interest_relevance, 2),
            'relevance_score': round(interest_relevance, 2),  # Alias for API compatibility
            'cultural_fit': round(cultural_fit, 2),
            'platform_fit': round(platform_fit, 2),
            'emotional_resonance': round(emotional_resonance, 2),
            'personality_modifier': round(personality_modifier, 3),
            'weighted_sum': round(weighted_sum, 2),
            # Emotional prediction
            'predicted_emotions': emotion_prediction['predicted_emotions'],
            'dominant_emotion': emotion_prediction['dominant_emotion'],
            'emotional_intensity': emotion_prediction['emotional_intensity'],
            # Behavioral prediction
            'predicted_actions': action_prediction['predicted_actions'],
            'most_likely_action': action_prediction['most_likely_action'],
            # Engagement metrics
            'engagement_likelihood': round(engagement_likelihood, 2),
            'share_likelihood': round(share_likelihood, 2)
        }
    
    def _calculate_value_alignment(self, content_analysis: Dict, persona: Persona) -> float:
        """
        Calculate alignment between content values and persona core values.
        
        Uses keyword matching to detect value themes in content and compares
        with persona's core values.
        
        Args:
            content_analysis: Content analysis dictionary
            persona: Persona object
        
        Returns:
            Value alignment score (0-100)
        """
        # Get content text
        content_text = content_analysis.get('cleaned_text', '').lower()
        
        # Get moral framing data if available
        moral_framing = content_analysis.get('moral_framing', {})
        moral_categories = moral_framing.get('moral_categories', [])
        
        # Get persona's core values
        persona_values = [v.lower() for v in persona.psychographics.core_values]
        
        if not persona_values:
            return 50.0  # Neutral score if no values defined
        
        # Value keyword mapping (expanded from moral framing)
        value_keywords = {
            'family': ['family', 'families', 'parent', 'mother', 'father', 'children', 'home', 'together'],
            'success': ['success', 'achieve', 'achievement', 'win', 'victory', 'excellence', 'best'],
            'tradition': ['tradition', 'traditional', 'heritage', 'culture', 'custom', 'ritual', 'ancient'],
            'freedom': ['freedom', 'liberty', 'independent', 'choice', 'free'],
            'authenticity': ['authentic', 'genuine', 'real', 'honest', 'truth', 'transparent'],
            'diversity': ['diverse', 'diversity', 'inclusive', 'inclusion', 'different', 'variety'],
            'sustainability': ['sustainable', 'eco', 'green', 'environment', 'planet', 'nature'],
            'creativity': ['creative', 'creativity', 'art', 'artistic', 'innovative', 'original'],
            'community': ['community', 'together', 'collective', 'society', 'social', 'unity'],
            'quality': ['quality', 'premium', 'excellence', 'superior', 'finest', 'best'],
            'innovation': ['innovation', 'innovative', 'new', 'modern', 'future', 'advanced'],
            'trust': ['trust', 'reliable', 'dependable', 'honest', 'integrity'],
            'respect': ['respect', 'honor', 'dignity', 'esteem'],
            'progress': ['progress', 'growth', 'development', 'improve', 'better', 'forward']
        }
        
        # Count value matches
        matches = 0
        total_checks = len(persona_values)
        
        for persona_value in persona_values:
            # Check if value appears directly in content
            if persona_value in content_text:
                matches += 1
                continue
            
            # Check if value keywords appear in content
            keywords = value_keywords.get(persona_value, [persona_value])
            for keyword in keywords:
                if keyword in content_text:
                    matches += 1
                    break
        
        # Calculate alignment percentage
        alignment_score = (matches / total_checks) * 100 if total_checks > 0 else 50.0
        
        # Boost score if moral framing aligns with persona values
        if moral_categories:
            moral_value_overlap = len(set(moral_categories) & set(persona_values))
            if moral_value_overlap > 0:
                alignment_score = min(alignment_score + (moral_value_overlap * 10), 100)
        
        return alignment_score
    
    def _calculate_tone_match(self, content_analysis: Dict, persona: Persona) -> float:
        """
        Calculate how well content tone matches persona communication preferences.
        
        Considers sentiment, formality, and humor style.
        
        Args:
            content_analysis: Content analysis dictionary
            persona: Persona object
        
        Returns:
            Tone match score (0-100)
        """
        score = 50.0  # Start with neutral
        
        # Get sentiment data
        sentiment = content_analysis.get('sentiment', {})
        polarity = sentiment.get('polarity', 0.0)
        
        # Get persona preferences
        communication_formality = persona.cultural_profile.communication_formality
        humor_styles = persona.cultural_profile.humor_style
        
        # Get content text
        content_text = content_analysis.get('cleaned_text', '').lower()
        
        # Check formality match
        formal_indicators = ['please', 'kindly', 'respectfully', 'sincerely', 'regards']
        casual_indicators = ['hey', 'hi', 'lol', 'haha', 'cool', 'awesome', 'yeah']
        
        formal_count = sum(1 for word in formal_indicators if word in content_text)
        casual_count = sum(1 for word in casual_indicators if word in content_text)
        
        if communication_formality == 'formal' and formal_count > casual_count:
            score += 20
        elif communication_formality == 'casual' and casual_count > formal_count:
            score += 20
        elif communication_formality == 'mixed':
            score += 10  # Mixed accepts both
        
        # Check humor style match
        emotions = content_analysis.get('emotions', [])
        if 'humor' in emotions and humor_styles:
            score += 15
        
        # Check sentiment alignment with persona's emotional triggers
        emotional_triggers = persona.behavioral_triggers.emotional_triggers
        
        # Positive content generally resonates well
        if polarity > 0.3:
            score += 10
        # Very negative content is risky
        elif polarity < -0.3:
            score -= 15
        
        return min(max(score, 0), 100)
    
    def _calculate_interest_relevance(self, content_text: str, persona: Persona) -> float:
        """
        Calculate relevance of content topics to persona interests.
        
        Uses keyword matching to detect topics and compare with persona interests.
        
        Args:
            content_text: Cleaned content text
            persona: Persona object
        
        Returns:
            Interest relevance score (0-100)
        """
        content_lower = content_text.lower()
        persona_interests = [i.lower() for i in persona.psychographics.interests]
        
        if not persona_interests:
            return 50.0  # Neutral if no interests defined
        
        # Interest keyword mapping
        interest_keywords = {
            'technology': ['tech', 'digital', 'app', 'software', 'ai', 'gadget', 'device', 'online'],
            'fashion': ['fashion', 'style', 'clothing', 'outfit', 'trend', 'wear', 'dress', 'look'],
            'sports': ['sport', 'game', 'play', 'fitness', 'athletic', 'team', 'match', 'win'],
            'travel': ['travel', 'trip', 'journey', 'destination', 'explore', 'adventure', 'vacation'],
            'food': ['food', 'eat', 'cook', 'recipe', 'taste', 'delicious', 'meal', 'cuisine'],
            'music': ['music', 'song', 'sing', 'artist', 'band', 'concert', 'listen'],
            'entertainment': ['entertainment', 'movie', 'show', 'watch', 'fun', 'enjoy'],
            'health': ['health', 'wellness', 'fitness', 'exercise', 'healthy', 'workout'],
            'beauty': ['beauty', 'makeup', 'skincare', 'cosmetic', 'glow', 'beautiful'],
            'education': ['learn', 'education', 'study', 'knowledge', 'skill', 'course', 'teach'],
            'finance': ['money', 'finance', 'invest', 'save', 'bank', 'wealth', 'financial'],
            'gaming': ['game', 'gaming', 'play', 'gamer', 'console', 'esports'],
            'activism': ['activism', 'cause', 'change', 'movement', 'justice', 'rights'],
            'social_media': ['social', 'post', 'share', 'like', 'follow', 'viral', 'trending']
        }
        
        # Count interest matches
        matches = 0
        for interest in persona_interests:
            # Direct match
            if interest in content_lower:
                matches += 1
                continue
            
            # Keyword match
            keywords = interest_keywords.get(interest, [interest])
            for keyword in keywords:
                if keyword in content_lower:
                    matches += 1
                    break
        
        # Calculate relevance score
        relevance_score = (matches / len(persona_interests)) * 100 if persona_interests else 50.0
        
        return min(relevance_score, 100)
    
    def _calculate_cultural_fit(self, content_analysis: Dict, persona: Persona) -> float:
        """
        Calculate cultural fit based on SCS score and persona cultural profile.
        
        Lower SCS score = better cultural fit for most personas.
        Some personas (progressive, low traditionalism) are more tolerant.
        
        Args:
            content_analysis: Content analysis dictionary
            persona: Persona object
        
        Returns:
            Cultural fit score (0-100)
        """
        # Get SCS score (0-100, higher = more sensitive/risky)
        scs_score = content_analysis.get('scs_score', 0.0)
        
        # Get persona's cultural sensitivity factors
        traditionalism = persona.cultural_profile.traditionalism
        religious_sensitivity = persona.cultural_profile.religious_sensitivity
        
        # Calculate persona's overall cultural sensitivity
        # Higher traditionalism/religious sensitivity = less tolerant of cultural issues
        persona_sensitivity = (traditionalism + religious_sensitivity) / 2
        
        # Calculate fit score
        # If content has low SCS (safe), fit is high
        # If content has high SCS, fit depends on persona tolerance
        if scs_score < 20:
            # Safe content - good fit for everyone
            fit_score = 90
        elif scs_score < 40:
            # Moderate risk - depends on persona
            if persona_sensitivity < 50:
                fit_score = 75  # Progressive persona tolerates it
            else:
                fit_score = 50  # Traditional persona cautious
        else:
            # High risk content
            if persona_sensitivity < 30:
                fit_score = 60  # Very progressive might still accept
            elif persona_sensitivity < 60:
                fit_score = 30  # Moderate persona concerned
            else:
                fit_score = 10  # Traditional persona rejects
        
        return fit_score
    
    def _calculate_platform_fit(self, platform: str, persona: Persona) -> float:
        """
        Calculate how well the platform matches persona's platform preferences.
        
        Args:
            platform: Platform name (e.g., "instagram", "youtube")
            persona: Persona object
        
        Returns:
            Platform fit score (0-100)
        """
        platform_lower = platform.lower()
        platform_affinity = persona.media_behavior.platform_affinity
        
        # Get affinity score for this platform (0-1 scale)
        affinity = platform_affinity.get(platform_lower, 0.5)
        
        # Convert to 0-100 scale
        return affinity * 100
    
    def _calculate_emotional_resonance(self, content_analysis: Dict, persona: Persona) -> float:
        """
        Calculate emotional resonance between content emotions and persona triggers.
        
        Args:
            content_analysis: Content analysis dictionary
            persona: Persona object
        
        Returns:
            Emotional resonance score (0-100)
        """
        # Get content emotions
        content_emotions = content_analysis.get('emotions', [])
        
        # Get persona's emotional triggers
        emotional_triggers = persona.behavioral_triggers.emotional_triggers
        engagement_triggers = persona.behavioral_triggers.engagement_triggers
        
        if not content_emotions:
            return 50.0  # Neutral if no emotions detected
        
        score = 50.0
        
        # Check if content emotions match persona's emotional triggers
        for emotion in content_emotions:
            if emotion in emotional_triggers:
                score += 10
        
        # Check if content has engagement triggers
        content_text = content_analysis.get('cleaned_text', '').lower()
        for trigger in engagement_triggers:
            if trigger.lower() in content_text:
                score += 5
        
        return min(score, 100)
    
    def _calculate_personality_modifier(self, content_analysis: Dict, psychographics) -> float:
        """
        Calculate personality-based modifier using Big Five (OCEAN) traits.
        
        Adjusts resonance based on how content characteristics align with
        personality traits.
        
        Args:
            content_analysis: Content analysis dictionary
            psychographics: Persona's psychographics object
        
        Returns:
            Modifier value (typically 0.8 to 1.5)
        """
        modifier = 1.0
        
        content_text = content_analysis.get('cleaned_text', '').lower()
        sentiment = content_analysis.get('sentiment', {})
        emotions = content_analysis.get('emotions', [])
        
        # High Openness: More receptive to creative, novel content
        creative_indicators = ['new', 'innovative', 'unique', 'creative', 'original', 'different']
        is_creative = any(word in content_text for word in creative_indicators)
        if is_creative:
            openness_factor = psychographics.openness / 100
            modifier *= 1 + (openness_factor * 0.2)
        
        # High Conscientiousness: Prefer detailed, factual content
        detail_indicators = ['detail', 'fact', 'proven', 'research', 'study', 'data']
        is_detailed = any(word in content_text for word in detail_indicators)
        if is_detailed:
            conscientiousness_factor = psychographics.conscientiousness / 100
            modifier *= 1 + (conscientiousness_factor * 0.15)
        
        # High Extraversion: Respond to social, energetic content
        social_indicators = ['share', 'together', 'community', 'join', 'connect', 'social']
        is_social = any(word in content_text for word in social_indicators)
        if is_social or 'joy' in emotions:
            extraversion_factor = psychographics.extraversion / 100
            modifier *= 1 + (extraversion_factor * 0.15)
        
        # High Agreeableness: Respond to warm, cooperative messaging
        warm_indicators = ['care', 'help', 'support', 'kind', 'love', 'together', 'family']
        is_warm = any(word in content_text for word in warm_indicators)
        if is_warm:
            agreeableness_factor = psychographics.agreeableness / 100
            modifier *= 1 + (agreeableness_factor * 0.1)
        
        # High Neuroticism: More sensitive to negative/fear content
        if 'fear' in emotions or 'urgency' in emotions:
            neuroticism_factor = psychographics.neuroticism / 100
            modifier *= 1 + (neuroticism_factor * 0.1)
        
        # Cap modifier at reasonable bounds
        return min(max(modifier, 0.8), 1.5)
    
    def predict_emotion(
        self,
        content_analysis: Dict,
        persona: Persona
    ) -> Dict:
        """
        Predict emotional response of a persona to content.
        
        Maps content emotions to persona's emotional triggers and predicts
        the dominant emotion and its intensity.
        
        Args:
            content_analysis: Content analysis dictionary with detected emotions
            persona: Persona object
        
        Returns:
            Dictionary containing:
                - predicted_emotions: Dict of emotion -> intensity (0-1)
                - dominant_emotion: Primary predicted emotion
                - emotional_intensity: Overall intensity (0-100)
        
        Requirements: 4.2
        """
        # Get content emotions and sentiment
        content_emotions = content_analysis.get('emotions', [])
        sentiment = content_analysis.get('sentiment', {})
        polarity = sentiment.get('polarity', 0.0)
        
        # Get persona's emotional triggers
        emotional_triggers = persona.behavioral_triggers.emotional_triggers
        engagement_triggers = persona.behavioral_triggers.engagement_triggers
        friction_triggers = persona.behavioral_triggers.friction_triggers
        
        # Initialize emotion scores
        emotion_scores = {
            'joy': 0.0,
            'interest': 0.0,
            'skepticism': 0.0,
            'anger': 0.0,
            'fear': 0.0,
            'indifference': 0.0,
            'excitement': 0.0
        }
        
        # Base emotions from content
        for emotion in content_emotions:
            if emotion in emotion_scores:
                emotion_scores[emotion] = 0.6
            elif emotion == 'humor':
                emotion_scores['joy'] += 0.4
            elif emotion == 'nostalgia':
                emotion_scores['interest'] += 0.3
            elif emotion == 'pride':
                emotion_scores['joy'] += 0.3
            elif emotion == 'inspiration':
                emotion_scores['excitement'] += 0.4
            elif emotion == 'urgency':
                emotion_scores['excitement'] += 0.3
        
        # Adjust based on persona's emotional triggers
        content_text = content_analysis.get('cleaned_text', '').lower()
        
        # Check if content triggers positive emotions for this persona
        for emotion_type, trigger_keywords in emotional_triggers.items():
            match_count = sum(1 for keyword in trigger_keywords if keyword.lower() in content_text)
            if match_count > 0:
                # Map emotion types to our standard emotions
                if emotion_type in ['joy', 'happiness']:
                    emotion_scores['joy'] += min(match_count * 0.2, 0.4)
                elif emotion_type in ['anger', 'frustration']:
                    emotion_scores['anger'] += min(match_count * 0.2, 0.4)
                elif emotion_type in ['fear', 'anxiety']:
                    emotion_scores['fear'] += min(match_count * 0.2, 0.4)
                else:
                    emotion_scores['interest'] += min(match_count * 0.1, 0.3)
        
        # Check engagement triggers (increase interest/excitement)
        engagement_match = sum(1 for trigger in engagement_triggers if trigger.lower() in content_text)
        if engagement_match > 0:
            emotion_scores['interest'] += min(engagement_match * 0.15, 0.4)
            emotion_scores['excitement'] += min(engagement_match * 0.1, 0.3)
        
        # Check friction triggers (increase skepticism/anger)
        friction_match = sum(1 for trigger in friction_triggers if trigger.lower() in content_text)
        if friction_match > 0:
            emotion_scores['skepticism'] += min(friction_match * 0.2, 0.5)
            emotion_scores['anger'] += min(friction_match * 0.15, 0.4)
        
        # Adjust based on sentiment polarity
        if polarity > 0.3:
            # Positive sentiment boosts joy
            emotion_scores['joy'] += 0.3
            emotion_scores['excitement'] += 0.2
        elif polarity < -0.3:
            # Negative sentiment boosts negative emotions
            emotion_scores['anger'] += 0.2
            emotion_scores['skepticism'] += 0.2
        else:
            # Neutral sentiment may lead to indifference
            emotion_scores['indifference'] += 0.2
        
        # Adjust based on persona's personality traits
        # High neuroticism = more intense negative emotions
        if persona.psychographics.neuroticism > 60:
            emotion_scores['fear'] *= 1.2
            emotion_scores['anger'] *= 1.1
        
        # High extraversion = more intense positive emotions
        if persona.psychographics.extraversion > 70:
            emotion_scores['joy'] *= 1.2
            emotion_scores['excitement'] *= 1.2
        
        # Low openness = more skepticism to novel content
        if persona.psychographics.openness < 40:
            emotion_scores['skepticism'] += 0.2
        
        # Normalize scores to 0-1 range
        for emotion in emotion_scores:
            emotion_scores[emotion] = min(emotion_scores[emotion], 1.0)
        
        # If no emotions triggered, default to indifference
        if all(score < 0.1 for score in emotion_scores.values()):
            emotion_scores['indifference'] = 0.6
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0]
        dominant_intensity = emotion_scores[dominant_emotion]
        
        # Calculate overall emotional intensity (0-100)
        # Sum of all emotion scores, normalized
        total_intensity = sum(emotion_scores.values())
        emotional_intensity = min(total_intensity * 40, 100)  # Scale to 0-100
        
        return {
            'predicted_emotions': {k: round(v, 2) for k, v in emotion_scores.items()},
            'dominant_emotion': dominant_emotion,
            'emotional_intensity': round(emotional_intensity, 2)
        }
    
    def predict_actions(
        self,
        content_analysis: Dict,
        persona: Persona,
        resonance_score: float
    ) -> Dict:
        """
        Predict behavioral actions (like, share, comment, ignore, report).
        
        Calculates likelihood of specific actions based on resonance score,
        persona engagement style, and content characteristics.
        
        Args:
            content_analysis: Content analysis dictionary
            persona: Persona object
            resonance_score: Pre-calculated resonance score (0-100)
        
        Returns:
            Dictionary containing:
                - predicted_actions: Dict of action -> likelihood (0-1)
                - most_likely_action: Primary predicted action
        
        Requirements: 4.5
        """
        # Initialize action likelihoods
        action_likelihoods = {
            'like': 0.0,
            'share': 0.0,
            'comment': 0.0,
            'ignore': 0.0,
            'report': 0.0
        }
        
        # Base likelihoods on resonance score
        # High resonance = more likely to engage
        resonance_factor = resonance_score / 100
        
        # Get persona's engagement style
        engagement_style = persona.media_behavior.engagement_style
        sharing_propensity = persona.media_behavior.sharing_propensity
        comment_likelihood = persona.media_behavior.comment_likelihood
        
        # Get content characteristics
        content_text = content_analysis.get('cleaned_text', '').lower()
        sentiment = content_analysis.get('sentiment', {})
        polarity = sentiment.get('polarity', 0.0)
        
        # Get persona triggers
        share_triggers = persona.behavioral_triggers.share_triggers
        engagement_triggers = persona.behavioral_triggers.engagement_triggers
        friction_triggers = persona.behavioral_triggers.friction_triggers
        ignore_triggers = persona.behavioral_triggers.ignore_triggers
        report_triggers = persona.behavioral_triggers.report_triggers
        
        # Calculate LIKE likelihood
        # Base on resonance and engagement style
        if engagement_style == 'passive':
            action_likelihoods['like'] = resonance_factor * 0.3
        elif engagement_style == 'reactive':
            action_likelihoods['like'] = resonance_factor * 0.6
        elif engagement_style == 'proactive':
            action_likelihoods['like'] = resonance_factor * 0.8
        elif engagement_style == 'creator':
            action_likelihoods['like'] = resonance_factor * 0.7
        
        # Positive sentiment increases like likelihood
        if polarity > 0.3:
            action_likelihoods['like'] += 0.1
        
        # Calculate SHARE likelihood
        # Base on sharing propensity and share triggers
        share_base = {
            'never': 0.05,
            'selective': 0.3,
            'frequent': 0.6,
            'viral': 0.8
        }.get(sharing_propensity, 0.3)
        
        action_likelihoods['share'] = share_base * resonance_factor
        
        # Check for share triggers in content
        share_trigger_matches = sum(1 for trigger in share_triggers if trigger.lower() in content_text)
        if share_trigger_matches > 0:
            action_likelihoods['share'] += min(share_trigger_matches * 0.1, 0.3)
        
        # Calculate COMMENT likelihood
        # Base on comment likelihood and engagement style
        comment_base = {
            'never': 0.02,
            'rare': 0.15,
            'sometimes': 0.4,
            'often': 0.7
        }.get(comment_likelihood, 0.2)
        
        action_likelihoods['comment'] = comment_base * resonance_factor
        
        # Proactive and creator personas comment more
        if engagement_style in ['proactive', 'creator']:
            action_likelihoods['comment'] += 0.15
        
        # Calculate IGNORE likelihood
        # Inverse of resonance
        action_likelihoods['ignore'] = 1.0 - resonance_factor
        
        # Check for ignore triggers
        ignore_trigger_matches = sum(1 for trigger in ignore_triggers if trigger.lower() in content_text)
        if ignore_trigger_matches > 0:
            action_likelihoods['ignore'] += min(ignore_trigger_matches * 0.15, 0.4)
        
        # Passive personas ignore more
        if engagement_style == 'passive':
            action_likelihoods['ignore'] += 0.2
        
        # Calculate REPORT likelihood
        # Generally low, but increases with friction triggers
        action_likelihoods['report'] = 0.02
        
        # Check for report triggers (offensive content)
        report_trigger_matches = sum(1 for trigger in report_triggers if trigger.lower() in content_text)
        if report_trigger_matches > 0:
            action_likelihoods['report'] += min(report_trigger_matches * 0.2, 0.6)
        
        # High SCS score increases report likelihood
        scs_score = content_analysis.get('scs_score', 0.0)
        if scs_score > 60:
            action_likelihoods['report'] += 0.2
        
        # Traditional/sensitive personas more likely to report
        if persona.cultural_profile.traditionalism > 70:
            action_likelihoods['report'] *= 1.5
        
        # Normalize all likelihoods to 0-1 range
        for action in action_likelihoods:
            action_likelihoods[action] = min(max(action_likelihoods[action], 0.0), 1.0)
        
        # Ensure ignore and engagement actions are somewhat mutually exclusive
        # If engagement is high, reduce ignore
        engagement_total = action_likelihoods['like'] + action_likelihoods['share'] + action_likelihoods['comment']
        if engagement_total > 0.5:
            action_likelihoods['ignore'] *= 0.5
        
        # Find most likely action
        most_likely_action = max(action_likelihoods.items(), key=lambda x: x[1])[0]
        
        return {
            'predicted_actions': {k: round(v, 2) for k, v in action_likelihoods.items()},
            'most_likely_action': most_likely_action
        }
