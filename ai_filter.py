# ai_filter.py
# AI-powered job matching using Google AI Studio (Gemini)

import google.generativeai as genai
import json
import config

# Configure Google AI
if config.GOOGLE_AI_KEY:
    genai.configure(api_key=config.GOOGLE_AI_KEY)

def analyze_job_match(job):
    """
    Use Google AI Studio (Gemini) to analyze if job matches candidate profile.
    
    Args:
        job: Job dictionary with title, company, description, etc.
    
    Returns:
        Dictionary with:
        {
            'is_match': bool,
            'score': int (0-10),
            'reasoning': str,
            'role_category': str,
            'key_strengths': list,
            'concerns': list
        }
    """
    
    if not config.GOOGLE_AI_KEY:
        # Fallback: basic keyword matching if no AI available
        return fallback_keyword_match(job)
    
    # Build prompt
    prompt = f"""
You are analyzing if a job matches a candidate's profile for job search.

CANDIDATE PROFILE:
{config.YOUR_PROFILE}

JOB TO ANALYZE:
Title: {job.get('title', 'No title')}
Company: {job.get('company', 'Unknown')}
Location: {job.get('location', 'Unknown')}
Description: {job.get('description', 'No description')[:2000]}

SOURCE CONTEXT:
- Source: {job.get('source', 'Unknown')}
- Search Category: {job.get('search_category', 'General')}

TASK:
Analyze if this job is a good match for this candidate.

EVALUATION CRITERIA:
1. Role Type Match: Does the role align with target roles (Learning Designer, Instructional Designer, Product Designer for education, etc.)?
2. Education Focus: Is this genuinely education/learning-focused work?
3. Mission Alignment: Does it involve underserved populations, evidence-based approaches, or inclusive design?
4. Experience Match: Does it leverage candidate's 8+ years in teaching, EdTech, research?
5. Skills Fit: Learning science, product thinking, user research, systematic frameworks?
6. Career Growth: Would this be a good next step given Harvard master's program?

SCORING GUIDE:
9-10: Perfect match - dream job, apply immediately
7-8: Strong match - high priority, apply soon
5-6: Decent match - worth considering
3-4: Weak match - maybe if nothing better
0-2: Poor match - wrong role type or not education-focused

IMPORTANT FILTERS:
- EXCLUDE pure software engineering, sales, marketing (unless learning-focused)
- INCLUDE roles that combine education + product/design/research
- PRIORITIZE roles with impact on underserved populations
- VALUE evidence-based, research-driven approaches

Respond ONLY with valid JSON (no markdown, no code blocks, no preamble):
{{
    "is_match": true/false,
    "score": 0-10,
    "reasoning": "2-3 sentence explanation of why this is/isn't a match",
    "role_category": "learning_design|instructional_design|product_design|user_research|program_mgmt|edtech|consultant|other",
    "key_strengths": ["strength1", "strength2"],
    "concerns": ["concern1", "concern2"]
}}
"""
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        # Clean response text
        text = response.text.strip()
        
        # Remove markdown code blocks if present
        if text.startswith('```'):
            text = '\n'.join(text.split('\n')[1:-1])
        if text.startswith('json'):
            text = text[4:].strip()
        
        # Parse JSON
        result = json.loads(text)
        
        # Validate required fields
        required_fields = ['is_match', 'score', 'reasoning', 'role_category']
        if not all(field in result for field in required_fields):
            raise ValueError("Missing required fields in AI response")
        
        return result
    
    except json.JSONDecodeError as e:
        print(f"  ⚠️  AI JSON parse error: {e}")
        print(f"  Response was: {text[:200]}")
        return fallback_keyword_match(job)
    
    except Exception as e:
        print(f"  ⚠️  AI analysis error: {e}")
        return fallback_keyword_match(job)

