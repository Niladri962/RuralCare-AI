def routine_handler(state: dict) -> dict:

    return {
        "next_action": "ROUTINE",

        "routine_response": (
            "Based on the information currently available, "
            "there is no indication of an immediate emergency. "
            "A routine medical consultation may be appropriate."
        ),
    }