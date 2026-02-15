# 🚀 QUICK START GUIDE

**Your complete job monitoring system (Option C - Hybrid) is ready!**

---

## ⚡ What You Have

**✅ Complete working system with:**
- Daily Greenhouse scraping (25 EdTech companies, FREE)
- Geography-based API rotation (USA/Singapore/Dubai)
- AI-powered job matching (Google Gemini)
- **🌐 Beautiful HTML Dashboard** (access from any device)
- Email alerts (immediate + daily digest) - OPTIONAL
- GitHub Actions automation

**📊 Expected Results:**
- 10-30 new jobs daily
- 3-8 quality matches daily
- **Dashboard updates daily automatically**
- **$0/month cost** (all free tiers)

---

## 🎯 3-STEP SETUP (60 minutes total)

### STEP 1: Get API Keys (30 min)

**Google AI Studio** → https://aistudio.google.com/
- Click "Get API key"
- Copy key (starts with AIza...)
- FREE: 1500 requests/day

**Adzuna** → https://developer.adzuna.com/signup
- Create account
- Create application
- Copy App ID and App Key
- FREE: 250 calls/month

**SendGrid** → https://signup.sendgrid.com/
- Create account
- Settings → API Keys → Create
- Settings → Sender Authentication → Verify sender email
- Copy API key and verified email
- FREE: 100 emails/day

---

### STEP 2: GitHub Setup (15 min)

**Create repository:**
1. Go to github.com → New repository
2. Name: `job-monitor`
3. Private
4. Create

**Upload code:**
```bash
cd job-monitor  # (the folder you downloaded)
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/job-monitor.git
git push -u origin main
```

**Add secrets:**
1. Go to repo → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each:
   - `GOOGLE_AI_KEY`
   - `ADZUNA_APP_ID`
   - `ADZUNA_APP_KEY`

**Optional (if you want email alerts):**
   - `SENDGRID_API_KEY`
   - `EMAIL_FROM` (your verified sender)
   - `EMAIL_TO` (your personal email)

**Enable GitHub Pages (for dashboard):**
1. Settings → Pages
2. Source: "Deploy from a branch"
3. Branch: "main", Folder: "/ (root)"
4. Save
5. Your dashboard will be at: `https://YOUR_USERNAME.github.io/job-monitor/dashboard.html`
6. **📱 Bookmark this URL!**

**See GITHUB_PAGES_SETUP.md for detailed instructions.**

---

### STEP 3: Test & Deploy (15 min)

**Local test (optional):**
```bash
pip install -r requirements.txt

# Set environment variables (or run setup.sh)
export GOOGLE_AI_KEY="your_key"
export ADZUNA_APP_ID="your_id"
export ADZUNA_APP_KEY="your_key"
export SENDGRID_API_KEY="your_key"
export EMAIL_FROM="verified@email.com"
export EMAIL_TO="your@email.com"

# Run
python main.py
```

**Enable automation:**
1. GitHub repo → Actions tab
2. Enable workflows
3. Click "Daily Job Monitor" → "Run workflow"
4. Wait 10 minutes
5. Check your email! 📧

---

## 📁 File Structure

```
job-monitor/
├── README.md              ← Full documentation
├── QUICKSTART.md          ← This file
├── setup.sh               ← Automated setup script
├── config.py              ← Configuration (customize here)
├── main.py                ← Main orchestrator
├── ai_filter.py           ← AI matching
├── database.py            ← Job tracking
├── alerter.py             ← Email alerts
├── scrapers/
│   ├── greenhouse.py      ← Greenhouse scraper
│   └── adzuna.py          ← API search
├── .github/workflows/
│   └── daily-job-check.yml ← GitHub Actions
└── requirements.txt       ← Dependencies
```

---

## ⚙️ Quick Customization

**Change your profile** → Edit `config.py`:
```python
YOUR_PROFILE = """
Your experience...
Your skills...
Your interests...
"""
```

