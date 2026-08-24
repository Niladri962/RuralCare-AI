def emergency_handler(state: dict) -> dict:

    return {
        "next_action": "EMERGENCY",

        "emergency_response": (
            "Your reported symptoms may require immediate "
            "medical attention. Please seek emergency medical "
            "care immediately or contact your local emergency service."
        ),
    }