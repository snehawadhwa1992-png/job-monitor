# 🎯 Job Monitor - Automated Job Search System

**Find Learning Design, EdTech, and education-focused roles across USA, Singapore, and Dubai.**

**Access your jobs via beautiful web dashboard - no email needed!**

---

## 🚀 QUICK LINKS

- **📱 Setup Guide:** [QUICKSTART.md](QUICKSTART.md) - Get running in 60 minutes
- **🌐 Dashboard Setup:** [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) - Enable web access
- **📚 Full Documentation:** Keep reading below

---

## ✨ HOW IT WORKS

**Every day automatically:**
1. ✅ Scrapes 25 top EdTech companies (Anthropic, Khan Academy, Duolingo, etc.)
2. ✅ Searches USA/Singapore/Dubai jobs via APIs (rotates every 2-3 days)
3. ✅ AI filters jobs (scores 0-10 based on your profile)
4. ✅ **Generates beautiful web dashboard** (access from any device)
5. ✅ Optionally emails you high-priority matches

**You just:**
- Open dashboard URL on phone or laptop
- See new jobs sorted by match quality
- Filter, click to apply, track applications
- **5 minutes per day, fully automated**

**Cost: $0/month** (all free tiers)

---

## 🌐 DASHBOARD

**Access from anywhere:** `https://YOUR_USERNAME.github.io/job-monitor/dashboard.html`

**Features:**
- 📱 Works on phone, tablet, laptop
- 🎯 Filter by score, date, location, source
- ✓ Track which jobs you've applied to
- 🔄 Auto-updates daily
- 🎨 Beautiful, professional design

**See [GITHUB_PAGES_SETUP.md](GITHUB_PAGES_SETUP.md) for setup.**

---

## 📊 EXPECTED RESULTS

**Per day:**
- 10-30 new jobs discovered
- 3-8 quality matches (score 6+)
- 0-2 high-priority (score 8+)

**Coverage:**
- 25 top EdTech companies (daily)
- ALL companies in 4 categories (rotation)
- USA, Singapore, Dubai

**Cost:** $0/month forever

---

## ⚡ 60-MINUTE SETUP

### 1. Get API Keys (30 min)

**Google AI Studio:**
- https://aistudio.google.com/ → Get API key
- FREE: 1500 requests/day

**Adzuna:**
- https://developer.adzuna.com/signup
- Create app: "Job Monitor" - "Personal job search tool"
- FREE: 250 calls/month

**SendGrid (OPTIONAL):**
- https://signup.sendgrid.com/ → Verify sender
- FREE: 100 emails/day
- Skip if you just want dashboard

### 2. GitHub Setup (15 min)

```bash
# Create repo on github.com: job-monitor (private)

# Upload code
cd job-monitor
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/job-monitor.git
git push -u origin main
```

**Add secrets** (Settings → Secrets → Actions):
- `GOOGLE_AI_KEY`
- `ADZUNA_APP_ID`
- `ADZUNA_APP_KEY`
- (Optional: `SENDGRID_API_KEY`, `EMAIL_FROM`, `EMAIL_TO`)

**Enable GitHub Pages** (Settings → Pages):
- Source: Deploy from branch → main → / (root)
- Save
- Dashboard: `https://YOUR_USERNAME.github.io/job-monitor/dashboard.html`

### 3. Test & Use (15 min)

1. Actions → "Daily Job Monitor" → Run workflow
2. Wait 10 minutes
3. Open dashboard URL
4. Bookmark on all devices
5. Done!

**Full guide:** [QUICKSTART.md](QUICKSTART.md)

---

## ⚙️ CONFIGURATION

**Update your profile:** Edit `config.py` → `YOUR_PROFILE`

**Add companies:** Edit `config.py` → `GREENHOUSE_COMPANIES`

**Adjust geography:** Edit `config.py` → `GEOGRAPHIES`

**Change thresholds:** Edit `config.py` → `IMMEDIATE_ALERT_THRESHOLD`

---

## 📱 DAILY WORKFLOW

1. Open dashboard URL
2. See "5 New Jobs Today"
3. Filter: "Score 8+"
4. Click "View Job & Apply"
5. Mark as applied
6. Done in 5 minutes!

---

## 🐛 TROUBLESHOOTING

**Dashboard 404:** Wait 2 min, hard refresh  
**No jobs:** Check GitHub Actions logs  
**API errors:** Verify secrets  
**Email issues:** Just use dashboard instead!

**Full troubleshooting:** [QUICKSTART.md](QUICKSTART.md)

---

## 📁 FILES

```
job-monitor/
├── QUICKSTART.md              ← Start here
├── GITHUB_PAGES_SETUP.md      ← Dashboard setup
├── README.md                   ← This file
├── config.py                   ← Your settings
├── main.py                     ← Orchestrator
├── ai_filter.py                ← AI matching
├── dashboard_generator.py      ← Creates dashboard
├── database.py                 ← Job tracking
├── alerter.py                  ← Email (optional)
├── scrapers/
│   ├── greenhouse.py           ← 25 companies
│   └── adzuna.py               ← API search
└── .github/workflows/
    └── daily-job-check.yml     ← Automation
```

---

**Start with [QUICKSTART.md](QUICKSTART.md) now!**

**Built for Sneha • February 2026**
