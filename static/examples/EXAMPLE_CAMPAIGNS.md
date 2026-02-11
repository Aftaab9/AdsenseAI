# Example Campaigns for Testing

## Safe Campaigns (Expected: GREEN - Good to Post)

### Example 1: Diwali Celebration
**Caption:** `Celebrating India's diversity this Diwali! 🪔 Join us in spreading joy and light across the nation. #HappyDiwali #IndianFestival`

**Platform:** Instagram

**Posting Date:** 2025-10-18

**Influencer:** Yes

**Expected Results:**
- ✅ High Virality Score (80-90)
- ✅ Low Backlash Risk (10-20)
- ✅ Positive Sentiment
- ✅ No Cultural Alerts

---

### Example 2: Unity in Diversity
**Caption:** `India's strength lies in its beautiful diversity. Every culture, every tradition makes us stronger together. 🇮🇳 #UnityInDiversity #IncredibleIndia`

**Platform:** YouTube

**Influencer:** No

**Expected Results:**
- ✅ High Virality Score (75-85)
- ✅ Low Backlash Risk (5-15)
- ✅ Positive Sentiment
- ✅ No Cultural Alerts

---

### Example 3: Independence Day Pride
**Caption:** `Proud to be Indian! 🇮🇳 Celebrating 78 years of freedom and progress. Jai Hind! #IndependenceDay #ProudIndian`

**Platform:** Instagram

**Posting Date:** 2025-08-15

**Influencer:** Yes

**Expected Results:**
- ✅ Very High Virality Score (85-95)
- ✅ Very Low Backlash Risk (0-10)
- ✅ Strong Positive Sentiment
- ✅ No Cultural Alerts

---

## Moderate Risk Campaigns (Expected: YELLOW - Review Required)

### Example 4: Festival Food Promotion
**Caption:** `Enjoy our special meat dishes this festive season! Limited time offer on all non-veg items. #FestiveFood #SpecialOffer`

**Platform:** Instagram

**Posting Date:** 2025-10-18 (near Diwali)

**Influencer:** No

**Expected Results:**
- ⚠️ Moderate Virality Score (40-60)
- ⚠️ Moderate Backlash Risk (40-60)
- ⚠️ Festival Proximity Alert
- ⚠️ Cultural Sensitivity Warning

---

### Example 5: Beauty Standards
**Caption:** `Get glowing skin this season! Our new range helps you achieve that radiant, fair complexion you've always wanted. #BeautyGoals #GlowingSkin`

**Platform:** Twitter

**Influencer:** Yes

**Expected Results:**
- ⚠️ Moderate Virality Score (50-65)
- ⚠️ High Backlash Risk (50-70)
- ⚠️ Colorism Alert (fair complexion reference)
- ⚠️ Mixed Sentiment

---

## High Risk Campaigns (Expected: RED - Do Not Post)

### Example 6: Colorism & Beauty
**Caption:** `Fair skin is the key to beauty! Get our whitening cream now and transform your complexion. Be fair, be beautiful! #FairSkin #BeautyStandards`

**Platform:** Twitter

**Influencer:** No

**Expected Results:**
- 🛑 Low Virality Score (20-40)
- 🛑 Very High Backlash Risk (80-95)
- 🛑 Critical Colorism Alerts
- 🛑 Negative Perceived Intent
- 🛑 Multiple Cultural Triggers

---

### Example 7: Geopolitical Controversy
**Caption:** `Pakistan vs India - who's better? Let's settle this debate once and for all! Share your thoughts on Kashmir issue. #IndoPak #Controversy`

**Platform:** Twitter

**Influencer:** No

**Expected Results:**
- 🛑 Moderate Virality Score (60-70) - controversial content spreads
- 🛑 Very High Backlash Risk (85-100)
- 🛑 Critical Geopolitical Alerts (Pakistan, Kashmir)
- 🛑 Very Negative Perceived Intent
- 🛑 High Ad-Fatigue Risk

---

### Example 8: Religious Insensitivity
**Caption:** `Try our new beef burger special! Perfect for breaking your fast. Also serving pork dishes during Ramadan. #FoodLovers #SpecialMenu`

**Platform:** Instagram

**Posting Date:** 2025-03-15 (during Ramadan)

**Influencer:** No

**Expected Results:**
- 🛑 Very Low Virality Score (10-25)
- 🛑 Extremely High Backlash Risk (90-100)
- 🛑 Multiple Critical Religious Alerts (beef, pork, Ramadan)
- 🛑 Festival Sensitivity Alert
- 🛑 Extremely Negative Perceived Intent

---

## How to Test with Images

### For Safe Campaigns:
- Use images with: Diya lamps, Indian flags, diverse people celebrating, traditional decorations
- Avoid: Religious symbols, political imagery, skin tone focus

### For Moderate Risk:
- Use images with: Food items, beauty products, festival scenes
- May include: Subtle cultural elements that need context

### For High Risk:
- Avoid testing with: Images showing colorism, religious conflicts, political statements
- These are for demonstration of the detection system only

---

## Testing Instructions

1. **Copy the caption** from any example above
2. **Select the platform** mentioned
3. **Set the posting date** if specified
4. **Check influencer** if mentioned
5. **Upload an image** (optional) - see image guidelines above
6. **Click "Analyze Campaign"**
7. **Compare results** with expected outcomes

---

## Image Upload Testing

We have **25 sample images** available in `static/examples/images/`:

| Category | Count | Examples |
|----------|-------|----------|
| Safe | 12 | Diwali, Republic Day, Eid, Christmas, Holi, Onam, Pongal |
| Moderate | 7 | Food promo, Beauty products, Sale, Fitness, Party |
| Risky | 6 | Colorism, Political, Geopolitical, Religious, Caste |

📖 **See [SAMPLE_IMAGES_DOCUMENTATION.md](SAMPLE_IMAGES_DOCUMENTATION.md) for:**
- Detailed expected scores for each image
- Suggested test captions
- Cultural alerts to expect
- Why risky images fail

### Quick Test Combinations

**Safe Test:**
- Image: `diwali_celebration_safe.jpg`
- Caption: "Celebrating India's diversity this Diwali! 🪔"
- Expected: ✅ Green, Virality 80-90, Backlash 5-15

**Moderate Test:**
- Image: `beauty_glow_moderate.jpg`
- Caption: "Achieve your glow goals! ✨ Our new skincare range."
- Expected: ⚠️ Yellow, Virality 55-70, Backlash 35-55

**Risky Test:**
- Image: `fair_skin_risky.jpg`
- Caption: "Fair skin is the key to beauty!"
- Expected: 🛑 Red, Virality 30-50, Backlash 75-95

---

*Note: These examples are for testing the AdsenseAI system's detection capabilities. Always use culturally sensitive and respectful content in real campaigns.*
