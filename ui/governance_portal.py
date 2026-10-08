import os
import sys

# Ensure project root is in Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
from src.models import AIInitiativeIntake
from src.governance_engine import AIGovernanceEngine

st.set_page_config(page_title="AI-Program-OS | Enterprise Governance Portal", layout="wide", page_icon="🏛️")

st.title("🏛️ AI-Program-OS: Enterprise AI Intake & Architecture Review Board")
st.markdown("**Program Operating System | Multi-Tier Risk Governance | Technical RFC Generation** | *100% Free & Open-Source*")

engine = AIGovernanceEngine()

tab1, tab2, tab3 = st.tabs([
    "📥 Intake & Multi-Tier Risk Audit",
    "🚦 Cross-Functional Stage-Gate Board",
    "📄 Generated Architecture RFC Viewer"
])

# ----------------- TAB 1: INTAKE & RISK AUDIT -----------------
with tab1:
    st.subheader("Enterprise AI Initiative Intake")
    st.caption("Submit or evaluate AI initiatives across business units to establish clear ownership and risk classification.")

    col1, col2 = st.columns(2)

    with col1:
        preset = st.selectbox(
            "Select Pre-Configured Initiative or Custom",
            [
                "1. Payments Wire Dispute Autonomous Copilot (JPMorgan/Goldman Sachs Style)",
                "2. Internal Engineering Code & Spec Search (Figma/Anthropic Style)",
                "3. Direct-to-Consumer Streaming Recommender (Paramount Style)"
            ]
        )

        if preset.startswith("1"):
            init_id = "AI-PAY-201"
            title = "Autonomous Wire & ACH Dispute Triage Agent"
            team = "Global Banking & Payments Operations"
            problem = "High manual operational hours spent triaging high-value wire dispute claims."
            users = "Payment Operations Specialists & Compliance Officers"
            provider = "OpenAI Cloud"
            data_class = "Restricted_PII_Financial"
            cost = 65000.0
            stores_cust = True
            auto_act = True
        elif preset.startswith("2"):
            init_id = "AI-ENG-089"
            title = "Internal Code & Context Store Assistant"
            team = "Platform Engineering"
            problem = "Context rot and API drift across growing micro-frontend repositories."
            users = "Enterprise Software Engineers"
            provider = "Local OSS (Ollama/vLLM)"
            data_class = "Internal"
            cost = 18000.0
            stores_cust = False
            auto_act = False
        else:
            init_id = "AI-STR-304"
            title = "Personalized Live Playback Stream Curator"
            team = "Streaming Personalization Squad"
            problem = "Low engagement on live events due to generic recommended broadcast feeds."
            users = "Direct-to-Consumer Streaming Subscribers"
            provider = "Anthropic Claude"
            data_class = "Confidential"
            cost = 42000.0
            stores_cust = False
            auto_act = False

        with st.form("intake_form"):
            st.markdown(f"**Initiative ID:** `{init_id}`")
            f_title = st.text_input("Initiative Title", title)
            f_team = st.text_input("Requesting Business Line / Team", team)
            f_problem = st.text_area("Business Problem & Objective", problem, height=80)
            
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                f_provider = st.selectbox("Model Provider", ["OpenAI Cloud", "Anthropic Claude", "Local OSS (Ollama/vLLM)", "In-House Fine-Tuned"], index=["OpenAI Cloud", "Anthropic Claude", "Local OSS (Ollama/vLLM)", "In-House Fine-Tuned"].index(provider))
                f_stores = st.checkbox("Stores Customer Data in Vendor Cloud", stores_cust)
            with c_p2:
                f_data = st.selectbox("Data Classification", ["Public", "Internal", "Confidential", "Restricted_PII_Financial"], index=["Public", "Internal", "Confidential", "Restricted_PII_Financial"].index(data_class))
                f_auto = st.checkbox("Autonomous Financial/Write Actions Allowed", auto_act)

            f_cost = st.number_input("Estimated Annual Cloud/Inference Cost ($)", value=cost, step=5000.0)
            
            submit_btn = st.form_submit_button("⚡ Run Governance & Risk Audit", type="primary")

    with col2:
        if submit_btn:
            intake_obj = AIInitiativeIntake(
                initiative_id=init_id,
                title=f_title,
                requesting_team=f_team,
                business_problem=f_problem,
                target_users=users,
                model_provider=f_provider,
                data_classification=f_data,
                annual_cost_estimate_usd=f_cost,
                stores_customer_data=f_stores,
                autonomous_actions_allowed=f_auto
            )

            report, rfc = engine.evaluate_initiative(intake_obj)

            # Store in session state for tabs 2 and 3
            st.session_state["active_report"] = report
            st.session_state["active_rfc"] = rfc

            st.markdown(f"### Governance Evaluation: `{report.risk_tier}`")
            
            r1, r2 = st.columns(2)
            with r1:
                if report.risk_tier == "TIER_1_CRITICAL":
                    st.error("🚨 TIER 1: CRITICAL RISK")
                elif report.risk_tier == "TIER_2_HIGH":
                    st.warning("⚠️ TIER 2: HIGH RISK")
                else:
                    st.success("✅ TIER 3/4: MODERATE / LOW RISK")
            
            with r2:
                st.metric("Estimated Annual Budget", f"${intake_obj.annual_cost_estimate_usd:,.0f}")

            st.markdown("**Gating Review Status:**")
            st.info(f"🛡️ **InfoSec Gate:** `{report.security_gate}` | ⚖️ **Legal & Privacy Gate:** `{report.legal_privacy_gate}`")

            if report.compliance_flags:
                st.markdown("**Compliance & Architecture Flags:**")
                for flag in report.compliance_flags:
                    st.markdown(f"- ⚠️ {flag}")

            if report.responsible_ai_risks:
                st.markdown("**Responsible AI & Safety Risks:**")
                for risk in report.responsible_ai_risks:
                    st.markdown(f"- 🛑 {risk}")

