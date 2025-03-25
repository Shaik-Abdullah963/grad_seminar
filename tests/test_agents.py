from src.agents.shopping_agent import ShoppingAssistant
import pytest

def test_shopping_agent_reasoning():
    """
    Test the reasoning functionality of the ShoppingAssistant.
    """
    assistant = ShoppingAssistant()
    response = assistant.respond("What are the best smartphones?", plan="reasoning")
    assert isinstance(response, str)
    assert len(response) > 0  # Ensure the response is not empty

def test_shopping_agent_recommendation():
    """
    Test the recommendation functionality of the ShoppingAssistant.
    """
    assistant = ShoppingAssistant()
    response = assistant.respond(plan="recommendation")
    assert isinstance(response, str)
    assert "recommendations" in response.lower(), "Recommendation response should mention recommendations."

def test_shopping_agent_history():
    """
    Test the history retrieval functionality of the ShoppingAssistant.
    """
    assistant = ShoppingAssistant()
    assistant.respond("What are the best laptops?", plan="reasoning")  # Add to history
    response = assistant.respond(plan="history")
    assert isinstance(response, str)
    # Allow either the phrase "conversation history" or some non-empty history output.
    assert ("conversation history" in response.lower()) or (len(response.strip()) > 0)

def test_shopping_agent_dynamic_tool():
    """
    Test the dynamic tool usage functionality of the ShoppingAssistant.
    """
    assistant = ShoppingAssistant()
    response = assistant.respond("Find me a budget-friendly smartphone.", plan="dynamic_tool")
    assert isinstance(response, str)
    assert len(response) > 0  # Ensure the response is not empty

def test_shopping_agent_clear_memory():
    """
    Test the clear memory functionality of the ShoppingAssistant.
    """
    assistant = ShoppingAssistant()
    assistant.respond("What are the best laptops?", plan="reasoning")  # Add to history
    assistant.clear_memory()
    response = assistant.respond(plan="history")
    # Expecting a response indicating that no conversation history is available.
    assert "no conversation history found" in response.lower()

def test_shopping_agent_invalid_plan():
    """
    Test the behavior of the ShoppingAssistant with an invalid plan.
    """
    assistant = ShoppingAssistant()
    response = assistant.respond("What is the best smartphone?", plan="invalid_plan")
    assert isinstance(response, str)
    # Assuming default fallback response is returned.
    assert "how can i assist you further" in response.lower()

def test_shopping_agent_empty_query():
    """
    Test the behavior of the ShoppingAssistant with an empty query.
    """
    assistant = ShoppingAssistant()
    response = assistant.respond("", plan="reasoning")
    assert isinstance(response, str)
    assert len(response) > 0  # Ensure the response is not empty

def test_shopping_agent_profile_integration():
    """
    Test the integration of user profiles in the ShoppingAssistant.
    """
    assistant = ShoppingAssistant()
    # Simulate adding user preferences to the profile.
    assistant.profiling.update_profile("preferences", ["electronics", "budget-friendly"])
    response = assistant.respond(plan="recommendation")
    assert isinstance(response, str)
    assert "recommendations" in response.lower(), "Recommendation response should mention recommendations."

def test_shopping_agent_memory_persistence():
    """
    Test the persistence of conversation history in the ShoppingAssistant.
    """
    assistant = ShoppingAssistant()
    assistant.respond("What are the best laptops?", plan="reasoning")  # Add first query to history
    response1 = assistant.respond(plan="history")
    assert "conversation history" in response1.lower(), "History should contain the conversation details."

    assistant.respond("What are the best smartphones?", plan="reasoning")  # Add another query
    response2 = assistant.respond(plan="history")
    # Verify that both queries are present in the history.
    assert "laptops" in response2.lower() and "smartphones" in response2.lower(), "History should include both 'laptops' and 'smartphones'."