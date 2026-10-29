import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="AI Risk Assessment Assistant", page_icon="🛡️", layout="wide")

RISK_GUIDANCE = {
    "Cybersecurity": {
        "description": "Exposure to hacking, phishing, malware, or unauthorized access.",
        "actions": [
            "Enable multi-factor authentication on email and business accounts.",
            "Install security updates and use reputable endpoint protection.",
            "Train staff to identify phishing and suspicious attachments.",
            "Keep encrypted, tested backups separate from everyday devices."
        ]
    },
    "Financial": {
        "description": "Cash-flow pressure, unpaid invoices, fraud, or unexpected costs.",
        "actions": [
            "Review cash flow weekly and maintain a short-term forecast.",
            "Separate business and personal accounts and reconcile transactions.",
            "Set invoice follow-up reminders and approval limits for payments.",
            "Build an emergency reserve appropriate to the business."
        ]
    },
    "Operational": {
        "description": "Disruption caused by supplier problems, equipment failure, or process gaps.",
        "actions": [
            "Document critical processes and assign backup owners.",
            "Identify alternative suppliers for essential goods or services.",
            "Schedule preventive maintenance for critical equipment.",
            "Create and test a simple business continuity plan."
        ]
    },
    "Compliance": {
        "description": "Failure to meet applicable legal, tax, privacy, or industry requirements.",
        "actions": [
            "Maintain a calendar of relevant filing and renewal deadlines.",
            "Limit collection of personal data and define retention periods.",
            "Keep required records organized and restrict access to them.",
            "Ask a qualified professional to verify obligations for your industry."
        ]
    },
    "People": {
        "description": "Risks involving staff training, key-person dependency, or accidental mistakes.",
        "actions": [
            "Provide regular onboarding and security awareness training.",
            "Use least-privilege access and promptly remove access when roles change.",
            "Document key tasks so one person is not the only person who can do them.",
            "Use clear approval and escalation procedures for sensitive work."
        ]
    },
}

def score_risk(likelihood: int, impact: int) -> tuple[int, str]:
    score = likelihood * impact
    if score >= 20:
        level = "Critical"
    elif score >= 12:
        level = "High"
    elif score >= 6:
        level = "Medium"
    else:
        level = "Low"
    return score, level

def risk_recommendations(category: str, level: str, custom: str) -> str:
    actions = RISK_GUIDANCE[category]["actions"]
    if level in ("Critical", "High"):
        actions = actions[:3]
    else:
        actions = actions[:2]
    result = " ".join(f"{i+1}. {action}" for i, action in enumerate(actions))
    if custom.strip():
        result += f" Additional note: {custom.strip()}"
    return result

st.title("🛡️ AI Risk Assessment Assistant")
st.caption("A practical decision-support prototype for small businesses")
st.warning("This prototype uses transparent, rule-based scoring and predefined recommendations. It is not a substitute for legal, financial, cybersecurity, or insurance advice.")

with st.sidebar:
    st.header("Business profile")
    business_name = st.text_input("Business name", value="Sample Small Business")
    business_type = st.selectbox("Business type", [
        "Retail shop", "Restaurant / café", "Professional services",
        "Online business", "Manufacturing", "Other"
    ])
    employee_count = st.selectbox("Number of employees", ["1–5", "6–20", "21–50", "51+"])
    st.markdown("---")
    st.markdown("**Scoring guide**")
    st.write("Likelihood: 1 = Rare, 5 = Almost certain")
    st.write("Impact: 1 = Minor, 5 = Severe")

st.subheader("Assess a business risk")
with st.form("risk_form"):
    c1, c2 = st.columns(2)
    with c1:
        risk_title = st.text_input("Risk title", placeholder="e.g., No multi-factor authentication")
        category = st.selectbox("Risk category", list(RISK_GUIDANCE.keys()))
        likelihood = st.slider("Likelihood", min_value=1, max_value=5, value=3)
    with c2:
        impact = st.slider("Impact", min_value=1, max_value=5, value=3)
        owner = st.text_input("Person responsible (optional)", placeholder="e.g., Owner / IT support")
        status = st.selectbox("Current status", ["Open", "In progress", "Mitigated", "Accepted"])
    details = st.text_area("Risk details (do not enter passwords or sensitive personal data)", placeholder="Describe the situation and possible consequences.")
    custom_note = st.text_input("Additional recommendation context (optional)")
    submitted = st.form_submit_button("Assess risk", type="primary")

if "assessments" not in st.session_state:
    st.session_state.assessments = []

if submitted:
    if not risk_title.strip():
        st.error("Please enter a risk title.")
    else:
        score, level = score_risk(likelihood, impact)
        record = {
            "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "Business": business_name.strip() or "Unnamed business",
            "Business type": business_type,
            "Employees": employee_count,
            "Risk title": risk_title.strip(),
            "Category": category,
            "Details": details.strip(),
            "Likelihood": likelihood,
            "Impact": impact,
            "Score": score,
            "Level": level,
            "Owner": owner.strip(),
            "Status": status,
            "Recommendations": risk_recommendations(category, level, custom_note)
        }
        st.session_state.assessments.append(record)
        st.success("Assessment added to this session.")

if st.session_state.assessments:
    df = pd.DataFrame(st.session_state.assessments)
    st.subheader("Assessment dashboard")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total risks", len(df))
    m2.metric("Critical risks", int((df["Level"] == "Critical").sum()))
    m3.metric("High risks", int((df["Level"] == "High").sum()))
    m4.metric("Mitigated", int((df["Status"] == "Mitigated").sum()))

    st.markdown("### Risk register")
    st.dataframe(df[["Risk title", "Category", "Likelihood", "Impact", "Score", "Level", "Owner", "Status"]], use_container_width=True, hide_index=True)

    st.markdown("### Recommendations")
    ordered = df.sort_values("Score", ascending=False)
    for _, row in ordered.iterrows():
        with st.expander(f'{row["Level"]}: {row["Risk title"]} — score {row["Score"]}/25'):
            st.write(row["Details"] or RISK_GUIDANCE[row["Category"]]["description"])
            st.write(row["Recommendations"])
            st.caption(f'Owner: {row["Owner"] or "Not assigned"} · Status: {row["Status"]}')

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download risk report (CSV)", data=csv_data,
                       file_name="business_risk_assessment.csv", mime="text/csv")
    if st.button("Clear assessments from this session"):
        st.session_state.assessments = []
        st.rerun()
else:
    st.info("Add your first risk above to populate the dashboard.")
    st.markdown("### Example risks to assess")
    examples = pd.DataFrame([
        {"Risk": "No tested data backups", "Category": "Cybersecurity", "Likelihood": 4, "Impact": 5},
        {"Risk": "Late customer payments", "Category": "Financial", "Likelihood": 3, "Impact": 4},
        {"Risk": "Only one supplier for key stock", "Category": "Operational", "Likelihood": 3, "Impact": 4},
    ])
    st.dataframe(examples, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("Prototype note: Assessments are held in the current browser session only. They are not saved to a permanent database. Review and validate recommendations before acting.")
