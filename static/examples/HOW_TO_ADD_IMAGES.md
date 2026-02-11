# How to Add Sample Images for Testing

## Quick Start

The AdsenseAI system can analyze images along with text. To test this feature, you can add sample images to this folder.

## Where to Place Images

Place your test images in this folder:
```
static/examples/images/
```

## ✅ Sample Images Available (25 Total)

We have created 25 diverse sample images for comprehensive testing:

### Safe Images (10) - Expected: ✅ Green
1. **diwali_safe.jpg** - Diwali celebration theme
2. **diwali_celebration_safe.jpg** - Festival of Lights
3. **indian_flag_safe.jpg** - Indian patriotic theme
4. **republic_day_safe.jpg** - Republic Day celebration
5. **diversity_safe.jpg** - Unity in diversity theme
6. **unity_diversity_safe.jpg** - Incredible India theme
7. **holi_colors_safe.jpg** - Holi festival theme
8. **eid_mubarak_safe.jpg** - Eid celebration
9. **christmas_joy_safe.jpg** - Christmas celebration
10. **onam_festival_safe.jpg** - Kerala harvest festival
11. **pongal_harvest_safe.jpg** - Tamil harvest festival
12. **ganesh_chaturthi_safe.jpg** - Ganesh Chaturthi

### Moderate Risk Images (7) - Expected: ⚠️ Yellow
1. **festival_food_moderate.jpg** - Food promotion
2. **food_promo_moderate.jpg** - Food festival
3. **beauty_products_moderate.jpg** - Beauty products
4. **beauty_glow_moderate.jpg** - Skincare promotion
5. **sale_discount_moderate.jpg** - Mega sale promotion
6. **fitness_body_moderate.jpg** - Fitness transformation
7. **alcohol_party_moderate.jpg** - Party theme

### Risky Images (6) - Expected: 🛑 Red (For Testing Detection Only)
1. **fair_skin_risky.jpg** - Colorism trigger
2. **political_debate_risky.jpg** - Political controversy
3. **border_tension_risky.jpg** - Geopolitical sensitivity
4. **religious_comparison_risky.jpg** - Religious sensitivity
5. **caste_reference_risky.jpg** - Caste/class sensitivity
6. **meat_festival_risky.jpg** - Religious dietary sensitivity

📖 **See [SAMPLE_IMAGES_DOCUMENTATION.md](SAMPLE_IMAGES_DOCUMENTATION.md) for detailed expected results and test captions.**

These are placeholder images with text overlays. For production testing, use real stock photos.

## Recommended Test Images

### Safe Campaign Images (Expected: Low Risk)
- **Diwali Diyas**: Traditional oil lamps, rangoli patterns
- **Indian Flag**: National flag, patriotic symbols
- **Diverse Celebrations**: People of different backgrounds celebrating together
- **Traditional Festivals**: Holi colors, Eid celebrations, Christmas decorations
- **Unity Themes**: Hands joined together, diverse group photos

### Moderate Risk Images (Expected: Medium Risk)
- **Food Items**: Various cuisines, restaurant dishes
- **Beauty Products**: Cosmetics, skincare items (without skin tone focus)
- **Festival Scenes**: Crowded celebrations, religious gatherings

### High Risk Images (For Testing Detection Only)
- **Colorism Indicators**: Before/after skin lightening ads
- **Religious Symbols**: Isolated religious imagery without context
- **Political Content**: Political figures, controversial symbols

## Image Guidelines

### Format
- **Supported**: JPEG, PNG, GIF, WebP
- **Max Size**: 10MB
- **Recommended Size**: 800x800 to 1920x1080 pixels

### Quality
- Use clear, high-resolution images
- Avoid blurry or pixelated images
- Ensure good lighting and visibility

## How to Use Images in Testing

### Method 1: Drag and Drop
1. Open http://localhost:8000
2. Drag an image from your file explorer
3. Drop it onto the "Campaign Image" upload area
4. See the preview appear
5. Click "Analyze Campaign"

### Method 2: Click to Upload
1. Click on the "Campaign Image" upload area
2. Browse and select an image
3. See the preview appear
4. Click "Analyze Campaign"

## What the System Analyzes in Images

The Google Gemini API analyzes:

1. **Visual Emotions**: Joy, pride, celebration, anger, fear
2. **Cultural Symbols**: Religious symbols, national symbols, traditional elements
3. **Skin Tone Representation**: Colorism indicators, diversity
4. **Text Overlays**: Any text visible in the image
5. **Brand Elements**: Logos, product placements
6. **Festival References**: Diwali lamps, Eid crescents, Christmas trees
7. **Sensitivity Triggers**: Controversial imagery, inappropriate content

## Example Test Scenarios

### Scenario 1: Safe Diwali Campaign
**Text**: "Celebrating India's diversity this Diwali! 🪔"
**Image**: Diwali diyas with rangoli
**Expected**: ✅ Green recommendation, high virality, low backlash

### Scenario 2: Festival Food (Moderate Risk)
**Text**: "Enjoy our special meat dishes this festive season!"
**Image**: Food platter with meat items
**Expected**: ⚠️ Yellow recommendation, moderate backlash

### Scenario 3: Colorism Detection (High Risk)
**Text**: "Fair skin is the key to beauty!"
**Image**: Before/after skin lightening comparison
**Expected**: 🛑 Red recommendation, high backlash, critical alerts

## Generating Your Own Test Images

If you don't have sample images, you can:

1. **Use Free Stock Photos**:
   - Unsplash.com
   - Pexels.com
   - Pixabay.com
   - Search for: "Diwali", "Indian festival", "diversity", etc.

2. **Create Simple Graphics**:
   - Use Canva.com (free)
   - Create festival-themed designs
   - Add text overlays for testing

3. **Screenshot Examples**:
   - Take screenshots of social media posts
   - Use for testing purposes only

## Privacy & Ethics

⚠️ **Important**:
- Only use images you have rights to use
- Don't use images of real people without permission
- Test images are for development purposes only
- Don't share sensitive or private images

## Troubleshooting

### Image Not Uploading
- Check file size (must be under 10MB)
- Verify file format (JPEG, PNG, GIF, WebP)
- Try a different browser

### No Image Analysis Results
- Ensure GEMINI_API_KEY is set in .env file
- Check server logs for API errors
- Verify internet connection

### Slow Analysis
- Large images take longer to process
- Gemini API may have rate limits
- Consider resizing images to 1920x1080 or smaller

## API Key Setup

To enable image analysis, you need a Gemini API key:

1. Visit: https://makersuite.google.com/app/apikey
2. Create a new API key (free tier available)
3. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```
4. Restart the server

## Need Help?

- Check the main README.md for setup instructions
- Review EXAMPLE_CAMPAIGNS.md for text examples
- Check server logs for error messages

---

*Happy Testing! 🎉*
