# AdsenseAI Campaign Risk Analyzer - Synthetic Data Generator
# Generates cultural triggers, festival calendar, and historical campaigns data

import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict


class SyntheticDataGenerator:
    """Generates synthetic datasets for the AdsenseAI system"""
    
    def __init__(self, data_dir: str = "Data"):
        """
        Initialize the synthetic data generator
        
        Args:
            data_dir: Directory where data files will be saved
        """
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
    
    def generate_cultural_triggers(self) -> str:
        """
        Generate cultural triggers database CSV
        
        Creates a comprehensive database of cultural sensitivity triggers
        for the Indian market including religious, colorism, geopolitical,
        and cultural categories with severity levels and risk weights.
        
        Requirements: 3.2, 10.3
        
        Returns:
            Path to the generated CSV file
        """
        triggers = [
            # Religious triggers - Critical severity
            {
                "keyword": "beef",
                "category": "Religious",
                "alert_message": "Beef references are highly sensitive in India due to religious beliefs",
                "severity": "critical",
                "risk_weight": 40
            },
            {
                "keyword": "cow meat",
                "category": "Religious",
                "alert_message": "Cow meat references are highly sensitive in Hindu culture",
                "severity": "critical",
                "risk_weight": 40
            },
            {
                "keyword": "pork",
                "category": "Religious",
                "alert_message": "Pork references may offend Muslim audiences",
                "severity": "high",
                "risk_weight": 30
            },
            {
                "keyword": "interfaith",
                "category": "Religious",
                "alert_message": "Interfaith themes can polarize audiences",
                "severity": "high",
                "risk_weight": 25
            },
            {
                "keyword": "temple",
                "category": "Religious",
                "alert_message": "Religious place references require careful context",
                "severity": "medium",
                "risk_weight": 15
            },
            {
                "keyword": "mosque",
                "category": "Religious",
                "alert_message": "Religious place references require careful context",
                "severity": "medium",
                "risk_weight": 15
            },
            {
                "keyword": "church",
                "category": "Religious",
                "alert_message": "Religious place references require careful context",
                "severity": "medium",
                "risk_weight": 15
            },
            {
                "keyword": "gurudwara",
                "category": "Religious",
                "alert_message": "Religious place references require careful context",
                "severity": "medium",
                "risk_weight": 15
            },
            {
                "keyword": "hindu muslim",
                "category": "Religious",
                "alert_message": "Religious community comparisons can be divisive",
                "severity": "high",
                "risk_weight": 30
            },
            
            # Colorism triggers - Critical severity
            {
                "keyword": "fair skin",
                "category": "Colorism",
                "alert_message": "Fair skin references trigger colorism backlash",
                "severity": "critical",
                "risk_weight": 40
            },
            {
                "keyword": "gora",
                "category": "Colorism",
                "alert_message": "Skin tone language detected - colorism concern",
                "severity": "critical",
                "risk_weight": 35
            },
            {
                "keyword": "whitening",
                "category": "Colorism",
                "alert_message": "Skin whitening references are highly controversial",
                "severity": "critical",
                "risk_weight": 40
            },
            {
                "keyword": "fair and lovely",
                "category": "Colorism",
                "alert_message": "Fair skin beauty standards trigger backlash",
                "severity": "critical",
                "risk_weight": 40
            },
            {
                "keyword": "dark skin",
                "category": "Colorism",
                "alert_message": "Skin tone references can perpetuate colorism",
                "severity": "high",
                "risk_weight": 30
            },
            {
                "keyword": "dusky",
                "category": "Colorism",
                "alert_message": "Euphemistic skin tone language is problematic",
                "severity": "high",
                "risk_weight": 25
            },
            {
                "keyword": "complexion",
                "category": "Colorism",
                "alert_message": "Complexion references may imply colorism",
                "severity": "medium",
                "risk_weight": 20
            },
            
            # Geopolitical triggers - Critical/High severity
            {
                "keyword": "pakistan",
                "category": "Geopolitical",
                "alert_message": "Cross-border references can polarize audiences",
                "severity": "high",
                "risk_weight": 30
            },
            {
                "keyword": "kashmir",
                "category": "Geopolitical",
                "alert_message": "Kashmir references are extremely sensitive",
                "severity": "critical",
                "risk_weight": 40
            },
            {
                "keyword": "china",
                "category": "Geopolitical",
                "alert_message": "China references can trigger nationalist sentiment",
                "severity": "high",
                "risk_weight": 25
            },
            {
                "keyword": "border",
                "category": "Geopolitical",
                "alert_message": "Border references may evoke geopolitical tensions",
                "severity": "medium",
                "risk_weight": 20
            },
            {
                "keyword": "army",
                "category": "Geopolitical",
                "alert_message": "Military references require respectful context",
                "severity": "medium",
                "risk_weight": 15
            },
            {
                "keyword": "soldier",
                "category": "Geopolitical",
                "alert_message": "Military references require respectful context",
                "severity": "medium",
                "risk_weight": 15
            },
            
            # Cultural norms triggers
            {
                "keyword": "alcohol",
                "category": "Cultural",
                "alert_message": "Alcohol promotion has cultural and legal restrictions",
                "severity": "medium",
                "risk_weight": 20
            },
            {
                "keyword": "drinking",
                "category": "Cultural",
                "alert_message": "Drinking references may conflict with cultural values",
                "severity": "medium",
                "risk_weight": 18
            },
            {
                "keyword": "consent",
                "category": "Cultural",
                "alert_message": "Consent themes require sensitive handling",
                "severity": "high",
                "risk_weight": 25
            },
            {
                "keyword": "harassment",
                "category": "Cultural",
                "alert_message": "Harassment themes require careful context",
                "severity": "high",
                "risk_weight": 30
            },
            {
                "keyword": "dowry",
                "category": "Cultural",
                "alert_message": "Dowry references touch on sensitive social issues",
                "severity": "high",
                "risk_weight": 25
            },
            {
                "keyword": "caste",
                "category": "Cultural",
                "alert_message": "Caste references are highly sensitive",
                "severity": "critical",
                "risk_weight": 35
            },
            {
                "keyword": "reservation",
                "category": "Cultural",
                "alert_message": "Reservation policy references can be divisive",
                "severity": "high",
                "risk_weight": 30
            },
            {
                "keyword": "love jihad",
                "category": "Cultural",
                "alert_message": "Communally charged terminology detected",
                "severity": "critical",
                "risk_weight": 40
            },
            {
                "keyword": "beef ban",
                "category": "Cultural",
                "alert_message": "Politically and religiously sensitive topic",
                "severity": "critical",
                "risk_weight": 40
            },
            
            # Regional sensitivity
            {
                "keyword": "north indian",
                "category": "Regional",
                "alert_message": "Regional comparisons can be divisive",
                "severity": "medium",
                "risk_weight": 15
            },
            {
                "keyword": "south indian",
                "category": "Regional",
                "alert_message": "Regional comparisons can be divisive",
                "severity": "medium",
                "risk_weight": 15
            },
            {
                "keyword": "madrasi",
                "category": "Regional",
                "alert_message": "Outdated regional terminology is offensive",
                "severity": "high",
                "risk_weight": 25
            },
            
            # Gender and social issues
            {
                "keyword": "objectification",
                "category": "Gender",
                "alert_message": "Objectification themes trigger backlash",
                "severity": "high",
                "risk_weight": 30
            },
            {
                "keyword": "item song",
                "category": "Gender",
                "alert_message": "Item song references imply objectification",
                "severity": "medium",
                "risk_weight": 20
            },
            {
                "keyword": "fair bride",
                "category": "Gender",
                "alert_message": "Combines colorism and gender stereotypes",
                "severity": "critical",
                "risk_weight": 40
            }
        ]
        
        # Write to CSV
        filepath = os.path.join(self.data_dir, "cultural_triggers.csv")
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['keyword', 'category', 'alert_message', 'severity', 'risk_weight']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for trigger in triggers:
                writer.writerow(trigger)
        
        return filepath

    
    def generate_festival_calendar(self) -> str:
        """
        Generate festival calendar CSV
        
        Creates a calendar of major Indian festivals with dates,
        sensitivity keywords, and descriptions for cultural context.
        
        Requirements: 3.3, 10.4
        
        Returns:
            Path to the generated CSV file
        """
        festivals = [
            {
                "festival_name": "Diwali",
                "date_2025": "2025-10-20",
                "sensitivity_keywords": "alcohol;meat;negative;gambling",
                "description": "Festival of lights - avoid negative themes, alcohol, meat, and gambling references"
            },
            {
                "festival_name": "Eid al-Fitr",
                "date_2025": "2025-03-30",
                "sensitivity_keywords": "pork;alcohol;non-halal",
                "description": "Islamic festival marking end of Ramadan - respect dietary restrictions"
            },
            {
                "festival_name": "Eid al-Adha",
                "date_2025": "2025-06-07",
                "sensitivity_keywords": "pork;alcohol;disrespect",
                "description": "Islamic festival of sacrifice - respect religious practices"
            },
            {
                "festival_name": "Holi",
                "date_2025": "2025-03-14",
                "sensitivity_keywords": "consent;harassment;force;non-consensual",
                "description": "Festival of colors - avoid non-consensual themes and harassment"
            },
            {
                "festival_name": "Independence Day",
                "date_2025": "2025-08-15",
                "sensitivity_keywords": "political;pakistan;anti-national;partition",
                "description": "National pride day - avoid political controversy and divisive themes"
            },
            {
                "festival_name": "Republic Day",
                "date_2025": "2025-01-26",
                "sensitivity_keywords": "political;anti-national;constitution",
                "description": "Constitutional celebration - avoid political controversy"
            },
            {
                "festival_name": "Ganesh Chaturthi",
                "date_2025": "2025-08-27",
                "sensitivity_keywords": "disrespect;mockery;religious",
                "description": "Hindu festival celebrating Lord Ganesha - respect religious sentiments"
            },
            {
                "festival_name": "Durga Puja",
                "date_2025": "2025-09-30",
                "sensitivity_keywords": "disrespect;mockery;religious;bengali",
                "description": "Major Hindu festival in Eastern India - respect religious and regional sentiments"
            },
            {
                "festival_name": "Navratri",
                "date_2025": "2025-09-22",
                "sensitivity_keywords": "alcohol;meat;non-veg;disrespect",
                "description": "Nine nights of worship - avoid alcohol, meat, and disrespectful content"
            },
            {
                "festival_name": "Dussehra",
                "date_2025": "2025-10-02",
                "sensitivity_keywords": "negative;evil;disrespect",
                "description": "Victory of good over evil - maintain positive messaging"
            },
            {
                "festival_name": "Karva Chauth",
                "date_2025": "2025-10-09",
                "sensitivity_keywords": "mockery;tradition;patriarchy",
                "description": "Traditional fasting ritual - balance respect with modern values"
            },
            {
                "festival_name": "Guru Nanak Jayanti",
                "date_2025": "2025-11-05",
                "sensitivity_keywords": "disrespect;religious;sikh",
                "description": "Sikh festival celebrating Guru Nanak - respect religious sentiments"
            },
            {
                "festival_name": "Christmas",
                "date_2025": "2025-12-25",
                "sensitivity_keywords": "disrespect;religious;christian",
                "description": "Christian festival - respect religious sentiments"
            },
            {
                "festival_name": "Makar Sankranti",
                "date_2025": "2025-01-14",
                "sensitivity_keywords": "negative;harvest",
                "description": "Harvest festival - maintain positive messaging"
            },
            {
                "festival_name": "Pongal",
                "date_2025": "2025-01-15",
                "sensitivity_keywords": "negative;harvest;tamil;south",
                "description": "Tamil harvest festival - respect regional traditions"
            },
            {
                "festival_name": "Maha Shivaratri",
                "date_2025": "2025-02-26",
                "sensitivity_keywords": "disrespect;mockery;religious;shiva",
                "description": "Hindu festival honoring Lord Shiva - respect religious sentiments"
            },
            {
                "festival_name": "Ramadan",
                "date_2025": "2025-03-01",
                "sensitivity_keywords": "food;eating;disrespect;fasting",
                "description": "Islamic month of fasting - respect fasting practices, avoid food promotion"
            },
            {
                "festival_name": "Ram Navami",
                "date_2025": "2025-04-06",
                "sensitivity_keywords": "disrespect;religious;ram;ayodhya",
                "description": "Hindu festival celebrating Lord Ram - respect religious sentiments"
            },
            {
                "festival_name": "Mahavir Jayanti",
                "date_2025": "2025-04-10",
                "sensitivity_keywords": "violence;meat;non-veg;jain",
                "description": "Jain festival - avoid violence, meat, and non-vegetarian content"
            },
            {
                "festival_name": "Buddha Purnima",
                "date_2025": "2025-05-12",
                "sensitivity_keywords": "disrespect;religious;buddhist",
                "description": "Buddhist festival celebrating Buddha's birth - respect religious sentiments"
            },
            {
                "festival_name": "Raksha Bandhan",
                "date_2025": "2025-08-09",
                "sensitivity_keywords": "sibling;family;tradition",
                "description": "Festival celebrating sibling bonds - respect family values"
            },
            {
                "festival_name": "Janmashtami",
                "date_2025": "2025-08-16",
                "sensitivity_keywords": "disrespect;mockery;krishna;religious",
                "description": "Hindu festival celebrating Lord Krishna's birth - respect religious sentiments"
            },
            {
                "festival_name": "Onam",
                "date_2025": "2025-08-28",
                "sensitivity_keywords": "negative;kerala;south;harvest",
                "description": "Kerala harvest festival - respect regional traditions"
            },
            {
                "festival_name": "Gandhi Jayanti",
                "date_2025": "2025-10-02",
                "sensitivity_keywords": "violence;disrespect;political;gandhi",
                "description": "Birth anniversary of Mahatma Gandhi - maintain non-violence and respect"
            }
        ]
        
        # Write to CSV
        filepath = os.path.join(self.data_dir, "festival_calendar.csv")
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['festival_name', 'date_2025', 'sensitivity_keywords', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for festival in festivals:
                writer.writerow(festival)
        
        return filepath

    
    def generate_historical_campaigns(self) -> str:
        """
        Generate historical campaigns CSV
        
        Creates synthetic campaign examples with realistic patterns
        of virality and backlash outcomes for the Indian market,
        including brand names, outcomes, and lessons learned.
        
        Requirements: 8.5, 10.2
        
        Returns:
            Path to the generated CSV file
        """
        campaigns = [
            # Successful campaigns
            {
                "brand": "Surf Excel",
                "campaign_name": "Holi Unity Ad",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 92,
                "outcome": "Success",
                "lessons_learned": "Positive festival messaging works when authentic and promotes unity"
            },
            {
                "brand": "Zomato",
                "campaign_name": "Delivery Hero",
                "platform": "Instagram",
                "backlash_occurred": "no",
                "virality_score": 88,
                "outcome": "Success",
                "lessons_learned": "Relatable everyday heroes resonate well with Indian audiences"
            },
            {
                "brand": "Google India",
                "campaign_name": "Reunion",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 95,
                "outcome": "Success",
                "lessons_learned": "Emotional storytelling about India-Pakistan friendship works when apolitical"
            },
            {
                "brand": "Cadbury",
                "campaign_name": "Kuch Meetha Ho Jaye",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 85,
                "outcome": "Success",
                "lessons_learned": "Celebrating small moments and traditions creates positive engagement"
            },
            {
                "brand": "Ariel",
                "campaign_name": "Share The Load",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 90,
                "outcome": "Success",
                "lessons_learned": "Progressive social messaging works when respectful and relatable"
            },
            {
                "brand": "Vicks",
                "campaign_name": "Touch of Care",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 87,
                "outcome": "Success",
                "lessons_learned": "Inclusive storytelling about transgender community resonates when authentic"
            },
            {
                "brand": "Tata Tea",
                "campaign_name": "Jaago Re",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 82,
                "outcome": "Success",
                "lessons_learned": "Social awakening campaigns work when they inspire without preaching"
            },
            {
                "brand": "Dove",
                "campaign_name": "Real Beauty India",
                "platform": "Instagram",
                "backlash_occurred": "no",
                "virality_score": 78,
                "outcome": "Success",
                "lessons_learned": "Body positivity messaging resonates when it challenges beauty standards"
            },
            {
                "brand": "Amazon India",
                "campaign_name": "Diwali Deliveries",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 84,
                "outcome": "Success",
                "lessons_learned": "Festival-themed content works when it celebrates traditions authentically"
            },
            {
                "brand": "Flipkart",
                "campaign_name": "Kids Exchange Offer",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 89,
                "outcome": "Success",
                "lessons_learned": "Humorous takes on parenting resonate across demographics"
            },
            
            # Campaigns with backlash
            {
                "brand": "Tanishq",
                "campaign_name": "Interfaith Baby Shower",
                "platform": "Instagram",
                "backlash_occurred": "yes",
                "virality_score": 85,
                "outcome": "Backlash",
                "lessons_learned": "Interfaith themes polarize - test with focus groups before launch"
            },
            {
                "brand": "Dabur",
                "campaign_name": "Karva Chauth LGBTQ",
                "platform": "Twitter",
                "backlash_occurred": "yes",
                "virality_score": 78,
                "outcome": "Backlash",
                "lessons_learned": "Traditional festivals + modern values = controversy without careful framing"
            },
            {
                "brand": "FabIndia",
                "campaign_name": "Jashn-e-Riwaaz Diwali",
                "platform": "Twitter",
                "backlash_occurred": "yes",
                "virality_score": 72,
                "outcome": "Backlash",
                "lessons_learned": "Using Urdu for Hindu festival seen as cultural appropriation by some"
            },
            {
                "brand": "Manyavar",
                "campaign_name": "Kanyamaan Dowry",
                "platform": "YouTube",
                "backlash_occurred": "yes",
                "virality_score": 68,
                "outcome": "Mixed",
                "lessons_learned": "Dowry messaging seen as tone-deaf when brand sells wedding products"
            },
            {
                "brand": "Red Label Tea",
                "campaign_name": "Free Ka Matlab",
                "platform": "YouTube",
                "backlash_occurred": "yes",
                "virality_score": 65,
                "outcome": "Backlash",
                "lessons_learned": "Caste-related messaging extremely sensitive - avoid unless expertly handled"
            },
            {
                "brand": "Myntra",
                "campaign_name": "Bold Fashion Statement",
                "platform": "Instagram",
                "backlash_occurred": "yes",
                "virality_score": 70,
                "outcome": "Backlash",
                "lessons_learned": "Logo resembling inappropriate imagery triggers backlash - test visual elements"
            },
            {
                "brand": "Surf Excel",
                "campaign_name": "Holi Stain Protection",
                "platform": "Twitter",
                "backlash_occurred": "yes",
                "virality_score": 62,
                "outcome": "Backlash",
                "lessons_learned": "Hindu-Muslim unity themes polarize in politically charged climate"
            },
            {
                "brand": "Lux",
                "campaign_name": "Fair Skin Glow",
                "platform": "Instagram",
                "backlash_occurred": "yes",
                "virality_score": 55,
                "outcome": "Backlash",
                "lessons_learned": "Fair skin messaging triggers colorism backlash - avoid completely"
            },
            {
                "brand": "Pepsi",
                "campaign_name": "Kashmir Campaign",
                "platform": "Twitter",
                "backlash_occurred": "yes",
                "virality_score": 58,
                "outcome": "Backlash",
                "lessons_learned": "Kashmir references extremely sensitive - avoid geopolitical topics"
            },
            {
                "brand": "Reebok",
                "campaign_name": "Fitness Challenge Ramadan",
                "platform": "Instagram",
                "backlash_occurred": "yes",
                "virality_score": 60,
                "outcome": "Backlash",
                "lessons_learned": "Fitness promotion during fasting month seen as insensitive"
            },
            
            # Mixed outcome campaigns
            {
                "brand": "Nike India",
                "campaign_name": "Da Da Ding",
                "platform": "YouTube",
                "backlash_occurred": "no",
                "virality_score": 81,
                "outcome": "Success",
                "lessons_learned": "Women empowerment in sports resonates when showing real athletes"
            },
            {
                "brand": "Swiggy",
                "campaign_name": "Voice of Hunger",
                "platform": "Instagram",
                "backlash_occurred": "no",
                "virality_score": 76,
                "outcome": "Success",
                "lessons_learned": "Humorous food content works across platforms and demographics"
            },
            {
                "brand": "Paytm",
                "campaign_name": "Cashless India",
                "platform": "Twitter",
                "backlash_occurred": "no",
                "virality_score": 73,
                "outcome": "Success",
                "lessons_learned": "Practical utility messaging resonates during relevant moments"
            },
            {
                "brand": "Amul",
                "campaign_name": "Topical Ads",
                "platform": "Twitter",
                "backlash_occurred": "no",
                "virality_score": 86,
                "outcome": "Success",
                "lessons_learned": "Timely, witty commentary on current events works when apolitical"
            },
            {
                "brand": "Ola",
                "campaign_name": "Chalo Niklo",
                "platform": "Instagram",
                "backlash_occurred": "no",
                "virality_score": 74,
                "outcome": "Success",
                "lessons_learned": "Travel and exploration themes resonate with aspirational audiences"
            }
        ]
        
        # Write to CSV
        filepath = os.path.join(self.data_dir, "historical_campaigns.csv")
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['brand', 'campaign_name', 'platform', 'backlash_occurred', 
                         'virality_score', 'outcome', 'lessons_learned']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for campaign in campaigns:
                writer.writerow(campaign)
        
        return filepath
    
    def generate_all(self) -> Dict[str, str]:
        """
        Generate all synthetic datasets
        
        Returns:
            Dictionary with paths to all generated files
        """
        return {
            'cultural_triggers': self.generate_cultural_triggers(),
            'festival_calendar': self.generate_festival_calendar(),
            'historical_campaigns': self.generate_historical_campaigns()
        }


# Convenience function for easy import
def generate_synthetic_data(data_dir: str = "Data") -> Dict[str, str]:
    """
    Generate all synthetic datasets
    
    Args:
        data_dir: Directory where data files will be saved
        
    Returns:
        Dictionary with paths to all generated files
    """
    generator = SyntheticDataGenerator(data_dir)
    return generator.generate_all()


if __name__ == "__main__":
    # Generate data when run as script
    print("Generating synthetic data...")
    paths = generate_synthetic_data()
    print("\nGenerated files:")
    for name, path in paths.items():
        print(f"  {name}: {path}")
    print("\nSynthetic data generation complete!")
