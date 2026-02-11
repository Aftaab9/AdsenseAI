# AdsenseAI Campaign Risk Analyzer - Data Loader Module
# Loads cultural triggers, festival calendar, and historical campaigns data

import csv
import os
import sys
from typing import List, Dict, Optional
from datetime import datetime
import logging

# Handle relative imports for both module and standalone execution
if __name__ == "__main__":
    # Add parent directory to path for standalone execution
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
    from app.data.synthetic_data_generator import generate_synthetic_data
else:
    from .synthetic_data_generator import generate_synthetic_data

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    """Loads and caches data for the AdsenseAI system"""
    
    def __init__(self, data_dir: str = "Data"):
        """
        Initialize the data loader
        
        Args:
            data_dir: Directory where data files are located
        """
        self.data_dir = data_dir
        
        # Cache for loaded data
        self._cultural_triggers: Optional[List[Dict]] = None
        self._festival_calendar: Optional[List[Dict]] = None
        self._historical_campaigns: Optional[List[Dict]] = None
        self._twitter_data: Optional[List[Dict]] = None
        self._reddit_data: Optional[List[Dict]] = None
        self._instagram_analytics: Optional[List[Dict]] = None
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
    
    def _load_csv(self, filename: str, required_fields: List[str]) -> List[Dict]:
        """
        Load a CSV file and return list of dictionaries
        
        Args:
            filename: Name of the CSV file
            required_fields: List of required field names
            
        Returns:
            List of dictionaries with CSV data
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)
                
                # Validate required fields
                if data and not all(field in data[0] for field in required_fields):
                    logger.warning(f"Missing required fields in {filename}")
                    return []
                
                logger.info(f"Loaded {len(data)} records from {filename}")
                return data
                
        except FileNotFoundError:
            logger.warning(f"File not found: {filepath}")
            return []
        except Exception as e:
            logger.error(f"Error loading {filename}: {str(e)}")
            return []
    
    def load_cultural_triggers(self, use_synthetic_fallback: bool = True) -> List[Dict]:
        """
        Load cultural triggers database
        
        Args:
            use_synthetic_fallback: Generate synthetic data if file not found
            
        Returns:
            List of cultural trigger dictionaries
            
        Requirements: 10.1, 10.3
        """
        # Return cached data if available
        if self._cultural_triggers is not None:
            return self._cultural_triggers
        
        required_fields = ['keyword', 'category', 'alert_message', 'severity', 'risk_weight']
        data = self._load_csv('cultural_triggers.csv', required_fields)
        
        # Generate synthetic data if file not found and fallback enabled
        if not data and use_synthetic_fallback:
            logger.info("Generating synthetic cultural triggers data...")
            generate_synthetic_data(self.data_dir)
            data = self._load_csv('cultural_triggers.csv', required_fields)
        
        # Convert risk_weight to int
        for trigger in data:
            try:
                trigger['risk_weight'] = int(trigger['risk_weight'])
            except (ValueError, KeyError):
                trigger['risk_weight'] = 0
        
        # Cache the data
        self._cultural_triggers = data
        return data
    
    def load_festival_calendar(self, use_synthetic_fallback: bool = True) -> List[Dict]:
        """
        Load festival calendar
        
        Args:
            use_synthetic_fallback: Generate synthetic data if file not found
            
        Returns:
            List of festival dictionaries
            
        Requirements: 10.1, 10.4
        """
        # Return cached data if available
        if self._festival_calendar is not None:
            return self._festival_calendar
        
        required_fields = ['festival_name', 'date_2025', 'sensitivity_keywords', 'description']
        data = self._load_csv('festival_calendar.csv', required_fields)
        
        # Generate synthetic data if file not found and fallback enabled
        if not data and use_synthetic_fallback:
            logger.info("Generating synthetic festival calendar data...")
            generate_synthetic_data(self.data_dir)
            data = self._load_csv('festival_calendar.csv', required_fields)
        
        # Parse sensitivity keywords into lists
        for festival in data:
            if 'sensitivity_keywords' in festival:
                festival['sensitivity_keywords'] = festival['sensitivity_keywords'].split(';')
        
        # Cache the data
        self._festival_calendar = data
        return data
    
    def load_historical_campaigns(self, use_synthetic_fallback: bool = True) -> List[Dict]:
        """
        Load historical campaigns database
        
        Args:
            use_synthetic_fallback: Generate synthetic data if file not found
            
        Returns:
            List of historical campaign dictionaries
            
        Requirements: 10.1, 10.2
        """
        # Return cached data if available
        if self._historical_campaigns is not None:
            return self._historical_campaigns
        
        required_fields = ['brand', 'campaign_name', 'platform', 'backlash_occurred', 
                          'virality_score', 'outcome', 'lessons_learned']
        data = self._load_csv('historical_campaigns.csv', required_fields)
        
        # Generate synthetic data if file not found and fallback enabled
        if not data and use_synthetic_fallback:
            logger.info("Generating synthetic historical campaigns data...")
            generate_synthetic_data(self.data_dir)
            data = self._load_csv('historical_campaigns.csv', required_fields)
        
        # Convert virality_score to int and backlash_occurred to bool
        for campaign in data:
            try:
                campaign['virality_score'] = int(campaign['virality_score'])
            except (ValueError, KeyError):
                campaign['virality_score'] = 0
            
            campaign['backlash_occurred'] = campaign.get('backlash_occurred', '').lower() == 'yes'
        
        # Cache the data
        self._historical_campaigns = data
        return data
    
    def load_twitter_data(self) -> List[Dict]:
        """
        Load Twitter sentiment data
        
        Returns:
            List of Twitter data dictionaries with structured sentiment
            Format: [{'text': str, 'sentiment': int, 'source': 'twitter'}, ...]
            
        Requirements: 10.5
        """
        # Return cached data if available
        if self._twitter_data is not None:
            return self._twitter_data
        
        # Twitter_Data.csv has fields: clean_text, category (sentiment: -1, 0, 1)
        raw_data = self._load_csv('Twitter_Data.csv', [])
        
        # Parse and structure for sentiment analysis
        structured_data = []
        for row in raw_data:
            try:
                text = row.get('clean_text', '')
                category = row.get('category', '0')
                
                # Skip if text is None or empty
                if not text or text is None:
                    continue
                
                text = text.strip()
                if not text:
                    continue
                
                # Convert category to int
                try:
                    sentiment = int(category) if category else 0
                except (ValueError, TypeError):
                    sentiment = 0
                
                structured_data.append({
                    'text': text,
                    'sentiment': sentiment,  # -1: negative, 0: neutral, 1: positive
                    'source': 'twitter'
                })
            except Exception as e:
                # Silently skip problematic rows
                continue
        
        logger.info(f"Structured {len(structured_data)} Twitter records for sentiment analysis")
        
        # Cache the data
        self._twitter_data = structured_data
        return structured_data
    
    def load_reddit_data(self) -> List[Dict]:
        """
        Load Reddit discussion data
        
        Returns:
            List of Reddit data dictionaries with structured sentiment
            Format: [{'text': str, 'sentiment': int, 'source': 'reddit'}, ...]
            
        Requirements: 10.5
        """
        # Return cached data if available
        if self._reddit_data is not None:
            return self._reddit_data
        
        # Reddit_Data.csv has fields: clean_comment, category (sentiment: -1, 0, 1)
        raw_data = self._load_csv('Reddit_Data.csv', [])
        
        # Parse and structure for sentiment analysis
        structured_data = []
        for row in raw_data:
            try:
                text = row.get('clean_comment', '')
                category = row.get('category', '0')
                
                # Skip if text is None or empty
                if not text or text is None:
                    continue
                
                text = text.strip()
                if not text:
                    continue
                
                # Convert category to int
                try:
                    sentiment = int(category) if category else 0
                except (ValueError, TypeError):
                    sentiment = 0
                
                structured_data.append({
                    'text': text,
                    'sentiment': sentiment,  # -1: negative, 0: neutral, 1: positive
                    'source': 'reddit'
                })
            except Exception as e:
                # Silently skip problematic rows
                continue
        
        logger.info(f"Structured {len(structured_data)} Reddit records for sentiment analysis")
        
        # Cache the data
        self._reddit_data = structured_data
        return structured_data
    
    def load_instagram_analytics(self) -> List[Dict]:
        """
        Load Instagram analytics data
        
        Returns:
            List of Instagram analytics dictionaries with structured engagement metrics
            Format: [{'post_id': str, 'likes': int, 'comments': int, 'engagement_rate': float, ...}, ...]
            
        Requirements: 10.5
        """
        # Return cached data if available
        if self._instagram_analytics is not None:
            return self._instagram_analytics
        
        # Instagram_Analytics.csv has engagement metrics
        raw_data = self._load_csv('Instagram_Analytics.csv', [])
        
        # Parse and structure for engagement pattern recognition
        structured_data = []
        for row in raw_data:
            try:
                # Extract and convert numeric fields
                post_data = {
                    'post_id': row.get('post_id', ''),
                    'upload_date': row.get('upload_date', ''),
                    'media_type': row.get('media_type', ''),
                    'content_category': row.get('content_category', ''),
                    'traffic_source': row.get('traffic_source', ''),
                }
                
                # Convert numeric fields
                numeric_fields = [
                    'likes', 'comments', 'shares', 'saves', 'reach', 'impressions',
                    'caption_length', 'hashtags_count', 'followers_gained'
                ]
                
                for field in numeric_fields:
                    try:
                        post_data[field] = int(row.get(field, 0))
                    except (ValueError, TypeError):
                        post_data[field] = 0
                
                # Convert engagement_rate to float
                try:
                    post_data['engagement_rate'] = float(row.get('engagement_rate', 0))
                except (ValueError, TypeError):
                    post_data['engagement_rate'] = 0.0
                
                structured_data.append(post_data)
                
            except Exception as e:
                logger.warning(f"Error parsing Instagram row: {str(e)}")
                continue
        
        logger.info(f"Structured {len(structured_data)} Instagram analytics records")
        
        # Cache the data
        self._instagram_analytics = structured_data
        return structured_data
    
    def load_all_core_data(self, use_synthetic_fallback: bool = True) -> Dict[str, List[Dict]]:
        """
        Load all core datasets (cultural triggers, festivals, campaigns)
        
        Args:
            use_synthetic_fallback: Generate synthetic data if files not found
            
        Returns:
            Dictionary with all core data
            
        Requirements: 10.1
        """
        return {
            'cultural_triggers': self.load_cultural_triggers(use_synthetic_fallback),
            'festival_calendar': self.load_festival_calendar(use_synthetic_fallback),
            'historical_campaigns': self.load_historical_campaigns(use_synthetic_fallback)
        }
    
    def load_all_datasets(self, use_synthetic_fallback: bool = True) -> Dict[str, List[Dict]]:
        """
        Load all available datasets including social media data
        
        Args:
            use_synthetic_fallback: Generate synthetic data if core files not found
            
        Returns:
            Dictionary with all available data
            
        Requirements: 10.1, 10.5
        """
        data = self.load_all_core_data(use_synthetic_fallback)
        
        # Add social media datasets if available
        twitter = self.load_twitter_data()
        if twitter:
            data['twitter_data'] = twitter
        
        reddit = self.load_reddit_data()
        if reddit:
            data['reddit_data'] = reddit
        
        instagram = self.load_instagram_analytics()
        if instagram:
            data['instagram_analytics'] = instagram
        
        return data
    
    def get_trigger_by_keyword(self, keyword: str) -> Optional[Dict]:
        """
        Get cultural trigger by keyword
        
        Args:
            keyword: Trigger keyword to search for
            
        Returns:
            Trigger dictionary or None if not found
        """
        triggers = self.load_cultural_triggers()
        keyword_lower = keyword.lower()
        
        for trigger in triggers:
            if trigger.get('keyword', '').lower() == keyword_lower:
                return trigger
        
        return None
    
    def get_festival_by_name(self, festival_name: str) -> Optional[Dict]:
        """
        Get festival by name
        
        Args:
            festival_name: Festival name to search for
            
        Returns:
            Festival dictionary or None if not found
        """
        festivals = self.load_festival_calendar()
        name_lower = festival_name.lower()
        
        for festival in festivals:
            if festival.get('festival_name', '').lower() == name_lower:
                return festival
        
        return None
    
    def get_campaigns_by_platform(self, platform: str) -> List[Dict]:
        """
        Get historical campaigns by platform
        
        Args:
            platform: Platform name (Instagram, YouTube, TikTok, Twitter)
            
        Returns:
            List of campaign dictionaries for the platform
        """
        campaigns = self.load_historical_campaigns()
        platform_lower = platform.lower()
        
        return [
            campaign for campaign in campaigns
            if campaign.get('platform', '').lower() == platform_lower
        ]
    
    def clear_cache(self):
        """Clear all cached data"""
        self._cultural_triggers = None
        self._festival_calendar = None
        self._historical_campaigns = None
        self._twitter_data = None
        self._reddit_data = None
        self._instagram_analytics = None
        logger.info("Data cache cleared")
    
    def get_sentiment_training_data(self) -> List[Dict]:
        """
        Get combined sentiment training data from Twitter and Reddit
        
        Returns:
            List of dictionaries with text and sentiment labels
            Format: [{'text': str, 'sentiment': int, 'source': str}, ...]
            
        Requirements: 10.5
        """
        twitter_data = self.load_twitter_data()
        reddit_data = self.load_reddit_data()
        
        combined_data = twitter_data + reddit_data
        logger.info(f"Combined {len(combined_data)} sentiment training samples")
        
        return combined_data
    
    def get_engagement_patterns(self, platform: str = 'instagram') -> Dict:
        """
        Get engagement pattern statistics from Instagram analytics
        
        Args:
            platform: Platform name (currently only 'instagram' supported)
            
        Returns:
            Dictionary with engagement statistics
            
        Requirements: 10.5
        """
        if platform.lower() != 'instagram':
            logger.warning(f"Platform {platform} not supported for engagement patterns")
            return {}
        
        instagram_data = self.load_instagram_analytics()
        
        if not instagram_data:
            return {}
        
        # Calculate aggregate statistics
        total_posts = len(instagram_data)
        
        # Average metrics
        avg_likes = sum(post['likes'] for post in instagram_data) / total_posts
        avg_comments = sum(post['comments'] for post in instagram_data) / total_posts
        avg_shares = sum(post['shares'] for post in instagram_data) / total_posts
        avg_engagement_rate = sum(post['engagement_rate'] for post in instagram_data) / total_posts
        
        # Group by media type
        media_type_stats = {}
        for post in instagram_data:
            media_type = post['media_type']
            if media_type not in media_type_stats:
                media_type_stats[media_type] = {
                    'count': 0,
                    'avg_engagement': 0,
                    'total_engagement': 0
                }
            media_type_stats[media_type]['count'] += 1
            media_type_stats[media_type]['total_engagement'] += post['engagement_rate']
        
        # Calculate averages for media types
        for media_type in media_type_stats:
            count = media_type_stats[media_type]['count']
            media_type_stats[media_type]['avg_engagement'] = (
                media_type_stats[media_type]['total_engagement'] / count
            )
        
        return {
            'total_posts': total_posts,
            'avg_likes': avg_likes,
            'avg_comments': avg_comments,
            'avg_shares': avg_shares,
            'avg_engagement_rate': avg_engagement_rate,
            'media_type_stats': media_type_stats
        }


# Global data loader instance
_global_loader: Optional[DataLoader] = None


def get_data_loader(data_dir: str = "Data") -> DataLoader:
    """
    Get global data loader instance (singleton pattern)
    
    Args:
        data_dir: Directory where data files are located
        
    Returns:
        DataLoader instance
    """
    global _global_loader
    
    if _global_loader is None:
        _global_loader = DataLoader(data_dir)
    
    return _global_loader


if __name__ == "__main__":
    # Test data loading when run as script
    print("Testing data loader...")
    loader = DataLoader()
    
    print("\nLoading cultural triggers...")
    triggers = loader.load_cultural_triggers()
    print(f"Loaded {len(triggers)} cultural triggers")
    if triggers:
        print(f"Sample trigger: {triggers[0]}")
    
    print("\nLoading festival calendar...")
    festivals = loader.load_festival_calendar()
    print(f"Loaded {len(festivals)} festivals")
    if festivals:
        print(f"Sample festival: {festivals[0]}")
    
    print("\nLoading historical campaigns...")
    campaigns = loader.load_historical_campaigns()
    print(f"Loaded {len(campaigns)} historical campaigns")
    if campaigns:
        print(f"Sample campaign: {campaigns[0]}")
    
    print("\n" + "="*60)
    print("Loading social media datasets...")
    print("="*60)
    
    print("\nLoading Twitter data...")
    twitter = loader.load_twitter_data()
    print(f"Loaded {len(twitter)} Twitter records")
    if twitter:
        print(f"Sample Twitter record: {twitter[0]}")
        # Show sentiment distribution
        sentiments = [t['sentiment'] for t in twitter]
        print(f"Sentiment distribution: Positive={sentiments.count(1)}, "
              f"Neutral={sentiments.count(0)}, Negative={sentiments.count(-1)}")
    
    print("\nLoading Reddit data...")
    reddit = loader.load_reddit_data()
    print(f"Loaded {len(reddit)} Reddit records")
    if reddit:
        print(f"Sample Reddit record: {reddit[0]}")
        # Show sentiment distribution
        sentiments = [r['sentiment'] for r in reddit]
        print(f"Sentiment distribution: Positive={sentiments.count(1)}, "
              f"Neutral={sentiments.count(0)}, Negative={sentiments.count(-1)}")
    
    print("\nLoading Instagram analytics...")
    instagram = loader.load_instagram_analytics()
    print(f"Loaded {len(instagram)} Instagram records")
    if instagram:
        print(f"Sample Instagram record: {instagram[0]}")
    
    print("\n" + "="*60)
    print("Testing helper methods...")
    print("="*60)
    
    print("\nGetting combined sentiment training data...")
    sentiment_data = loader.get_sentiment_training_data()
    print(f"Total sentiment training samples: {len(sentiment_data)}")
    
    print("\nGetting Instagram engagement patterns...")
    engagement_patterns = loader.get_engagement_patterns()
    if engagement_patterns:
        print(f"Total posts analyzed: {engagement_patterns['total_posts']}")
        print(f"Average engagement rate: {engagement_patterns['avg_engagement_rate']:.2f}%")
        print(f"Media type statistics: {engagement_patterns['media_type_stats']}")
    
    print("\n" + "="*60)
    print("Data loading test complete!")
    print("="*60)
