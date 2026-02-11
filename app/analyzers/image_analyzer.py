# AdsenseAI Campaign Risk Analyzer - Image Analyzer Module
# Uses Google Gemini API for visual content analysis

import os
import base64
import json
from typing import Dict, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class ImageAnalyzer:
    """
    Image analyzer using Google Gemini API for visual content analysis.
    
    Analyzes campaign images for:
    - Visual emotions (joy, pride, nostalgia, etc.)
    - Cultural symbols (religious imagery, festival references)
    - Sensitivity flags (colorism, political references)
    - Text overlays
    - Brand elements
    
    Uses Gemini 1.5 Flash model (free tier) for analysis.
    
    Requirements: 12.1, 12.2
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the image analyzer with Gemini API.
        
        Args:
            api_key: Google Gemini API key. If None, reads from GEMINI_API_KEY env variable.
            
        Requirements: 12.1
        """
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Please set GEMINI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        # Configure Gemini API
        genai.configure(api_key=self.api_key)
        
        # Initialize model (gemini-2.5-flash for free tier)
        try:
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except:
            # Fallback to other available models
            try:
                self.model = genai.GenerativeModel('gemini-flash-latest')
            except:
                self.model = genai.GenerativeModel('gemini-pro-latest')
        
        # Analysis prompt template
        self.analysis_prompt = """Analyze this marketing image for the Indian market. Provide a detailed analysis in JSON format with the following structure:

{
  "visual_emotions": ["list of emotions detected: joy, pride, nostalgia, celebration, inspiration, etc."],
  "cultural_symbols": ["list of cultural/religious symbols: diya, rangoli, temple, mosque, etc."],
  "sensitivity_flags": ["list of potential sensitivity issues: colorism, religious imagery, political references, etc."],
  "text_overlay": "any text visible in the image",
  "brand_elements": ["list of brand elements: logo, product, packaging, etc."],
  "festival_references": ["list of festival references: Diwali, Eid, Holi, etc."],
  "skin_tone_representation": "description of skin tone representation and diversity",
  "emotional_tone": "overall emotional tone of the imagery",
  "visual_style": "description of visual style: modern, traditional, minimalist, etc.",
  "color_palette": ["dominant colors in the image"],
  "composition": "description of image composition and layout"
}

Focus on identifying:
1. Emotional tone and visual emotions
2. Cultural and religious symbols that may be sensitive in India
3. Skin tone representation and potential colorism indicators
4. Festival or cultural references
5. Any text overlays or brand messaging
6. Potential sensitivity triggers for Indian audiences

Provide only the JSON response, no additional text."""

        # OCR prompt template for extracting text from images
        self.ocr_prompt = """Extract ALL text visible in this image. This includes:
- Headlines and titles
- Body text and captions
- Brand names and slogans
- Hashtags and mentions
- Call-to-action text
- Any other readable text

Return the extracted text in JSON format:
{
  "extracted_text": "The complete text found in the image, preserving line breaks where appropriate",
  "text_elements": [
    {"type": "headline", "text": "Main headline text"},
    {"type": "body", "text": "Body text content"},
    {"type": "cta", "text": "Call to action text"},
    {"type": "hashtag", "text": "#hashtag"},
    {"type": "brand", "text": "Brand name"}
  ],
  "language": "primary language of the text (e.g., English, Hindi, Hinglish)",
  "text_confidence": "high/medium/low - confidence in text extraction accuracy"
}

If no text is visible in the image, return:
{
  "extracted_text": "",
  "text_elements": [],
  "language": "none",
  "text_confidence": "high"
}

Provide only the JSON response, no additional text."""
    
    def analyze_image(self, image_data: str) -> Dict:
        """
        Analyze campaign image using Gemini API.
        
        Args:
            image_data: Base64 encoded image string (with or without data URI prefix)
            
        Returns:
            Dictionary containing visual analysis results
            
        Requirements: 12.1, 12.2
        """
        try:
            # Parse base64 image data
            image_bytes = self._parse_image_data(image_data)
            
            # Create image part for Gemini
            image_part = {
                'mime_type': 'image/jpeg',  # Assume JPEG, Gemini handles most formats
                'data': image_bytes
            }
            
            # Generate content with image and prompt
            response = self.model.generate_content([self.analysis_prompt, image_part])
            
            # Parse JSON response
            analysis_result = self._parse_gemini_response(response.text)
            
            # Calculate visual EMC score
            visual_emc_score = self._calculate_visual_emc(analysis_result)
            analysis_result['visual_emc_score'] = visual_emc_score
            
            # Calculate visual SCS score
            visual_scs_score = self._calculate_visual_scs(analysis_result)
            analysis_result['visual_scs_score'] = visual_scs_score
            
            return analysis_result
            
        except Exception as e:
            # Return error result with empty analysis
            return {
                'error': str(e),
                'visual_emotions': [],
                'cultural_symbols': [],
                'sensitivity_flags': [],
                'text_overlay': '',
                'brand_elements': [],
                'festival_references': [],
                'visual_emc_score': 0,
                'visual_scs_score': 0
            }
    
    def extract_text_from_image(self, image_data: str) -> Dict:
        """
        Extract text from image using Gemini API OCR capabilities.
        
        This method uses Gemini's vision capabilities to perform OCR
        and extract all visible text from the image.
        
        Args:
            image_data: Base64 encoded image string (with or without data URI prefix)
            
        Returns:
            Dictionary containing:
            - extracted_text: Complete text found in the image
            - text_elements: List of text elements with types
            - language: Primary language of the text
            - text_confidence: Confidence level of extraction
            
        Requirements: 15.2
        """
        try:
            # Parse base64 image data
            image_bytes = self._parse_image_data(image_data)
            
            # Create image part for Gemini
            image_part = {
                'mime_type': 'image/jpeg',
                'data': image_bytes
            }
            
            # Generate content with image and OCR prompt
            response = self.model.generate_content([self.ocr_prompt, image_part])
            
            # Parse JSON response
            ocr_result = self._parse_ocr_response(response.text)
            
            return ocr_result
            
        except Exception as e:
            # Return error result with empty extraction
            return {
                'error': str(e),
                'extracted_text': '',
                'text_elements': [],
                'language': 'unknown',
                'text_confidence': 'low'
            }
    
    def _parse_ocr_response(self, response_text: str) -> Dict:
        """
        Parse Gemini OCR response text into structured dictionary.
        
        Args:
            response_text: Raw response text from Gemini
            
        Returns:
            Parsed dictionary with OCR results
        """
        try:
            # Try to extract JSON from response
            response_text = response_text.strip()
            
            # Remove markdown code block markers if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]
            elif response_text.startswith('```'):
                response_text = response_text[3:]
            
            if response_text.endswith('```'):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Ensure all expected fields exist with defaults
            default_result = {
                'extracted_text': '',
                'text_elements': [],
                'language': 'unknown',
                'text_confidence': 'medium'
            }
            
            # Merge with defaults
            default_result.update(result)
            return default_result
            
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract text directly
            return {
                'extracted_text': response_text if response_text else '',
                'text_elements': [],
                'language': 'unknown',
                'text_confidence': 'low',
                'parse_error': 'Failed to parse Gemini OCR response as JSON'
            }
    
    def analyze_image_with_ocr(self, image_data: str) -> Dict:
        """
        Perform both visual analysis and OCR text extraction on an image.
        
        This is a convenience method that combines analyze_image() and
        extract_text_from_image() into a single call.
        
        Args:
            image_data: Base64 encoded image string
            
        Returns:
            Dictionary containing both visual analysis and OCR results
            
        Requirements: 15.2, 15.3
        """
        # Perform visual analysis
        analysis_result = self.analyze_image(image_data)
        
        # Perform OCR extraction
        ocr_result = self.extract_text_from_image(image_data)
        
        # Merge results
        analysis_result['ocr_result'] = ocr_result
        
        # If text_overlay is empty but OCR found text, use OCR result
        if not analysis_result.get('text_overlay') and ocr_result.get('extracted_text'):
            analysis_result['text_overlay'] = ocr_result['extracted_text']
        
        return analysis_result
    
    def _parse_image_data(self, image_data: str) -> bytes:
        """
        Parse base64 image data, handling data URI prefix if present.
        
        Args:
            image_data: Base64 encoded image string
            
        Returns:
            Raw image bytes
        """
        # Remove data URI prefix if present (e.g., "data:image/jpeg;base64,")
        if image_data.startswith('data:'):
            # Find the comma that separates the prefix from the data
            comma_index = image_data.find(',')
            if comma_index != -1:
                image_data = image_data[comma_index + 1:]
        
        # Decode base64 to bytes
        image_bytes = base64.b64decode(image_data)
        return image_bytes
    
    def _parse_gemini_response(self, response_text: str) -> Dict:
        """
        Parse Gemini API response text into structured dictionary.
        
        Args:
            response_text: Raw response text from Gemini
            
        Returns:
            Parsed dictionary with analysis results
        """
        try:
            # Try to extract JSON from response
            # Sometimes Gemini wraps JSON in markdown code blocks
            response_text = response_text.strip()
            
            # Remove markdown code block markers if present
            if response_text.startswith('```json'):
                response_text = response_text[7:]  # Remove ```json
            elif response_text.startswith('```'):
                response_text = response_text[3:]  # Remove ```
            
            if response_text.endswith('```'):
                response_text = response_text[:-3]  # Remove trailing ```
            
            response_text = response_text.strip()
            
            # Parse JSON
            result = json.loads(response_text)
            
            # Ensure all expected fields exist with defaults
            default_result = {
                'visual_emotions': [],
                'cultural_symbols': [],
                'sensitivity_flags': [],
                'text_overlay': '',
                'brand_elements': [],
                'festival_references': [],
                'skin_tone_representation': '',
                'emotional_tone': '',
                'visual_style': '',
                'color_palette': [],
                'composition': ''
            }
            
            # Merge with defaults
            default_result.update(result)
            return default_result
            
        except json.JSONDecodeError:
            # If JSON parsing fails, return empty result
            return {
                'visual_emotions': [],
                'cultural_symbols': [],
                'sensitivity_flags': [],
                'text_overlay': '',
                'brand_elements': [],
                'festival_references': [],
                'skin_tone_representation': '',
                'emotional_tone': '',
                'visual_style': '',
                'color_palette': [],
                'composition': '',
                'parse_error': 'Failed to parse Gemini response as JSON'
            }
    
    def _calculate_visual_emc(self, analysis: Dict) -> float:
        """
        Calculate visual emotional-moral content score.
        
        Based on:
        - Number of visual emotions detected
        - Emotional tone intensity
        - Cultural/moral framing in imagery
        
        Args:
            analysis: Parsed analysis dictionary
            
        Returns:
            Visual EMC score (0-100)
            
        Requirements: 12.2
        """
        score = 0.0
        
        # Component 1: Visual emotions (0-40 points)
        emotions = analysis.get('visual_emotions', [])
        emotion_score = min(len(emotions) * 10, 40)
        score += emotion_score
        
        # Component 2: Emotional tone (0-30 points)
        emotional_tone = analysis.get('emotional_tone', '').lower()
        if any(word in emotional_tone for word in ['strong', 'intense', 'powerful', 'vibrant']):
            score += 30
        elif any(word in emotional_tone for word in ['moderate', 'positive', 'warm']):
            score += 20
        elif any(word in emotional_tone for word in ['subtle', 'calm', 'gentle']):
            score += 10
        
        # Component 3: Cultural/moral framing (0-30 points)
        cultural_symbols = analysis.get('cultural_symbols', [])
        festival_refs = analysis.get('festival_references', [])
        
        if len(cultural_symbols) > 0 or len(festival_refs) > 0:
            score += min((len(cultural_symbols) + len(festival_refs)) * 10, 30)
        
        return min(score, 100)
    
    def _calculate_visual_scs(self, analysis: Dict) -> float:
        """
        Calculate visual socio-cultural sensitivity score.
        
        Based on:
        - Sensitivity flags detected
        - Cultural symbols that may be controversial
        - Skin tone representation issues
        
        Args:
            analysis: Parsed analysis dictionary
            
        Returns:
            Visual SCS score (0-100)
            
        Requirements: 12.2, 12.4
        """
        score = 0.0
        
        # Component 1: Sensitivity flags (major contributor)
        sensitivity_flags = analysis.get('sensitivity_flags', [])
        
        for flag in sensitivity_flags:
            flag_lower = flag.lower()
            
            # Critical sensitivity issues (40 points each)
            if any(word in flag_lower for word in ['colorism', 'fair skin', 'skin whitening', 'religious conflict']):
                score += 40
            
            # High sensitivity issues (30 points each)
            elif any(word in flag_lower for word in ['religious', 'political', 'caste', 'communal']):
                score += 30
            
            # Medium sensitivity issues (20 points each)
            elif any(word in flag_lower for word in ['cultural appropriation', 'stereotype', 'insensitive']):
                score += 20
            
            # Low sensitivity issues (10 points each)
            else:
                score += 10
        
        # Component 2: Skin tone representation
        skin_tone = analysis.get('skin_tone_representation', '').lower()
        if any(word in skin_tone for word in ['only fair', 'only light', 'lack of diversity', 'colorism']):
            score += 35
        elif any(word in skin_tone for word in ['predominantly fair', 'mostly light']):
            score += 20
        
        # Component 3: Controversial cultural symbols
        cultural_symbols = analysis.get('cultural_symbols', [])
        controversial_symbols = ['beef', 'pork', 'alcohol', 'religious conflict']
        
        for symbol in cultural_symbols:
            if any(word in symbol.lower() for word in controversial_symbols):
                score += 25
        
        return min(score, 100)
    
    def analyze_image_file(self, image_path: str) -> Dict:
        """
        Analyze image from file path.
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary containing visual analysis results
        """
        try:
            # Read image file and encode to base64
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Analyze the image
            return self.analyze_image(image_base64)
            
        except Exception as e:
            return {
                'error': f"Failed to read image file: {str(e)}",
                'visual_emotions': [],
                'cultural_symbols': [],
                'sensitivity_flags': [],
                'text_overlay': '',
                'brand_elements': [],
                'festival_references': [],
                'visual_emc_score': 0,
                'visual_scs_score': 0
            }
    
    def get_api_status(self) -> Dict:
        """
        Check if Gemini API is configured and accessible.
        
        Returns:
            Dictionary with API status information
        """
        return {
            'configured': bool(self.api_key),
            'model': 'gemini-2.5-flash',
            'api_key_present': bool(self.api_key),
            'api_key_length': len(self.api_key) if self.api_key else 0
        }


# Convenience function for quick image analysis
def analyze_campaign_image(image_data: str, api_key: Optional[str] = None) -> Dict:
    """
    Convenience function to analyze a campaign image.
    
    Args:
        image_data: Base64 encoded image string
        api_key: Optional Gemini API key
        
    Returns:
        Dictionary containing visual analysis results
    """
    analyzer = ImageAnalyzer(api_key)
    return analyzer.analyze_image(image_data)
