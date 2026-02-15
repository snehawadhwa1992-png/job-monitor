# 🌐 GITHUB PAGES SETUP GUIDE

**Enable GitHub Pages to access your dashboard from anywhere via a clean URL.**

---

## ⚡ QUICK SETUP (2 minutes)

### Step 1: Push Your Code to GitHub

```bash
cd job-monitor
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/job-monitor.git
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to your GitHub repository
2. Click **"Settings"** tab (top right)
3. Scroll down to **"Pages"** in left sidebar
4. Under **"Source"**:
   - Select: **"Deploy from a branch"**
   - Branch: **"main"**
   - Folder: **"/ (root)"**
5. Click **"Save"**
6. Wait 1-2 minutes for deployment

### Step 3: Get Your URL

After 1-2 minutes:
1. Refresh the Pages settings page
2. You'll see: **"Your site is live at https://YOUR_USERNAME.github.io/job-monitor/"**
3. Your dashboard URL is: **https://YOUR_USERNAME.github.io/job-monitor/dashboard.html**

**✅ Bookmark this URL on all your devices!**

---

## 📱 HOW TO USE

### On Computer:
```
Open: https://YOUR_USERNAME.github.io/job-monitor/dashboard.html
Bookmark: ⭐ Add to bookmarks bar
Daily: Click bookmark to check new jobs
```

### On Phone:
```
Open: https://YOUR_USERNAME.github.io/job-monitor/dashboard.html
Add to Home Screen (iOS):
  1. Tap Share button
  2. "Add to Home Screen"
  3. Name it "Job Monitor"
  4. Tap "Add"
  
Add to Home Screen (Android):
  1. Tap menu (3 dots)
  2. "Add to Home screen"
  3. Name it "Job Monitor"
  4. Tap "Add"
```

**Now it's like an app on your phone!** 📱

---

## 🔄 HOW IT UPDATES

**Automatic daily:**
1. GitHub Actions runs at 9 AM UTC
2. Scrapes jobs, filters with AI
3. Generates new dashboard.html
4. Commits to repository
5. GitHub Pages auto-deploys (~30 seconds)
6. **Your dashboard URL is updated!**

**You just:**
- Open the URL (or tap the icon)
- See fresh jobs from that morning
- Filter, sort, apply
- Mark jobs as applied
- Done!

---

## 🎯 EXAMPLE WORKFLOW

**Monday 9:30 AM:**
```
1. Tap "Job Monitor" icon on phone
2. See "5 New Jobs Today"
3. Filter: "Score 8+"
4. See 2 high-priority jobs
5. Tap "View Job & Apply" on interesting one
6. Opens in new tab, you apply
7. Back to dashboard, tap "Mark as Applied"
8. Green checkmark appears ✓
9. Continue with day
```

**Takes 5 minutes total.**

---

## 🛠️ TROUBLESHOOTING

### "404 - Page not found"

**Wait 2 minutes** after enabling Pages, then refresh.

If still 404:
1. Check Settings → Pages shows "Your site is live"
2. Make sure you committed `dashboard.html` to repo
3. Check branch is "main" in Pages settings
4. Try: `https://YOUR_USERNAME.github.io/job-monitor/` (without dashboard.html)

### Dashboard shows old jobs

1. Check GitHub Actions ran today (Actions tab)
2. Check `dashboard.html` was updated (see commit history)
3. **Hard refresh**: Ctrl+Shift+R (PC) or Cmd+Shift+R (Mac)
4. Clear browser cache

### Can't access on phone

1. Make sure you're using the full URL with `dashboard.html`
2. Try opening in private/incognito mode first
3. If works in incognito, clear browser cache
4. Check repo is **public** (or you're logged into GitHub)

### "Applied" marks not syncing between devices

**This is normal!** 
- Applied status is stored in browser localStorage
- Each device tracks separately
- This is intentional (privacy + offline work)

---

## 🔒 PRIVACY OPTIONS

### Option 1: Public Repository (Recommended)
- ✅ Easy to access from any device
- ✅ No login needed
- ✅ Can share with friends
- ⚠️ Anyone with URL can see your job search
- **Good if:** You don't mind job search being visible

### Option 2: Private Repository
- ✅ Only you can access
- ✅ More private
- ❌ Must be logged into GitHub to view
- ❌ Slightly less convenient on phone
- **Good if:** You want complete privacy

**To make private:**
1. Settings → General
2. Scroll to bottom: "Danger Zone"
3. "Change visibility" → Private

**GitHub Pages still works with private repos!**

---

## 🎨 CUSTOMIZATION

Want to customize the dashboard look?

Edit `dashboard_generator.py`:
```python
# Change colors (line ~50-100 in style section)
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
# Change to your preferred colors

# Change layout, fonts, etc.
# All CSS is in the <style> section
```

After editing:
```bash
python main.py  # Regenerate dashboard
git add dashboard_generator.py dashboard.html
git commit -m "Customize dashboard"
git push
```

Dashboard updates automatically!

---

## 📊 ADVANCED: Custom Domain

Want `jobs.yourdomain.com` instead of GitHub URL?

1. Buy domain (Namecheap, Google Domains, etc.)
2. GitHub Settings → Pages → Custom domain
3. Add your domain
4. Update DNS (CNAME record)
5. Enable HTTPS

**Full guide:** https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

---

## ✅ FINAL CHECKLIST

After setup, verify:

- [ ] Dashboard loads at GitHub Pages URL
- [ ] Shows today's date in header
- [ ] Filters work (click buttons)
- [ ] "View Job" buttons open job URLs
- [ ] "Mark as Applied" buttons work
- [ ] Applied jobs show green checkmark ✓
- [ ] Bookmarked on all devices
- [ ] Added to phone home screen

**You're all set!** 🎉

---

## 📱 YOUR URLS (Fill these in)

**Dashboard URL:**
```
https://YOUR_USERNAME.github.io/job-monitor/dashboard.html
```

**Repository URL:**
```
https://github.com/YOUR_USERNAME/job-monitor
```

**GitHub Actions (check runs):**
```
https://github.com/YOUR_USERNAME/job-monitor/actions
```

**Replace YOUR_USERNAME with your actual GitHub username!**

---

## 🎯 NEXT STEPS

1. ✅ Enable GitHub Pages (2 minutes)
2. ✅ Bookmark dashboard URL
3. ✅ Add to phone home screen
4. ✅ Check it tomorrow morning after first run
5. ✅ Enjoy automated job hunting!

**Questions? Check README.md or QUICKSTART.md**
