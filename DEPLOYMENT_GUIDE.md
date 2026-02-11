# Deployment Guide - AdsenseAI Campaign Risk Analyzer

## 🚀 Deploy to Render (Recommended - FREE)

Render is the easiest platform to deploy FastAPI applications with a free tier.

### Prerequisites
1. GitHub account
2. Render account (free): https://render.com
3. Your Gemini API key

### Step-by-Step Deployment

#### 1. Push Code to GitHub

**Create a new repository on GitHub:**
1. Go to https://github.com/new
2. Name: `adsenseai-campaign-analyzer`
3. Make it Public or Private
4. Don't initialize with README (we have one)
5. Click "Create repository"

**Push your code:**
```bash
# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - AdsenseAI Campaign Risk Analyzer"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/adsenseai-campaign-analyzer.git

# Push
git branch -M main
git push -u origin main
```

#### 2. Deploy on Render

**Option A: Using render.yaml (Automatic)**

1. Go to https://render.com/dashboard
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Click "Apply"
6. Add environment variable:
   - Key: `GEMINI_API_KEY`
   - Value: Your Gemini API key
7. Click "Create Web Service"

**Option B: Manual Setup**

1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** adsenseai-campaign-analyzer
   - **Region:** Singapore (or closest to you)
   - **Branch:** main
   - **Runtime:** Python 3
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python -m textblob.download_corpora
     ```
   - **Start Command:**
     ```
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Plan:** Free
5. Add Environment Variables:
   - `GEMINI_API_KEY`: Your API key
   - `PYTHON_VERSION`: 3.9.18
6. Click "Create Web Service"

#### 3. Wait for Deployment

- First deployment takes 5-10 minutes
- Render will:
  - Install Python
  - Install dependencies
  - Download TextBlob corpora
  - Start the server
- Watch the logs in real-time

#### 4. Access Your App

Once deployed, you'll get a URL like:
```
https://adsenseai-campaign-analyzer.onrender.com
```

**Test it:**
- Main app: https://your-app.onrender.com
- API docs: https://your-app.onrender.com/docs
- Health check: https://your-app.onrender.com/api/health

### Important Notes

**Free Tier Limitations:**
- ⚠️ App sleeps after 15 minutes of inactivity
- ⚠️ First request after sleep takes 30-60 seconds to wake up
- ✅ 750 hours/month free (enough for testing)
- ✅ Auto-deploys on git push

**To Keep App Awake:**
- Upgrade to paid plan ($7/month)
- Or use a service like UptimeRobot to ping every 14 minutes

---

## 🚂 Deploy to Railway (Alternative - FREE Trial)

Railway offers $5 free credit per month.

### Steps

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Python
6. Add environment variables:
   - `GEMINI_API_KEY`: Your API key
7. Deploy!

**Your URL:** `https://your-app.up.railway.app`

---

## ☁️ Deploy to Google Cloud Run (Scalable)

For production use with auto-scaling.

### Prerequisites
- Google Cloud account
- Docker installed
- gcloud CLI installed

### Steps

#### 1. Create Dockerfile

Already created in your project root.

#### 2. Build and Deploy

```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Build
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/adsenseai

# Deploy
gcloud run deploy adsenseai \
  --image gcr.io/YOUR_PROJECT_ID/adsenseai \
  --platform managed \
  --region asia-south1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key_here
```

**Your URL:** `https://adsenseai-xxxxx-as.a.run.app`

---

## 📦 Files Created for Deployment

### 1. `render.yaml`
Configuration for Render deployment (Blueprint)

### 2. `Procfile`
Tells platforms how to start the app

### 3. `runtime.txt`
Specifies Python version

### 4. `.gitignore`
Excludes unnecessary files from git

### 5. `Dockerfile` (if needed)
For containerized deployment

---

## 🔧 Environment Variables

Make sure to set these on your deployment platform:

| Variable | Required | Description |
|----------|----------|-------------|
| `GEMINI_API_KEY` | Yes | Google Gemini API key for image analysis |
| `PYTHON_VERSION` | No | Python version (default: 3.9.18) |
| `PORT` | No | Auto-set by platform |

---

## 🧪 Testing Deployment

After deployment, test these endpoints:

```bash
# Health check
curl https://your-app.onrender.com/api/health

# API docs
open https://your-app.onrender.com/docs

# Test analysis
curl -X POST https://your-app.onrender.com/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "caption": "Test campaign",
    "platform": "Instagram",
    "posting_date": "2026-02-11"
  }'
```

---

## 🐛 Troubleshooting

### Build Fails

**Error: "Could not find a version that satisfies..."**
- Check `requirements.txt` has correct versions
- Try: `pip install -r requirements.txt` locally first

**Error: "TextBlob corpora not found"**
- Add to build command: `python -m textblob.download_corpora`

### App Crashes

**Check logs:**
- Render: Dashboard → Logs tab
- Railway: Dashboard → Deployments → Logs
- Cloud Run: Cloud Console → Logs

**Common issues:**
- Missing environment variables
- Port binding (use `$PORT` not `8000`)
- File paths (use relative paths)

### Slow Response

**Free tier limitations:**
- App sleeps after inactivity
- First request wakes it up (30-60s)
- Solution: Upgrade to paid tier or use ping service

---

## 💰 Cost Comparison

| Platform | Free Tier | Paid | Best For |
|----------|-----------|------|----------|
| **Render** | 750 hrs/month | $7/month | Testing, demos |
| **Railway** | $5 credit/month | Pay-as-you-go | Small projects |
| **Cloud Run** | 2M requests/month | Pay-per-use | Production |
| **Heroku** | None | $7/month | Legacy apps |

---

## 🎯 Recommended: Render

For your use case, **Render is the best choice** because:
- ✅ Free tier available
- ✅ Easy setup (5 minutes)
- ✅ Auto-deploys from GitHub
- ✅ Good for demos and testing
- ✅ Can upgrade later if needed

---

## 📝 Next Steps

1. **Push to GitHub** (see Step 1 above)
2. **Deploy to Render** (see Step 2 above)
3. **Test your deployment**
4. **Share your URL!**

Your app will be live at:
```
https://adsenseai-campaign-analyzer.onrender.com
```

---

## 🆘 Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- Cloud Run Docs: https://cloud.google.com/run/docs

---

**Ready to deploy? Start with Step 1: Push to GitHub!** 🚀
