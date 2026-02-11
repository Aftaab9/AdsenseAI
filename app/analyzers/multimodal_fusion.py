# AdsenseAI Campaign Risk Analyzer - Multi-Modal Fusion Module
# Combines text and visual analysis for comprehensive campaign assessment

from typing import Dict, List, Optional


class MultiModalFusion:
    """
    Multi-modal fusion module that combines text and visual analysis.
    
    Implements fusion strategies for:
    - EMC scores (text: 60%, visual: 40%)
    - SCS scores (worst case scenario - maximum)
    - Emotions (union of both modalities)
    
    Requirements: 12.3
    """
    
    def __init__(self):
        """Initialize the multi-modal fusion module"""
        pass
    
    def combine_emc_scores(self, text_emc: float, visual_emc: float) -> Dict:
        """
        Combine text and visual EMC scores using weighted average.
        
        Text analysis gets 60% weight as it's typically more explicit.
        Visual analysis gets 40% weight as it provides contextual cues.
        
        Args:
            text_emc: EMC score from text analysis (0-100)
            visual_emc: EMC score from visual analysis (0-100)
            
        Returns:
            Dictionary with combined EMC score and breakdown
            
        Requirements: 12.3
        """
        # Weighted combination: text 60%, visual 40%
        combined_emc = (text_emc * 0.6) + (visual_emc * 0.4)
        
        return {
            'combined_emc_score': round(combined_emc, 2),
            'text_emc': round(text_emc, 2),
            'visual_emc': round(visual_emc, 2),
            'text_weight': 0.6,
            'visual_weight': 0.4
        }
    
    def combine_scs_scores(self, text_scs: float, visual_scs: float) -> Dict:
        """
        Combine text and visual SCS scores using maximum (worst case).
        
        Takes the maximum score because a single sensitivity issue
        in either modality can trigger backlash. This is a conservative
        approach that prioritizes risk detection.
        
        Args:
            text_scs: SCS score from text analysis (0-100)
            visual_scs: SCS score from visual analysis (0-100)
            
        Returns:
            Dictionary with combined SCS score and breakdown
            
        Requirements: 12.3
        """
        # Take maximum (worst case scenario)
        combined_scs = max(text_scs, visual_scs)
        
        # Determine which modality contributed the higher risk
        primary_source = 'text' if text_scs >= visual_scs else 'visual'
        
        return {
            'combined_scs_score': round(combined_scs, 2),
            'text_scs': round(text_scs, 2),
            'visual_scs': round(visual_scs, 2),
            'fusion_strategy': 'maximum',
            'primary_risk_source': primary_source
        }
    
    def combine_emotions(self, text_emotions: List[str], 
                        visual_emotions: List[str]) -> Dict:
        """
        Combine emotions from text and visual analysis.
        
        Takes the union of emotions from both modalities, as emotions
        can be expressed through either text or visuals. Preserves
        unique emotions and tracks their sources.
        
        Args:
            text_emotions: List of emotions from text analysis
            visual_emotions: List of emotions from visual analysis
            
        Returns:
            Dictionary with combined emotions and source tracking
            
        Requirements: 12.3
        """
        # Create union of emotions (unique emotions from both)
        combined_emotions = list(set(text_emotions + visual_emotions))
        
        # Track which emotions came from which modality
        text_only = [e for e in text_emotions if e not in visual_emotions]
        visual_only = [e for e in visual_emotions if e not in text_emotions]
        both = [e for e in text_emotions if e in visual_emotions]
        
        return {
            'combined_emotions': sorted(combined_emotions),
            'emotion_count': len(combined_emotions),
            'text_emotions': sorted(text_emotions),
            'visual_emotions': sorted(visual_emotions),
            'text_only': sorted(text_only),
            'visual_only': sorted(visual_only),
            'both_modalities': sorted(both),
            'modality_agreement': len(both) / max(len(combined_emotions), 1)
        }
    
    def combine_cultural_symbols(self, text_symbols: List[str],
                                 visual_symbols: List[str]) -> Dict:
        """
        Combine cultural symbols detected in text and visual content.
        
        Args:
            text_symbols: Cultural symbols from text analysis
            visual_symbols: Cultural symbols from visual analysis
            
        Returns:
            Dictionary with combined cultural symbols
        """
        # Union of cultural symbols
        combined_symbols = list(set(text_symbols + visual_symbols))
        
        return {
            'combined_symbols': sorted(combined_symbols),
            'symbol_count': len(combined_symbols),
            'text_symbols': sorted(text_symbols),
            'visual_symbols': sorted(visual_symbols)
        }
    
    def combine_sensitivity_flags(self, text_flags: List[str],
                                  visual_flags: List[str]) -> Dict:
        """
        Combine sensitivity flags from text and visual analysis.
        
        Args:
            text_flags: Sensitivity flags from text
            visual_flags: Sensitivity flags from visuals
            
        Returns:
            Dictionary with combined sensitivity flags
        """
        # Union of sensitivity flags
        combined_flags = list(set(text_flags + visual_flags))
        
        return {
            'combined_flags': sorted(combined_flags),
            'flag_count': len(combined_flags),
            'text_flags': sorted(text_flags),
            'visual_flags': sorted(visual_flags)
        }
    
    def fuse_analyses(self, text_analysis: Dict, 
                     image_analysis: Optional[Dict] = None) -> Dict:
        """
        Perform complete multi-modal fusion of text and image analysis.
        
        If no image analysis is provided, returns text-only results.
        
        Args:
            text_analysis: Complete text analysis results
            image_analysis: Optional image analysis results
            
        Returns:
            Dictionary with fused multi-modal analysis
            
        Requirements: 12.3
        """
        # If no image analysis, return text-only results
        if not image_analysis or 'error' in image_analysis:
            return {
                'mode': 'text_only',
                'emc_score': text_analysis.get('emc_score', 0),
                'scs_score': text_analysis.get('scs_score', 0),
                'emotions': text_analysis.get('emotions', []),
                'has_image_analysis': False
            }
        
        # Extract scores from text analysis
        text_emc = text_analysis.get('emc_score', 0)
        text_scs = text_analysis.get('scs_score', 0)
        text_emotions = text_analysis.get('emotions', [])
        
        # Extract scores from image analysis
        visual_emc = image_analysis.get('visual_emc_score', 0)
        visual_scs = image_analysis.get('visual_scs_score', 0)
        visual_emotions = image_analysis.get('visual_emotions', [])
        
        # Combine EMC scores (weighted average)
        emc_fusion = self.combine_emc_scores(text_emc, visual_emc)
        
        # Combine SCS scores (maximum)
        scs_fusion = self.combine_scs_scores(text_scs, visual_scs)
        
        # Combine emotions (union)
        emotion_fusion = self.combine_emotions(text_emotions, visual_emotions)
        
        # Combine cultural symbols if available
        text_symbols = text_analysis.get('cultural_symbols', [])
        visual_symbols = image_analysis.get('cultural_symbols', [])
        symbol_fusion = self.combine_cultural_symbols(text_symbols, visual_symbols)
        
        # Combine sensitivity flags if available
        text_flags = text_analysis.get('sensitivity_flags', [])
        visual_flags = image_analysis.get('sensitivity_flags', [])
        flag_fusion = self.combine_sensitivity_flags(text_flags, visual_flags)
        
        return {
            'mode': 'multi_modal',
            'has_image_analysis': True,
            
            # Combined scores
            'emc_score': emc_fusion['combined_emc_score'],
            'scs_score': scs_fusion['combined_scs_score'],
            'emotions': emotion_fusion['combined_emotions'],
            
            # Detailed fusion results
            'emc_fusion': emc_fusion,
            'scs_fusion': scs_fusion,
            'emotion_fusion': emotion_fusion,
            'symbol_fusion': symbol_fusion,
            'flag_fusion': flag_fusion,
            
            # Modality agreement metrics
            'emotion_agreement': emotion_fusion['modality_agreement'],
            'primary_risk_source': scs_fusion['primary_risk_source']
        }


# Convenience function for quick multi-modal fusion
def fuse_text_and_image_analysis(text_analysis: Dict,
                                 image_analysis: Optional[Dict] = None) -> Dict:
    """
    Convenience function to fuse text and image analysis.
    
    Args:
        text_analysis: Complete text analysis results
        image_analysis: Optional image analysis results
        
    Returns:
        Dictionary with fused multi-modal analysis
    """
    fusion = MultiModalFusion()
    return fusion.fuse_analyses(text_analysis, image_analysis)
