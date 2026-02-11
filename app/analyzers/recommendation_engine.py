# AdsenseAI Campaign Risk Analyzer - Recommendation Engine Module
# Generates actionable Go/Caution/Stop recommendations based on risk analysis

from typing import Dict, List, Optional


class RecommendationEngine:
    """
    Generates actionable recommendations for campaign content based on comprehensive risk analysis.
    
    Recommendation levels:
    - GO (Green): Low risk, high potential - safe to post
    - CAUTION (Yellow): Moderate risk - review and revise recommended
    - STOP (Red): High risk - do not post without major revisions
    
    Based on requirements 8.1, 8.2, 8.3, 8.4, 8.5
    """
    
    def __init__(self, data_loader=None):
        """
        Initialize the recommendation engine
        
        Args:
            data_loader: DataLoader instance for accessing historical campaigns
        """
        self.data_loader = data_loader
    
    def generate_recommendation(self, virality_score: float, backlash_risk: float,
                               cultural_alerts: List[Dict], perceived_intent: float,
                               tpb_scores: Dict, sentiment: Dict,
                               platform: str = None) -> Dict:
        """
        Generate comprehensive recommendation with decision logic, reasoning, and suggestions.
        
        Decision Logic:
        - STOP: backlash >= 70 OR critical alerts OR intent < -50
        - CAUTION: backlash 40-69 OR any alerts OR intent -50 to 0
        - GO: backlash < 40 AND no alerts AND virality >= 60
        
        Args:
            virality_score: Virality prediction (0-100)
            backlash_risk: Backlash risk score (0-100)
            cultural_alerts: List of cultural alert dictionaries
            perceived_intent: Perceived intent score (-100 to +100)
            tpb_scores: TPB framework scores dictionary
            sentiment: Sentiment analysis dictionary
            platform: Social media platform name (optional, for historical matching)
            
        Returns:
            Dictionary containing recommendation status, action, message, reasoning, and suggestions
            
        Requirements: 8.1, 8.2, 8.3, 8.4
        """
        # Determine recommendation status using decision logic
        status, action = self._determine_status(backlash_risk, cultural_alerts, 
                                                perceived_intent, virality_score)
        
        # Generate reasoning based on analysis results
        reasoning = self._generate_reasoning(status, virality_score, backlash_risk,
                                            cultural_alerts, perceived_intent, 
                                            tpb_scores, sentiment)
        
        # Generate suggestions for improvement (especially for STOP/CAUTION)
        suggestions = self._generate_suggestions(status, backlash_risk, cultural_alerts,
                                                perceived_intent, sentiment, tpb_scores)
        
        # Generate main recommendation message
        message = self._generate_message(status, virality_score, backlash_risk)
        
        # Get similar historical campaigns if platform provided
        similar_campaigns = []
        if platform and self.data_loader:
            similar_campaigns = self._find_similar_campaigns(platform, backlash_risk, virality_score)
        
        return {
            'status': status,
            'action': action,
            'message': message,
            'reasoning': reasoning,
            'suggestions': suggestions,
            'similar_campaigns': similar_campaigns
        }
    
    def _determine_status(self, backlash_risk: float, cultural_alerts: List[Dict],
                         perceived_intent: float, virality_score: float) -> tuple:
        """
        Determine recommendation status using decision logic.
        
        Decision Logic (IMPROVED):
        - STOP: backlash >= 70 OR critical alerts OR intent < -50
        - CAUTION: backlash 35-69 OR high alerts OR intent -50 to 20 OR (low virality AND alerts)
        - GO: backlash < 35 AND (no critical/high alerts) AND (virality >= 55 OR no alerts)
        
        Args:
            backlash_risk: Backlash risk score (0-100)
            cultural_alerts: List of cultural alert dictionaries
            perceived_intent: Perceived intent score (-100 to +100)
            virality_score: Virality prediction (0-100)
            
        Returns:
            Tuple of (status, action) strings
            
        Requirements: 8.1, 8.2, 8.3
        """
        # Check for critical and high severity alerts
        has_critical_alerts = any(
            alert.get('severity', '').lower() == 'critical' 
            for alert in cultural_alerts
        )
        
        has_high_alerts = any(
            alert.get('severity', '').lower() == 'high' 
            for alert in cultural_alerts
        )
        
        # STOP conditions (more strict for critical issues)
        if backlash_risk >= 70:
            return ('stop', 'Do Not Post')
        
        if has_critical_alerts:
            return ('stop', 'Do Not Post')
        
        if perceived_intent < -50:
            return ('stop', 'Do Not Post')
        
        # CAUTION conditions (adjusted thresholds)
        if 35 <= backlash_risk < 70:
            return ('caution', 'Review Required')
        
        if has_high_alerts:
            return ('caution', 'Review Required')
        
        if -50 <= perceived_intent < 20:  # Expanded range
            return ('caution', 'Review Required')
        
        # Low virality with any alerts = caution
        if virality_score < 55 and len(cultural_alerts) > 0:
            return ('caution', 'Review Required')
        
        # GO conditions (more lenient for good content)
        # High virality + low backlash = strong GO signal
        if virality_score >= 70 and backlash_risk < 25:
            return ('go', 'Excellent - Post Now!')
        
        if virality_score >= 55 and backlash_risk < 35:
            return ('go', 'Good to Post')
        
        # Low backlash with no serious alerts = GO
        if backlash_risk < 35 and not has_critical_alerts and not has_high_alerts:
            return ('go', 'Safe to Post')
        
        # Default to caution if unclear
        return ('caution', 'Review Required')
    
    def _generate_reasoning(self, status: str, virality_score: float, 
                           backlash_risk: float, cultural_alerts: List[Dict],
                           perceived_intent: float, tpb_scores: Dict,
                           sentiment: Dict) -> List[str]:
        """
        Generate specific reasoning for the recommendation based on analysis results.
        
        Args:
            status: Recommendation status (go, caution, stop)
            virality_score: Virality prediction (0-100)
            backlash_risk: Backlash risk score (0-100)
            cultural_alerts: List of cultural alert dictionaries
            perceived_intent: Perceived intent score (-100 to +100)
            tpb_scores: TPB framework scores dictionary
            sentiment: Sentiment analysis dictionary
            
        Returns:
            List of reasoning strings
            
        Requirements: 8.4
        """
        reasoning = []
        
        # TPB behavioral intention reasoning
        behavioral_intention = tpb_scores.get('behavioral_intention', 0)
        if behavioral_intention >= 75:
            reasoning.append(f"High TPB behavioral intention ({behavioral_intention:.0f}%) indicates strong sharing likelihood")
        elif behavioral_intention >= 50:
            reasoning.append(f"Moderate TPB behavioral intention ({behavioral_intention:.0f}%) suggests decent engagement potential")
        elif behavioral_intention < 40:
            reasoning.append(f"Low TPB behavioral intention ({behavioral_intention:.0f}%) indicates limited engagement potential")
        
        # Perceived intent reasoning
        if perceived_intent >= 50:
            reasoning.append(f"Positive perceived intent ({perceived_intent:.0f}) suggests authentic messaging")
        elif perceived_intent >= 0:
            reasoning.append(f"Neutral perceived intent ({perceived_intent:.0f}) - content may lack clear authenticity signals")
        elif perceived_intent >= -50:
            reasoning.append(f"Negative perceived intent ({perceived_intent:.0f}) - risk of being perceived as manipulative")
        else:
            reasoning.append(f"Highly negative perceived intent ({perceived_intent:.0f}) - likely to be seen as manipulative")
        
        # Cultural sensitivity reasoning
        if len(cultural_alerts) == 0:
            reasoning.append("No cultural sensitivity issues detected")
        else:
            critical_count = sum(1 for a in cultural_alerts if a.get('severity') == 'critical')
            high_count = sum(1 for a in cultural_alerts if a.get('severity') == 'high')
            
            if critical_count > 0:
                reasoning.append(f"{critical_count} critical cultural sensitivity alert(s) detected")
            if high_count > 0:
                reasoning.append(f"{high_count} high-severity cultural sensitivity alert(s) detected")
            
            if critical_count == 0 and high_count == 0:
                reasoning.append(f"{len(cultural_alerts)} cultural sensitivity alert(s) detected (medium/low severity)")
        
        # Virality reasoning
        if virality_score >= 75:
            reasoning.append(f"Very high virality potential ({virality_score:.0f}%)")
        elif virality_score >= 60:
            reasoning.append(f"High virality potential ({virality_score:.0f}%)")
        elif virality_score < 40:
            reasoning.append(f"Limited virality potential ({virality_score:.0f}%)")
        
        # Backlash reasoning
        if backlash_risk >= 70:
            reasoning.append(f"Critical backlash risk ({backlash_risk:.0f}%) - high likelihood of negative reaction")
        elif backlash_risk >= 50:
            reasoning.append(f"High backlash risk ({backlash_risk:.0f}%) - significant risk of negative reaction")
        elif backlash_risk >= 30:
            reasoning.append(f"Moderate backlash risk ({backlash_risk:.0f}%)")
        else:
            reasoning.append(f"Low backlash risk ({backlash_risk:.0f}%)")
        
        # Sentiment reasoning
        polarity = sentiment.get('polarity', 0)
        if polarity > 0.5:
            reasoning.append("Strong positive sentiment detected")
        elif polarity < -0.3:
            reasoning.append("Negative sentiment detected - may trigger backlash")
        
        return reasoning
    
    def _generate_suggestions(self, status: str, backlash_risk: float,
                             cultural_alerts: List[Dict], perceived_intent: float,
                             sentiment: Dict, tpb_scores: Dict) -> List[str]:
        """
        Generate content revision suggestions for STOP/CAUTION cases.
        
        Args:
            status: Recommendation status (go, caution, stop)
            backlash_risk: Backlash risk score (0-100)
            cultural_alerts: List of cultural alert dictionaries
            perceived_intent: Perceived intent score (-100 to +100)
            sentiment: Sentiment analysis dictionary
            tpb_scores: TPB framework scores dictionary
            
        Returns:
            List of suggestion strings
            
        Requirements: 8.4
        """
        suggestions = []
        
        # Only provide suggestions for STOP and CAUTION
        if status == 'go':
            return suggestions
        
        # Cultural sensitivity suggestions
        if len(cultural_alerts) > 0:
            critical_alerts = [a for a in cultural_alerts if a.get('severity') == 'critical']
            high_alerts = [a for a in cultural_alerts if a.get('severity') == 'high']
            
            if critical_alerts:
                keywords = [a.get('keyword', '') for a in critical_alerts]
                suggestions.append(f"Remove or rephrase critical triggers: {', '.join(keywords)}")
            
            if high_alerts:
                keywords = [a.get('keyword', '') for a in high_alerts]
                suggestions.append(f"Consider revising high-risk references: {', '.join(keywords)}")
            
            # Category-specific suggestions
            categories = set(a.get('category', '') for a in cultural_alerts)
            if 'Religious' in categories:
                suggestions.append("Avoid religious references or ensure they are respectful and inclusive")
            if 'Colorism' in categories:
                suggestions.append("Remove skin tone references and focus on inclusive beauty standards")
            if 'Geopolitical' in categories:
                suggestions.append("Avoid geopolitical topics that may polarize audiences")
        
        # Perceived intent suggestions
        if perceived_intent < 0:
            suggestions.append("Increase authenticity by adding genuine storytelling or user testimonials")
            suggestions.append("Reduce promotional language and focus on value-driven messaging")
        
        # Sentiment suggestions
        polarity = sentiment.get('polarity', 0)
        subjectivity = sentiment.get('subjectivity', 0)
        
        if polarity < 0:
            suggestions.append("Reframe negative messaging with positive or solution-oriented language")
        
        if subjectivity > 0.7:
            suggestions.append("Balance subjective claims with objective facts or data")
        
        # TPB-based suggestions
        attitude = tpb_scores.get('attitude', 0)
        if attitude < 50:
            suggestions.append("Enhance emotional appeal to improve audience attitude toward sharing")
        
        # Backlash-specific suggestions
        if backlash_risk >= 70:
            suggestions.append("Consider major content revision or alternative messaging approach")
            suggestions.append("Test content with focus groups before posting")
        elif backlash_risk >= 50:
            suggestions.append("Review content with cultural sensitivity experts")
        
        return suggestions
    
    def _generate_message(self, status: str, virality_score: float, 
                         backlash_risk: float) -> str:
        """
        Generate main recommendation message.
        
        Args:
            status: Recommendation status (go, caution, stop)
            virality_score: Virality prediction (0-100)
            backlash_risk: Backlash risk score (0-100)
            
        Returns:
            Recommendation message string
            
        Requirements: 8.1, 8.2, 8.3
        """
        if status == 'stop':
            if backlash_risk >= 70:
                return f"Critical backlash risk detected ({backlash_risk:.0f}%). Major content revision required before posting."
            else:
                return "Critical issues detected. Do not post without addressing cultural sensitivity concerns."
        
        elif status == 'caution':
            if backlash_risk >= 50:
                return f"Moderate to high backlash risk ({backlash_risk:.0f}%). Review and revise content before posting."
            else:
                return "Some concerns detected. Review cultural sensitivity alerts and consider revisions."
        
        else:  # go
            if virality_score >= 75:
                return f"Content shows strong viral potential ({virality_score:.0f}%) with minimal risk. Excellent candidate for posting!"
            elif virality_score >= 60:
                return f"Content shows good viral potential ({virality_score:.0f}%) with low risk. Safe to post!"
            else:
                return "Content is safe to post with minimal risk, though viral potential is moderate."
    
    def _find_similar_campaigns(self, platform: str, backlash_risk: float,
                               virality_score: float, limit: int = 3) -> List[Dict]:
        """
        Find similar historical campaigns by platform and outcome.
        
        Matches campaigns based on:
        - Same platform
        - Similar outcome pattern (high virality, high backlash, etc.)
        
        Args:
            platform: Social media platform name
            backlash_risk: Current campaign backlash risk (0-100)
            virality_score: Current campaign virality score (0-100)
            limit: Maximum number of similar campaigns to return
            
        Returns:
            List of similar campaign dictionaries with lessons learned
            
        Requirements: 8.5
        """
        if not self.data_loader:
            return []
        
        try:
            # Get all campaigns for this platform
            platform_campaigns = self.data_loader.get_campaigns_by_platform(platform)
            
            if not platform_campaigns:
                return []
            
            # Determine current campaign outcome pattern
            high_virality = virality_score >= 60
            high_backlash = backlash_risk >= 50
            
            # Score campaigns by similarity
            scored_campaigns = []
            for campaign in platform_campaigns:
                campaign_virality = campaign.get('virality_score', 0)
                campaign_backlash = campaign.get('backlash_occurred', False)
                
                # Calculate similarity score
                similarity = 0
                
                # Match virality pattern
                campaign_high_virality = campaign_virality >= 60
                if campaign_high_virality == high_virality:
                    similarity += 50
                
                # Match backlash pattern
                campaign_high_backlash = campaign_backlash or campaign.get('outcome', '').lower() == 'backlash'
                if campaign_high_backlash == high_backlash:
                    similarity += 50
                
                scored_campaigns.append({
                    'campaign': campaign,
                    'similarity': similarity
                })
            
            # Sort by similarity and take top matches
            scored_campaigns.sort(key=lambda x: x['similarity'], reverse=True)
            top_campaigns = scored_campaigns[:limit]
            
            # Format results
            similar_campaigns = []
            for item in top_campaigns:
                campaign = item['campaign']
                similar_campaigns.append({
                    'brand': campaign.get('brand', 'Unknown'),
                    'campaign': campaign.get('campaign_name', 'Unknown'),
                    'outcome': campaign.get('outcome', 'Unknown'),
                    'lesson': campaign.get('lessons_learned', 'No lesson available')
                })
            
            return similar_campaigns
            
        except Exception as e:
            # Silently handle errors and return empty list
            return []
