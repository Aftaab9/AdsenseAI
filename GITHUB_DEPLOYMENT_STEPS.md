# GitHub Deployment - Step by Step

## 📋 Overview

This guide will help you push **only the essential files** to GitHub (username: **Aftaab9**) and deploy to Render.

## ✅ What's Been Done

1. **Updated `.gitignore`** - Excludes all unnecessary files:
   - Test files (`test_*.py`)
   - Example files (`example_*.py`)
   - Debug files (`debug_*.py`)
   - Documentation files (`TASK_*.md`, `*_SUMMARY.md`)
   - UI folders (Next.js - not needed)
   - Batch files (`*.bat`)
   - IDE folders (`.vscode/`, `.kiro/`)

2. **Created deployment files**:
   - `render.yaml` - Render configuration
   - `Procfile` - Start command
   - `runtime.txt` - Python version
   - `.gitignore` - File exclusions

## 🚀 Deployment Steps

### Step 1: Check What Will Be Committed

Run this to see which files will be included:

```bash
python check_files.py
```

This will show you:
- All files that will be committed
- Total file count (should be ~50 files)
- Any unwanted files detected

### Step 2: Initialize Git

```bash
git init
```

### Step 3: Add Files

```bash
git add .
```

The `.gitignore` will automatically exclude unnecessary files.

### Step 4: Verify Files

```bash
# See what will be committed
git status

# Count files
git ls-files | wc -l
```

You should see approximately **50 essential files**.

### Step 5: Commit

```bash
git commit -m "Initial commit - AdsenseAI Campaign Risk Analyzer"
```

### Step 6: Create GitHub Repository

**Option A: Create on GitHub Website**
1. Go to https://github.com/new
2. Repository name: `adsenseai-campaign-analyzer`
3. Description: "AI-powered campaign risk analyzer for Indian market"
4. Make it **Public** (required for free Render deployment)
5. **Don't** initialize with README
6. Click "Create repository"

**Option B: Use GitHub CLI** (if installed)
```bash
gh repo create adsenseai-campaign-analyzer --public --source=. --remote=origin
```

### Step 7: Add Remote

```bash
git remote add origin https://github.com/Aftaab9/adsenseai-campaign-analyzer.git
```

### Step 8: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

### Step 9: Verify on GitHub

1. Go to https://github.com/Aftaab9/adsenseai-campaign-analyzer
2. Check that only essential files are there
3. Should see:
   - `app/` folder
   - `Data/` folder
   - `templates/` folder
   - `static/` folder
   - `requirements.txt`
   - `README.md`
   - `render.yaml`
   - etc.

## 🎯 Deploy to Render

### Step 1: Sign Up on Render

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub (use Aftaab9 account)

### Step 2: Create New Web Service

1. Click "New +" → "Blueprint"
2. Connect your GitHub account
3. Select repository: `adsenseai-campaign-analyzer`
4. Render will detect `render.yaml` automatically
5. Click "Apply"

### Step 3: Add Environment Variable

1. In the Render dashboard, go to your service
2. Click "Environment" tab
3. Add variable:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Your Gemini API key
4. Click "Save Changes"

### Step 4: Deploy

1. Render will automatically start deploying
2. Watch the logs in real-time
3. Deployment takes 5-10 minutes
4. Status will change to "Live" when ready

### Step 5: Access Your App

Your app will be live at:
```
https://adsenseai-campaign-analyzer.onrender.com
```

Test it:
- Main app: https://adsenseai-campaign-analyzer.onrender.com
- API docs: https://adsenseai-campaign-analyzer.onrender.com/docs
- Health: https://adsenseai-campaign-analyzer.onrender.com/api/health

## 📊 Expected Results

### Files on GitHub
- **~50 essential files** (not 200+)
- No test files
- No example files
- No documentation clutter
- Clean, production-ready code

### Render Deployment
- **Build time:** 5-10 minutes
- **Status:** Live
- **URL:** https://adsenseai-campaign-analyzer.onrender.com
- **Free tier:** 750 hours/month

## 🔧 Troubleshooting

### "Too many files in git status"

```bash
# Clear git cache
git rm -r --cached .

# Re-add with updated gitignore
git add .

# Check again
git status
```

### "Repository already exists"

```bash
# Remove old remote
git remote remove origin

# Add new remote
git remote add origin https://github.com/Aftaab9/adsenseai-campaign-analyzer.git

# Force push
git push -u origin main --force
```

### "Build failed on Render"

Check Render logs for errors. Common issues:
- Missing `GEMINI_API_KEY` environment variable
- Wrong Python version (should be 3.9.18)
- Missing dependencies in `requirements.txt`

### "App is slow to respond"

Free tier apps sleep after 15 minutes of inactivity.
- First request after sleep takes 30-60 seconds
- Subsequent requests are fast
- Upgrade to paid tier ($7/month) to keep app always on

## ✅ Checklist

- [ ] Run `python check_files.py` to verify files
- [ ] Initialize git: `git init`
- [ ] Add files: `git add .`
- [ ] Commit: `git commit -m "Initial commit"`
- [ ] Create GitHub repo (public)
- [ ] Add remote: `git remote add origin ...`
- [ ] Push: `git push -u origin main`
- [ ] Verify on GitHub
- [ ] Sign up on Render
- [ ] Create Blueprint from repo
- [ ] Add `GEMINI_API_KEY` environment variable
- [ ] Wait for deployment
- [ ] Test the live URL

## 🎉 Success!

Once deployed, your app will be accessible at:
```
https://adsenseai-campaign-analyzer.onrender.com
```

Share this URL with anyone - it's live on the internet! 🌐

---

**Need help?** Check:
- `DEPLOYMENT_GUIDE.md` - Detailed deployment guide
- `DEPLOY_TO_GITHUB.md` - GitHub-specific instructions
- Render docs: https://render.com/docs
