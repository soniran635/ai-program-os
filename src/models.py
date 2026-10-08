from pydantic import BaseModel, Field
from typing import List, Optional

class AIInitiativeIntake(BaseModel):
    initiative_id: str
    title: str
    requesting_team: str  # e.g., 'Payments Operations', 'Studio Creative', 'Customer Experience'
    business_problem: str
    target_users: str
    model_provider: str  # 'OpenAI Cloud', 'Anthropic Claude', 'Local OSS (Ollama/vLLM)', 'In-House Fine-Tuned'
    data_classification: str  # 'Public', 'Internal', 'Confidential', 'Restricted_PII_Financial'
    annual_cost_estimate_usd: float
    stores_customer_data: bool
    autonomous_actions_allowed: bool

class RiskAssessmentReport(BaseModel):
    initiative_id: str
    risk_tier: str  # 'TIER_1_CRITICAL', 'TIER_2_HIGH', 'TIER_3_MODERATE', 'TIER_4_LOW'
    security_gate: str  # 'APPROVED', 'PENDING_SECURITY_AUDIT', 'REJECTED'
    legal_privacy_gate: str  # 'APPROVED', 'PENDING_DPA_LEGAL_REVIEW', 'BLOCKED'
    compliance_flags: List[str]
    responsible_ai_risks: List[str]

class ArchitectureRFC(BaseModel):
    rfc_id: str
    initiative_id: str
    title: str
    stage: str  # 'Intake_Submitted', 'Security_Legal_Review', 'Architecture_Review_Board', 'Approved_For_Build'
    data_flow_summary: str
    graceful_degradation_plan: str
    required_signoffs: List[str]
    rfc_markdown: str
