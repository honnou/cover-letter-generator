# 🚀 Quick Start - Deploy Your Cover Letter Generator

This is a **standalone repository** ready to deploy to Vercel! Follow these simple steps:

## Step 1: Push to GitHub

### Option A: Using the Setup Script (Easiest)

```bash
cd /home/user/cover-letter-generator-standalone
./setup-github.sh
```

Then:
1. Go to [github.com/new](https://github.com/new)
2. Create a new repository named `cover-letter-generator`
3. **Don't** initialize with README or .gitignore
4. Run: `git push -u origin main`

### Option B: Manual Setup

1. **Create a new repository on GitHub:**
   - Go to [github.com/new](https://github.com/new)
   - Name: `cover-letter-generator`
   - Description: AI-powered cover letter generator
   - Public or Private (your choice)
   - **Don't** check any initialization options
   - Click "Create repository"

2. **Push your code:**
   ```bash
   cd /home/user/cover-letter-generator-standalone
   git remote add origin https://github.com/YOUR_USERNAME/cover-letter-generator.git
   git branch -M main
   git push -u origin main
   ```

## Step 2: Deploy to Vercel

### From Your Computer:

1. **Clone the repository you just created:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/cover-letter-generator.git
   cd cover-letter-generator
   ```

2. **Deploy to Vercel:**
   ```bash
   npx vercel
   ```

   - Log in to Vercel (or create free account)
   - Follow the prompts (press Enter for defaults)
   - **You'll get your URL!** 🎉

3. **Add your Anthropic API key (optional but recommended):**
   ```bash
   npx vercel env add ANTHROPIC_API_KEY
   ```
   - Paste your API key from [console.anthropic.com](https://console.anthropic.com/)
   - Select: Production, Preview, Development

4. **Redeploy with API key:**
   ```bash
   npx vercel --prod
   ```

### Or Via Vercel Dashboard (Even Easier!):

1. **Go to:** [vercel.com/new](https://vercel.com/new)
2. **Import** your `cover-letter-generator` repository from GitHub
3. **Deploy** (no configuration needed!)
4. **Add API key:**
   - Go to Project Settings → Environment Variables
   - Add: `ANTHROPIC_API_KEY` = your key
   - Redeploy

## Step 3: Save to Your Home Screen 📱

**Your Vercel URL:** `https://cover-letter-generator-xyz.vercel.app`

**On iPhone:**
1. Open URL in Safari
2. Share → "Add to Home Screen"
3. Name it "Cover Letter Generator"

**On Android:**
1. Open URL in Chrome
2. Menu → "Add to Home Screen"

## 🔑 Get Your Anthropic API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign in or create account
3. Navigate to API Keys
4. Click "Create Key"
5. Copy the key (starts with `sk-ant-...`)
6. Add credits to your account ($5 free to start)

**Cost:** About $0.003 per cover letter (very affordable!)

## ✅ That's It!

You now have:
- ✅ Your own deployed cover letter generator
- ✅ A public URL you can access anywhere
- ✅ A mobile app-like experience
- ✅ Free hosting on Vercel

**Any issues?** Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed troubleshooting.
