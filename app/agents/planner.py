from app.services.llm import client


def planner_agent(state: dict) -> dict:

    user_message = state.get(
        "user_message",
        "",
    )

    conversation_history = state.get(
        "conversation_history",
        [],
    )

    patient_information = state.get(
        "patient_information",
        {},
    )

    conversation_text = ""

    for message in conversation_history:

        role = message.get(
            "role",
            "",
        )

        content = message.get(
            "content",
            "",
        )

        conversation_text += (
            f"{role}: {content}\n"
        )

    prompt = f"""
You are the Planner Agent for a rural healthcare
triage assistant.

Your role is to identify what information is missing
and ask the patient the next useful question.

You are NOT a doctor.

Do NOT diagnose the patient.

Do NOT prescribe medication.

Do NOT invent patient information.

Patient's latest message:

{user_message}

Previously extracted patient information:

{patient_information}

Conversation history:

{conversation_text}

Your response must contain:

1. What the patient has reported.
2. Important information that is still missing.
3. ONE clear follow-up question.

Keep the question simple and understandable
for a patient.

If the patient reports a potentially life-threatening
symptom such as severe chest pain or severe difficulty
breathing, do not delay emergency guidance merely to
ask additional questions.
"""

    response = client.invoke(
        prompt
    )

    return {
        "planner_response":
            response.content
    }