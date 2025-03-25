from langchain.tools import Tool

def fetch_product_data(preferences):
    """Mock function to fetch product data based on preferences.
    
    Args:
        preferences (list): A list of user preferences.
        
    Returns:
        list: A list of product names.
    """
    # Replace this with actual logic to fetch product data based on preferences.
    return ["Product A", "Product B", "Product C"]

def fetch_product_data_tool():
    """Define a tool for fetching product data."""
    return Tool(
        name="fetch_product_data",
        func=fetch_product_data,
        description="Fetch product data based on user preferences."
    )