# ----------------- TAB 2: STAGE-GATE BOARD -----------------
with tab2:
    st.subheader("Cross-Functional Governance Pipeline (Stage-Gate)")
    st.caption("Tracking enterprise sign-offs across Legal, InfoSec, Enterprise Architecture, and Procurement.")

    sg_data = pd.DataFrame([
        {"Initiative ID": "AI-PAY-201", "Title": "Payments Wire Dispute Agent", "Risk Tier": "TIER 1 (Critical)", "InfoSec": "Audit Required", "Legal / DPA": "Pending DPA", "ARB Review": "Under Review", "Status": "In Review"},
        {"Initiative ID": "AI-ENG-089", "Title": "Internal Code & Context Search", "Risk Tier": "TIER 3 (Moderate)", "InfoSec": "Approved (OSS)", "Legal / DPA": "Approved", "ARB Review": "Approved", "Status": "Approved for Build"},
        {"Initiative ID": "AI-STR-304", "Title": "Live Stream Personalizer", "Risk Tier": "TIER 2 (High)", "InfoSec": "Approved (Cloud)", "Legal / DPA": "Pending Vendor Addendum", "ARB Review": "Under Review", "Status": "In Review"}
    ])
    st.dataframe(sg_data, use_container_width=True, hide_index=True)

    st.markdown("### Stage-Gate Decision Matrix")
    g1, g2, g3, g4 = st.columns(4)
    with g1:
        st.markdown("**1. Intake & Routing**")
        st.success("Complete (Defined problem & scope)")
    with g2:
        st.markdown("**2. Security & Compliance**")
        st.warning("InfoSec Review Active")
    with g3:
        st.markdown("**3. Architecture Review (ARB)**")
        st.info("Technical RFC Scheduled")
    with g4:
        st.markdown("**4. Operational Handoff**")
        st.markdown("*Pending Gating Approval*")

# ----------------- TAB 3: RFC VIEWER -----------------
with tab3:
    st.subheader("Technical Architecture Review Board (ARB) RFC Document")
    st.caption("Standardized technical RFC generated automatically from the governance engine.")

    if "active_rfc" in st.session_state:
        st.markdown(st.session_state["active_rfc"].rfc_markdown)
    else:
        st.info("Run an intake evaluation in Tab 1 to generate and inspect the technical RFC document.")
