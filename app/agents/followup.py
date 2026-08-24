def followup_handler(state: dict) -> dict:
    """
    Handles cases where the system does not have enough
    information to safely determine urgency.
    """

    planner_response = state.get(
        "planner_response",
        "",
    )

    return {
        "next_action": "NEED_MORE_INFORMATION",

        "followup_response": planner_response,
    }