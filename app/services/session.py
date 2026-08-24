from typing import Dict, List


# Temporary in-memory session storage.
#
# This is suitable for local development.
# Later we will replace this with Redis or PostgreSQL
# for production deployment on Render.

sessions: Dict[str, List[dict]] = {}


def get_conversation(session_id: str) -> List[dict]:
    """
    Return the conversation history for a session.
    """

    return sessions.get(
        session_id,
        [],
    )


def add_message(
    session_id: str,
    role: str,
    content: str,
) -> None:
    """
    Add a message to the session conversation.
    """

    if session_id not in sessions:

        sessions[session_id] = []

    sessions[session_id].append(
        {
            "role": role,
            "content": content,
        }
    )


def clear_conversation(
    session_id: str,
) -> None:
    """
    Delete a conversation session.
    """

    sessions.pop(
        session_id,
        None,
    )