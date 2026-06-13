import streamlit as st
import urllib.parse
from database.db import engine
from database.models import Base
Base.metadata.create_all(bind=engine)
from ui.register import show_register
from ui.login import show_login
from ui.dashboard import show_dashboard
from backend.ai.skill_extractor import extract_skills_llm
from backend.matching.skill_matcher import compare_skills
from backend.ai.recommender import recommend_skills
from backend.parsers.pdf_parser import extract_pdf_text
from backend.parsers.docx_parser import extract_docx_text
from database.models import Resume
from database.db import SessionLocal

COURSE_LINKS = {
    "python":           ("https://www.coursera.org/learn/python", "~6 hrs"),
    "sql":              ("https://www.coursera.org/learn/sql-for-data-science", "~5 hrs"),
    "power bi":         ("https://learn.microsoft.com/en-us/training/powerplatform/power-bi/", "~5 hrs"),
    "tableau":          ("https://www.coursera.org/specializations/data-visualization", "~6 hrs"),
    "machine learning": ("https://www.coursera.org/learn/machine-learning", "~12 hrs"),
    "excel":            ("https://www.coursera.org/learn/excel-skills-for-business", "~4 hrs"),
    "pandas":           ("https://www.coursera.org/projects/data-analysis-pandas", "~4 hrs"),
    "numpy":            ("https://www.coursera.org/projects/python-numpy", "~3 hrs"),
    "java":             ("https://www.coursera.org/specializations/java-programming", "~8 hrs"),
    "c++":              ("https://www.coursera.org/learn/c-plus-plus-a", "~8 hrs"),
    "react":            ("https://react.dev/learn", "~10 hrs"),
    "fastapi":          ("https://fastapi.tiangolo.com/tutorial/", "~4 hrs"),
    "streamlit":        ("https://docs.streamlit.io/get-started", "~3 hrs"),
    "mongodb":          ("https://learn.mongodb.com/", "~5 hrs"),
    "mysql":            ("https://www.coursera.org/learn/database-management", "~6 hrs"),
}

