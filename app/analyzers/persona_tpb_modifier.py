# AdsenseAI Campaign Risk Analyzer - Persona-Specific TPB Modifier
# Modifies Theory of Planned Behaviour (TPB) scores based on persona characteristics
# Requirements: 12.1-12.3

from typing import Dict, List
from app.models import Persona


class PersonaTPBModifier:
    """
    Modifies TPB (Theory of Planned Behaviour) scores based on persona characteristics.
    
    This class takes base TPB scores calculated from content analysis and adjusts them
    based on a specific persona's:
    - Values and psychographic profile (affects attitude)
    - Social factors and cultural profile (affects subjective norms)
    - Digital behavior and platform preferences (affects perceived control)
    
    The modified scores provide persona-specific predictions of behavioral intention.
    
    Requirements: 12.1, 12.2, 12.3
    """
    
    def __init__(self):
        """Initialize the PersonaTPBModifier"""
        pass
    
    def modify_tpb_for_persona(
        self,
        base_tpb: Dict,
        persona: Persona,
        content_analysis: Dict
    ) -> Dict:
        """
        Modify base TPB scores based on persona characteristics.
        
        Takes the base TPB scores (calculated from content alone) and adjusts them
        based on how this specific persona would respond to the content.
        
        Args:
            base_tpb: Base TPB scores from TPBCalculator
                {
                    'attitude': float,
                    'subjective_norms': float,
                    'perceived_control': float,
                    'behavioral_intention': float
                }
            persona: Persona object with demographic, psychographic, and behavioral data
            content_analysis: Content analysis results including emotions, sentiment, topics
        
        Returns:
            Dictionary with persona-modified TPB scores:
            {
                'attitude': float,
                'subjective_norms': float,
                'perceived_control': float,
                'behavioral_intention': float,
                'attitude_modifier': float,
                'norms_modifier': float,
                'control_modifier': float,
                'modifications_applied': List[str]
            }
        
        Requirements: 12.1, 12.2
        """
        # Extract base scores
        base_attitude = base_tpb.get('attitude', 50.0)
        base_norms = base_tpb.get('subjective_norms', 50.0)
        base_control = base_tpb.get('perceived_control', 50.0)
        
        # Calculate persona-specific modifiers
        attitude_modifier = self._calculate_attitude_modifier(
            persona, content_analysis
        )
        norms_modifier = self._calculate_norms_modifier(
            persona, content_analysis
        )
        control_modifier = self._calculate_control_modifier(
            persona, content_analysis
        )
        
        # Apply modifiers to base scores
        modified_attitude = self._apply_modifier(base_attitude, attitude_modifier)
        modified_norms = self._apply_modifier(base_norms, norms_modifier)
        modified_control = self._apply_modifier(base_control, control_modifier)
        
        # Recalculate behavioral intention with modified scores
        # Using same weights as TPBCalculator: Attitude 40%, Norms 35%, Control 25%
        modified_intention = (
            modified_attitude * 0.40 +
            modified_norms * 0.35 +
            modified_control * 0.25
        )
        modified_intention = min(max(modified_intention, 0), 100)
        
        # Track which modifications were applied
        modifications_applied = []
        if abs(attitude_modifier) > 0.05:
            modifications_applied.append(f"Attitude: {attitude_modifier:+.2f}")
        if abs(norms_modifier) > 0.05:
            modifications_applied.append(f"Norms: {norms_modifier:+.2f}")
        if abs(control_modifier) > 0.05:
            modifications_applied.append(f"Control: {control_modifier:+.2f}")
        
        return {
            'attitude': round(modified_attitude, 2),
            'subjective_norms': round(modified_norms, 2),
            'perceived_control': round(modified_control, 2),
            'behavioral_intention': round(modified_intention, 2),
            'attitude_modifier': round(attitude_modifier, 2),
            'norms_modifier': round(norms_modifier, 2),
            'control_modifier': round(control_modifier, 2),
            'modifications_applied': modifications_applied,
            'base_attitude': base_attitude,
            'base_norms': base_norms,
            'base_control': base_control,
            'base_intention': base_tpb.get('behavioral_intention', 50.0)
        }
    
    def _calculate_attitude_modifier(
        self,
        persona: Persona,
        content_analysis: Dict
    ) -> float:
        """
        Calculate attitude modifier based on persona values and psychographics.
        
        Attitude is influenced by:
        - Value alignment: Does content align with persona's core values?
        - Personality traits (OCEAN): How does personality affect content reception?
        - Interests: Is content relevant to persona's interests?
        
        Returns modifier in range -0.5 to +0.5 (multiplier for base attitude)
        
        Requirements: 12.1
        """
        modifier = 0.0
        
        # 1. Value Alignment Modifier (-0.2 to +0.2)
        # Check if content values align with persona values
        content_values = content_analysis.get('detected_values', [])
        persona_values = persona.psychographics.core_values
        
        if content_values and persona_values:
            # Calculate overlap
            matching_values = set(content_values) & set(persona_values)
            if matching_values:
                # Positive modifier for value alignment
                alignment_strength = len(matching_values) / max(len(persona_values), 1)
                modifier += alignment_strength * 0.2
            else:
                # Check for value conflicts
                conflicting_pairs = [
                    ({'tradition', 'family'}, {'freedom', 'independence'}),
                    ({'success', 'achievement'}, {'community', 'collective'}),
                    ({'innovation', 'change'}, {'stability', 'tradition'})
                ]
                for persona_set, content_set in conflicting_pairs:
                    if any(v in persona_values for v in persona_set) and \
                       any(v in content_values for v in content_set):
                        modifier -= 0.15
                        break
        
        # 2. Personality (OCEAN) Modifier (-0.15 to +0.15)
        # High openness: More receptive to creative/novel content
        if content_analysis.get('is_creative', False) or content_analysis.get('is_novel', False):
            openness_factor = (persona.psychographics.openness - 50) / 100
            modifier += openness_factor * 0.15
        
        # High conscientiousness: Prefer factual/detailed content
        if content_analysis.get('is_detailed', False) or content_analysis.get('has_facts', False):
            conscientiousness_factor = (persona.psychographics.conscientiousness - 50) / 100
            modifier += conscientiousness_factor * 0.1
        
        # High extraversion: Respond to social/energetic content
        if content_analysis.get('is_social', False) or content_analysis.get('is_energetic', False):
            extraversion_factor = (persona.psychographics.extraversion - 50) / 100
            modifier += extraversion_factor * 0.1
        
        # 3. Interest Relevance Modifier (-0.15 to +0.15)
        content_topics = content_analysis.get('topics', [])
        persona_interests = persona.psychographics.interests
        
        if content_topics and persona_interests:
            matching_interests = set(content_topics) & set(persona_interests)
            if matching_interests:
                interest_strength = len(matching_interests) / max(len(persona_interests), 1)
                modifier += interest_strength * 0.15
            elif len(set(content_topics) & set(persona.behavioral_triggers.ignore_triggers)) > 0:
                # Content matches ignore triggers
                modifier -= 0.15
        
        # Clamp modifier to -0.5 to +0.5
        return max(min(modifier, 0.5), -0.5)
    
    def _calculate_norms_modifier(
        self,
        persona: Persona,
        content_analysis: Dict
    ) -> float:
        """
        Calculate subjective norms modifier based on persona social factors.
        
        Subjective norms are influenced by:
        - Cultural profile: Collectivism, family orientation, status consciousness
        - Social behavior: Sharing propensity, engagement style
        - Platform affinity: How much persona uses the target platform
        
        Returns modifier in range -0.5 to +0.5 (multiplier for base norms)
        
        Requirements: 12.2
        """
        modifier = 0.0
        
        # 1. Cultural Collectivism Modifier (-0.2 to +0.2)
        # Low individualism (high collectivism) = stronger social norms
        collectivism_score = 100 - persona.cultural_profile.individualism
        if collectivism_score > 60:
            # Collectivist personas feel stronger social pressure
            modifier += 0.2
        elif collectivism_score < 40:
            # Individualist personas feel less social pressure
            modifier -= 0.15
        
        # 2. Family Orientation Modifier (0 to +0.15)
        # High family orientation increases social pressure for family-related content
        content_themes = content_analysis.get('themes', [])
        if 'family' in content_themes or 'relationships' in content_themes:
            if persona.cultural_profile.family_orientation > 70:
                modifier += 0.15
        
        # 3. Status Consciousness Modifier (-0.15 to +0.15)
        # High status consciousness increases social pressure for aspirational content
        if content_analysis.get('is_aspirational', False) or \
           content_analysis.get('is_premium', False):
            status_factor = (persona.cultural_profile.status_consciousness - 50) / 100
            modifier += status_factor * 0.15
        
        # 4. Sharing Propensity Modifier (-0.2 to +0.2)
        sharing_map = {
            'never': -0.2,
            'selective': -0.05,
            'frequent': 0.1,
            'viral': 0.2
        }
        sharing_modifier = sharing_map.get(persona.media_behavior.sharing_propensity, 0)
        modifier += sharing_modifier
        
        # 5. Platform Affinity Modifier (-0.15 to +0.15)
        platform = content_analysis.get('platform', 'instagram').lower()
        platform_affinity = persona.media_behavior.platform_affinity.get(platform, 0.5)
        # Convert 0-1 affinity to -0.15 to +0.15 modifier
        affinity_modifier = (platform_affinity - 0.5) * 0.3
        modifier += affinity_modifier
        
        # Clamp modifier to -0.5 to +0.5
        return max(min(modifier, 0.5), -0.5)
    
    def _calculate_control_modifier(
        self,
        persona: Persona,
        content_analysis: Dict
    ) -> float:
        """
        Calculate perceived control modifier based on persona digital behavior.
        
        Perceived control is influenced by:
        - Digital literacy: Tech adoption level, platform familiarity
        - Engagement style: Active vs passive behavior
        - Ad receptivity: Comfort with branded content
        
        Returns modifier in range -0.3 to +0.3 (multiplier for base control)
        
        Requirements: 12.2
        """
        modifier = 0.0
        
        # 1. Engagement Style Modifier (-0.15 to +0.15)
        # Active engagers feel more control over their actions
        engagement_map = {
            'passive': -0.15,
            'reactive': -0.05,
            'proactive': 0.1,
            'creator': 0.15
        }
        engagement_modifier = engagement_map.get(persona.media_behavior.engagement_style, 0)
        modifier += engagement_modifier
        
        # 2. Ad Receptivity Modifier (-0.15 to +0.1)
        # Ad-averse personas feel less control (defensive)
        # Ad-receptive personas feel more control (comfortable)
        receptivity_map = {
            'ad_blocker': -0.15,
            'tolerant': -0.05,
            'receptive': 0.05,
            'engaged': 0.1
        }
        receptivity_modifier = receptivity_map.get(persona.media_behavior.ad_receptivity, 0)
        modifier += receptivity_modifier
        
        # 3. Platform Familiarity Modifier (0 to +0.1)
        # High platform affinity = more comfortable = more control
        platform = content_analysis.get('platform', 'instagram').lower()
        platform_affinity = persona.media_behavior.platform_affinity.get(platform, 0.5)
        if platform_affinity > 0.7:
            modifier += 0.1
        elif platform_affinity < 0.3:
            modifier -= 0.1
        
        # 4. Content Complexity Modifier (-0.1 to 0)
        # Complex content reduces perceived control for less engaged personas
        if content_analysis.get('is_complex', False):
            if persona.media_behavior.engagement_style in ['passive', 'reactive']:
                modifier -= 0.1
        
        # Clamp modifier to -0.3 to +0.3
        return max(min(modifier, 0.3), -0.3)
    
    def _apply_modifier(self, base_score: float, modifier: float) -> float:
        """
        Apply a modifier to a base score.
        
        Modifier is a multiplier that adjusts the base score:
        - Positive modifier: Increases score
        - Negative modifier: Decreases score
        
        Args:
            base_score: Base score (0-100)
            modifier: Modifier (-0.5 to +0.5)
        
        Returns:
            Modified score (0-100)
        """
        # Apply modifier as a percentage change
        # modifier of 0.2 = 20% increase, -0.2 = 20% decrease
        modified_score = base_score * (1 + modifier)
        
        # Clamp to 0-100 range
        return max(min(modified_score, 100), 0)
