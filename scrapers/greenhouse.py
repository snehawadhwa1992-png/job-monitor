# scrapers/greenhouse.py
# Scrape job postings from Greenhouse boards

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

def scrape_greenhouse_board(company_slug, timeout=10):
    """
    Scrape all jobs from a Greenhouse board.
    
    Args:
        company_slug: Company identifier (e.g., 'anthropic', 'khanacademy')
        timeout: Request timeout in seconds
    
    Returns:
        List of job dictionaries, or None if board doesn't exist/error
    """
    url = f"https://boards.greenhouse.io/{company_slug}"
    
    try:
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 404:
            print(f"  ⚠️  Greenhouse board not found: {company_slug}")
            return None
        
        if response.status_code != 200:
            print(f"  ❌ Error {response.status_code} for {company_slug}")
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        jobs = []
        
        # Greenhouse uses 'opening' class for job listings
        openings = soup.find_all('div', class_='opening')
        
        if not openings:
            # Try alternative structure (some boards use different HTML)
            openings = soup.find_all('section', class_='level-0')
        
        for opening in openings:
            try:
                # Extract job title and URL
                title_elem = opening.find('a')
                if not title_elem:
                    continue
                
                title = title_elem.text.strip()
                job_url = title_elem.get('href', '')
                
                # Make URL absolute if relative
                if job_url.startswith('/'):
                    job_url = f"https://boards.greenhouse.io{job_url}"
                elif not job_url.startswith('http'):
                    job_url = f"https://boards.greenhouse.io/{company_slug}{job_url}"
                
                # Extract location
                location_elem = opening.find('span', class_='location')
                location = location_elem.text.strip() if location_elem else 'Location not specified'
                
                # Extract department if available
                department_elem = opening.find('span', class_='department')
                department = department_elem.text.strip() if department_elem else None
                
                job = {
                    'title': title,
                    'url': job_url,
                    'location': location,
                    'company': company_slug.replace('-', ' ').title(),
                    'company_slug': company_slug,
                    'department': department,
                    'source': 'Greenhouse',
                    'date_found': datetime.now().isoformat(),
                    'raw_html': str(opening)[:500]  # First 500 chars for debugging
                }
                
                jobs.append(job)
            
            except Exception as e:
                print(f"  ⚠️  Error parsing job in {company_slug}: {e}")
                continue
        
        if jobs:
            print(f"  ✓ Found {len(jobs)} jobs at {company_slug}")
        
        return jobs
    
    except requests.Timeout:
        print(f"  ⏱️  Timeout scraping {company_slug}")
        return None
    
    except Exception as e:
        print(f"  ❌ Error scraping {company_slug}: {e}")
        return None

def scrape_all_greenhouse_companies(company_list, delay=1):
    """
    Scrape all companies in list with rate limiting.
    
    Args:
        company_list: List of company slugs
        delay: Seconds to wait between requests (be respectful)
    
    Returns:
        List of all jobs found across all companies
    """
    print(f"\n🏢 Scraping {len(company_list)} Greenhouse boards...")
    
    all_jobs = []
    successful = 0
    failed = 0
    
    for i, company in enumerate(company_list, 1):
        print(f"[{i}/{len(company_list)}] {company}")
        
        jobs = scrape_greenhouse_board(company)
        
        if jobs is not None:
            all_jobs.extend(jobs)
            successful += 1
        else:
            failed += 1
        
        # Rate limiting - be respectful
        if i < len(company_list):
            time.sleep(delay)
    
    print(f"\n✅ Greenhouse scraping complete:")
    print(f"   - Successful: {successful}")
    print(f"   - Failed: {failed}")
    print(f"   - Total jobs: {len(all_jobs)}")
    
    return all_jobs

def get_job_description(job_url, timeout=10):
    """
    Fetch full job description from Greenhouse job page.
    Use this when you need the full description for AI filtering.
    
    Args:
        job_url: Full URL to job posting
        timeout: Request timeout
    
    Returns:
        String with job description, or None if error
    """
    try:
        response = requests.get(job_url, timeout=timeout)
        
        if response.status_code != 200:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find job description content
        content_div = soup.find('div', id='content')
        if content_div:
            # Extract text, clean up
            description = content_div.get_text(separator='\n', strip=True)
            return description
        
        return None
    
    except Exception as e:
        print(f"  ⚠️  Error fetching description: {e}")
        return None

if __name__ == "__main__":
    # Test scraping
    print("Testing Greenhouse scraper...")
    
    test_companies = ["anthropic", "khanacademy", "duolingo"]
    
    for company in test_companies:
        print(f"\n{'='*60}")
        print(f"Testing: {company}")
        print('='*60)
        
        jobs = scrape_greenhouse_board(company)
        
        if jobs:
            print(f"\nSample jobs:")
            for job in jobs[:3]:  # Show first 3
                print(f"  - {job['title']}")
                print(f"    Location: {job['location']}")
                print(f"    URL: {job['url']}")