def fallback_keyword_match(job):
    """
    Fallback keyword-based matching when AI is unavailable.
    Simple but fast.
    """
    title = job.get('title', '').lower()
    description = job.get('description', '').lower()
    combined = title + ' ' + description
    
    # Check for role type matches
    role_matches = 0
    matched_role = "other"
    
    role_keywords = {
        'learning_design': ['learning designer', 'learning design', 'learning experience'],
        'instructional_design': ['instructional designer', 'instructional design', 'curriculum'],
        'product_design': ['product designer', 'product design', 'ux design'],
        'user_research': ['user researcher', 'ux researcher', 'user research'],
        'program_mgmt': ['program manager', 'program management', 'partnership manager'],
        'edtech': ['educational technologist', 'edtech', 'education technology'],
        'consultant': ['consultant', 'consulting']
    }
    
    for role_type, keywords in role_keywords.items():
        if any(keyword in combined for keyword in keywords):
            role_matches += 1
            matched_role = role_type
    
    # Check for exclude keywords
    for exclude in config.EXCLUDE_KEYWORDS:
        if exclude.lower() in title:
            return {
                'is_match': False,
                'score': 0,
                'reasoning': f"Excluded role type: {exclude}",
                'role_category': 'excluded',
                'key_strengths': [],
                'concerns': ['Not target role type']
            }
    
    # Check for education focus
    edu_keywords = ['education', 'learning', 'teaching', 'student', 'school', 'university', 'edtech']
    edu_match = any(keyword in combined for keyword in edu_keywords)
    
    # Calculate score
    score = 0
    if role_matches > 0:
        score += 4
    if edu_match:
        score += 3
    
    # Bonus points
    if 'ai' in combined or 'artificial intelligence' in combined:
        score += 1
    if 'underserved' in combined or 'equity' in combined or 'inclusive' in combined:
        score += 1
    if 'research' in combined or 'evidence' in combined:
        score += 1
    
    is_match = score >= 5
    
    return {
        'is_match': is_match,
        'score': min(score, 10),
        'reasoning': f"Keyword match: role={role_matches>0}, education={edu_match}",
        'role_category': matched_role,
        'key_strengths': ['Role type match'] if role_matches > 0 else [],
        'concerns': [] if is_match else ['Weak keyword match']
    }

def filter_jobs(jobs, min_score=6):
    """
    Filter list of jobs using AI analysis.
    
    Args:
        jobs: List of job dictionaries
        min_score: Minimum score to keep (default 6)
    
    Returns:
        List of jobs that match, with analysis added to each job
    """
    print(f"\n🤖 AI filtering {len(jobs)} jobs...")
    
    matched_jobs = []
    
    for i, job in enumerate(jobs, 1):
        if i % 10 == 0:
            print(f"  Progress: {i}/{len(jobs)}")
        
        # Run AI analysis
        analysis = analyze_job_match(job)
        
        # Add analysis to job
        job['ai_analysis'] = analysis
        job['match_score'] = analysis['score']
        
        # Keep if matches threshold
        if analysis['is_match'] and analysis['score'] >= min_score:
            matched_jobs.append(job)
    
    print(f"✅ AI filtering complete: {len(matched_jobs)} matches")
    return matched_jobs

if __name__ == "__main__":
    # Test AI filtering
    print("Testing AI filter...")
    
    test_job = {
        'title': 'Learning Designer',
        'company': 'Khan Academy',
        'location': 'Remote USA',
        'description': 'We are seeking a Learning Designer to create evidence-based learning experiences for underserved students. You will work with our product and research teams to design adaptive learning pathways using AI.',
        'source': 'Test',
        'search_category': 'EdTech Platforms'
    }
    
    print("\nAnalyzing test job...")
    print(f"Title: {test_job['title']}")
    print(f"Company: {test_job['company']}")
    
    result = analyze_job_match(test_job)
    
    print(f"\n📊 RESULTS:")
    print(f"Match: {result['is_match']}")
    print(f"Score: {result['score']}/10")
    print(f"Category: {result['role_category']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Strengths: {result.get('key_strengths', [])}")
    print(f"Concerns: {result.get('concerns', [])}")
