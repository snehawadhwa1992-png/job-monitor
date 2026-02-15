# main.py
# Main orchestrator for Hybrid Job Monitoring System (Option C)

import sys
from datetime import datetime
import config
from scrapers import greenhouse, adzuna
from ai_filter import filter_jobs
from database import load_seen_jobs, filter_new_jobs, save_new_job, cleanup_old_jobs
from alerter import send_immediate_alert, send_daily_digest
from dashboard_generator import generate_dashboard

def main():
    """
    Main job monitoring workflow (Option C - Hybrid):
    1. Daily: Scrape all Greenhouse companies (FREE, unlimited)
    2. Rotation: API search for today's geography (96 API calls/month, within free tier)
    3. AI filter all new jobs
    4. Send alerts
    """
    
    print("="*70)
    print(f"🚀 JOB MONITOR - HYBRID SYSTEM (Option C)")
    print(f"📅 {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}")
    print("="*70)
    
    # Load database of seen jobs
    seen_jobs = load_seen_jobs(config.DATABASE_FILE)
    
    # Clean up old jobs (keep last 90 days)
    seen_jobs = cleanup_old_jobs(seen_jobs, days_to_keep=90)
    
    all_new_matches = {
        'greenhouse': [],
        'api_searches': []
    }
    
    # ===== TIER 1: GREENHOUSE SCRAPING (Daily, FREE) =====
    print(f"\n{'='*70}")
    print("TIER 1: GREENHOUSE SCRAPING (Daily)")
    print('='*70)
    
    greenhouse_jobs = greenhouse.scrape_all_greenhouse_companies(
        config.GREENHOUSE_COMPANIES,
        delay=1  # 1 second between requests to be respectful
    )
    
    # Filter for new jobs
    greenhouse_new = filter_new_jobs(greenhouse_jobs, seen_jobs)
    
    if greenhouse_new:
        print(f"\n🤖 AI filtering {len(greenhouse_new)} new Greenhouse jobs...")
        
        # AI filter
        greenhouse_matched = filter_jobs(
            greenhouse_new,
            min_score=config.DAILY_DIGEST_THRESHOLD
        )
        
        # Save to database and collect matches
        for job in greenhouse_matched:
            save_new_job(job, seen_jobs, config.DATABASE_FILE)
            all_new_matches['greenhouse'].append(job)
            
            # Send immediate alert for high-priority matches
            if job['match_score'] >= config.IMMEDIATE_ALERT_THRESHOLD:
                send_immediate_alert(job)
    
    # ===== TIER 2: API SEARCH (Geography Rotation) =====
    print(f"\n{'='*70}")
    print("TIER 2: API SEARCH (Geography Rotation)")
    print('='*70)
    
    # Determine which geography to search today
    today_geography = config.get_geography_for_today()
    print(f"\n📍 Today's geography: {today_geography}")
    
    # Get optimized search queries for this geography
    queries = config.get_search_queries_for_geography(today_geography)
    print(f"🔍 Running {len(queries)} optimized search queries...")
    
    # Search using Adzuna
    api_jobs = adzuna.search_geography_all_queries(today_geography, queries)
    
    # Filter for new jobs
    api_new = filter_new_jobs(api_jobs, seen_jobs)
    
    if api_new:
        print(f"\n🤖 AI filtering {len(api_new)} new API jobs...")
        
        # AI filter
        api_matched = filter_jobs(
            api_new,
            min_score=config.DAILY_DIGEST_THRESHOLD
        )
        
        # Save to database and collect matches
        for job in api_matched:
            save_new_job(job, seen_jobs, config.DATABASE_FILE)
            all_new_matches['api_searches'].append(job)
            
            # Send immediate alert for high-priority matches
            if job['match_score'] >= config.IMMEDIATE_ALERT_THRESHOLD:
                send_immediate_alert(job)
    
    # ===== SUMMARY & DIGEST =====
    print(f"\n{'='*70}")
    print("SUMMARY")
    print('='*70)
    
    total_greenhouse = len(greenhouse_jobs)
    total_api = len(api_jobs)
    total_new = len(greenhouse_new) + len(api_new)
    total_matches = len(all_new_matches['greenhouse']) + len(all_new_matches['api_searches'])
    
    print(f"\n📊 Today's Results:")
    print(f"   Greenhouse:")
    print(f"     - Total jobs found: {total_greenhouse}")
    print(f"     - New jobs: {len(greenhouse_new)}")
    print(f"     - Matches (score {config.DAILY_DIGEST_THRESHOLD}+): {len(all_new_matches['greenhouse'])}")
    print(f"\n   API Search ({today_geography}):")
    print(f"     - Total jobs found: {total_api}")
    print(f"     - New jobs: {len(api_new)}")
    print(f"     - Matches (score {config.DAILY_DIGEST_THRESHOLD}+): {len(all_new_matches['api_searches'])}")
    print(f"\n   🎯 Total new matches: {total_matches}")
    
    # Send daily digest (if email configured)
    if config.SENDGRID_API_KEY and total_matches > 0:
        print(f"\n📧 Sending daily digest...")
        send_daily_digest(all_new_matches, today_geography)
    elif total_matches > 0:
        print(f"\n📧 Email not configured, skipping digest")
    else:
        print(f"\n📧 No matches to send today")
    
    # ===== GENERATE DASHBOARD =====
    print(f"\n{'='*70}")
    print("GENERATING DASHBOARD")
    print('='*70)
    
    dashboard_path = config.DATABASE_FILE.replace('jobs_seen.json', 'dashboard.html')
    generate_dashboard(seen_jobs, dashboard_path)
    
    print(f"\n🌐 Dashboard ready!")
    print(f"   Local: file://{dashboard_path}")
    print(f"   GitHub: https://github.com/YOUR_USERNAME/job-monitor/blob/main/dashboard.html")
    print(f"   GitHub Pages: https://YOUR_USERNAME.github.io/job-monitor/dashboard.html")
    
    print(f"\n{'='*70}")
    print("✅ JOB MONITOR COMPLETE")
    print(f"⏰ {datetime.now().strftime('%I:%M %p')}")
    print('='*70)
    
    return total_matches

if __name__ == "__main__":
    try:
        matches = main()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
