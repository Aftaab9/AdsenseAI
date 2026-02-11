# AdsenseAI Campaign Risk Analyzer - Cultural Sensitivity Detector Module
# Detects cultural triggers and festival proximity for Indian market

import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from app.data.data_loader import get_data_loader


class CulturalSensitivityDetector:
    """
    Cultural sensitivity detector for Indian market.
    Detects cultural triggers and checks festival proximity.
    """
    
    def __init__(self):
        """Initialize the cultural sensitivity detector"""
        self.data_loader = get_data_loader()
        self._cultural_triggers = None
        self._festival_calendar = None
        
        # CRITICAL FIX 1: Compound pattern detection for harmful framing
        # Detects combinations of triggers + amplifiers + solutions that compound harm
        self.HARMFUL_PATTERNS = {
            'colorism_discrimination': {
                'primary': ['dark skin', 'dusky', 'wheatish', 'kaali', 'dark complexion'],
                'amplifiers': ['hold back', 'hold you back', 'problem', 'barrier', 'obstacle', 
                              'job', 'career', 'marriage', 'success', 'confidence'],
                'solutions': ['fairness', 'whitening', 'brightening', 'lighter', 'fair skin',
                             'serum', 'cream', 'treatment'],
                'multiplier': 2.5,
                'base_score': 40
            },
            'colorism_beauty': {
                'primary': ['fair skin', 'gori', 'white', 'light skin', 'pale'],
                'amplifiers': ['beautiful', 'pretty', 'attractive', 'gorgeous', 'stunning',
                              'desirable', 'perfect'],
                'solutions': ['cream', 'serum', 'treatment', 'product'],
                'multiplier': 2.0,
                'base_score': 35
            },
            'body_shaming': {
                'primary': ['fat', 'thin', 'skinny', 'overweight', 'underweight', 'body'],
                'amplifiers': ['problem', 'ugly', 'shame', 'embarrass', 'unattractive',
                              'disgusting', 'gross'],
                'solutions': ['lose weight', 'gain weight', 'slim', 'diet', 'transform'],
                'multiplier': 2.0,
                'base_score': 30
            }
        }
    
    def _load_data(self):
        """Load cultural triggers and festival calendar if not already loaded"""
        if self._cultural_triggers is None:
            self._cultural_triggers = self.data_loader.load_cultural_triggers()
        if self._festival_calendar is None:
            self._festival_calendar = self.data_loader.load_festival_calendar()
    
    def detect_compound_patterns(self, text: str) -> List[Dict]:
        """
        CRITICAL FIX 1: Detect compound harmful patterns.
        
        Identifies combinations of primary triggers + amplifiers + solutions
        that compound harm (e.g., colorism discrimination).
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of detected compound pattern dictionaries
        """
        if not text or not text.strip():
            return []
        
        text_lower = text.lower()
        detected_patterns = []
        
        for pattern_name, pattern_def in self.HARMFUL_PATTERNS.items():
            # Check for primary trigger
            primary_found = any(
                primary in text_lower 
                for primary in pattern_def['primary']
            )
            
            if not primary_found:
                continue
            
            # Check for amplifiers
            amplifiers_found = [
                amp for amp in pattern_def['amplifiers']
                if amp in text_lower
            ]
            
            # Check for solutions
            solutions_found = [
                sol for sol in pattern_def['solutions']
                if sol in text_lower
            ]
            
            # Compound pattern detected if primary + (amplifiers OR solutions)
            if amplifiers_found or solutions_found:
                # Calculate compound risk
                base_score = pattern_def['base_score']
                multiplier = pattern_def['multiplier']
                
                # More amplifiers/solutions = higher risk
                compound_factor = len(amplifiers_found) + len(solutions_found)
                compound_score = base_score * multiplier * min(compound_factor, 2)
                
                detected_patterns.append({
                    'pattern_type': pattern_name,
                    'keyword': pattern_name.replace('_', ' ').title(),
                    'category': 'Compound Pattern',
                    'severity': 'critical',
                    'risk_weight': int(compound_score),
                    'message': f"Harmful compound pattern detected: {pattern_name.replace('_', ' ')}",
                    'source': 'compound_detection',
                    'amplifiers': amplifiers_found,
                    'solutions': solutions_found,
                    'multiplier': multiplier
                })
        
        return detected_patterns
    
    def detect_triggers(self, text: str, image_analysis: Optional[Dict] = None) -> List[Dict]:
        """
        Detect cultural triggers in text and optionally image analysis results.
        
        Args:
            text: Text content to analyze
            image_analysis: Optional image analysis results from Gemini API
            
        Returns:
            List of detected trigger dictionaries with details
            
        Requirements: 3.1, 3.2
        """
        self._load_data()
        
        if not text or not text.strip():
            return []
        
        detected_triggers = []
        text_lower = text.lower()
        
        # CRITICAL FIX 1: Check compound patterns FIRST (highest priority)
        compound_patterns = self.detect_compound_patterns(text)
        detected_triggers.extend(compound_patterns)
        
        # Check each cultural trigger
        for trigger in self._cultural_triggers:
            keyword = trigger.get('keyword', '').lower()
            
            # Use word boundary matching to avoid partial matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            
            if re.search(pattern, text_lower):
                detected_triggers.append({
                    'keyword': trigger.get('keyword', ''),
                    'category': trigger.get('category', ''),
                    'severity': trigger.get('severity', ''),
                    'risk_weight': trigger.get('risk_weight', 0),
                    'message': trigger.get('alert_message', ''),
                    'source': 'text'
                })
        
        # Check image analysis for visual triggers if provided
        if image_analysis:
            sensitivity_flags = image_analysis.get('sensitivity_flags', [])
            for flag in sensitivity_flags:
                # Add visual triggers with appropriate risk weights
                detected_triggers.append({
                    'keyword': flag.get('element', 'visual_element'),
                    'category': flag.get('category', 'Visual'),
                    'severity': flag.get('severity', 'medium'),
                    'risk_weight': self._get_visual_risk_weight(flag.get('severity', 'medium')),
                    'message': flag.get('message', 'Visual sensitivity detected'),
                    'source': 'image'
                })
        
        return detected_triggers
    
    def _get_visual_risk_weight(self, severity: str) -> int:
        """
        Get risk weight for visual triggers based on severity
        
        Args:
            severity: Severity level (critical, high, medium, low)
            
        Returns:
            Risk weight integer
        """
        severity_weights = {
            'critical': 40,
            'high': 30,
            'medium': 20,
            'low': 10
        }
        return severity_weights.get(severity.lower(), 15)
    
    def check_festival_proximity(self, posting_date: str, content: str) -> List[Dict]:
        """
        Check if posting date is near sensitive festivals and if content
        conflicts with festival sensitivities.
        
        Args:
            posting_date: Posting date in YYYY-MM-DD format
            content: Text content to check for keyword conflicts
            
        Returns:
            List of festival proximity alerts
            
        Requirements: 3.3
        """
        self._load_data()
        
        if not posting_date or not content:
            return []
        
        try:
            # Parse posting date
            post_date = datetime.strptime(posting_date, '%Y-%m-%d')
        except (ValueError, TypeError):
            # Invalid date format
            return []
        
        alerts = []
        content_lower = content.lower()
        
        # Check each festival
        for festival in self._festival_calendar:
            try:
                # Parse festival date
                festival_date_str = festival.get('date_2025', '')
                festival_date = datetime.strptime(festival_date_str, '%Y-%m-%d')
                
                # Calculate days difference
                days_diff = abs((festival_date - post_date).days)
                
                # Alert if within 7 days
                if days_diff <= 7:
                    festival_name = festival.get('festival_name', '')
                    sensitivity_keywords = festival.get('sensitivity_keywords', [])
                    
                    # Check if content contains conflicting keywords
                    conflicts = []
                    for keyword in sensitivity_keywords:
                        if keyword.lower() in content_lower:
                            conflicts.append(keyword)
                    
                    # ONLY add alert if there are actual conflicts
                    # Festival proximity without conflicts is not a risk
                    if conflicts:
                        # Determine severity based on proximity
                        severity = 'critical' if days_diff <= 3 else 'high'
                        risk_weight = 35 if days_diff <= 3 else 25
                        
                        alert = {
                            'festival': festival_name,
                            'festival_date': festival_date_str,
                            'days_away': days_diff,
                            'severity': severity,
                            'risk_weight': risk_weight,
                            'conflicts': conflicts,
                            'message': self._generate_festival_message(
                                festival_name, days_diff, conflicts
                            ),
                            'description': festival.get('description', '')
                        }
                        
                        alerts.append(alert)
                    
            except (ValueError, TypeError, KeyError):
                # Skip festivals with invalid dates
                continue
        
        return alerts
    
    def _generate_festival_message(self, festival_name: str, days_away: int, 
                                   conflicts: List[str]) -> str:
        """
        Generate appropriate festival proximity message
        
        Args:
            festival_name: Name of the festival
            days_away: Days until/since festival
            conflicts: List of conflicting keywords
            
        Returns:
            Alert message string
        """
        if conflicts:
            conflict_str = ', '.join(conflicts)
            return (f"Posting near {festival_name} ({days_away} days away) with "
                   f"potentially sensitive content: {conflict_str}")
        else:
            return (f"Posting near {festival_name} ({days_away} days away). "
                   f"Ensure messaging is appropriate and respectful.")
    
    def calculate_scs_score(self, text: str, posting_date: Optional[str] = None,
                           image_analysis: Optional[Dict] = None) -> Dict:
        """
        Calculate Socio-Cultural Sensitivity (SCS) score.
        
        Aggregates trigger risk weights, festival proximity penalties,
        and norm violation indicators.
        
        Args:
            text: Text content to analyze
            posting_date: Optional posting date for festival proximity check
            image_analysis: Optional image analysis results
            
        Returns:
            Dictionary containing SCS score and component breakdowns
            
        Requirements: 3.4, 3.5
        """
        if not text or not text.strip():
            return {
                'scs_score': 0.0,
                'triggers_found': 0,
                'festival_alerts': 0,
                'total_risk_weight': 0,
                'detected_triggers': [],
                'festival_proximity': [],
                'severity_breakdown': {
                    'critical': 0,
                    'high': 0,
                    'medium': 0,
                    'low': 0
                }
            }
        
        # Detect cultural triggers
        detected_triggers = self.detect_triggers(text, image_analysis)
        
        # Check festival proximity if date provided
        festival_alerts = []
        if posting_date:
            festival_alerts = self.check_festival_proximity(posting_date, text)
        
        # Calculate total risk weight from triggers
        trigger_risk = sum(trigger.get('risk_weight', 0) for trigger in detected_triggers)
        
        # Calculate festival proximity penalty
        festival_risk = sum(alert.get('risk_weight', 0) for alert in festival_alerts)
        
        # Count norm violations (critical and high severity triggers)
        norm_violations = sum(
            1 for trigger in detected_triggers
            if trigger.get('severity', '').lower() in ['critical', 'high']
        )
        norm_violations += sum(
            1 for alert in festival_alerts
            if alert.get('severity', '').lower() in ['critical', 'high']
        )
        
        # Norm violation penalty
        norm_violation_penalty = norm_violations * 10
        
        # Calculate total SCS score (0-100)
        scs_score = trigger_risk + festival_risk + norm_violation_penalty
        scs_score = min(scs_score, 100)  # Cap at 100
        
        # Count severity breakdown
        severity_breakdown = {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
        
        for trigger in detected_triggers:
            severity = trigger.get('severity', '').lower()
            if severity in severity_breakdown:
                severity_breakdown[severity] += 1
        
        for alert in festival_alerts:
            severity = alert.get('severity', '').lower()
            if severity in severity_breakdown:
                severity_breakdown[severity] += 1
        
        return {
            'scs_score': round(scs_score, 2),
            'triggers_found': len(detected_triggers),
            'festival_alerts': len(festival_alerts),
            'total_risk_weight': trigger_risk + festival_risk,
            'norm_violations': norm_violations,
            'detected_triggers': detected_triggers,
            'festival_proximity': festival_alerts,
            'severity_breakdown': severity_breakdown
        }
    
    def get_all_triggers(self) -> List[Dict]:
        """
        Get all available cultural triggers
        
        Returns:
            List of all cultural trigger dictionaries
        """
        self._load_data()
        return self._cultural_triggers
    
    def get_all_festivals(self) -> List[Dict]:
        """
        Get all festivals in calendar
        
        Returns:
            List of all festival dictionaries
        """
        self._load_data()
        return self._festival_calendar
    
    def get_triggers_by_category(self, category: str) -> List[Dict]:
        """
        Get cultural triggers by category
        
        Args:
            category: Category name (Religious, Colorism, Geopolitical, etc.)
            
        Returns:
            List of triggers in the category
        """
        self._load_data()
        category_lower = category.lower()
        
        return [
            trigger for trigger in self._cultural_triggers
            if trigger.get('category', '').lower() == category_lower
        ]
