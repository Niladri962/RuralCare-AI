import json
import re
from app.config import get_llm

llm = get_llm()

def extract_patient_information(
    state: dict,
) -> dict:

    """
    Extract structured patient information from the
    current message and previous conversation.

    The extractor only records information explicitly
    stated by the patient.

    It must not invent or diagnose medical conditions.
    """

    user_message = state.get(
        "user_message",
        "",
    )

    conversation_history = state.get(
        "conversation_history",
        [],
    )

    previous_information = state.get(
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

    conversation_text += (
        f"user: {user_message}"
    )


    prompt = f"""
You are a medical information extraction agent.

Your job is ONLY to extract facts explicitly stated
by the patient.

Do NOT diagnose the patient.

Do NOT assume missing information.

Do NOT infer medical conditions.

Do NOT invent values.

If information is not available, use null.

Previous structured information:

{json.dumps(previous_information, indent=2)}

Conversation:

{conversation_text}

Extract the following fields:

age
sex
symptoms
symptom_duration
temperature
pain_location
pain_severity
breathing_difficulty
chest_pain
dizziness
nausea
vomiting
cough
medical_conditions
medications
allergies

Return ONLY valid JSON.

Example:

{{
    "age": 25,
    "sex": null,
    "symptoms": ["fever"],
    "symptom_duration": "2 days",
    "temperature": "102°F",
    "pain_location": null,
    "pain_severity": null,
    "breathing_difficulty": false,
    "chest_pain": false,
    "dizziness": null,
    "nausea": null,
    "vomiting": null,
    "cough": null,
    "medical_conditions": [],
    "medications": [],
    "allergies": []
}}

Important:

- Preserve previously known information.
- Add newly provided information.
- Do not remove valid information unless the patient explicitly corrects it.
"""


    response = llm.invoke(prompt)


    raw_content = response.content

    try:

        extracted = json.loads(
            raw_content
        )

    except json.JSONDecodeError:

        extracted = fallback_extraction(
            user_message,
            previous_information,
        )


    merged_information = merge_patient_information(
        previous_information,
        extracted,
    )


    missing_information = find_missing_information(
        merged_information
    )


    return {

        "patient_information":
            merged_information,

        "missing_information":
            missing_information,

    }


def merge_patient_information(
    previous: dict,
    new: dict,
) -> dict:

    """
    Merge newly extracted information with
    previously known information.
    """

    result = dict(previous)


    for key, value in new.items():

        if value is None:
            continue

        if value == "":
            continue

        if value == [] and key in result:
            continue

        result[key] = value


    return result


def find_missing_information(
    information: dict,
) -> list:

    """
    Identify basic information that may still be useful
    for triage.

    This is not a diagnostic rule.
    """

    missing = []


    if not information.get("age"):

        missing.append(
            "age"
        )


    if not information.get(
        "symptoms"
    ):

        missing.append(
            "symptoms"
        )


    if not information.get(
        "symptom_duration"
    ):

        missing.append(
            "symptom_duration"
        )


    return missing


def fallback_extraction(
    message: str,
    previous: dict,
) -> dict:

    """
    Basic deterministic fallback if the LLM returns
    invalid JSON.

    This does not attempt diagnosis.
    """

    result = dict(previous)


    age_match = re.search(
        r"\b(\d{1,3})\s*(?:years?|yrs?)\b",
        message.lower(),
    )

    if age_match:

        result["age"] = int(
            age_match.group(1)
        )


    temperature_match = re.search(
        r"\b(\d{2,3}(?:\.\d+)?)\s*°?\s*(?:f|fahrenheit)\b",
        message.lower(),
    )

    if temperature_match:

        result["temperature"] = (
            temperature_match.group(1)
            + "°F"
        )


    symptoms = list(
        result.get(
            "symptoms",
            [],
        )
    )


    symptom_words = [
        "fever",
        "cough",
        "headache",
        "vomiting",
        "nausea",
        "dizziness",
        "chest pain",
        "breathing difficulty",
        "shortness of breath",
        "sore throat",
        "body pain",
    ]


    message_lower = message.lower()


    for symptom in symptom_words:

        if symptom in message_lower:

            if symptom not in symptoms:

                symptoms.append(
                    symptom
                )


    result["symptoms"] = symptoms


    if (
        "chest pain"
        in message_lower
    ):

        result["chest_pain"] = True


    if (
        "breathing difficulty"
        in message_lower
        or "difficulty breathing"
        in message_lower
        or "shortness of breath"
        in message_lower
    ):

        result[
            "breathing_difficulty"
        ] = True


    return result