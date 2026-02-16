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

EXPERIENCE (8+ years spanning teaching, EdTech product development, consulting, and adult learning):

Teaching & Instructional Design:
- Teach for India Fellow and Program Manager: Worked with children in underserved communities including red-light districts, developing evidence-based teaching approaches and managing educational programs
- Shiv Nadar School: Explored instructional design excellence through experimentation with innovative teaching methods to achieve optimal learning outcomes

EdTech Product Development:
- Byju's & Bhanzu: Led MVP development, curriculum development, and content development for learning platforms
- Designed learning experiences combining pedagogical principles with product thinking
- Developed educational content and curricula aligned with learning science frameworks

Consulting & Learning Systems:
- Genpact & Aga Khan Foundation: Large-scale technology adoption projects
- Learning System Development: Designed and implemented comprehensive learning systems and frameworks
- Change Management: Led organizational change initiatives for technology adoption and learning transformation

Adult Learning & User Research:
- Wisdom Circle: Adult learning product development and user research with older adults navigating technology
- Conducted qualitative research to understand learner needs and barriers

RESEARCH & FRAMEWORKS:

Research:
- Examining technology adoption and engagement among underserved populations (older adults)
- Developed 5 evidence-based design principles for age-inclusive technology
- Validated through expert interviews with professionals from AARP, GetSetUp, and other organizations
- Focus on cognitive partnership with AI: Exploring how humans and AI systems can work together in learning contexts
- Construct development around human-AI collaboration in educational settings

EXPERTISE & CORE COMPETENCIES:

Learning Design & Instruction:
- Learning Design (instructional strategies, learning experiences, learner-centered design)
- Instructional Design (curriculum development, content design, assessment design)
- Learning Science principles and evidence-based approaches
- AI-integrated learning (designing learning experiences that leverage AI tools and capabilities)
- Learning Analytics (measuring learning outcomes, data-driven design decisions)

Product & Research:
- Product Thinking and user-centered design
- User Research and qualitative methods
- Inclusive Design for diverse and underserved populations
- Implementation at Scale (systems thinking, organizational change)

Frameworks & Approaches:
- Evidence-based frameworks and systematic approaches
- Design principles for overlooked or underserved populations
- Human-centered research methodologies

TARGET ROLES:

Primary Focus:
- Learning Designer
- Instructional Designer
- Learning Experience Designer (LXD)
- Educational Technologist

Product & Research (Education-focused):
- Product Designer (education products)
- User Researcher (learning/education)
- Product Manager (education technology - seeking candidates transitioning into PM roles or those with strong learning design background even without extensive PM experience)
- Program Manager (education/learning programs)

Consulting & Strategy:
- Learning Consultant
- L&D Consultant
- Education Consultant

PREFERENCES:

Industries/Sectors:
- AI + Education (companies using AI for learning)
- EdTech Platforms (learning management systems, online education)
- Corporate Learning & L&D (workplace training, employee development, learning systems)
- Nonprofits/Foundations (educational nonprofits, social impact organizations)

Work Values:
- Evidence-based approaches
- Focus on underserved or overlooked populations
- Systematic and rigorous design processes
- Combining learning science with product thinking
- Impact-driven work

Locations:
- USA (all states, including remote)
- Singapore
- Dubai/UAE
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

import os

# Get the directory where this script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use relative paths that work both locally and on GitHub Actions
DATABASE_FILE = os.path.join(BASE_DIR, "jobs_seen.json")
LOG_FILE = os.path.join(BASE_DIR, "job_monitor.log")