**Add companies** → Edit `config.py`:
```python
GREENHOUSE_COMPANIES = [
    "anthropic",
    "new-company-here",  # Add more
]
```

**Adjust frequency** → Edit `config.py`:
```python
GEOGRAPHIES = {
    "USA": {"check_frequency": 1},  # Daily
    "Singapore": {"check_frequency": 2},  # Every 2 days
}
```

---

## 📧 What You'll Get

**🌐 Beautiful Dashboard** (Main way to view jobs):
```
Access: https://YOUR_USERNAME.github.io/job-monitor/dashboard.html

Features:
✅ Filter by: Date, Score, Location, Source
✅ Sort by: Score, Date, Company
✅ One-click "View Job & Apply"
✅ Track which jobs you've applied to
✅ Mobile-friendly (add to phone home screen!)
✅ Auto-updates daily
```

**📱 Daily Routine:**
1. Open dashboard URL (or tap phone icon)
2. See "5 New Jobs Today"
3. Filter: "Score 8+"
4. Click "View Job & Apply"
5. Mark as applied
6. Done in 5 minutes!

---

**📧 Email Alerts** (Optional - requires SendGrid):

**Immediate Alerts** (Score 8-10):
```
Subject: 🔥 High Match Job (9/10): Learning Designer @ Anthropic

[Beautiful formatted email with:]
- Job details
- Why it matches
- Apply button
```

**Daily Digest** (All matches 6+):
```
Subject: Daily Job Digest - 5 new matches

Greenhouse: 3 jobs from 25 companies
API Search: 2 jobs (USA)

🔥 Learning Designer @ Khan Academy (9/10)
⚡ Program Manager @ Duolingo (7/10)
✓ Instructional Designer @ Coursera (6/10)
```

**Note:** Dashboard is recommended over email - more interactive and always up-to-date!

---

## 🔄 How It Works

**Every Day (Automated):**

**9 AM UTC:**
1. ✅ Scrape 25 Greenhouse companies (FREE)
2. ✅ Search today's geography via API
   - Monday: USA
   - Tuesday: Singapore
   - Wednesday: Dubai
   - Thursday: USA
   - (repeats)
3. ✅ AI filter all jobs (score 0-10)
4. ✅ Email you matches

**Geography Coverage:**
- USA: Every 2 days → ~180 searches/year
- Singapore: Every 3 days → ~120 searches/year
- Dubai: Every 3 days → ~120 searches/year

---

## 🎯 What Gets Searched

**Greenhouse (Daily):**
- Anthropic, OpenAI
- Khan Academy, Duolingo, Coursera
- Newsela, Quizlet, Clever
- Pluralsight, Udemy, Guild
- + 15 more EdTech companies

**API Search (Rotation):**
- 8 role types: Learning Designer, Instructional Designer, Product Designer, User Researcher, Program Manager, LXD, EdTech, Consultant
- 4 categories: AI+Education, EdTech Platforms, Corporate Learning, Nonprofits
- 3 geographies: USA, Singapore, Dubai

**= Comprehensive coverage of ALL education-focused roles**

---

## 🐛 Troubleshooting

**No emails?**
- Check spam folder
- Verify SendGrid sender email
- Check GitHub Actions logs

**API errors?**
```bash
python scrapers/adzuna.py  # Test Adzuna
python ai_filter.py          # Test AI
```

**Reset database:**
```bash
rm jobs_seen.json
python main.py
```

---

## 📊 Free Tier Limits

**You're using:**
- Adzuna: ~96 calls/month (limit: 250) ✅
- Google AI: ~500 calls/month (limit: 45,000) ✅
- SendGrid: ~30 emails/month (limit: 3,000) ✅

**All safe! Well within free tiers.**

---

## 🎉 You're All Set!

1. ✅ Get API keys
2. ✅ Push to GitHub
3. ✅ Add secrets
4. ✅ Enable Actions
5. ✅ Check email tomorrow morning

**Questions? Check README.md for full details.**

---

**Built for Sneha • February 2026**
