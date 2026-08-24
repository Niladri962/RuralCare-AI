from app.graph.workflow import healthcare_graph


def test_planner():

    result = healthcare_graph.invoke(
        {
            "user_message": "I have had a fever since yesterday."
        }
    )

    print("\nPlanner response:")
    print(result["planner_response"])

    assert "planner_response" in result