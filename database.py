# database.py
# Simple JSON database to track which jobs we've already seen

import json
import os
from datetime import datetime
import hashlib

def get_job_id(job):
    """
    Generate unique ID for a job based on title + company + location.
    This helps us deduplicate jobs from different sources.
    """
    key = f"{job.get('title', '')}_{job.get('company', '')}_{job.get('location', '')}"
    return hashlib.md5(key.encode()).hexdigest()

def load_seen_jobs(database_file="/home/claude/job-monitor/jobs_seen.json"):
    """
    Load database of previously seen jobs.
    
    Returns:
        Dictionary mapping job_id -> job data
    """
    if not os.path.exists(database_file):
        return {}
    
    try:
        with open(database_file, 'r') as f:
            data = json.load(f)
        print(f"📂 Loaded {len(data)} previously seen jobs")
        return data
    except Exception as e:
        print(f"⚠️  Error loading database: {e}")
        return {}

def save_seen_jobs(seen_jobs, database_file="/home/claude/job-monitor/jobs_seen.json"):
    """
    Save seen jobs database to disk.
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(database_file), exist_ok=True)
        
        with open(database_file, 'w') as f:
            json.dump(seen_jobs, f, indent=2)
        print(f"💾 Saved {len(seen_jobs)} jobs to database")
    except Exception as e:
        print(f"❌ Error saving database: {e}")

def is_new_job(job, seen_jobs):
    """
    Check if job is new (not in database).
    
    Args:
        job: Job dictionary
        seen_jobs: Database of seen jobs
    
    Returns:
        True if job is new, False if already seen
    """
    job_id = get_job_id(job)
    return job_id not in seen_jobs

def save_new_job(job, seen_jobs, database_file="/home/claude/job-monitor/jobs_seen.json"):
    """
    Add a new job to the database and save.
    
    Args:
        job: Job dictionary
        seen_jobs: Current database
        database_file: Path to database file
    """
    job_id = get_job_id(job)
    
    # Add metadata
    job['job_id'] = job_id
    job['first_seen'] = datetime.now().isoformat()
    
    # Save to database
    seen_jobs[job_id] = job
    
    # Persist to disk
    save_seen_jobs(seen_jobs, database_file)

def filter_new_jobs(jobs, seen_jobs):
    """
    Filter list of jobs to only new ones we haven't seen before.
    
    Args:
        jobs: List of job dictionaries
        seen_jobs: Database of seen jobs
    
    Returns:
        List of only new jobs
    """
    new_jobs = []
    
    for job in jobs:
        if is_new_job(job, seen_jobs):
            new_jobs.append(job)
    
    print(f"🆕 Found {len(new_jobs)} new jobs (out of {len(jobs)} total)")
    
    return new_jobs

def get_jobs_by_date_range(seen_jobs, days_back=7):
    """
    Get jobs found in the last N days.
    Useful for weekly summaries.
    """
    from datetime import datetime, timedelta
    
    cutoff = datetime.now() - timedelta(days=days_back)
    recent_jobs = []
    
    for job_id, job in seen_jobs.items():
        first_seen = datetime.fromisoformat(job.get('first_seen', '2000-01-01'))
        if first_seen >= cutoff:
            recent_jobs.append(job)
    
    return recent_jobs

def cleanup_old_jobs(seen_jobs, days_to_keep=90):
    """
    Remove jobs older than N days from database to keep it manageable.
    
    Args:
        seen_jobs: Database of seen jobs
        days_to_keep: Keep jobs from last N days
    
    Returns:
        Cleaned database
    """
    from datetime import datetime, timedelta
    
    cutoff = datetime.now() - timedelta(days=days_to_keep)
    cleaned = {}
    removed_count = 0
    
    for job_id, job in seen_jobs.items():
        first_seen = datetime.fromisoformat(job.get('first_seen', '2000-01-01'))
        if first_seen >= cutoff:
            cleaned[job_id] = job
        else:
            removed_count += 1
    
    if removed_count > 0:
        print(f"🧹 Cleaned {removed_count} old jobs from database")
    
    return cleaned

if __name__ == "__main__":
    # Test database functions
    print("Testing database module...")
    
    # Create test jobs
    test_jobs = [
        {
            'title': 'Learning Designer',
            'company': 'Test Company',
            'location': 'Remote USA',
            'url': 'https://example.com/job1'
        },
        {
            'title': 'Product Designer',
            'company': 'Another Company',
            'location': 'Singapore',
            'url': 'https://example.com/job2'
        }
    ]
    
    # Test loading (empty database)
    seen = load_seen_jobs("/tmp/test_jobs.json")
    print(f"Initial database: {len(seen)} jobs")
    
    # Test filtering new jobs
    new = filter_new_jobs(test_jobs, seen)
    print(f"New jobs: {len(new)}")
    
    # Save jobs
    for job in new:
        save_new_job(job, seen, "/tmp/test_jobs.json")
    
    # Try again - should find no new jobs
    new = filter_new_jobs(test_jobs, seen)
    print(f"New jobs (second time): {len(new)}")
