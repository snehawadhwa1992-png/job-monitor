# alerter.py
# Send email alerts for new job matches

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import config
from datetime import datetime

def send_immediate_alert(job):
    """
    Send immediate alert for high-priority job (score 8+).
    
    Args:
        job: Job dictionary with AI analysis
    """
    if not config.SENDGRID_API_KEY or not config.EMAIL_TO:
        print("  ⚠️  Email not configured, skipping alert")
        return
    
    analysis = job.get('ai_analysis', {})
    score = analysis.get('score', 0)
    
    subject = f"🔥 High Match Job ({score}/10): {job['title']} @ {job['company']}"
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background-color: #f44336; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">🔥 High Priority Match</h1>
            <p style="margin: 5px 0; font-size: 24px; font-weight: bold;">{score}/10</p>
        </div>
        
        <div style="padding: 20px;">
            <h2 style="color: #333;">{job['title']}</h2>
            <p style="color: #666; font-size: 18px;"><strong>{job['company']}</strong></p>
            <p style="color: #888;">📍 {job['location']}</p>
            
            <div style="margin: 20px 0; padding: 15px; background-color: #f5f5f5; border-left: 4px solid #4CAF50;">
                <p style="margin: 0; color: #333;"><strong>Why this matches:</strong></p>
                <p style="margin: 10px 0;">{analysis.get('reasoning', 'Strong match for your profile')}</p>
            </div>
            
            <div style="margin: 20px 0;">
                <p style="margin: 5px 0;"><strong>Category:</strong> {analysis.get('role_category', 'N/A').replace('_', ' ').title()}</p>
                <p style="margin: 5px 0;"><strong>Source:</strong> {job.get('source', 'Unknown')}</p>
                <p style="margin: 5px 0;"><strong>Found:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            
            <div style="margin: 30px 0; text-align: center;">
                <a href="{job['url']}" style="background-color: #4CAF50; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; font-weight: bold; display: inline-block;">
                    VIEW JOB & APPLY →
                </a>
            </div>
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #888;">
                <p>This is an automated alert from your job monitoring system.</p>
                <p>Jobs with score 8+ are sent immediately as high-priority matches.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        message = Mail(
            from_email=config.EMAIL_FROM,
            to_emails=config.EMAIL_TO,
            subject=subject,
            html_content=html_content
        )
        
        sg = SendGridAPIClient(config.SENDGRID_API_KEY)
        response = sg.send(message)
        
        print(f"  ✓ Immediate alert sent: {job['title']} ({score}/10)")
        
    except Exception as e:
        print(f"  ❌ Error sending immediate alert: {e}")