st.set_page_config(
    page_title="AI Resume Intelligence Platform",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/tabler-icons.min.css">
""", unsafe_allow_html=True)

st.markdown("""
<style>
* { box-sizing: border-box; }

[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 0.5px solid #e8e8e4;
}
[data-testid="stSidebar"] > div:first-child {
    padding: 1.25rem 1rem 1rem;
}
.sidebar-brand {
    display: flex; align-items: center; gap: 9px;
    padding: 2px 6px 1.25rem;
    border-bottom: 0.5px solid #ebebeb;
    margin-bottom: 1.25rem;
}
.brand-icon {
    width: 28px; height: 28px; background: #1a56db;
    border-radius: 7px; display: flex;
    align-items: center; justify-content: center; flex-shrink: 0;
}
.brand-name { font-size: 14px; font-weight: 600; color: #111; letter-spacing: -0.01em; }

.nav-label {
    font-size: 10.5px; font-weight: 600; letter-spacing: 0.07em;
    text-transform: uppercase; color: #aaa; padding: 0 8px; 
    margin-bottom: 2px;
}
.nav-divider { height: 0.5px; background: #ebebeb; margin: 6px 8px; }

div[data-testid="stSidebar"] div.element-container {
    margin-bottom: -10px !important;
}

div[data-testid="stSidebar"] div[data-testid="stButton"] > button {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    width: 100% !important;
    background: transparent !important;
    border: none !important;
    color: #555 !important;
    padding: 6px 12px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    text-align: left !important;
    box-shadow: none !important;
    transition: background 0.1s ease, color 0.1s ease;
}

div[data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
    background: #f4f4f2 !important;
    color: #111 !important;
}
div[data-testid="stSidebar"] div.active-nav-btn div[data-testid="stButton"] > button {
    background: #f0f0ee !important;
    color: #1a1a1a !important;
    font-weight: 500 !important;
}

div[data-testid="stSidebar"] div.logout-btn-wrap div[data-testid="stButton"] > button {
    color: #e24b4a !important;
}
div[data-testid="stSidebar"] div.logout-btn-wrap div[data-testid="stButton"] > button:hover {
    background: #fcebeb !important;
}

.main .block-container {
    background-color: #fafaf8; padding-top: 2rem; max-width: 1080px;
}
div[data-testid="stMainView"] div[data-testid="stButton"] > button {
    background: #1a56db !important; color: white !important;
    border: none !important; border-radius: 8px !important;
    font-size: 14px !important; font-weight: 500 !important;
}
div[data-testid="stMainView"] div[data-testid="stButton"] > button:hover {
    background: #1648c0 !important; color: white !important;
}
.page-header { margin-bottom: 1.75rem; }
.page-header h1 {
    font-size: 24px !important; font-weight: 700 !important;
    color: #0a0a0a !important; letter-spacing: -0.02em;
    margin: 0 0 4px !important; padding: 0 !important;
}
.page-header p { font-size: 15px; color: #555; margin: 0; }

.section-label {
    font-size: 12px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.07em; color: #777;
    margin-bottom: 10px; margin-top: 1.5rem;
}

.upload-card-title {
    font-size: 14px; font-weight: 600; color: #0a0a0a;
    margin-bottom: 0.5rem;
    display: flex; align-items: center; gap: 7px;
}
.upload-card-title i { font-size: 16px; color: #666; }

.score-card {
    background: #ffffff; border: 0.5px solid #e8e8e4;
    border-radius: 12px; padding: 1.25rem 1.5rem;
    display: flex; align-items: center; gap: 1.5rem; margin-bottom: 1.25rem;
}
.score-ring-wrap { position: relative; width: 76px; height: 76px; flex-shrink: 0; }
.score-ring-wrap svg { width: 76px; height: 76px; transform: rotate(-90deg); }
.score-ring-bg  { fill: none; stroke: #ebebeb; stroke-width: 6; }
.score-ring-fill { fill: none; stroke-width: 6; stroke-linecap: round; stroke-dasharray: 201; }
.score-num {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-size: 16px; font-weight: 700; color: #0a0a0a;
}
.score-ring-label { font-size: 10px; color: #aaa; text-align: center; margin-top: 4px; font-weight: 500; }
.score-info { flex: 1; }
.score-info h3 { font-size: 16px; font-weight: 700; margin: 0 0 4px; }
.score-info p  { font-size: 13px; color: #666; margin: 0 0 10px; line-height: 1.5; }
.score-bar-wrap { height: 3px; background: #ebebeb; border-radius: 2px; }
.score-bar-fill { height: 3px; border-radius: 2px; }

.skills-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 1.25rem; }
.skill-card {
    background: #ffffff; border: 0.5px solid #e8e8e4;
    border-radius: 12px; padding: 1rem 1.25rem;
}
.skill-card-header { display: flex; align-items: center; gap: 7px; margin-bottom: 10px; }
.skill-card-header i    { font-size: 15px; color: #aaa; }
.skill-card-header span { font-size: 13px; font-weight: 700; color: #0a0a0a; }
.tag-wrap { display: flex; flex-wrap: wrap; gap: 5px; }
.tag {
    font-size: 12px; padding: 3px 8px; border-radius: 4px;
    background: #f0f0ed; color: #555;
    border: 0.5px solid #e8e8e4; font-weight: 500;
}
.tag-match { background: #eaf3de; color: #3b6d11; border-color: #c0dd97; }
.tag-miss  { background: #fcebeb; color: #a32d2d; border-color: #f0a0a0; }

.rec-list { display: flex; flex-direction: column; gap: 8px; margin-top: 0.5rem; }
.rec-item {
    display: flex; align-items: center; gap: 12px;
    background: #ffffff; border: 0.5px solid #e8e8e4;
    border-radius: 10px; padding: 0.875rem 1.25rem;
}
.rec-item-info { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.rec-item-info span { font-size: 14px; font-weight: 600; color: #0a0a0a; }
.rec-item-info a { font-size: 12px; color: #1a56db; text-decoration: none; font-weight: 500; }
.rec-item-info a:hover { text-decoration: underline; }
</style>
""", unsafe_allow_html=True)

# ── Nav config ───────────────────────────────────────────────────────
AUTH_NAV = [
    ("Login",    "ti-login"),
    ("Register", "ti-user-plus"),
]
APP_NAV = [
    ("Dashboard",       "ti-layout-dashboard"),
    ("Resume analysis", "ti-file-description"),
    ("Resume library",  "ti-copy"),
]

# ── Session state & Query Param Processing ───────────────────────────
if "logged_in"         not in st.session_state: st.session_state.logged_in = False
if "page"              not in st.session_state: st.session_state.page = "Dashboard"
if "auth_page"         not in st.session_state: st.session_state.auth_page = "Login"
if "completed_courses" not in st.session_state: st.session_state.completed_courses = {}
if "analysis_completed" not in st.session_state: st.session_state.analysis_completed = False
if "analysis_results"   not in st.session_state: st.session_state.analysis_results = {}
if "resume_history"    not in st.session_state: st.session_state.resume_history = []

# Callback function to handle checkbox verification cleanly without breaks
def update_course_status(skill_key):
    checkbox_key = f"course_{skill_key}"
    if checkbox_key in st.session_state:
        st.session_state.completed_courses[skill_key] = st.session_state[checkbox_key]

# Process click changes instantly using query params
params = st.query_params
if "nav" in params:
    raw_val = params["nav"].replace("_", " ")
    
    if not st.session_state.logged_in:
        auth_labels = [l for l, _ in AUTH_NAV]
        if raw_val in auth_labels:
            st.session_state.auth_page = raw_val
    else:
        app_labels = [l for l, _ in APP_NAV]
        if raw_val in app_labels:
            st.session_state.page = raw_val
        elif raw_val == "Logout":
            st.session_state.logged_in = False
            st.session_state.page = "Dashboard"
            st.query_params.clear()
            st.rerun()

# ── Navigation State Updaters ────────────────────────────────────────
def set_page(page_name):
    st.session_state.page = page_name

def set_auth_page(auth_name):
    st.session_state.auth_page = auth_name

# ── Sidebar Render ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-icon">
            <svg width="15" height="15" viewBox="0 0 15 15" fill="none">
                <path d="M2 3.5h11M2 7.5h7M2 11.5h9"
                      stroke="white" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <span class="brand-name">Resume Analytics</span>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.logged_in:
        st.markdown('<div class="nav-label">Account</div>', unsafe_allow_html=True)
        for label, icon in AUTH_NAV:
            is_active = st.session_state.auth_page == label
            wrapper_class = "active-nav-btn" if is_active else "inactive-nav-btn"
            
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            st.markdown(f'<div style="display: flex; align-items: center; padding-left: 12px;"><i class="ti {icon}" style="font-size: 16px; margin-right: -10px; color: inherit; z-index: 5; pointer-events: none;"></i>', unsafe_allow_html=True)
            if st.button(label, key=f"auth_{label}"):
                st.session_state.auth_page = label
                st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)
            
    else:
        st.markdown('<div class="nav-label">Main</div>', unsafe_allow_html=True)
        for label, icon in APP_NAV:
            is_active = st.session_state.page == label
            wrapper_class = "active-nav-btn" if is_active else "inactive-nav-btn"
            
            st.markdown(f'<div class="{wrapper_class}">', unsafe_allow_html=True)
            st.markdown(f'<div style="display: flex; align-items: center; padding-left: 12px;"><i class="ti {icon}" style="font-size: 16px; margin-right: -10px; color: inherit; z-index: 5; pointer-events: none;"></i>', unsafe_allow_html=True)
            if st.button(label, key=f"nav_{label}"):
                st.session_state.page = label
                st.rerun()
            st.markdown('</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="nav-divider"></div>', unsafe_allow_html=True)

        # Logout Button
        st.markdown('<div class="logout-btn-wrap">', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; align-items: center; padding-left: 12px;"><i class="ti ti-logout" style="font-size: 16px; margin-right: -10px; color: inherit; z-index: 5; pointer-events: none;"></i>', unsafe_allow_html=True)
        if st.button("Log out", key="nav_logout"):
            st.session_state.logged_in = False
            st.session_state.page = "Dashboard"
            st.rerun()
        st.markdown('</div></div>', unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────
def score_label(score):
    if score >= 75: return "Strong match",        "#3b6d11"
    if score >= 50: return "Good match",          "#185fa5"
    if score >= 25: return "Partial match",        "#ba7517"
    return             "Below average match",      "#a32d2d"

def score_offset(score):
    return 201 - (score / 100) * 201

def render_tag(skill, cls=""):
    return f'<span class="tag {cls}">{skill}</span>'

# ── Page routing ──────────────────────────────────────────────────────
if not st.session_state.logged_in:
    if st.session_state.auth_page == "Login":
        show_login()
    else:
        show_register()
else:
    if st.session_state.page == "Dashboard":
        db = SessionLocal()
        resumes = db.query(Resume).all()
        db.close()
        total_resumes = len(resumes)
        avg_score = (
            sum(r.match_score for r in resumes)
            / total_resumes
        ) if total_resumes else 0
        best_score = max(
            [r.match_score for r in resumes],
            default=0
        )
        completed_courses = sum(
            st.session_state.completed_courses.values()
        )
        st.markdown("""
        <div class="page-header">
            <h1>Dashboard</h1>
            <p>Your resume analytics overview</p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Total Resumes",
                total_resumes
            )
        with col2:
            st.metric(
                "Average Score",
                f"{avg_score:.1f}%"
            )
        with col3:
            st.metric(
                "Best Score",
                f"{best_score:.1f}%"
            )
        with col4:
            st.metric(
                "Courses Completed",
                completed_courses
            )
        st.divider()
        st.subheader("Recent Analyses")
        if resumes:
            for resume in resumes[-5:]:
                st.write(
                    f"📄 {resume.filename}"
                )
                st.progress(
                    resume.match_score / 100
                )
                st.caption(
                    f"{resume.match_score}% Match Score"
                )
        else:
            st.info(
                "No resume analyses available yet."
            )

    elif st.session_state.page == "Resume analysis":
        st.markdown("""
        <div class="page-header">
            <h1>Resume analysis</h1>
            <p>Compare your resume against a job description</p>
        </div>""", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<div class="upload-card-title" style="font-size: 14px; font-weight:500; margin-bottom:8px;">
                <i class="ti ti-file-text"></i> Resume
            </div>""", unsafe_allow_html=True)
            uploaded_resume = st.file_uploader("Upload resume", type=["pdf","docx"],
                                               label_visibility="collapsed", key="res_upload")
            resume_text = st.text_area("Or paste resume text", height=220,
                                       placeholder="Paste resume content here...", key="res_text")
        with col2:
            st.markdown("""<div class="upload-card-title" style="font-size: 14px; font-weight:500; margin-bottom:8px;">
                <i class="ti ti-briefcase"></i> Job description
            </div>""", unsafe_allow_html=True)
            jd_file = st.file_uploader("Upload job description", type=["pdf","docx","txt"],
                                       label_visibility="collapsed", key="jd_upload")
            jd_text = st.text_area("Or paste job description", height=220,
                                   placeholder="Paste job description here...", key="jd_text")

        analyze_btn = st.button("Analyze resume", use_container_width=True)

        if analyze_btn:
            if uploaded_resume:
                if uploaded_resume.name.endswith(".pdf"):
                    resume_text = extract_pdf_text(uploaded_resume)
                elif uploaded_resume.name.endswith(".docx"):
                    resume_text = extract_docx_text(uploaded_resume)
            if jd_file:
                if jd_file.name.endswith(".pdf"):
                    jd_text = extract_pdf_text(jd_file)
                elif jd_file.name.endswith(".docx"):
                    jd_text = extract_docx_text(jd_file)
                elif jd_file.name.endswith(".txt"):
                    jd_text = jd_file.read().decode("utf-8")

            if not resume_text:
                st.error("Please upload or paste your resume.")
                st.stop()
            if not jd_text:
                st.error("Please upload or paste the job description.")
                st.stop()

            with st.spinner("Analyzing…"):
                resume_skills = extract_skills_llm(resume_text)
                jd_skills     = extract_skills_llm(jd_text)
                result        = compare_skills(resume_skills, jd_skills)
                matched_skills = result["matched"]
                missing_skills = result["missing"]
                score          = result["score"]
                db = SessionLocal()
                resume_record = Resume(
                    filename=uploaded_resume.name
                    if uploaded_resume
                    else "Pasted Resume",
                    match_score=score,
                    matched_count=len(matched_skills),
                    missing_count=len(missing_skills)
                )
                db.add(resume_record)
                db.commit()
                db.close()
            label, label_color = score_label(score)
            st.session_state.analysis_results = {
                'resume_skills': resume_skills,
                'jd_skills': jd_skills,
                'matched_skills': matched_skills,
                'missing_skills': missing_skills,
                'score': score,
                'label': label,
                'label_color': label_color,
                'offset': score_offset(score)
            }
            st.session_state.analysis_completed = True

        if st.session_state.analysis_completed:
            results = st.session_state.analysis_results
            
            st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class="score-card">
                <div>
                    <div class="score-ring-wrap">
                        <svg viewBox="0 0 76 76">
                            <circle class="score-ring-bg" cx="38" cy="38" r="32"/>
                            <circle class="score-ring-fill" cx="38" cy="38" r="32"
                                stroke="{results['label_color']}"
                                stroke-dashoffset="{results['offset']:.1f}"/>
                        </svg>
                        <div class="score-num">{results['score']}%</div>
                    </div>
                    <div class="score-ring-label">ATS match</div>
                </div>
                <div class="score-info">
                    <h3 style="color:{results['label_color']}">{results['label']}</h3>
                    <p>Your resume matches <strong>{len(results['matched_skills'])}</strong> of
                    <strong>{len(results['jd_skills'])}</strong> required skills.
                    Add missing skills to improve your chances.</p>
                    <div class="score-bar-wrap">
                        <div class="score-bar-fill" style="width:{results['score']}%; background:{results['label_color']};"></div>
                    </div>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown('<div class="section-label">Skills breakdown</div>', unsafe_allow_html=True)

            res_tags     = "".join(render_tag(s, "tag-match" if s in results['matched_skills'] else "") for s in results['resume_skills'])
            jd_tags      = "".join(render_tag(s, "tag-match" if s in results['matched_skills'] else "tag-miss") for s in results['jd_skills'])
            matched_tags = "".join(render_tag(s, "tag-match") for s in results['matched_skills'])
            missing_tags = "".join(render_tag(s, "tag-miss")  for s in results['missing_skills'])

            st.markdown(f"""
            <div class="skills-grid">
                <div class="skill-card">
                    <div class="skill-card-header">
                        <i class="ti ti-file-text"></i><span>Resume skills</span>
                    </div>
                    <div class="tag-wrap">{res_tags or '<span style="font-size:12px;color:#aaa">No skills found</span>'}</div>
                </div>
                <div class="skill-card">
                    <div class="skill-card-header">
                        <i class="ti ti-briefcase"></i><span>JD skills</span>
                    </div>
                    <div class="tag-wrap">{jd_tags or '<span style="font-size:12px;color:#aaa">No skills found</span>'}</div>
                </div>
                <div class="skill-card">
                    <div class="skill-card-header">
                        <i class="ti ti-circle-check" style="color:#3b6d11"></i><span>Matched skills</span>
                    </div>
                    <div class="tag-wrap">{matched_tags or '<span style="font-size:12px;color:#aaa">None matched</span>'}</div>
                </div>
                <div class="skill-card">
                    <div class="skill-card-header">
                        <i class="ti ti-circle-x" style="color:#a32d2d"></i><span>Missing skills</span>
                    </div>
                    <div class="tag-wrap">{missing_tags or '<span style="font-size:12px;color:#aaa">None missing</span>'}</div>
                </div>
            </div>""", unsafe_allow_html=True)

            if results['missing_skills']:
                st.markdown('<div class="section-label">Recommended tutorials</div>', unsafe_allow_html=True)
                st.markdown('<div class="rec-list">', unsafe_allow_html=True)
                
                for skill in results['missing_skills']:
                    info = COURSE_LINKS.get(skill.lower())
                    link = info[0] if info else f"https://www.google.com/search?q={urllib.parse.quote(skill + ' tutorial')}"
                    duration = info[1] if info else "~varies"
                    
                    st.markdown(f"""
                    <div class="rec-item">
                        <div style="width:16px; height:16px; border-radius:3px; border:0.5px solid #e8e8e4; background:#fff; flex-shrink:0;"></div>
                        <div class="rec-item-info">
                            <span>{skill.title()}</span>
                            <a href="{link}" target="_blank">Learn {skill.title()} &rarr;</a>
                        </div>
                        <div style="display:flex; align-items:center; gap:5px; font-size:12px; color:#888; flex-shrink:0;">
                            <i class="ti ti-clock" style="font-size:15px;"></i> {duration}
                        </div>
                    </div>""", unsafe_allow_html=True)
                    
                    st.checkbox(
                        f"Mark {skill.title()} as completed",
                        value=st.session_state.completed_courses.get(skill, False),
                        key=f"course_{skill}",
                        on_change=update_course_status,
                        args=(skill,)
                    )
                
                st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == "Resume library":
        st.markdown("""
        <div class="page-header">
            <h1>Resume library</h1>
            <p>View previously analyzed resumes and match scores</p>
        </div>""", unsafe_allow_html=True)
        from datetime import datetime
        db = SessionLocal()
        # Query all records from the table, sorted by latest ID
        db_resumes = db.query(Resume).order_by(Resume.id.desc()).all()
        db.close()
        if not db_resumes:
            st.info("No resumes found in the database. Go to 'Resume analysis' to parse your first resume.")
        else:
            # --- Filter & Search Row Inputs ---
            col_search, col_filters = st.columns([1, 2])
            
            with col_search:
                search_query = st.text_input("Search", placeholder="Search by filename...", label_visibility="collapsed", key="lib_db_search")
            
            with col_filters:
                filter_choice = st.radio(
                    "Filter",
                    ["All", "High (75%+)", "Medium (50-74%)", "Low (<50%)"],
                    horizontal=True,
                    label_visibility="collapsed",
                    key="lib_db_filter"
                )

            # --- Map DB Records to Filtering Pipeline ---
            filtered_data = []
            for r in db_resumes:
                # --- FIX: Directly pull the newly added column values from the model object ---
                matched_count = getattr(r, 'matched_count', 0) 
                missing_count = getattr(r, 'missing_count', 0)
                
                # Format a display date (Use uploaded_at from your models.py)
                record_date = getattr(r, 'uploaded_at', None)
                date_str = record_date.strftime("%d-%m-%Y") if record_date else datetime.now().strftime("%d-%m-%Y")

                entry = {
                    "id": r.id,  # Keep track of database ID for unique keys
                    "filename": r.filename,
                    "date": date_str,
                    "score": float(r.match_score),
                    "matched": matched_count,
                    "missing": missing_count
                }
                filtered_data.append(entry)

            # Apply Search Filtering
            if search_query:
                filtered_data = [r for r in filtered_data if search_query.lower() in r['filename'].lower()]

            # Apply Score Category Filtering
            if filter_choice == "High (75%+)":
                filtered_data = [r for r in filtered_data if r['score'] >= 75]
            elif filter_choice == "Medium (50-74%)":
                filtered_data = [r for r in filtered_data if 50 <= r['score'] < 75]
            elif filter_choice == "Low (<50%)":
                filtered_data = [r for r in filtered_data if r['score'] < 50]

            # --- Render Library Grid ---
            if not filtered_data:
                st.warning("No records match your selected filters.")
            else:
                # Structure cards symmetrically inside 2 columns
                cols = st.columns(2) 
                for i, res in enumerate(filtered_data):
                    with cols[i % 2]:
                        # Assign color profiles dynamically based on standard ranges
                        if res['score'] >= 75:
                            color = "#3b6d11"  # Green
                        elif res['score'] >= 50:
                            color = "#ba7517"  # Amber
                        else:
                            color = "#a32d2d"  # Red
                        
                        st.markdown(f"""
                        <div class="library-card" style="margin-bottom: 10px;">
                            <div class="card-header-wrap">
                                <div class="file-icon-box">
                                    <i class="ti ti-file-text" style="color:#aaa; font-size:20px;"></i>
                                </div>
                                <div class="file-info">
                                    <h4>{res['filename']}</h4>
                                    <span>{res['date']}</span>
                                </div>
                            </div>
                            <div class="match-row">
                                <span class="match-label">Match Score</span>
                                <span class="match-value" style="color:{color}">{res['score']}%</span>
                            </div>
                            <div class="stats-row" style="margin-bottom: 15px;">
                                <div class="stat-item"><i class="ti ti-circle-check" style="color:#3b6d11;"></i> {res['matched']} matched</div>
                                <div class="stat-item"><i class="ti ti-circle-x" style="color:#a32d2d;"></i> {res['missing']} missing</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Operational Streamlit action buttons nested beneath card components
                        btn_col1, btn_col2 = st.columns(2)
                        with btn_col1:
                            # --- FIX: Appended database ID to key to prevent Streamlit DuplicateKeyErrors ---
                            st.button("View", key=f"db_view_{res['id']}_{i}", use_container_width=True)
                        with btn_col2:
                            st.button("Re-analyze", key=f"db_re_{res['id']}_{i}", use_container_width=True)
                        st.markdown("<br>", unsafe_allow_html=True)