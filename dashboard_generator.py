# dashboard_generator.py
# Generate beautiful interactive HTML dashboard for job viewing

import json
from datetime import datetime, timedelta
import os

def generate_dashboard(jobs_database, output_path="/home/claude/job-monitor/dashboard.html"):
    """
    Generate beautiful HTML dashboard from jobs database.
    
    Args:
        jobs_database: Dictionary of job_id -> job data
        output_path: Where to save dashboard.html
    """
    
    # Convert jobs dict to list and sort by score and date
    jobs_list = list(jobs_database.values())
    jobs_list.sort(key=lambda x: (
        -x.get('match_score', 0),  # Higher score first
        x.get('first_seen', '')    # More recent first
    ), reverse=False)
    
    # Calculate stats
    total_jobs = len(jobs_list)
    today = datetime.now().date()
    
    new_today = [j for j in jobs_list if datetime.fromisoformat(j.get('first_seen', '2000-01-01')).date() == today]
    new_this_week = [j for j in jobs_list if datetime.fromisoformat(j.get('first_seen', '2000-01-01')).date() >= today - timedelta(days=7)]
    
    high_matches = [j for j in jobs_list if j.get('match_score', 0) >= 8]
    
    # Get last update time
    last_update = datetime.now().strftime('%B %d, %Y at %I:%M %p')
    
    # Generate jobs HTML
    jobs_html = generate_jobs_html(jobs_list)
    
    # Generate full HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Monitor Dashboard</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        /* Header */
        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            color: #333;
            font-size: 32px;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        
        .stat-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        
        .stat-card .number {{
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .stat-card .label {{
            font-size: 12px;
            opacity: 0.9;
        }}
        
        /* Filters */
        .filters {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .filter-section {{
            margin-bottom: 15px;
        }}
        
        .filter-section:last-child {{
            margin-bottom: 0;
        }}
        
        .filter-label {{
            font-weight: 600;
            color: #333;
            margin-bottom: 8px;
            display: block;
            font-size: 14px;
        }}
        
        .filter-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        
        .filter-btn {{
            padding: 8px 16px;
            border: 2px solid #e0e0e0;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            color: #666;
            transition: all 0.2s;
        }}
        
        .filter-btn:hover {{
            border-color: #667eea;
            color: #667eea;
        }}
        
        .filter-btn.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: transparent;
        }}
        
        /* Jobs list */
        .jobs-container {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}
        
        .job-card {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        
        .job-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }}
        
        .job-card.applied {{
            opacity: 0.6;
            border-left: 4px solid #4CAF50;
        }}
        
        .job-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 15px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .job-title {{
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin-bottom: 5px;
        }}
        
        .job-company {{
            font-size: 16px;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .job-location {{
            font-size: 14px;
            color: #888;
        }}
        
        .score-badge {{
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 16px;
            white-space: nowrap;
        }}
        
        .score-9-10 {{
            background: #f44336;
            color: white;
        }}
        
        .score-7-8 {{
            background: #FF9800;
            color: white;
        }}
        
        .score-6 {{
            background: #4CAF50;
            color: white;
        }}
        
        .job-details {{
            margin: 15px 0;
        }}
        
        .job-reasoning {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 15px 0;
        }}
        
        .job-reasoning strong {{
            color: #333;
            display: block;
            margin-bottom: 8px;
        }}
        
        .job-reasoning p {{
            color: #555;
            line-height: 1.6;
        }}
        
        .job-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }}
        
        .meta-tag {{
            display: inline-block;
            padding: 6px 12px;
            background: #f0f0f0;
            border-radius: 4px;
            font-size: 12px;
            color: #666;
        }}
        
        .job-actions {{
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }}
        
        .btn {{
            padding: 12px 24px;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            transition: all 0.2s;
            text-decoration: none;
            display: inline-block;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
        }}
        
        .btn-secondary {{
            background: white;
            color: #667eea;
            border: 2px solid #667eea;
        }}
        
        .btn-secondary:hover {{
            background: #667eea;
            color: white;
        }}
        
        .btn-success {{
            background: #4CAF50;
            color: white;
        }}
        
        .no-jobs {{
            background: white;
            border-radius: 12px;
            padding: 40px;
            text-align: center;
            color: #666;
        }}
        
        .no-jobs-icon {{
            font-size: 48px;
            margin-bottom: 15px;
        }}
        
        /* Mobile responsive */
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 24px;
            }}
            
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .job-title {{
                font-size: 18px;
            }}
            
            .job-header {{
                flex-direction: column;
            }}
            
            .filter-buttons {{
                font-size: 12px;
            }}
        }}
        
        /* New today indicator */
        .new-today {{
            display: inline-block;
            background: #FF9800;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: bold;
            margin-left: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>🎯 Job Monitor Dashboard</h1>
            <div class="subtitle">Last updated: {last_update}</div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="number">{total_jobs}</div>
                    <div class="label">Total Jobs</div>
                </div>
                <div class="stat-card">
                    <div class="number">{len(new_today)}</div>
                    <div class="label">New Today</div>
                </div>
                <div class="stat-card">
                    <div class="number">{len(new_this_week)}</div>
                    <div class="label">This Week</div>
                </div>
                <div class="stat-card">
                    <div class="number">{len(high_matches)}</div>
                    <div class="label">High Matches (8+)</div>
                </div>
            </div>
        </div>
        
        <!-- Filters -->
        <div class="filters">
            <div class="filter-section">
                <span class="filter-label">Date Range:</span>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="date" data-value="all">All Jobs</button>
                    <button class="filter-btn" data-filter="date" data-value="today">New Today</button>
                    <button class="filter-btn" data-filter="date" data-value="week">This Week</button>
                    <button class="filter-btn" data-filter="date" data-value="applied">Applied</button>
                </div>
            </div>
            
            <div class="filter-section">
                <span class="filter-label">Score:</span>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="score" data-value="all">All Scores</button>
                    <button class="filter-btn" data-filter="score" data-value="9">9-10</button>
                    <button class="filter-btn" data-filter="score" data-value="8">8+</button>
                    <button class="filter-btn" data-filter="score" data-value="7">7+</button>
                    <button class="filter-btn" data-filter="score" data-value="6">6+</button>
                </div>
            </div>
            
            <div class="filter-section">
                <span class="filter-label">Location:</span>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="location" data-value="all">All Locations</button>
                    <button class="filter-btn" data-filter="location" data-value="usa">USA</button>
                    <button class="filter-btn" data-filter="location" data-value="singapore">Singapore</button>
                    <button class="filter-btn" data-filter="location" data-value="dubai">Dubai</button>
                </div>
            </div>
            
            <div class="filter-section">
                <span class="filter-label">Source:</span>
                <div class="filter-buttons">
                    <button class="filter-btn active" data-filter="source" data-value="all">All Sources</button>
                    <button class="filter-btn" data-filter="source" data-value="greenhouse">Greenhouse</button>
                    <button class="filter-btn" data-filter="source" data-value="adzuna">Adzuna</button>
                </div>
            </div>
        </div>
        
        <!-- Jobs List -->
        <div class="jobs-container" id="jobsContainer">
            {jobs_html}
        </div>
    </div>
    
    <script>
        // Track applied jobs in localStorage
        const appliedJobs = new Set(JSON.parse(localStorage.getItem('appliedJobs') || '[]'));
        
        // Mark already applied jobs
        appliedJobs.forEach(jobId => {{
            const card = document.querySelector(`[data-job-id="${{jobId}}"]`);
            if (card) {{
                card.classList.add('applied');
                const btn = card.querySelector('.mark-applied-btn');
                if (btn) {{
                    btn.textContent = '✓ Applied';
                    btn.classList.remove('btn-secondary');
                    btn.classList.add('btn-success');
                }}
            }}
        }});
        
        // Handle "Mark as Applied" buttons
        document.querySelectorAll('.mark-applied-btn').forEach(btn => {{
            btn.addEventListener('click', (e) => {{
                e.preventDefault();
                const jobId = btn.dataset.jobId;
                const card = document.querySelector(`[data-job-id="${{jobId}}"]`);
                
                if (appliedJobs.has(jobId)) {{
                    // Unapply
                    appliedJobs.delete(jobId);
                    card.classList.remove('applied');
                    btn.textContent = 'Mark as Applied';
                    btn.classList.remove('btn-success');
                    btn.classList.add('btn-secondary');
                }} else {{
                    // Apply
                    appliedJobs.add(jobId);
                    card.classList.add('applied');
                    btn.textContent = '✓ Applied';
                    btn.classList.remove('btn-secondary');
                    btn.classList.add('btn-success');
                }}
                
                localStorage.setItem('appliedJobs', JSON.stringify([...appliedJobs]));
            }});
        }});
        
        // Filtering logic
        let filters = {{
            date: 'all',
            score: 'all',
            location: 'all',
            source: 'all'
        }};
        
        // Filter button handlers
        document.querySelectorAll('.filter-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                const filterType = btn.dataset.filter;
                const filterValue = btn.dataset.value;
                
                // Update active state
                document.querySelectorAll(`[data-filter="${{filterType}}"]`).forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Update filter
                filters[filterType] = filterValue;
                
                // Apply filters
                applyFilters();
            }});
        }});
        
        function applyFilters() {{
            const jobs = document.querySelectorAll('.job-card');
            let visibleCount = 0;
            
            jobs.forEach(job => {{
                let show = true;
                
                // Date filter
                if (filters.date !== 'all') {{
                    const dateFilter = job.dataset.dateFilter;
                    if (filters.date === 'today' && dateFilter !== 'today') show = false;
                    if (filters.date === 'week' && dateFilter !== 'today' && dateFilter !== 'week') show = false;
                    if (filters.date === 'applied' && !job.classList.contains('applied')) show = false;
                }}
                
                // Score filter
                if (filters.score !== 'all') {{
                    const score = parseInt(job.dataset.score);
                    const minScore = parseInt(filters.score);
                    if (score < minScore) show = false;
                }}
                
                // Location filter
                if (filters.location !== 'all') {{
                    const location = job.dataset.location.toLowerCase();
                    if (!location.includes(filters.location)) show = false;
                }}
                
                // Source filter
                if (filters.source !== 'all') {{
                    const source = job.dataset.source.toLowerCase();
                    if (!source.includes(filters.source)) show = false;
                }}
                
                // Show/hide job
                job.style.display = show ? 'block' : 'none';
                if (show) visibleCount++;
            }});
            
            // Show "no jobs" message if nothing visible
            const container = document.getElementById('jobsContainer');
            let noJobsMsg = container.querySelector('.no-jobs');
            
            if (visibleCount === 0) {{
                if (!noJobsMsg) {{
                    noJobsMsg = document.createElement('div');
                    noJobsMsg.className = 'no-jobs';
                    noJobsMsg.innerHTML = '<div class="no-jobs-icon">🔍</div><p>No jobs match your current filters.</p><p style="margin-top: 10px; font-size: 14px;">Try adjusting your filters above.</p>';
                    container.appendChild(noJobsMsg);
                }}
            }} else {{
                if (noJobsMsg) noJobsMsg.remove();
            }}
        }}
    </script>
