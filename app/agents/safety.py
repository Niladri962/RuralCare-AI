import json

from app.services.llm import client, MODEL_NAME


SAFETY_SYSTEM_PROMPT = """
You are the Safety Validation Agent in a healthcare triage system.

Your job is to review the output produced by the Triage Agent
and determine whether the recommendation is safe to proceed with.

You are NOT a doctor.

You must NOT:
- diagnose the patient
- prescribe medication
- invent symptoms
- invent patient information

Review:
1. The patient's reported information.
2. The Planner output.
3. The Triage output.
4. Any deterministic safety guardrail result.

Return ONLY valid JSON:

{
    "approved": true,
    "final_urgency": "",
    "safety_reason": "",
    "next_action": ""
}

Allowed final_urgency values:

EMERGENCY
URGENT
ROUTINE
NEED_MORE_INFORMATION

Safety rules:

1. If the deterministic guardrail is triggered,
   EMERGENCY must be preserved.

2. Potentially life-threatening warning signs should not
   be downgraded to routine care.

3. If important information is missing,
   prefer NEED_MORE_INFORMATION unless an emergency
   warning sign is explicitly present.

4. Do not diagnose.

5. Do not prescribe medication.

6. If the recommendation is unsafe or unclear,
   set approved to false.

7. Keep the response concise.
"""


def safety_agent(state: dict) -> dict:

    planner_response = state.get(
        "planner_response",
        "",
    )

    triage_result = state.get(
        "triage_result",
        {},
    )

    guardrail_triggered = state.get(
        "guardrail_triggered",
        False,
    )

    guardrail_urgency = state.get(
        "guardrail_urgency",
        "",
    )

    guardrail_reason = state.get(
        "guardrail_reason",
        "",
    )

    input_data = {
        "planner": planner_response,
        "triage": triage_result,
        "guardrail_triggered": guardrail_triggered,
        "guardrail_urgency": guardrail_urgency,
        "guardrail_reason": guardrail_reason,
    }

    # --------------------------------
    # Deterministic emergency override
    # --------------------------------

    if guardrail_triggered:

        safety_result = {
            "approved": True,
            "final_urgency": "EMERGENCY",
            "safety_reason": guardrail_reason,
            "next_action": (
                "Seek immediate emergency medical evaluation "
                "or contact local emergency services."
            ),
        }

        return {
            "safety_result": safety_result,
            "next_action": "EMERGENCY",
        }

    # --------------------------------
    # LLM safety validation
    # --------------------------------

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SAFETY_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(
                    input_data,
                    ensure_ascii=False,
                ),
            },
        ],
        temperature=0,
        max_tokens=300,
    )

    raw_response = response.choices[0].message.content

    try:

        safety_result = json.loads(
            raw_response
        )

    except json.JSONDecodeError:

        safety_result = {
            "approved": False,
            "final_urgency": "NEED_MORE_INFORMATION",
            "safety_reason": (
                "Safety validation could not be safely processed."
            ),
            "next_action": (
                "Please provide additional information "
                "or seek appropriate medical evaluation."
            ),
        }

    return {
        "safety_result": safety_result,
        "next_action": safety_result.get(
            "final_urgency",
            "NEED_MORE_INFORMATION",
        ),
    }