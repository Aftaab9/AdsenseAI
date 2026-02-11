# AdsenseAI Campaign Risk Analyzer - Text Analysis Module
# Implements sentiment analysis, emotion detection, and text preprocessing

import re
from typing import Dict, List, Tuple
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class TextAnalyzer:
    """
    Text analysis module for campaign content.
    Implements dual sentiment analysis (TextBlob + VADER),
    emotion detection, and text preprocessing.
    """
    
    def __init__(self):
        """Initialize the TextAnalyzer with VADER sentiment analyzer"""
        self.vader = SentimentIntensityAnalyzer()
        
        # Cache for sentiment analysis results
        self._sentiment_cache = {}
        self._emotion_cache = {}
        self._max_cache_size = 1000
        
        # Emotion keyword dictionaries for Indian context
        self.emotion_keywords = {
            'joy': [
                'happy', 'happiness', 'joy', 'joyful', 'delighted', 'cheerful',
                'excited', 'excitement', 'celebrate', 'celebration', 'fun',
                'wonderful', 'amazing', 'fantastic', 'great', 'awesome',
                'smile', 'laugh', 'laughter', 'blessed', 'grateful'
            ],
            'nostalgia': [
                'remember', 'memories', 'childhood', 'nostalgia', 'nostalgic',
                'old days', 'throwback', 'reminisce', 'tradition', 'traditional',
                'heritage', 'roots', 'classic', 'vintage', 'timeless',
                'golden days', 'good old', 'back then'
            ],
            'pride': [
                'proud', 'pride', 'honor', 'honour', 'glory', 'achievement',
                'success', 'victory', 'triumph', 'excellence', 'indian',
                'india', 'nation', 'national', 'patriot', 'patriotic',
                'heritage', 'culture', 'legacy', 'dignity'
            ],
            'humor': [
                'funny', 'hilarious', 'lol', 'lmao', 'haha', 'hehe',
                'joke', 'comedy', 'comic', 'laugh', 'humor', 'humour',
                'witty', 'amusing', 'entertaining', 'fun', 'playful'
            ],
            'anger': [
                'angry', 'anger', 'furious', 'rage', 'mad', 'outrage',
                'outraged', 'frustrated', 'frustration', 'annoyed', 'irritated',
                'hate', 'hatred', 'disgusted', 'disgust', 'offensive',
                'unacceptable', 'wrong', 'injustice', 'unfair'
            ],
            'fear': [
                'fear', 'afraid', 'scared', 'worry', 'worried', 'anxious',
                'anxiety', 'nervous', 'concern', 'concerned', 'threat',
                'threatening', 'danger', 'dangerous', 'risk', 'risky',
                'unsafe', 'insecure', 'panic', 'terrified', 'miss out',
                'lose', 'losing', 'limited', 'last chance', 'running out'
            ],
            'inspiration': [
                'inspire', 'inspired', 'inspiring', 'inspiration', 'motivate',
                'motivated', 'motivating', 'motivation', 'empower', 'empowering',
                'hope', 'hopeful', 'dream', 'aspire', 'ambition', 'ambitious',
                'courage', 'courageous', 'brave', 'strength', 'strong',
                'believe', 'faith', 'determination', 'determined'
            ],
            'urgency': [
                'now', 'today', 'hurry', 'quick', 'quickly', 'fast', 'immediate',
                'immediately', 'urgent', 'asap', 'limited time', 'act now',
                'dont wait', 'dont miss', 'last chance', 'ending soon', 'expires',
                'deadline', 'while supplies last', 'limited offer', 'flash sale',
                'time sensitive', 'act fast', 'before its gone', 'only today'
            ]
        }
        
        # Moral framing keywords for Indian cultural context
        self.moral_keywords = {
            'values': [
                'value', 'values', 'principle', 'principles', 'ethics', 'ethical',
                'moral', 'morality', 'virtue', 'virtuous', 'integrity', 'honesty',
                'truth', 'truthful', 'authentic', 'authenticity', 'genuine'
            ],
            'duty': [
                'duty', 'responsibility', 'obligation', 'dharma', 'karma',
                'should', 'must', 'ought', 'deserve', 'right thing',
                'commitment', 'dedicated', 'devotion', 'loyal', 'loyalty'
            ],
            'family': [
                'family', 'families', 'parent', 'parents', 'mother', 'father',
                'children', 'son', 'daughter', 'brother', 'sister', 'home',
                'together', 'unity', 'bond', 'relationship', 'care', 'caring',
                'love', 'respect', 'elder', 'elders', 'generation'
            ],
            'community': [
                'community', 'society', 'social', 'collective', 'together',
                'unity', 'united', 'harmony', 'peace', 'cooperation',
                'neighbor', 'neighbourhood', 'village', 'nation', 'country',
                'people', 'everyone', 'all of us', 'we', 'our'
            ],
            'justice': [
                'justice', 'fair', 'fairness', 'equal', 'equality', 'equity',
                'right', 'rights', 'wrong', 'injustice', 'unfair', 'deserve',
                'discrimination', 'bias', 'prejudice', 'freedom', 'liberty'
            ],
            'tradition': [
                'tradition', 'traditional', 'culture', 'cultural', 'heritage',
                'custom', 'ritual', 'ceremony', 'festival', 'celebration',
                'ancient', 'wisdom', 'legacy', 'roots', 'ancestors',
                'sacred', 'holy', 'spiritual', 'religious', 'faith'
            ],
            'progress': [
                'progress', 'development', 'growth', 'future', 'modern',
                'innovation', 'change', 'transform', 'improve', 'improvement',
                'better', 'advancement', 'forward', 'evolve', 'evolution'
            ]
        }
        
        # CRITICAL FIX 3: Moral violation detection
        # Detects content that violates moral principles (dignity, equality, etc.)
        self.MORAL_VIOLATIONS = {
            'dignity_violation': {
                'keywords': ['dark skin', 'fat', 'ugly', 'inferior', 'worthless', 
                           'disgusting', 'gross', 'shameful', 'embarrassing'],
                'contexts': ['problem', 'issue', 'fix', 'change', 'transform', 
                           'solution', 'cure', 'treatment'],
                'score': 30
            },
            'discrimination_normalization': {
                'keywords': ['employers prefer', 'society wants', 'everyone knows',
                           'people like', 'nobody wants', 'everyone prefers'],
                'contexts': ['fair', 'light', 'white', 'slim', 'thin', 'tall',
                           'beautiful', 'attractive'],
                'score': 35
            },
            'victim_blaming': {
                'keywords': ['your fault', 'youre responsible', 'you let', 'dont let',
                           'because of you', 'due to your', 'if only you'],
                'contexts': ['job', 'rejection', 'marriage', 'failure', 'problem',
                           'issue', 'struggle'],
                'score': 40
            },
            'stereotype_reinforcement': {
                'keywords': ['real men', 'real women', 'good wife', 'good husband',
                           'proper woman', 'proper man', 'like a man', 'like a woman'],
                'contexts': ['should', 'must', 'need to', 'have to', 'supposed to',
                           'expected to'],
                'score': 30
            }
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess text for analysis.
        
        Args:
            text: Raw text content
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
        
        # Store original for emoji handling
        cleaned = text
        
        # Remove URLs
        cleaned = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', cleaned)
        
        # Remove mentions (@username)
        cleaned = re.sub(r'@\w+', '', cleaned)
        
        # Normalize hashtags (remove # but keep the word)
        cleaned = re.sub(r'#(\w+)', r'\1', cleaned)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Strip leading/trailing whitespace
        cleaned = cleaned.strip()
        
        return cleaned
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Perform dual sentiment analysis using TextBlob and VADER.
        Combines both algorithms for robust scoring.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing sentiment scores and labels
        """
        if not text or not text.strip():
            return {
                'polarity': 0.0,
                'subjectivity': 0.0,
                'positive': 0.0,
                'negative': 0.0,
                'neutral': 100.0,
                'label': 'Neutral',
                'textblob_polarity': 0.0,
                'vader_compound': 0.0
            }
        
        # Check cache first
        cache_key = hash(text[:500])  # Use first 500 chars for cache key
        if cache_key in self._sentiment_cache:
            return self._sentiment_cache[cache_key]
        
        # Clean text for analysis
        cleaned_text = self.clean_text(text)
        
        # TextBlob sentiment analysis
        blob = TextBlob(cleaned_text)
        textblob_polarity = blob.sentiment.polarity  # -1 to +1
        textblob_subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # VADER sentiment analysis (better for social media)
        vader_scores = self.vader.polarity_scores(cleaned_text)
        vader_compound = vader_scores['compound']  # -1 to +1
        vader_pos = vader_scores['pos'] * 100
        vader_neg = vader_scores['neg'] * 100
        vader_neu = vader_scores['neu'] * 100
        
        # Combine both algorithms (weighted average)
        # VADER gets more weight for social media content
        combined_polarity = (textblob_polarity * 0.4) + (vader_compound * 0.6)
        
        # Calculate positive, negative, neutral percentages
        # Use VADER's breakdown as it's more accurate for social media
        positive_pct = vader_pos
        negative_pct = vader_neg
        neutral_pct = vader_neu
        
        # Determine overall label
        if combined_polarity > 0.05:
            label = 'Positive'
        elif combined_polarity < -0.05:
            label = 'Negative'
        else:
            label = 'Neutral'
        
        result = {
            'polarity': round(combined_polarity, 3),
            'subjectivity': round(textblob_subjectivity, 3),
            'positive': round(positive_pct, 1),
            'negative': round(negative_pct, 1),
            'neutral': round(neutral_pct, 1),
            'label': label,
            'textblob_polarity': round(textblob_polarity, 3),
            'vader_compound': round(vader_compound, 3)
        }
        
        # Cache the result (limit cache size)
        if len(self._sentiment_cache) < self._max_cache_size:
            self._sentiment_cache[cache_key] = result
        
        return result
    
    def detect_emotions(self, text: str) -> List[str]:
        """
        Detect emotions in text using keyword matching.
        
        Args:
            text: Text content to analyze
            
        Returns:
            List of detected emotion labels
        """
        if not text or not text.strip():
            return []
        
        # Check cache first
        cache_key = hash(text[:500])
        if cache_key in self._emotion_cache:
            return self._emotion_cache[cache_key]
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        detected_emotions = []
        
        # Check each emotion category
        for emotion, keywords in self.emotion_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_emotions.append(emotion)
                    break  # Found this emotion, move to next category
        
        # Cache the result
        if len(self._emotion_cache) < self._max_cache_size:
            self._emotion_cache[cache_key] = detected_emotions
        
        return detected_emotions
    
    def detect_moral_framing(self, text: str) -> Dict:
        """
        Detect moral framing elements by identifying moral language
        and value-based judgments aligned with Indian cultural values.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing moral framing analysis
        """
        if not text or not text.strip():
            return {
                'has_moral_framing': False,
                'moral_categories': [],
                'moral_keyword_count': 0,
                'alignment_score': 0.0,
                'detected_keywords': []
            }
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        detected_categories = []
        detected_keywords = []
        total_keyword_count = 0
        
        # Check each moral category
        for category, keywords in self.moral_keywords.items():
            category_found = False
            for keyword in keywords:
                # Use word boundary matching to avoid partial matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    if not category_found:
                        detected_categories.append(category)
                        category_found = True
                    detected_keywords.append(keyword)
                    total_keyword_count += 1
        
        # Determine if moral framing is present
        has_moral_framing = total_keyword_count > 0
        
        # Calculate alignment with Indian cultural values
        # Categories aligned with Indian values get higher weights
        category_weights = {
            'family': 1.5,      # Very important in Indian culture
            'duty': 1.4,        # Dharma/karma concepts
            'tradition': 1.3,   # Cultural heritage valued
            'community': 1.2,   # Collectivist society
            'values': 1.1,      # General moral values
            'justice': 1.0,     # Universal value
            'progress': 0.9     # Sometimes conflicts with tradition
        }
        
        # Calculate weighted alignment score
        if detected_categories:
            weighted_sum = sum(category_weights.get(cat, 1.0) for cat in detected_categories)
            # Normalize to 0-100 scale (assume max 4 categories with avg weight 1.3)
            max_weighted = 4 * 1.5
            alignment_score = min((weighted_sum / max_weighted) * 100, 100)
        else:
            alignment_score = 0.0
        
        return {
            'has_moral_framing': has_moral_framing,
            'moral_categories': detected_categories,
            'moral_keyword_count': total_keyword_count,
            'alignment_score': round(alignment_score, 2),
            'detected_keywords': detected_keywords[:10]  # Limit to first 10 for brevity
        }
    
    def detect_moral_violations(self, text: str) -> Dict:
        """
        CRITICAL FIX 3: Detect moral violations (dignity, discrimination, etc.).
        
        Identifies content that violates moral principles even if it uses
        positive framing or moral keywords.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary with moral violation detection results
        """
        if not text or not text.strip():
            return {
                'violations_detected': False,
                'violations': [],
                'total_violation_score': 0
            }
        
        text_lower = text.lower()
        violations = []
        total_score = 0
        
        for violation_type, violation_def in self.MORAL_VIOLATIONS.items():
            # Check for keywords + contexts combination
            keywords_found = [
                kw for kw in violation_def['keywords']
                if kw in text_lower
            ]
            
            contexts_found = [
                ctx for ctx in violation_def['contexts']
                if ctx in text_lower
            ]
            
            # Violation detected if both keywords and contexts present
            if keywords_found and contexts_found:
                violations.append({
                    'type': violation_type,
                    'score': violation_def['score'],
                    'keywords': keywords_found[:3],  # Limit for brevity
                    'contexts': contexts_found[:3]
                })
                total_score += violation_def['score']
        
        return {
            'violations_detected': len(violations) > 0,
            'violations': violations,
            'total_violation_score': total_score
        }
    
    def calculate_emotional_intensity(self, text: str, sentiment: Dict = None, emotions: List[str] = None) -> Dict:
        """
        Calculate emotional intensity scores by measuring emotional arousal
        from sentiment and counting/weighting emotional triggers.
        
        Args:
            text: Text content to analyze
            sentiment: Pre-calculated sentiment dict (optional, will calculate if not provided)
            emotions: Pre-detected emotions list (optional, will detect if not provided)
            
        Returns:
            Dictionary containing emotional intensity metrics
        """
        # Get sentiment and emotions if not provided
        if sentiment is None:
            sentiment = self.analyze_sentiment(text)
        if emotions is None:
            emotions = self.detect_emotions(text)
        
        # Calculate emotional arousal from sentiment
        # Arousal is the absolute intensity of emotion (regardless of positive/negative)
        polarity = sentiment.get('polarity', 0.0)
        subjectivity = sentiment.get('subjectivity', 0.0)
        
        # Arousal level: high polarity (positive or negative) = high arousal
        # Subjectivity also contributes to arousal
        arousal_from_polarity = abs(polarity)  # 0 to 1
        arousal_from_subjectivity = subjectivity * 0.5  # 0 to 0.5
        arousal_level = min(arousal_from_polarity + arousal_from_subjectivity, 1.0)
        
        # Count emotional triggers
        emotion_count = len(emotions)
        
        # Weight emotional triggers based on type
        # High-arousal emotions get higher weights
        emotion_weights = {
            'joy': 1.2,
            'anger': 1.5,
            'fear': 1.4,
            'inspiration': 1.3,
            'pride': 1.2,
            'nostalgia': 1.0,
            'humor': 1.1,
            'urgency': 1.3  # High arousal for sales/promotional content
        }
        
        weighted_emotion_score = sum(emotion_weights.get(emotion, 1.0) for emotion in emotions)
        
        # Normalize weighted score (0-100 scale)
        # Assume max 4 emotions with average weight 1.3
        max_weighted_score = 4 * 1.5  # 6.0
        normalized_emotion_score = min((weighted_emotion_score / max_weighted_score) * 100, 100)
        
        # Calculate overall emotional intensity (0-100 scale)
        # Combines arousal level and emotion count
        intensity_score = (arousal_level * 60) + (normalized_emotion_score * 0.4)
        
        return {
            'arousal_level': round(arousal_level, 3),
            'emotion_count': emotion_count,
            'weighted_emotion_score': round(weighted_emotion_score, 2),
            'intensity_score': round(intensity_score, 2)
        }
    
    def calculate_emc_score(self, text: str) -> Dict:
        """
        Calculate Emotional-Moral Content (EMC) score by combining
        sentiment intensity, emotion count, moral keywords, moral violations, and arousal level.
        
        CRITICAL FIX 3: Now includes moral violation detection.
        
        Formula: EMC = (sentiment * 40) + (emotions * 15) + (moral_component * 25) + (arousal * 20)
        Moral_Component = (Moral_Keywords × 0.4 + Moral_Violations × 0.6) × 0.25
        If Moral_Violations > 20: EMC × 1.3
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing EMC score and component breakdowns
        """
        if not text or not text.strip():
            return {
                'emc_score': 0.0,
                'sentiment_component': 0.0,
                'emotion_component': 0.0,
                'moral_component': 0.0,
                'arousal_component': 0.0,
                'emotions': [],
                'moral_framing': {},
                'moral_violations': {},
                'sentiment': {}
            }
        
        # Get all required components
        sentiment = self.analyze_sentiment(text)
        emotions = self.detect_emotions(text)
        moral_framing = self.detect_moral_framing(text)
        moral_violations = self.detect_moral_violations(text)  # CRITICAL FIX 3
        emotional_intensity = self.calculate_emotional_intensity(text, sentiment, emotions)
        
        # Component 1: Sentiment intensity (0-40 points)
        # Use absolute polarity for intensity (high positive or negative = high EMC)
        sentiment_intensity = abs(sentiment.get('polarity', 0.0))  # 0 to 1
        sentiment_component = sentiment_intensity * 40
        
        # Component 2: Emotion count (0-15 points)
        # More emotions = higher EMC
        emotion_count = len(emotions)
        # Normalize: assume max 7 emotions (all categories)
        emotion_component = min((emotion_count / 7.0) * 15, 15)
        
        # Component 3: Moral component (0-25 points) - UPDATED WITH FIX 3
        # Combines moral keywords (40%) and moral violations (60%)
        moral_keyword_count = moral_framing.get('moral_keyword_count', 0)
        alignment_score = moral_framing.get('alignment_score', 0.0)  # 0-100
        
        # Moral keywords score
        keyword_score = min((moral_keyword_count / 10.0) * 100, 100)
        moral_keyword_component = ((keyword_score * 0.6) + (alignment_score * 0.4))
        
        # Moral violations score
        violation_score = moral_violations.get('total_violation_score', 0)  # 0-140 possible
        # Normalize to 0-100
        normalized_violation_score = min((violation_score / 140.0) * 100, 100)
        
        # Combine: 40% keywords, 60% violations
        moral_component = (moral_keyword_component * 0.4 + normalized_violation_score * 0.6) * 0.25
        
        # Component 4: Arousal level (0-20 points)
        arousal_level = emotional_intensity.get('arousal_level', 0.0)  # 0 to 1
        arousal_component = arousal_level * 20
        
        # Calculate total EMC score (0-100)
        emc_score = sentiment_component + emotion_component + moral_component + arousal_component
        
        # CRITICAL FIX 3: Apply multiplier if significant moral violations detected
        if violation_score > 20:
            emc_score = emc_score * 1.3
        
        emc_score = min(emc_score, 100)  # Cap at 100
        
        return {
            'emc_score': round(emc_score, 2),
            'sentiment_component': round(sentiment_component, 2),
            'emotion_component': round(emotion_component, 2),
            'moral_component': round(moral_component, 2),
            'arousal_component': round(arousal_component, 2),
            'emotions': emotions,
            'moral_framing': moral_framing,
            'moral_violations': moral_violations,  # NEW: Include violation details
            'sentiment': sentiment,
            'emotional_intensity': emotional_intensity
        }
    
    def measure_message_clarity(self, text: str) -> Dict:
        """
        Measure message clarity by calculating abstract language ratio
        and detecting question marks and open-ended statements.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing clarity metrics
        """
        if not text or not text.strip():
            return {
                'clarity_score': 100.0,
                'abstract_ratio': 0.0,
                'question_count': 0,
                'open_ended_indicators': 0,
                'word_count': 0
            }
        
        cleaned_text = self.clean_text(text)
        words = cleaned_text.split()
        word_count = len(words)
        
        if word_count == 0:
            return {
                'clarity_score': 100.0,
                'abstract_ratio': 0.0,
                'question_count': 0,
                'open_ended_indicators': 0,
                'word_count': 0
            }
        
        # Abstract language keywords (vague, conceptual terms)
        abstract_keywords = [
            'thing', 'things', 'something', 'anything', 'everything',
            'maybe', 'perhaps', 'possibly', 'might', 'could', 'would',
            'some', 'any', 'many', 'few', 'several', 'various',
            'kind of', 'sort of', 'type of', 'like', 'seems',
            'appears', 'suggests', 'implies', 'indicates',
            'concept', 'idea', 'notion', 'sense', 'feeling',
            'essence', 'nature', 'quality', 'aspect', 'element',
            'generally', 'usually', 'often', 'sometimes', 'rarely',
            'basically', 'essentially', 'fundamentally',
            'somewhat', 'rather', 'quite', 'fairly', 'pretty',
            'best', 'better', 'great', 'amazing', 'incredible',  # Superlatives (vague)
            'big', 'huge', 'massive', 'enormous',  # Size claims (vague)
            'more', 'most', 'less', 'least'  # Comparatives without context
        ]
        
        # Count abstract words
        text_lower = cleaned_text.lower()
        abstract_count = sum(1 for keyword in abstract_keywords if keyword in text_lower)
        
        # Calculate abstract ratio
        abstract_ratio = abstract_count / word_count if word_count > 0 else 0.0
        
        # Count question marks
        question_count = text.count('?')
        
        # Count open-ended indicators
        open_ended_phrases = [
            'what do you think', 'how do you feel', 'tell us', 'share your',
            'let us know', 'comment below', 'your thoughts', 'your opinion',
            'what if', 'imagine', 'consider', 'think about', 'wonder',
            'curious', 'explore', 'discover', 'find out'
        ]
        
        open_ended_count = sum(1 for phrase in open_ended_phrases if phrase in text_lower)
        
        # Calculate clarity score (0-100, higher = clearer)
        # Penalties for abstract language, questions, and open-ended statements
        clarity_score = 100.0
        clarity_score -= (abstract_ratio * 100) * 0.5  # Abstract language penalty
        clarity_score -= (question_count * 10)  # Question penalty
        clarity_score -= (open_ended_count * 15)  # Open-ended penalty
        clarity_score = max(clarity_score, 0.0)  # Floor at 0
        
        return {
            'clarity_score': round(clarity_score, 2),
            'abstract_ratio': round(abstract_ratio, 3),
            'question_count': question_count,
            'open_ended_indicators': open_ended_count,
            'word_count': word_count
        }
    
    def calculate_interpretive_openness(self, text: str, sentiment: Dict = None) -> Dict:
        """
        Calculate interpretive openness by assessing potential for
        multiple audience interpretations and cognitive elaboration requirements.
        
        Args:
            text: Text content to analyze
            sentiment: Pre-calculated sentiment dict (optional)
            
        Returns:
            Dictionary containing interpretive openness metrics
        """
        if not text or not text.strip():
            return {
                'openness_score': 0.0,
                'metaphor_count': 0,
                'ambiguous_pronouns': 0,
                'multiple_interpretations': False
            }
        
        if sentiment is None:
            sentiment = self.analyze_sentiment(text)
        
        cleaned_text = self.clean_text(text)
        text_lower = cleaned_text.lower()
        
        # Detect metaphorical/symbolic language
        metaphor_indicators = [
            'like', 'as if', 'as though', 'reminds', 'symbolizes',
            'represents', 'embodies', 'reflects', 'mirrors',
            'journey', 'path', 'bridge', 'door', 'window',
            'light', 'darkness', 'shadow', 'wave', 'storm',
            'seed', 'root', 'flower', 'tree', 'river', 'ocean'
        ]
        
        metaphor_count = sum(1 for indicator in metaphor_indicators if indicator in text_lower)
        
        # Count ambiguous pronouns (can refer to multiple things)
        ambiguous_pronouns = ['it', 'this', 'that', 'these', 'those', 'they', 'them']
        pronoun_count = sum(text_lower.count(' ' + pronoun + ' ') for pronoun in ambiguous_pronouns)
        
        # High subjectivity suggests multiple interpretations possible
        subjectivity = sentiment.get('subjectivity', 0.0)
        multiple_interpretations = subjectivity > 0.6 or metaphor_count > 2
        
        # Calculate openness score (0-100, higher = more open to interpretation)
        openness_score = 0.0
        openness_score += metaphor_count * 15  # Metaphors increase openness
        openness_score += min(pronoun_count * 5, 30)  # Ambiguous pronouns
        openness_score += subjectivity * 40  # Subjectivity
        openness_score = min(openness_score, 100)  # Cap at 100
        
        return {
            'openness_score': round(openness_score, 2),
            'metaphor_count': metaphor_count,
            'ambiguous_pronouns': pronoun_count,
            'multiple_interpretations': multiple_interpretations
        }
    
    def calculate_nam_score(self, text: str) -> Dict:
        """
        Calculate Narrative Ambiguity Measure (NAM) score.
        
        Formula: NAM = (abstract * 30) + (questions * 25) + (metaphors * 20) + ((100 - clarity) * 25)
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing NAM score and component breakdowns
        """
        if not text or not text.strip():
            return {
                'nam_score': 0.0,
                'abstract_component': 0.0,
                'question_component': 0.0,
                'metaphor_component': 0.0,
                'clarity_component': 0.0,
                'clarity_metrics': {},
                'openness_metrics': {}
            }
        
        # Get clarity and openness metrics
        clarity_metrics = self.measure_message_clarity(text)
        sentiment = self.analyze_sentiment(text)
        openness_metrics = self.calculate_interpretive_openness(text, sentiment)
        
        # Component 1: Abstract language (0-30 points)
        abstract_ratio = clarity_metrics.get('abstract_ratio', 0.0)
        abstract_component = min(abstract_ratio * 100, 100) * 0.30
        
        # Component 2: Questions (0-25 points)
        question_count = clarity_metrics.get('question_count', 0)
        open_ended = clarity_metrics.get('open_ended_indicators', 0)
        # Normalize: assume max 3 questions or open-ended statements
        question_score = min((question_count + open_ended) / 3.0, 1.0) * 100
        question_component = question_score * 0.25
        
        # Component 3: Metaphors (0-20 points)
        metaphor_count = openness_metrics.get('metaphor_count', 0)
        # Normalize: assume max 5 metaphors
        metaphor_score = min(metaphor_count / 5.0, 1.0) * 100
        metaphor_component = metaphor_score * 0.20
        
        # Component 4: Inverse clarity (0-25 points)
        clarity_score = clarity_metrics.get('clarity_score', 100.0)
        inverse_clarity = 100 - clarity_score
        clarity_component = inverse_clarity * 0.25
        
        # Calculate total NAM score (0-100)
        nam_score = abstract_component + question_component + metaphor_component + clarity_component
        nam_score = min(nam_score, 100)  # Cap at 100
        
        return {
            'nam_score': round(nam_score, 2),
            'abstract_component': round(abstract_component, 2),
            'question_component': round(question_component, 2),
            'metaphor_component': round(metaphor_component, 2),
            'clarity_component': round(clarity_component, 2),
            'clarity_metrics': clarity_metrics,
            'openness_metrics': openness_metrics
        }
    
    def analyze_text(self, text: str) -> Dict:
        """
        Perform complete text analysis including sentiment and emotions.
        
        Args:
            text: Text content to analyze
            
        Returns:
            Dictionary containing all analysis results
        """
        sentiment = self.analyze_sentiment(text)
        emotions = self.detect_emotions(text)
        
        return {
            'sentiment': sentiment,
            'emotions': emotions,
            'cleaned_text': self.clean_text(text)
        }
