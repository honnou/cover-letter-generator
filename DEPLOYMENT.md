# Deployment Guide

This guide will help you deploy the Cover Letter Generator to Vercel, giving you a public URL that you can access from anywhere and save to your mobile home screen.

## Prerequisites

- A [Vercel account](https://vercel.com) (free tier is perfect)
- [Vercel CLI](https://vercel.com/docs/cli) installed (optional, but recommended)
- An Anthropic API key (optional, for AI-powered generation)

## Option 1: Deploy via Vercel CLI (Recommended)

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Login to Vercel

```bash
vercel login
```

### Step 3: Deploy from this directory

```bash
cd cover-letter-generator
vercel
```

Follow the prompts:
- **Set up and deploy?** Yes
- **Which scope?** Choose your account
- **Link to existing project?** No (for first deployment)
- **What's your project name?** cover-letter-generator (or your choice)
- **In which directory is your code located?** ./ (current directory)

### Step 4: Configure Environment Variables

After deployment, add your AI API key:

```bash
vercel env add ANTHROPIC_API_KEY
```

When prompted:
- **What's the value?** Paste your Anthropic API key
- **Add to which environments?** Select Production, Preview, and Development

Or via the Vercel Dashboard:
1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** Your API key from https://console.anthropic.com/
   - **Environments:** Production, Preview, Development

### Step 5: Redeploy with API Key

```bash
vercel --prod
```

Your app will be live at: `https://your-project.vercel.app`

## Option 2: Deploy via Vercel Dashboard

### Step 1: Push to GitHub

If you haven't already:

```bash
git init
git add .
git commit -m "Add Cover Letter Generator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cover-letter-generator.git
git push -u origin main
```

### Step 2: Import to Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Click "Import Project"
3. Import your GitHub repository
4. Vercel will auto-detect the configuration from `vercel.json`
5. Click "Deploy"

### Step 3: Add Environment Variables

1. Go to your project settings in Vercel
2. Navigate to "Environment Variables"
3. Add:
   - **Name:** `ANTHROPIC_API_KEY`
   - **Value:** Your API key from https://console.anthropic.com/
   - **Environments:** Production, Preview, Development
4. Redeploy the project

## Accessing Your Deployed App

### On Desktop

Simply visit your Vercel URL: `https://your-project.vercel.app`

### On Mobile (iPhone/Android)

1. Open Safari (iPhone) or Chrome (Android)
2. Navigate to your Vercel URL
3. **iPhone:** Tap Share → "Add to Home Screen"
4. **Android:** Tap Menu → "Add to Home Screen"

Now you have an app-like icon that opens your Cover Letter Generator!

## Custom Domain (Optional)

Want a custom domain like `coverletters.yourdomain.com`?

1. Go to your project settings in Vercel
2. Navigate to "Domains"
3. Add your custom domain
4. Follow the DNS configuration instructions

## Updating Your Deployment

### If using CLI:

```bash
cd cover-letter-generator
vercel --prod
```

### If using GitHub integration:

Just push to your repository:

```bash
git add .
git commit -m "Update cover letter generator"
git push
```

Vercel will automatically redeploy!

## Monitoring and Logs

- **View logs:** `vercel logs`
- **View in dashboard:** https://vercel.com/dashboard

## Troubleshooting

### Build fails

- Check that all files are committed
- Verify `vercel.json` is present and valid
- Check build logs in Vercel dashboard

### API calls fail

- Verify environment variables are set correctly
- Check function logs in Vercel dashboard
- Ensure API key is valid

### File uploads don't work

- Vercel has a 4.5MB limit for serverless functions
- For large files, consider using Vercel Blob storage
- Or use client-side file reading (read in browser, send text only)

## Cost

The free Vercel tier includes:
- Unlimited deployments
- 100GB bandwidth per month
- Serverless function executions
- Automatic HTTPS

Perfect for personal use!

## Need Help?

- [Vercel Documentation](https://vercel.com/docs)
- [Vercel Community](https://github.com/vercel/vercel/discussions)
- Check your deployment logs for errors

---

**🎉 Once deployed, share your URL and let others use your tool too!**
