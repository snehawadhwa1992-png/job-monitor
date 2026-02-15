# config.py
# Configuration for Hybrid Job Monitoring System (Option C)

import os
from datetime import datetime

# ===== GREENHOUSE COMPANIES (Daily scraping, FREE) =====
GREENHOUSE_COMPANIES = [
    # AI + Education
    "anthropic",
    "openai",
    
    # K-12 & Higher Ed Platforms
    "khanacademy",
    "duolingo",
    "coursera",
    "udacity",
    "outschool",
    "codepath",
    "renaissancelearning-nam",
    "d2l",
    
    # Adaptive Learning
    "newsela",
    "quizlet",
    
    # Teacher Tools
    "clever",
    "seesaw",
    "goguardian",
    "remind",
    
    # Corporate Learning
    "pluralsight",
    "udemy",
    "guild",
    "multiverse",
    
    # Other Major EdTech
    "brainpop",
    "nearpod",
    "gradescope",
    "amplify",
]

# ===== ROLE CLUSTERS (for optimized API searches) =====

ROLE_CLUSTER_1_DESIGN = [
    "Learning Designer",
    "Instructional Designer",
    "Learning Experience Designer",
    "Educational Technologist"
]

ROLE_CLUSTER_2_PRODUCT = [
    "Product Designer",
    "User Researcher",
    "Program Manager",
    "Consultant"
]

# Combined for AI filtering
ALL_ROLE_TYPES = ROLE_CLUSTER_1_DESIGN + ROLE_CLUSTER_2_PRODUCT

# ===== CATEGORIES (Priority B) =====

CATEGORIES = {
    "AI + Education": [
        "AI education",
        "EdTech AI",
        "artificial intelligence learning",
        "machine learning education"
    ],
    "EdTech Platforms": [
        "EdTech",
        "educational technology",
        "learning platform",
        "e-learning"
    ],
    "Corporate Learning": [
        "corporate learning",
        "L&D",
        "workplace learning",
        "learning and development",
        "employee training"
    ],
    "Nonprofits/Foundations": [
        "nonprofit education",
        "education foundation",
        "NGO education",
        "social impact education"
    ]
}

# ===== GEOGRAPHIES =====

GEOGRAPHIES = {
    "USA": {
        "search_terms": ["United States", "USA", "US", "remote USA"],
        "check_frequency": 2  # Check every 2 days
    },
    "Singapore": {
        "search_terms": ["Singapore", "SG"],
        "check_frequency": 3  # Check every 3 days
    },
    "Dubai": {
        "search_terms": ["Dubai", "UAE", "United Arab Emirates"],
        "check_frequency": 3  # Check every 3 days
    }
}

# ===== SEARCH QUERIES (Optimized, combined role clusters) =====

def get_search_queries_for_geography(geography):
    """
    Generate 8 optimized search queries for a geography.
    Returns list of (query_string, category_name) tuples.
    """
    queries = []
    
    # Cluster 1: Design roles
    design_roles = " OR ".join(ROLE_CLUSTER_1_DESIGN)
    
    # Cluster 2: Product roles  
    product_roles = " OR ".join(ROLE_CLUSTER_2_PRODUCT)
    
    for category_name, keywords in CATEGORIES.items():
        # Query 1: Design roles + this category
        query_1 = f"({design_roles}) AND ({' OR '.join(keywords[:2])})"
        queries.append((query_1, f"{category_name} - Design"))
        
        # Query 2: Product roles + this category
        query_2 = f"({product_roles}) AND ({' OR '.join(keywords[:2])})"
        queries.append((query_2, f"{category_name} - Product"))
    
    return queries  # Returns 8 queries (4 categories × 2 role clusters)

# ===== EXCLUDE KEYWORDS =====

EXCLUDE_KEYWORDS = [
    "Software Engineer",
    "Senior Software Engineer",
    "Staff Engineer",
    "Data Scientist",
    "Data Engineer",
    "Sales Representative",
    "Account Executive",
    "Marketing Manager",
    "Business Development",
    "Customer Success Manager"
]

# ===== YOUR PROFILE (for AI filtering) =====

YOUR_PROFILE = """
Master's candidate in Learning Design, Innovation & Technology at Harvard Graduate School of Education (graduating 2026).

EXPERIENCE (8+ years):
- Teaching: Teach for India Fellow and Program Manager (underserved communities, red-light districts)
- EdTech Product: Byju's, Bhanzu (learning experience design, product development)
- Consulting: Genpact, Aga Khan Foundation (large-scale technology adoption)
- Adult Learning: Wisdom Circle (product development, user research with older adults)

RESEARCH:
- "Impact by Design" - examining technology adoption with underserved populations
- Developed 5 evidence-based design principles for age-inclusive technology
- Validated through expert interviews with AARP, GetSetUp professionals
- AgeTech Design Principles Assessment Tool (54 questions)

EXPERTISE:
- Learning Science + Product Thinking + Inclusive Design + Implementation at Scale
- Evidence-based frameworks and human-centered research
- Designing for overlooked/underserved populations (children to older adults)
- Systematic, data-driven approaches to learning design

INTERESTS:
- AI in education (cognitive partnership, not cognitive replacement)
- Underserved populations and equitable access
- Product development that combines learning science with user research
- Scaling evidence-based interventions

TARGET ROLES:
- Learning Designer, Instructional Designer, Learning Experience Designer
- Product Designer (education-focused), User Researcher (education-focused)
- Program Manager (education partnerships, impact-focused)
- Educational Technologist, Consultant (education transformation)
"""

# ===== SCORING THRESHOLDS =====

IMMEDIATE_ALERT_THRESHOLD = 8  # Score 8+ = immediate email
DAILY_DIGEST_THRESHOLD = 6     # Score 6+ included in daily digest

# ===== API CREDENTIALS (from environment variables) =====

# Google AI Studio
GOOGLE_AI_KEY = os.getenv('GOOGLE_AI_KEY')

# Adzuna
ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID')
ADZUNA_APP_KEY = os.getenv('ADZUNA_APP_KEY')

# SerpAPI (Google Jobs)
SERPAPI_KEY = os.getenv('SERPAPI_KEY')

# SendGrid (Email)
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'jobmonitor@yourdomain.com')
EMAIL_TO = os.getenv('EMAIL_TO')

# ===== GEOGRAPHY ROTATION SCHEDULE =====

def get_geography_for_today():
    """
    Determine which geography to search today based on rotation schedule.
    USA: Every 2 days
    Singapore: Every 3 days
    Dubai: Every 3 days
    
    Returns: geography name (USA, Singapore, or Dubai)
    """
    day_number = datetime.now().timetuple().tm_yday  # Day of year (1-365)
    
    # USA every 2 days: days 0, 2, 4, 6, 8, 10...
    # Singapore every 3 days starting day 1: days 1, 4, 7, 10, 13...
    # Dubai every 3 days starting day 3: days 3, 6, 9, 12, 15...
    
    if day_number % 2 == 0:
        return "USA"
    elif day_number % 3 == 1:
        return "Singapore"
    elif day_number % 3 == 0:
        return "Dubai"
    else:
        return "USA"  # Default fallback

# ===== FILE PATHS =====

DATABASE_FILE = "/home/claude/job-monitor/jobs_seen.json"
LOG_FILE = "/home/claude/job-monitor/job_monitor.log"
