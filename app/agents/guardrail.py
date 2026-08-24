def safety_guardrail(state: dict) -> dict:
    """
    Deterministic safety guardrail.

    This layer checks for explicit high-risk symptom combinations
    before the final LLM safety decision.

    It does not diagnose the patient.
    """

    user_message = state.get(
        "user_message",
        "",
    )

    user_message = user_message.lower().strip()

    emergency_patterns = [
        (
            ["chest pain", "difficulty breathing"],
            "Possible emergency: chest pain with breathing difficulty.",
        ),
        (
            ["chest pain", "shortness of breath"],
            "Possible emergency: chest pain with shortness of breath.",
        ),
        (
            ["severe chest pain"],
            "Possible emergency: severe chest pain was reported.",
        ),
        (
            ["unconscious"],
            "Possible emergency: loss of consciousness was reported.",
        ),
        (
            ["not breathing"],
            "Possible emergency: the person is reported as not breathing.",
        ),
        (
            ["severe bleeding"],
            "Possible emergency: severe bleeding was reported.",
        ),
    ]

    for keywords, reason in emergency_patterns:

        if all(
            keyword in user_message
            for keyword in keywords
        ):

            return {
                "guardrail_triggered": True,
                "guardrail_urgency": "EMERGENCY",
                "guardrail_reason": reason,
            }

    return {
        "guardrail_triggered": False,
        "guardrail_urgency": "",
        "guardrail_reason": "",
    }