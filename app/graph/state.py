from typing import TypedDict


class HealthcareState(TypedDict, total=False):

    # =========================
    # USER
    # =========================

    user_message: str

    conversation_history: list

    # =========================
    # PATIENT INFORMATION
    # =========================

    patient_information: dict

    symptoms: list[str]

    missing_information: list[str]

    # =========================
    # PLANNER
    # =========================

    planner_response: str

    # =========================
    # TRIAGE
    # =========================

    triage_result: dict

    # =========================
    # GUARDRAIL
    # =========================

    guardrail_triggered: bool

    guardrail_urgency: str

    guardrail_reason: str

    # =========================
    # SAFETY
    # =========================

    safety_result: dict

    # =========================
    # RESPONSES
    # =========================

    emergency_response: str

    urgent_response: str

    routine_response: str

    followup_response: str

    # =========================
    # FINAL
    # =========================

    next_action: str