def send_daily_digest(matched_jobs, geography_checked=None):
    """
    Send daily digest email with all matches.
    
    Args:
        matched_jobs: Dictionary with categories of jobs
                      e.g., {'greenhouse': [...], 'api_searches': [...]}
        geography_checked: Which geography was checked today (USA, Singapore, Dubai)
    """
    if not config.SENDGRID_API_KEY or not config.EMAIL_TO:
        print("  ⚠️  Email not configured, skipping digest")
        return
    
    # Flatten all jobs
    all_jobs = []
    greenhouse_jobs = matched_jobs.get('greenhouse', [])
    api_jobs = matched_jobs.get('api_searches', [])
    
    all_jobs.extend(greenhouse_jobs)
    all_jobs.extend(api_jobs)
    
    if not all_jobs:
        print("  ℹ️  No jobs to send in digest")
        return
    
    # Sort by score (highest first)
    all_jobs.sort(key=lambda x: x.get('match_score', 0), reverse=True)
    
    # Build email
    subject = f"Daily Job Digest - {len(all_jobs)} new matches"
    
    # Build job list HTML
    jobs_html = ""
    
    for job in all_jobs:
        analysis = job.get('ai_analysis', {})
        score = job.get('match_score', 0)
        
        # Color code by score
        if score >= 8:
            badge_color = "#f44336"  # Red
            emoji = "🔥"
        elif score >= 7:
            badge_color = "#FF9800"  # Orange
            emoji = "⚡"
        else:
            badge_color = "#4CAF50"  # Green
            emoji = "✓"
        
        jobs_html += f"""
        <div style="margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; color: #333;">{emoji} {job['title']}</h3>
                <div style="background-color: {badge_color}; color: white; padding: 5px 10px; border-radius: 3px; font-weight: bold;">
                    {score}/10
                </div>
            </div>
            <p style="margin: 5px 0; color: #666; font-size: 16px;">{job['company']} • {job['location']}</p>
            <p style="margin: 10px 0; color: #555; font-size: 14px;">{analysis.get('reasoning', '')}</p>
            <div style="margin: 10px 0;">
                <span style="display: inline-block; background-color: #f0f0f0; padding: 4px 8px; margin-right: 5px; border-radius: 3px; font-size: 12px;">
                    {analysis.get('role_category', 'N/A').replace('_', ' ').title()}
                </span>
                <span style="display: inline-block; background-color: #f0f0f0; padding: 4px 8px; margin-right: 5px; border-radius: 3px; font-size: 12px;">
                    {job.get('source', 'Unknown')}
                </span>
            </div>
            <a href="{job['url']}" style="color: #4CAF50; text-decoration: none; font-weight: bold;">
                View Job →
            </a>
        </div>
        """
    
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto;">
        <div style="background-color: #4CAF50; color: white; padding: 20px; text-align: center;">
            <h1 style="margin: 0;">📬 Daily Job Digest</h1>
            <p style="margin: 5px 0;">{datetime.now().strftime('%B %d, %Y')}</p>
            <p style="margin: 5px 0; font-size: 18px; font-weight: bold;">{len(all_jobs)} New Matches</p>
        </div>
        
        <div style="padding: 20px;">
            <div style="background-color: #f5f5f5; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
                <p style="margin: 0;"><strong>Today's Search:</strong></p>
                <p style="margin: 5px 0;">• Greenhouse: {len(greenhouse_jobs)} jobs from {len(config.GREENHOUSE_COMPANIES)} companies</p>
                <p style="margin: 5px 0;">• API Search: {len(api_jobs)} jobs ({geography_checked or 'Multiple geographies'})</p>
            </div>
            
            <h2 style="color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;">
                Your Matches
            </h2>
            
            {jobs_html}
            
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd; font-size: 12px; color: #888;">
                <p>This is your automated daily job digest.</p>
                <p>Jobs are scored 0-10 based on match to your profile:</p>
                <ul style="margin: 5px 0;">
                    <li>🔥 8-10: High priority - apply immediately</li>
                    <li>⚡ 7: Strong match - review soon</li>
                    <li>✓ 6: Decent match - worth considering</li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        message = Mail(
            from_email=config.EMAIL_FROM,
            to_emails=config.EMAIL_TO,
            subject=subject,
            html_content=html_content
        )
        
        sg = SendGridAPIClient(config.SENDGRID_API_KEY)
        response = sg.send(message)
        
        print(f"✅ Daily digest sent: {len(all_jobs)} jobs")
        
    except Exception as e:
        print(f"❌ Error sending digest: {e}")

if __name__ == "__main__":
    # Test email sending (requires valid credentials)
    print("Testing email alerts...")
    
    test_job = {
        'title': 'Learning Designer',
        'company': 'Test Company',
        'location': 'Remote USA',
        'url': 'https://example.com',
        'source': 'Test',
        'ai_analysis': {
            'score': 9,
            'reasoning': 'Perfect match for learning design role with focus on underserved populations',
            'role_category': 'learning_design',
            'is_match': True
        },
        'match_score': 9
    }
    
    print("\nNote: This will only work if you have valid SendGrid credentials")
    print("Testing immediate alert...")
    # send_immediate_alert(test_job)
    
    print("\nTesting daily digest...")
    # send_daily_digest({'greenhouse': [test_job], 'api_searches': []}, 'USA')
