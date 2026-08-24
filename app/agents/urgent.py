def urgent_handler(state: dict) -> dict:

    return {
        "next_action": "URGENT",

        "urgent_response": (
            "Your symptoms may require medical evaluation soon. "
            "Please arrange a medical consultation as soon as possible."
        ),
    }