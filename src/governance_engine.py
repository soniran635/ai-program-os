from src.models import AIInitiativeIntake, RiskAssessmentReport, ArchitectureRFC

class AIGovernanceEngine:
    """Enforces enterprise risk tiering, legal/security checks,

    and generates standardized Architecture Review Board (ARB) RFCs.
    """
    def evaluate_initiative(self, intake: AIInitiativeIntake) -> tuple[RiskAssessmentReport, ArchitectureRFC]:
        flags = []
        ai_risks = []
        tier = "TIER_4_LOW"
        sec_gate = "APPROVED"
        legal_gate = "APPROVED"

        # 1. Data Classification & Privacy Risk Analysis
        if intake.data_classification == "Restricted_PII_Financial":
            tier = "TIER_1_CRITICAL"
            legal_gate = "PENDING_DPA_LEGAL_REVIEW"
            flags.append("High-Risk Data: Restricted PII or financial data ingested. Requires Data Processing Agreement (DPA) and zero-retention guarantee from vendor.")
            ai_risks.append("Risk of sensitive PII leakage or training data contamination.")
        elif intake.data_classification == "Confidential":
            tier = "TIER_2_HIGH"
            flags.append("Confidential business data: Model vendor must confirm data is never used for foundation model training.")
        
        # 2. Autonomous Action / Financial Execution Risk
        if intake.autonomous_actions_allowed:
            if tier != "TIER_1_CRITICAL":
                tier = "TIER_2_HIGH"
            sec_gate = "PENDING_SECURITY_AUDIT"
            flags.append("Autonomous Execution: Agent permitted to perform write/execution actions. Mandatory Human-In-The-Loop (HITL) gate required.")
            ai_risks.append("Risk of unverified autonomous tool-calling loops or unauthorized financial state mutations.")

        # 3. Model Hosting & Provider Sovereignty
        if intake.model_provider in ["OpenAI Cloud", "Anthropic Claude"] and intake.stores_customer_data:
            flags.append("Third-party cloud hosting with customer data storage: Vendor security audit and SOC2 Type II verification mandatory.")
        elif "Local OSS" in intake.model_provider:
            flags.append("Self-hosted inference: Data sovereignty secured on-premise/VPC; zero public egress risk.")

        report = RiskAssessmentReport(
            initiative_id=intake.initiative_id,
            risk_tier=tier,
            security_gate=sec_gate,
            legal_privacy_gate=legal_gate,
            compliance_flags=flags,
            responsible_ai_risks=ai_risks
        )

        # 4. Generate Standardized Architecture Review RFC
        rfc_md = (
            f"# Technical Architecture RFC: {intake.title}\n"
            f"**RFC ID:** RFC-{intake.initiative_id} | **Risk Tier:** {tier} | **Stage:** Architecture Review Board\n\n"
            f"## 1. Business Problem & Objective\n{intake.business_problem}\n\n"
            f"## 2. Target Users & Operating Model\n"
            f"- **Requesting Team:** {intake.requesting_team}\n"
            f"- **Target Users:** {intake.target_users}\n"
            f"- **Model Deployment:** {intake.model_provider}\n"
            f"- **Estimated Annual Infrastructure Cost:** ${intake.annual_cost_estimate_usd:,.2f}\n\n"
            f"## 3. Data Flow & Boundary Controls\n"
            f"- **Data Classification:** {intake.data_classification}\n"
            f"- **Customer Data Storage:** {'Yes (Vendor Isolation Required)' if intake.stores_customer_data else 'No'}\n\n"
            f"## 4. Graceful Degradation & Fallback Strategy\n"
            f"If {intake.model_provider} encounters rate limits, latency spikes (>3.5s), or API 5xx outages, the system must "
            f"fail gracefully back to deterministic rule-based algorithms with automated customer notifications.\n\n"
            f"## 5. Governance Sign-Off Matrix\n"
            f"- [ ] InfoSec & Cyber Architecture: `{sec_gate}`\n"
            f"- [ ] Legal, Privacy & Compliance: `{legal_gate}`\n"
            f"- [ ] Architecture Review Board (ARB): Pending Review\n"
        )

        rfc = ArchitectureRFC(
            rfc_id=f"RFC-{intake.initiative_id}",
            initiative_id=intake.initiative_id,
            title=intake.title,
            stage="Architecture_Review_Board",
            data_flow_summary=f"Ingests {intake.data_classification} data via {intake.model_provider}.",
            graceful_degradation_plan="Fallback to rule-based deterministic routing on model timeout.",
            required_signoffs=["InfoSec", "Legal & Privacy", "Architecture Review Board", "Procurement"],
            rfc_markdown=rfc_md
        )

        return report, rfc
