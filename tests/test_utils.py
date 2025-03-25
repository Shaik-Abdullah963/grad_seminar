import pytest
from src.utils.helpers import fetch_product_data, fetch_product_data_tool

def test_fetch_product_data():
    """
    Test the fetch_product_data function.
    """
    # Mock user preferences
    preferences = ["electronics", "budget-friendly"]
    
    # Call the function
    result = fetch_product_data(preferences)
    
    # Assertions
    assert isinstance(result, list), "Expected result to be a list."
    assert len(result) > 0, "Expected non-empty list of products."
    assert all(isinstance(item, str) for item in result), "All items in the result should be strings."

def test_fetch_product_data_tool():
    """
    Test the fetch_product_data_tool function.
    """
    # Call the function
    tool = fetch_product_data_tool()
    
    # Assertions
    assert tool.name == "fetch_product_data", "Tool name should be 'fetch_product_data'."
    assert callable(tool.func), "Tool function should be callable."
    assert "Fetch product data" in tool.description, "Tool description should include 'Fetch product data'."