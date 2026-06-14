import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# Set up the Streamlit page
st.set_page_config(
    page_title="Blood Work Analyzer",
    page_icon="🩸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the redesigned UI
st.markdown(
    """
    <style>
    :root {
        color-scheme: dark;
    }
    .css-18e3th9 {
        background-color: #0f1724;
    }
    .stApp {
        background: linear-gradient(180deg, #101827 0%, #111827 100%);
        color: #e2e8f0;
    }
    .app-header {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .app-header h1 {
        margin: 0;
        font-size: 2.6rem;
        letter-spacing: -0.03em;
    }
    .app-header p {
        margin: 0.4rem 0 0;
        color: #cbd5e1;
        max-width: 720px;
        line-height: 1.6;
    }
    .badge {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 999px;
        padding: 0.9rem 1.2rem;
        color: #f8fafc;
        font-weight: 600;
        font-size: 0.95rem;
    }
    .card {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.16);
        border-radius: 24px;
        padding: 1.6rem;
        box-shadow: 0 30px 60px rgba(15, 23, 42, 0.3);
        margin-bottom: 1rem;
    }
    .card h2 {
        margin-top: 0;
        margin-bottom: 1rem;
        font-size: 1.6rem;
        color: #f8fafc;
    }
    .report-section {
        margin-bottom: 1.4rem;
    }
    .report-title {
        font-size: 0.95rem;
        letter-spacing: 0.08em;
        color: #94a3b8;
        margin-bottom: 0.8rem;
    }
    .metric-row {
        display: flex;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.6rem;
        font-size: 0.97rem;
    }
    .metric-row span {
        display: inline-block;
    }
    .metric-label {
        color: #e2e8f0;
        min-width: 240px;
    }
    .metric-value {
        color: #f1f5f9;
        min-width: 140px;
        text-align: right;
    }
    .metric-range {
        color: #94a3b8;
        min-width: 180px;
        text-align: right;
    }
    .status-pill {
        display: inline-flex;
        padding: 0.3rem 0.7rem;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-high {
        background: rgba(248, 113, 113, 0.18);
        color: #fecaca;
    }
    .status-normal {
        background: rgba(52, 211, 153, 0.16);
        color: #a7f3d0;
    }
    .status-low {
        background: rgba(59, 130, 246, 0.18);
        color: #bfdbfe;
    }
    .summary-card,
    .diet-card {
        min-height: 280px;
    }
    .summary-card .card-content,
    .diet-card .card-content {
        line-height: 1.8;
        color: #cbd5e1;
    }
    .streamlit-expanderHeader {
        color: #e2e8f0;
    }
    .stButton>button {
        border-radius: 999px;
        border: 1px solid rgba(148, 163, 184, 0.25);
        background: #0f1724;
        color: #f8fafc;
        padding: 0.9rem 1.4rem;
    }
    .stButton>button:hover {
        background: #111827;
    }
    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and description
st.markdown(
    """
    <div class='app-header'>
        <div>
            <h1>Blood Work Analyzer</h1>
            <p>Understand your blood work at a glance with a clean report layout, health summary, and diet guidance.</p>
        </div>
        <div class='badge'>Health Dashboard</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize LLM
@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(model='gemini-2.5-flash')

llm = get_llm()

# Sidebar for file upload
st.sidebar.header("Upload your blood work")
uploaded_file = st.sidebar.file_uploader("Select a blood work report (.txt)", type=["txt"])

# Default blood work data
default_blood_report = """LIPID PANEL
Total Cholesterol: 238 mg/dL        (Normal: <200)
LDL Cholesterol:   162 mg/dL        (Normal: <100)
HDL Cholesterol:   36 mg/dL         (Normal: >40)
Triglycerides:     188 mg/dL        (Normal: <150)

METABOLIC PANEL
Glucose (Fasting): 92 mg/dL         (Normal: 70-99)
HbA1c:             5.3%             (Normal: <5.7%)
Creatinine:        1.0 mg/dL        (Normal: 0.7-1.3)
eGFR:              82 mL/min        (Normal: >60)

LIVER FUNCTION
ALT:              28 U/L            (Normal: 7-40)
AST:              25 U/L            (Normal: 10-40)
Bilirubin Total:  0.8 mg/dL         (Normal: 0.2-1.2)
"""

# Load blood work data
if uploaded_file is not None:
    blood_report = uploaded_file.read().decode('utf-8')
    st.sidebar.success("File uploaded successfully")
else:
    blood_report = default_blood_report
    st.sidebar.info("Using sample blood work data. Upload a report to personalize the analysis.")

# Helper to render report rows inside a styled card
def render_report_card(report: str):
    lines = [line.strip() for line in report.splitlines() if line.strip()]
    html = ["<div class='card'>", "<h2>Blood Work Report</h2>"]
    section = None
    for line in lines:
        if line.isupper() and ':' not in line:
            if section is not None:
                html.append("</div>")
            section = line
            html.append(f"<div class='report-section'><div class='report-title'>{section}</div>")
            continue
        if ':' in line:
            parts = line.split(':', 1)
            label = parts[0].strip()
            rest = parts[1].strip()
            value, _, reference = rest.partition('(')
            reference = reference.strip(')') if reference else ''
            html.append(
                '<div class="metric-row">'
                f'<span class="metric-label">{label}</span>'
                f'<span class="metric-value">{value.strip()}</span>'
                f'<span class="metric-range">{reference.strip()}</span>'
                '</div>'
            )
    if section is not None:
        html.append("</div>")
    html.append("</div>")
    return "".join(html)

# Display the main layout
left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown(render_report_card(blood_report), unsafe_allow_html=True)
    if st.button("Analyze Blood Report", key="analyze_btn"):
        with st.spinner("Analyzing the blood report..."):
            extraction_prompt = f"""
You are a medical data extraction assistant.
From the blood report below, extract all test results and classify each one as HIGH, LOW, or NORMAL based on the reference range.
Provide the output as:
- Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range

Blood Report:
{blood_report}
"""
            extraction_response = llm.invoke(extraction_prompt)
            st.session_state.extracted_values = extraction_response.text
            st.success("Blood report analysis complete")

    if st.session_state.get('extracted_values'):
        st.markdown("<div class='card'><h2>Analysis Results</h2>", unsafe_allow_html=True)
        extracted_text = st.session_state.extracted_values
        lines = extracted_text.split('\n')
        for line in lines:
            if not line.strip():
                continue
            style = 'status-normal'
            if 'HIGH' in line.upper():
                style = 'status-high'
            elif 'LOW' in line.upper():
                style = 'status-low'
            st.markdown(f"<div class='metric-row'><span class='metric-label'>{line}</span><span class='status-pill {style}'>{''}</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown("<div class='card summary-card'><h2>Health Summary</h2><div class='card-content'>", unsafe_allow_html=True)
    health_content = st.session_state.get('health_summary', 'Generate a health summary to see your key insights here.')
    st.markdown(health_content)
    st.markdown("</div></div>", unsafe_allow_html=True)

    st.markdown("<div class='card diet-card'><h2>Suggested Diet Plan</h2><div class='card-content'>", unsafe_allow_html=True)
    diet_content = st.session_state.get('diet_plan', 'Generate a diet plan to see recommended foods to avoid and foods to eat more of.')
    st.markdown(diet_content)
    st.markdown("</div></div>", unsafe_allow_html=True)

    if st.button("Generate Health Summary & Diet Plan", key="summary_btn"):
        with st.spinner("Creating health summary and diet plan..."):
            extracted_values = st.session_state.get('extracted_values')
            if not extracted_values:
                extraction_prompt = f"""
You are a medical data extraction assistant.
From the blood report below, extract all test results and classify each one as HIGH, LOW, or NORMAL based on the reference range.
Provide the output as:
- Test Name: value | Status: HIGH/LOW/NORMAL | Reference: range

Blood Report:
{blood_report}
"""
                extraction_response = llm.invoke(extraction_prompt)
                extracted_values = extraction_response.text
                st.session_state.extracted_values = extracted_values

            diet_prompt = f"""
You are a clinical nutritionist.
Based on the blood work analysis below, write:
1. A short health summary in 4-5 lines
2. A concise diet plan with two sections: Foods to avoid and Foods to eat more of.

Blood Work Analysis:
{extracted_values}
"""
            diet_response = llm.invoke(diet_prompt)
            result_text = diet_response.text
            parts = result_text.split('\n\n')
            health_text = []
            diet_text = []
            for paragraph in parts:
                if 'avoid' in paragraph.lower() or 'eat' in paragraph.lower():
                    diet_text.append(paragraph)
                else:
                    health_text.append(paragraph)
            st.session_state.health_summary = '<br/>'.join(health_text).strip()
            st.session_state.diet_plan = '<br/>'.join(diet_text).strip()
            st.success("Health summary and diet plan generated")

# Footer
st.markdown("<div class='footer-text'>Made with ❤️ using Streamlit | For informational purposes only.</div>", unsafe_allow_html=True)
