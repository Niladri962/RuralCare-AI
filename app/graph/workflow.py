from langgraph.graph import (
    StateGraph,
    START,
    END,
)

from app.graph.state import HealthcareState

from app.agents.planner import planner_agent

from app.agents.extractor import (
    extract_patient_information,
)

from app.agents.triage import triage_agent

from app.agents.guardrail import (
    safety_guardrail,
)

from app.agents.safety import safety_agent

from app.agents.emergency import (
    emergency_handler,
)

from app.agents.urgent import (
    urgent_handler,
)

from app.agents.routine import (
    routine_handler,
)

from app.agents.followup import (
    followup_handler,
)


def route_after_safety(
    state: dict,
) -> str:

    # Deterministic emergency
    # guardrail has highest priority.

    if state.get(
        "guardrail_triggered",
        False,
    ):

        return "emergency"


    safety_result = state.get(
        "safety_result",
        {},
    )


    urgency = safety_result.get(
        "final_urgency",
        "NEED_MORE_INFORMATION",
    )


    if urgency == "EMERGENCY":

        return "emergency"


    if urgency == "URGENT":

        return "urgent"


    if urgency == "ROUTINE":

        return "routine"


    return "followup"


def build_healthcare_graph():

    graph = StateGraph(
        HealthcareState
    )


    # =========================
    # AGENTS
    # =========================

    graph.add_node(
        "planner",
        planner_agent,
    )


    graph.add_node(
        "extractor",
        extract_patient_information,
    )


    graph.add_node(
        "triage",
        triage_agent,
    )


    graph.add_node(
        "guardrail",
        safety_guardrail,
    )


    graph.add_node(
        "safety",
        safety_agent,
    )


    # =========================
    # HANDLERS
    # =========================

    graph.add_node(
        "emergency",
        emergency_handler,
    )


    graph.add_node(
        "urgent",
        urgent_handler,
    )


    graph.add_node(
        "routine",
        routine_handler,
    )


    graph.add_node(
        "followup",
        followup_handler,
    )


    # =========================
    # WORKFLOW
    # =========================

    graph.add_edge(
        START,
        "planner",
    )


    graph.add_edge(
        "planner",
        "extractor",
    )


    graph.add_edge(
        "extractor",
        "triage",
    )


    graph.add_edge(
        "triage",
        "guardrail",
    )


    graph.add_edge(
        "guardrail",
        "safety",
    )


    # =========================
    # ROUTING
    # =========================

    graph.add_conditional_edges(

        "safety",

        route_after_safety,

        {
            "emergency":
                "emergency",

            "urgent":
                "urgent",

            "routine":
                "routine",

            "followup":
                "followup",
        },
    )


    # =========================
    # END
    # =========================

    graph.add_edge(
        "emergency",
        END,
    )


    graph.add_edge(
        "urgent",
        END,
    )


    graph.add_edge(
        "routine",
        END,
    )


    graph.add_edge(
        "followup",
        END,
    )


    return graph.compile()


healthcare_graph = (
    build_healthcare_graph()
)