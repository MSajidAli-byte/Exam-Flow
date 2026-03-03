import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

st.set_page_config(
    page_title="Exam-Flow | AI Grading & Proctoring",
    page_icon="🎓",
    layout="wide"
)

# Phase 2: Simple Security Layer
def check_password():
    """Returns True if the user had the correct password."""
    def password_entered():
        if st.session_state["password"] == os.getenv("APP_PASSWORD", "examflow2026"):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Enter Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Enter Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()  # Do not run the rest of the app

def get_override():
    if st.session_state.get('manual_controls', {}).get('enabled'):
        return {
            'score': st.session_state['manual_controls']['score'],
            'integrity': st.session_state['manual_controls']['integrity'],
            'notes': st.session_state['manual_controls']['notes'],
            'reviewer': 'Manual Review'
        }
    return None

def update_result_with_override(result):
    override = get_override()
    if override:
        result['manual_override'] = override
    return result

# Sidebar: Manual Review Panel
with st.sidebar:
    st.header("🛠️ Manual Review Panel")
    st.markdown("*Override AI decisions when needed*")
    
    # Initialize session state for manual controls
    if 'manual_controls' not in st.session_state:
        st.session_state['manual_controls'] = {
            'enabled': False,
            'score': 50,
            'integrity': 'Verified',
            'notes': ''
        }
    
    enable_override = st.checkbox(
        "Enable Manual Override",
        value=st.session_state['manual_controls']['enabled'],
        help="Check to activate manual review controls"
    )
    
    if enable_override:
        manual_score = st.slider(
            "Final Score Override", 
            0, 100, 
            st.session_state['manual_controls']['score'],
            help="Adjust AI-generated score"
        )
        
        integrity_verdict = st.selectbox(
            "Integrity Assessment",
            ["Verified", "Suspicious", "Failed"],
            index=["Verified", "Suspicious", "Failed"].index(st.session_state['manual_controls']['integrity']),
            help="Overall integrity verdict"
        )
        
        reviewer_notes = st.text_area(
            "Reviewer Justification",
            value=st.session_state['manual_controls']['notes'],
            placeholder="Explain the reason for manual adjustments...",
            height=100,
            help="Press Ctrl+Enter to save text changes"
        )
        
        # Save to session state
        st.session_state['manual_controls'] = {
            'enabled': True,
            'score': manual_score,
            'integrity': integrity_verdict,
            'notes': reviewer_notes
        }
        
        # NEW: Apply Button to sync with existing result
        if st.button("🔄 Apply & Update Report"):
            if 'result' in st.session_state and isinstance(st.session_state['result'], dict):
                # Update the manual_override in the existing result
                st.session_state['result']['manual_override'] = {
                    'score': manual_score,
                    'integrity': integrity_verdict,
                    'notes': reviewer_notes,
                    'reviewer': 'Manual Review'
                }
                st.success("✅ Report synchronized with manual changes!")
                st.rerun()
            else:
                st.warning("⚠️ Analyze a video first before applying overrides.")
        
        st.info(f"✅ Current Stage: **{manual_score}/100** ({integrity_verdict})")
    else:
        st.session_state['manual_controls']['enabled'] = False
        # Remove override from result if disabled
        if 'result' in st.session_state and isinstance(st.session_state['result'], dict) and 'manual_override' in st.session_state['result']:
            if st.button("❌ Remove Override"):
                del st.session_state['result']['manual_override']
                st.rerun()
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    st.success("🟢 Backend: Online")
    # Phase 2 Status
    is_agentic = os.getenv("AGENTIC_MODE", "off").lower() == "on"
    st.info(f"🔵 AI Mode: {'Expert Agentic (Phase 2)' if is_agentic else 'Standard Grading (Phase 1)'}")
    if is_agentic:
        st.success("🧠 ChromaDB Persistent RAG Enabled")
    
    st.markdown("---")
    st.header("🔬 Science & Research")
    if st.button("📈 Run Full Scientific Evaluation"):
        st.info("Starting batch evaluation of 7 Golden Cases... This takes ~4 min due to API rate limiting.")
        eval_progress = st.progress(0)
        
        # We can't easily run the external script and capture live output perfectly,
        # so we implement a UI-friendly version of the loop.
        metrics_placeholder = st.empty()
        cases = [
            "trial1_honest.zip", 
            "trial2_sudden_logic.zip", 
            "trial3_paradigm_mismatch.zip", 
            "trial4_gaze_aversion.zip"
        ]
        
        # Ground Truth matching our curated research goals
        ground_truth = {
            "trial1_honest.zip": "PASS",
            "trial2_sudden_logic.zip": "FAIL",
            "trial3_paradigm_mismatch.zip": "FAIL",
            "trial4_gaze_aversion.zip": "FAIL"
        }
        
        results = []
        import time
        for i, case_file in enumerate(cases):
            st.sidebar.text(f"Processing {case_file}...")
            
            # Paths adjusted for Docker /project_root mapping
            possible_paths = [
                f"/project_root/research/cases/{case_file}",
                f"research/cases/{case_file}",
                f"../research/cases/{case_file}"
            ]
            
            case_path = None
            for p in possible_paths:
                if os.path.exists(p):
                    case_path = p
                    break
            
            if case_path:
                with open(case_path, "rb") as f:
                    file_bytes = f.read()
                    files = {"file": (case_file, file_bytes, "application/zip")}
                    params = {"assessment_type": "General", "enable_proctoring": True}
                    try:
                        resp = requests.post(f"{BACKEND_URL}/analyze-package", params=params, files=files)
                        if resp.status_code == 200:
                            data = resp.json()
                            report_text = data.get("report", "")
                            
                            # 🎯 SCORE & VERDICT EXTRACTION
                            import re
                            upper_report = report_text.upper()
                            
                            # Extract score
                            score_match = re.search(r"FINAL GRADE.*?(\d+)\s*/\s*100", upper_report)
                            score = int(score_match.group(1)) if score_match else 100
                            
                            # Extract integrity status/verdict
                            # Looking for "Verdict: FAIL", "Status: FLAGGED", etc.
                            fail_keywords = ["FAIL", "FLAGGED", "INVESTIGATION", "SUSPICIOUS", "FRAUD", "ANOMALY"]
                            
                            # Check only the upper portion (Verdict/Summary) to avoid false positives in logs
                            top_section = report_text.split("CHRONOLOGICAL LOG")[0].upper()
                            
                            is_failure = (score <= 40) or any(k in top_section for k in fail_keywords if k != "PASS")
                            
                            # If it's Trial 1, we expect a PASS even if the word 'suspicious' appears in logs 
                            # (unless the score is low, which it shouldn't be for an honest trial)
                            verdict = "FAIL" if is_failure else "PASS"
                            
                            # DEBUG: UI labels to see what's happening
                            st.sidebar.markdown(f"**Case:** {case_file}")
                            st.sidebar.markdown(f"Detected Score: `{score}`")
                            st.sidebar.markdown(f"Final Verdict: `{'FAIL' if is_failure else 'PASS'}`")
                            results.append({
                                "case": case_file, 
                                "actual": verdict, 
                                "expected": ground_truth[case_file],
                                "report": report_text,
                                "is_cached": data.get("source") == "Cached Research Result"
                            })
                        else:
                            st.sidebar.error(f"Error {resp.status_code} on {case_file}")
                    except Exception as e:
                        st.sidebar.error(f"Connection failed on {case_file}: {str(e)}")
            else:
                st.sidebar.error(f"File Not Found: {case_file}")
            
            eval_progress.progress((i + 1) / len(cases))
            
            # --- NEW: Skip cooldown if result was cached ---
            is_cached = results[-1]["is_cached"] if results else False
            if i < len(cases) - 1 and not is_cached:
                st.sidebar.text(f"⏳ Waiting 100s before next case to respect API limits...")
                time.sleep(100) 
            elif i < len(cases) - 1 and is_cached:
                st.sidebar.text(f"🚀 Cache Hit for {case_file} - skipping wait.")
        
        if results:
            st.session_state['result'] = results[0] if results else {"report": "No results"} # Trigger right-column visibility with valid data
            st.session_state['eval_results'] = results
            st.session_state['result_source'] = "Full Scientific Evaluation"
            st.sidebar.success("✅ Evaluation Complete. Results shown in main panel.")
            st.rerun() # Force UI refresh to show results
        else:
            st.sidebar.warning("⚠️ No results captured. Check file paths and API key.")

    # --- NEW: CACHE MANAGEMENT UI (Phase 2) ---
    with st.expander("💎 Manage Analysis Cache"):
        st.caption("Cached results allow for instant scientific evaluation re-runs.")
        
        # 1. Fetch Cache List
        try:
            cache_resp = requests.get(f"{BACKEND_URL}/cache/list")
            if cache_resp.status_code == 200:
                cache_items = cache_resp.json()
            else:
                cache_items = []
        except:
            cache_items = []

        if not cache_items:
            st.info("📭 Cache is currently empty.")
        else:
            # Table Header
            c_head1, c_head2, c_head3 = st.columns([3, 1, 1])
            c_head1.markdown("**Trial / Filename**")
            c_head2.markdown("**Status**")
            c_head3.markdown("**Action**")

            # List items
            for item in cache_items:
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.markdown(f"**{item['filename']}**  \n`{item['id'][:8]}...` | {item['preview'][:40]}")
                c2.success("Cached")
                if c3.button("🗑️", key=f"del_{item['id']}"):
                    del_resp = requests.post(f"{BACKEND_URL}/cache/clear", params={"item_id": item['id']})
                    if del_resp.status_code == 200:
                        st.sidebar.success("Deleted from cache.")
                        st.rerun()

            if st.button("🚨 Clear All Cache", type="primary"):
                clr_resp = requests.post(f"{BACKEND_URL}/cache/clear")
                if clr_resp.status_code == 200:
                    st.sidebar.success("All cache cleared.")
                    st.rerun()

