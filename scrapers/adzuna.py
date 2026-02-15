# scrapers/adzuna.py
# Search jobs using Adzuna API (250 calls/month free)

import requests
from datetime import datetime
import config

def search_adzuna(query, location="United States", results_per_page=50):
    """
    Search jobs via Adzuna API.
    
    Args:
        query: Search query (e.g., "Learning Designer AI education")
        location: Location string
        results_per_page: Number of results (max 50)
    
    Returns:
        List of job dictionaries
    """
    
    if not config.ADZUNA_APP_ID or not config.ADZUNA_APP_KEY:
        print("  ⚠️  Adzuna API credentials not configured")
        return []
    
    # Map location to Adzuna country code
    country_map = {
        "United States": "us",
        "USA": "us",
        "US": "us",
        "Singapore": "sg",
        "SG": "sg",
        "Dubai": "ae",  # UAE
        "UAE": "ae",
        "United Arab Emirates": "ae"
    }
    
    country = country_map.get(location, "us")
    
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
    
    params = {
        'app_id': config.ADZUNA_APP_ID,
        'app_key': config.ADZUNA_APP_KEY,
        'what': query,
        'results_per_page': results_per_page,
        'content-type': 'application/json',
        'sort_by': 'date'  # Most recent first
    }
    
    # Add location filter if not searching entire country
    if location not in ["United States", "USA", "US", "Singapore", "UAE"]:
        params['where'] = location
    
    try:
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            print(f"  ❌ Adzuna API error {response.status_code}: {response.text[:100]}")
            return []
        
        data = response.json()
        
        jobs = []
        for result in data.get('results', []):
            job = {
                'title': result.get('title', 'No title'),
                'company': result.get('company', {}).get('display_name', 'Unknown company'),
                'location': result.get('location', {}).get('display_name', location),
                'url': result.get('redirect_url', ''),
                'description': result.get('description', '')[:1000],  # Truncate long descriptions
                'salary_min': result.get('salary_min'),
                'salary_max': result.get('salary_max'),
                'contract_type': result.get('contract_type'),
                'source': 'Adzuna',
                'date_found': datetime.now().isoformat(),
                'created': result.get('created'),
            }
            jobs.append(job)
        
        print(f"  ✓ Adzuna: Found {len(jobs)} jobs for '{query[:50]}...'")
        return jobs
    
    except requests.Timeout:
        print(f"  ⏱️  Adzuna API timeout")
        return []
    
    except Exception as e:
        print(f"  ❌ Adzuna error: {e}")
        return []

def search_geography_all_queries(geography, queries):
    """
    Search all queries for a specific geography using Adzuna.
    
    Args:
        geography: Geography name (USA, Singapore, Dubai)
        queries: List of (query_string, category_name) tuples
    
    Returns:
        List of all jobs found
    """
    print(f"\n🔍 Searching Adzuna: {geography}")
    
    # Get location terms for this geography
    location_terms = config.GEOGRAPHIES[geography]['search_terms']
    primary_location = location_terms[0]
    
    all_jobs = []
    
    for i, (query, category) in enumerate(queries, 1):
        print(f"  [{i}/{len(queries)}] {category}")
        
        jobs = search_adzuna(query, primary_location)
        
        # Tag jobs with category for filtering
        for job in jobs:
            job['search_category'] = category
            job['geography'] = geography
        
        all_jobs.extend(jobs)
    
    print(f"\n✅ Adzuna {geography} complete: {len(all_jobs)} jobs")
    return all_jobs

if __name__ == "__main__":
    # Test Adzuna API
    print("Testing Adzuna API...")
    
    # Test query
    test_query = "Learning Designer"
    test_location = "United States"
    
    print(f"\nSearching: '{test_query}' in {test_location}")
    jobs = search_adzuna(test_query, test_location, results_per_page=10)
    
    print(f"\nResults: {len(jobs)} jobs")
    
    if jobs:
        print("\nSample jobs:")
        for job in jobs[:3]:
            print(f"\n  - {job['title']}")
            print(f"    Company: {job['company']}")
            print(f"    Location: {job['location']}")
            print(f"    URL: {job['url'][:60]}...")
