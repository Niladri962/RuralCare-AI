import json

from app.services.llm import client, MODEL_NAME


TRIAGE_SYSTEM_PROMPT = """
You are the Triage Agent in a healthcare triage assistant.

Your job is to assess the urgency of a user's reported symptoms.

You are NOT a doctor.

You must NOT:
- diagnose a disease
- prescribe medication
- claim certainty about a medical condition
- invent symptoms or patient information

Classify the situation into exactly ONE of:

EMERGENCY
URGENT
ROUTINE
NEED_MORE_INFORMATION

Definitions:

EMERGENCY:
Symptoms may indicate a potentially life-threatening situation
and require immediate emergency medical evaluation.

URGENT:
The situation may require medical evaluation soon but does not
currently appear to require immediate emergency escalation based
on the available information.

ROUTINE:
The information does not indicate an immediate or urgent concern,
and routine medical consultation may be appropriate.

NEED_MORE_INFORMATION:
There is not enough information to safely determine urgency.

Return ONLY valid JSON using this structure:

{
    "urgency": "",
    "reason": "",
    "recommended_action": "",
    "emergency_warning": false
}

Rules:

1. Do not diagnose.
2. Do not invent information.
3. If important information is missing, use NEED_MORE_INFORMATION.
4. If potentially serious warning signs are explicitly reported,
   prioritize EMERGENCY.
5. Keep the reason concise.
6. The recommended action must focus on seeking appropriate care,
   not treatment or medication.
"""


def triage_agent(state: dict) -> dict:

    planner_response = state.get(
        "planner_response",
        {},
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": TRIAGE_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(
                    planner_response,
                    ensure_ascii=False,
                ),
            },
        ],
        temperature=0,
        max_tokens=300,
    )

    raw_response = response.choices[0].message.content

    try:
        triage_result = json.loads(raw_response)

    except json.JSONDecodeError:

        triage_result = {
            "urgency": "NEED_MORE_INFORMATION",
            "reason": "The triage result could not be safely processed.",
            "recommended_action": (
                "Please provide additional information "
                "or seek appropriate medical evaluation."
            ),
            "emergency_warning": False,
        }

    return {
        "triage_result": triage_result,
        "next_action": triage_result.get(
            "urgency",
            "NEED_MORE_INFORMATION",
        ),
    }