</body>
</html>
"""
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard generated: {output_path}")
    print(f"   - Total jobs: {total_jobs}")
    print(f"   - New today: {len(new_today)}")
    print(f"   - This week: {len(new_this_week)}")
    print(f"   - High matches: {len(high_matches)}")

def generate_jobs_html(jobs_list):
    """Generate HTML for individual job cards."""
    
    if not jobs_list:
        return """
        <div class="no-jobs">
            <div class="no-jobs-icon">📭</div>
            <p>No jobs in database yet.</p>
            <p style="margin-top: 10px; font-size: 14px;">Jobs will appear here after the first monitoring run.</p>
        </div>
        """
    
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    jobs_html = ""
    
    for job in jobs_list:
        score = job.get('match_score', 0)
        analysis = job.get('ai_analysis', {})
        
        # Score badge
        if score >= 9:
            score_class = "score-9-10"
            score_emoji = "🔥"
        elif score >= 7:
            score_class = "score-7-8"
            score_emoji = "⚡"
        else:
            score_class = "score-6"
            score_emoji = "✓"
        
        # Date filtering
        job_date = datetime.fromisoformat(job.get('first_seen', '2000-01-01')).date()
        if job_date == today:
            date_filter = "today"
            new_badge = '<span class="new-today">NEW TODAY</span>'
        elif job_date >= week_ago:
            date_filter = "week"
            new_badge = ""
        else:
            date_filter = "old"
            new_badge = ""
        
        # Reasoning
        reasoning = analysis.get('reasoning', 'No detailed analysis available.')
        
        # Meta tags
        category = analysis.get('role_category', 'N/A').replace('_', ' ').title()
        source = job.get('source', 'Unknown')
        
        # Clean location for filtering
        location = job.get('location', 'Unknown')
        
        # Date display
        date_display = datetime.fromisoformat(job.get('first_seen', '2000-01-01')).strftime('%B %d, %Y at %I:%M %p')
        
        jobs_html += f"""
        <div class="job-card" 
             data-job-id="{job.get('job_id', '')}"
             data-score="{score}"
             data-location="{location}"
             data-source="{source}"
             data-date-filter="{date_filter}">
            
            <div class="job-header">
                <div>
                    <div class="job-title">
                        {score_emoji} {job.get('title', 'Untitled Position')}
                        {new_badge}
                    </div>
                    <div class="job-company">{job.get('company', 'Unknown Company')}</div>
                    <div class="job-location">📍 {location}</div>
                </div>
                <div class="score-badge {score_class}">
                    {score}/10
                </div>
            </div>
            
            <div class="job-reasoning">
                <strong>Why this matches:</strong>
                <p>{reasoning}</p>
            </div>
            
            <div class="job-meta">
                <span class="meta-tag">📂 {category}</span>
                <span class="meta-tag">🔍 {source}</span>
                <span class="meta-tag">📅 {date_display}</span>
            </div>
            
            <div class="job-actions">
                <a href="{job.get('url', '#')}" target="_blank" class="btn btn-primary">
                    🔗 View Job & Apply
                </a>
                <button class="btn btn-secondary mark-applied-btn" data-job-id="{job.get('job_id', '')}">
                    Mark as Applied
                </button>
            </div>
        </div>
        """
    
    return jobs_html

if __name__ == "__main__":
    # Test dashboard generation
    print("Testing dashboard generator...")
    
    # Create sample jobs
    sample_jobs = {
        "job1": {
            "job_id": "job1",
            "title": "Learning Designer",
            "company": "Khan Academy",
            "location": "Remote USA",
            "url": "https://example.com/job1",
            "source": "Greenhouse",
            "match_score": 9,
            "first_seen": datetime.now().isoformat(),
            "ai_analysis": {
                "score": 9,
                "reasoning": "Perfect match for learning design with focus on underserved populations and evidence-based approaches.",
                "role_category": "learning_design",
                "is_match": True
            }
        },
        "job2": {
            "job_id": "job2",
            "title": "Program Manager, Global Education",
            "company": "Anthropic",
            "location": "USA-Remote",
            "url": "https://example.com/job2",
            "source": "Greenhouse",
            "match_score": 8,
            "first_seen": (datetime.now() - timedelta(days=1)).isoformat(),
            "ai_analysis": {
                "score": 8,
                "reasoning": "Strong alignment with experience in education partnerships and underserved populations.",
                "role_category": "program_mgmt",
                "is_match": True
            }
        }
    }
    
    generate_dashboard(sample_jobs, "/tmp/test_dashboard.html")
    print("\n✓ Test dashboard created at /tmp/test_dashboard.html")
    print("Open this file in a browser to preview!")