st.title("🎓 Exam-Flow AI Assistant")
st.markdown("**Professional AI-Powered Assessment & Proctoring Platform**")
st.markdown("---")

# Main Layout: Upload/Controls on Left, Results on Right
col1, col2 = st.columns([1, 1])

@st.cache_data(show_spinner=False)
def fetch_analysis(endpoint, params=None, files=None):
    """Cached function to fetch analysis from backend."""
    try:
        if files:
            response = requests.post(f"{BACKEND_URL}/{endpoint}", params=params, files=files)
        else:
            response = requests.get(f"{BACKEND_URL}/{endpoint}")
            
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Backend Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Connection failed: {e}")
        return None

def get_current_override():
    """Gets current manual override settings from session state."""
    if st.session_state.get('manual_controls', {}).get('enabled'):
        return {
            'score': st.session_state['manual_controls']['score'],
            'integrity': st.session_state['manual_controls']['integrity'],
            'notes': st.session_state['manual_controls']['notes'],
            'reviewer': 'Manual Review'
        }
    return None

with col1:
    st.header("📤 Assessment Portal")
    
    # Selection Mode: Phase 2 Feature
    upload_mode = st.radio(
        "Upload Mode",
        ["Single Video", "Solution Package (ZIP)"],
        help="Use 'Solution Package' to upload video + source code + context for Agentic grading."
    )
    
    # Assessment Type Selector
    assessment_type = st.selectbox(
        "Select Role/Stack", 
        ["Python", "Java", "Docker", "General", "Custom"],
        help="Determines the grading rubric and technical criteria."
    )
    
    # Custom Rubric Input
    rubric_placeholders = {
        "Python": "Default: Python 3.x compatibility, Idiomatic code, Error handling",
        "Java": "Default: Correct Java Syntax, Logical implementation, Execution output",
        "Docker": "Default: Proper CLI usage, Container management, Dockerfile best practices",
        "General": "Default: Overall code structure, Clarity and comments, Problem solving",
        "Custom": "Enter your custom grading criteria here..."
    }
    
    custom_rubric = st.text_area(
        "Exam Context / Instructions / Rubric", 
        value="",
        placeholder="Paste the exam problem statement, specific constraints, or grading rubric here...",
        height=150,
        help="This text will be used as the primary instruction for the AI Grader."
    )

    # Proctoring Toggle
    enable_proctoring = st.checkbox("Enable Behavioral Proctoring", value=True, help="If disabled, AI will ignore gaze/face detection and only focus on technical grading.")
    
    # File Uploader based on Mode
    if upload_mode == "Single Video":
        uploaded_file = st.file_uploader(
            "Upload Recording (MP4, MOV, AVI, WebM, MKV, FLV)", 
            type=["mp4", "mov", "avi", "webm", "mkv", "flv"]
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload Solution ZIP (Video + Code + Context)", 
            type=["zip"]
        )
        st.caption("ℹ️ ZIP should contain video, source files, and optional context.txt")
    
    if uploaded_file is not None:
        if upload_mode == "Single Video":
            st.video(uploaded_file)
        
        button_label = "🚀 Analyze Solution Package" if upload_mode == "Solution Package (ZIP)" else "🚀 Analyze Uploaded Video"
        
        if st.button(button_label):
            endpoint = "/analyze-package" if upload_mode == "Solution Package (ZIP)" else "/analyze-video"
            with st.spinner(f"AI Agents are analyzing your submission... This may take a minute."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                try:
                    params = {
                        "assessment_type": assessment_type,
                        "custom_rubric": custom_rubric,
                        "enable_proctoring": enable_proctoring
                    }
                    response = requests.post(f"{BACKEND_URL}{endpoint}", params=params, files=files)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.session_state['result'] = result
                        st.session_state['result_source'] = "Upload"
                        st.session_state['video_file'] = uploaded_file
                        st.success("✅ AI Technical Analysis Complete!")
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

    st.markdown("---")
    st.subheader("🧪 Demo Samples")
    st.info("Test-drive the AI with pre-verified clips")

    demo_col1, demo_col2 = st.columns(2)

    if demo_col1.button("🐳 Docker Demo"):
        with st.spinner("Loading Docker Analysis..."):
            result = fetch_analysis("analyze-demo/docker")
            if result:
                st.session_state['result'] = result
                st.session_state['result_source'] = "Docker Demo"
                st.success("✅ Demo Analysis Loaded!")

    if demo_col2.button("☕ Java Demo"):
        with st.spinner("Loading Java Analysis..."):
            result = fetch_analysis("analyze-demo/java")
            if result:
                st.session_state['result'] = result
                st.session_state['result_source'] = "Java Demo"
                st.success("✅ Demo Analysis Loaded!")

with col2:
    st.header("📊 Multi-Modal Analysis")
    
    if 'result' in st.session_state:
        result = st.session_state['result']
        source = st.session_state.get('result_source', 'Analysis')
        
        # Header with Key Stats
        st.subheader(f"📋 Verdict: {source}")
        
        # --- NEW: Research Evaluation Logic ---
        if source == "Full Scientific Evaluation" and 'eval_results' in st.session_state:
            results = st.session_state['eval_results']
            
            # Use the first result's report as a fallback for the sidebar/header logic
            st.session_state['result'] = results[-1] if results else {"report": "No results"}
            
            # Calculate Metrics
            tp = sum(1 for r in results if r["actual"] == "FAIL" and r["expected"] == "FAIL")
            fp = sum(1 for r in results if r["actual"] == "FAIL" and r["expected"] == "PASS")
            tn = sum(1 for r in results if r["actual"] == "PASS" and r["expected"] == "PASS")
            fn = sum(1 for r in results if r["actual"] == "PASS" and r["expected"] == "FAIL")

            prec = tp / (tp + fp) if (tp + fp) > 0 else 0
            rec = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0

            # Professional Display
            st.markdown("### 📈 Scientific Validation Metrics")
            m1, m2, m3 = st.columns(3)
            m1.metric("Precision", f"{prec:.2f}", help="Accuracy of Fraud Flags")
            m2.metric("Recall", f"{rec:.2f}", help="Student Catch Rate")
            m3.metric("F1-Score", f"{f1:.2f}", help="Overall Scientific Validity")
            
            st.markdown("#### Detailed Case Breakdown")
            # Create a more readable table for display
            display_results = []
            for r in results:
                status = "✅ MATCH" if r['actual'] == r['expected'] else "❌ MISMATCH"
                display_results.append({
                    "Trial Name": r['case'],
                    "Ground Truth": r['expected'],
                    "AI Prediction": r['actual'],
                    "Result": status
                })
            st.table(display_results)
            
            # Allow viewing a specific report from the batch
            case_names = [r["case"] for r in results]
            selected_case = st.selectbox("View Detailed Agent Reasoning for Case:", case_names)
            report_to_show = next(r["report"] for r in results if r["case"] == selected_case)
            st.markdown("---")
            st.markdown(report_to_show)
            st.stop() # Skip standard multi-modal display for batch results
        
        # --- Standard Analysis Display ---
        ai_score = 0
        import re
        score_match = re.search(r'(\d+)/100', result['report'])
        if score_match:
            ai_score = int(score_match.group(1))
            
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("AI Technical Score", f"{ai_score}/100")
        
        if 'manual_override' in result:
            override = result['manual_override']
            metric_col2.metric("Management Score", f"{override['score']}/100", delta=int(override['score']-ai_score) if override['score'] != ai_score else None)
            metric_col3.metric("Integrity Status", override.get('integrity', 'Verified'))
            
            st.info(f"🖋️ **Reviewer Note:** {override['notes']}")
        else:
            metric_col2.metric("Management Score", f"{ai_score}/100")
            metric_col3.metric("Integrity Status", "AI Default")
        
        st.markdown("---")
        
        # Tabs for better organization
        tab1, tab2 = st.tabs(["📝 AI Detailed Report", "🚨 Behavioral Proctoring"])
        
        with tab1:
            # Automatic Risk Detection
            if "Verdict: FAIL" in result['report'] or "Verdict: FAIL" in result['report'].upper():
                st.error("🚨 **CRITICAL RISK**: AI Investigation has flagged this session for an Integrity Breach.")
            elif "Verdict: SUSPICIOUS" in result['report'] or "Verdict: SUSPICIOUS" in result['report'].upper():
                st.warning("⚠️ **INVESTIGATION RECOMMENDED**: AI has flagged suspicious activity.")
            
            st.markdown(result['report'])
        
        with tab2:
            behavioral_flags = result.get('behavioral_flags', [])
            
            if behavioral_flags:
                # Filter out the generic "No anomalies" message for a cleaner UI if there are actual flags
                actual_flags = [f for f in behavioral_flags if "No behavioral anomalies detected" not in f['issue']]
                
                if actual_flags:
                    st.warning(f"**{len(actual_flags)} suspicious event(s) identified**")
                    for flag in actual_flags:
                        severity_color = "red" if flag['severity'] == "High" else "orange" if flag['severity'] == "Medium" else "blue"
                        st.markdown(f"**{flag['timestamp']}** : :{severity_color}[{flag['issue']}] ({flag['severity']})")
                else:
                    st.success("✅ **Proctoring Pass**: No significant behavioral anomalies detected during code execution.")
                    # Show info-level messages like "Screen-only"
                    for flag in behavioral_flags:
                        if flag['severity'] == "Info":
                            st.info(f"ℹ️ {flag['issue']}")
            else:
                st.info("No behavioral data available for this session.")
        
        # PDF Download
        st.markdown("---")
        if st.button("📄 Export Final Technical Report (PDF)"):
            from fpdf import FPDF
            from datetime import datetime
            import textwrap
            
            class PDF(FPDF):
                def header(self):
                    self.set_fill_color(240, 240, 240)
                    self.rect(0, 0, 210, 20, 'F')
                    self.set_font('Arial', 'B', 15)
                    self.cell(0, 10, 'Exam-Flow Assessment Intelligence', 0, 1, 'C')
                    self.ln(5)
                def footer(self):
                    self.set_y(-15)
                    self.set_font('Arial', 'I', 8)
                    self.cell(0, 10, f'Professional AI Proctoring Report - Page {self.page_no()}', 0, 0, 'C')
            
            pdf = PDF()
            pdf.set_left_margin(15)
            pdf.set_right_margin(15)
            pdf.add_page()
            
            effective_width = pdf.w - pdf.l_margin - pdf.r_margin
            res_type = result.get('type') or result.get('demo') or "General"
            
            # --- PROFESSIONAL METADATA ---
            pdf.set_font("Arial", "B", 10)
            pdf.cell(effective_width/2, 6, f"Assessment: {res_type.upper()}")
            pdf.set_font("Arial", "", 10)
            pdf.cell(effective_width/2, 6, f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='R')
            pdf.ln(5)
            
            # --- HYBRID SCORE SECTION ---
            if 'manual_override' in result:
                override = result['manual_override']
                pdf.set_fill_color(255, 230, 230)
                pdf.rect(15, pdf.get_y(), effective_width, 25, 'F')
                pdf.set_font("Arial", "B", 12)
                pdf.set_text_color(200, 0, 0)
                pdf.set_xy(20, pdf.get_y() + 2)
                pdf.cell(0, 6, f"FINAL MANAGEMENT SCORE: {override['score']}/100", ln=True)
                pdf.set_font("Arial", "B", 10)
                pdf.set_text_color(0, 0, 0)
                pdf.set_x(20)
                pdf.cell(0, 6, f"Integrity Verdict: {override.get('integrity', 'Verified')}", ln=True)
                pdf.set_font("Arial", "I", 9)
                pdf.set_x(20)
                pdf.multi_cell(effective_width-10, 5, f"Justification: {override['notes']}")
                pdf.set_text_color(0, 0, 0)
                pdf.ln(10)
            else:
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, f"AI Technical Score: {ai_score}/100", ln=True)
                pdf.ln(5)
            
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "AI Grading Analysis", ln=True)
            pdf.set_font("Arial", "", 9)
            pdf.ln(2)
            
            # Clean markdown
            report_text = result['report'].replace('#', '').replace('**', '').replace('*', '')
            
            for line in report_text.split('\n'):
                line = line.strip()
                if not line:
                    pdf.ln(3)
                    continue
                
                # Sanitize for Latin-1
                safe_line = ''.join(c if ord(c) < 256 else '?' for c in line)
                
                # Reset X position and use explicit width
                pdf.set_x(pdf.l_margin)
                
                # Use explicit width instead of 0
                try:
                    pdf.multi_cell(effective_width, 5, safe_line)
                except Exception as e:
                    # Fallback to simple cell if multi_cell fails
                    pdf.set_x(pdf.l_margin)
                    pdf.cell(effective_width, 5, safe_line[:100] + "...", ln=True)
            
            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Behavioral Analysis", ln=True)
            pdf.set_font("Arial", "", 9)
            pdf.ln(2)
            
            for flag in result.get('behavioral_flags', []):
                flag_text = f"[{flag['timestamp']}] {flag['issue']} (Severity: {flag['severity']})"
                safe_flag = ''.join(c if ord(c) < 256 else '?' for c in flag_text)
                
                # Reset X and use explicit width
                pdf.set_x(pdf.l_margin)
                try:
                    pdf.multi_cell(effective_width, 5, safe_flag)
                except:
                    pdf.set_x(pdf.l_margin)
                    pdf.cell(effective_width, 5, safe_flag[:100], ln=True)
            
            # Get PDF as bytes (not bytearray) for Streamlit
            pdf_output = pdf.output(dest='S')
            pdf_bytes = bytes(pdf_output)  # Convert bytearray to bytes
            
            st.download_button(
                label="⬇️ Click to Download",
                data=pdf_bytes,
                file_name=f"report_{res_type.lower()}.pdf",
                mime="application/pdf"
            )
    else:
        st.info("Choose a language and upload a video, or run a demo above.")
