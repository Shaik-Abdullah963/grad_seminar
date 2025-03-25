from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from src.utils.helpers import fetch_product_data  # Ensure this is imported

class ActionModule:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["query", "history"],
                template="User query: {query}\nConversation history: {history}\nReason about the query and respond appropriately."
            )
        )

    def execute(self, plan, query=None):
        if plan == "reasoning":
            history = self.memory.get_history()
            response = self.llm_chain.run({"query": query, "history": history})
            self.memory.add_to_history(query, response)
            return response

        if plan == "recommendation":
            preferences = self.memory.get_past_recommendations()
            recommendation = fetch_product_data(preferences)  # Fetch based on preferences
            self.memory.add_recommendation(recommendation)
            return f"Based on your preferences, here are some recommendations: {recommendation}"

        if plan == "avoid_repetition":
            # Avoid recommending the same items repeatedly
            return "You've already seen these recommendations. Let me find something new."

        if plan == "history":
            history = self.memory.get_history()
            if not history:
                return "No conversation history found."
            return f"Here is your conversation history: {history}"

        # Default response for general queries
        return "How can I assist you further?"