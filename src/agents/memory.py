import logging
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents import initialize_agent, Tool
from src.utils.helpers import fetch_product_data_tool, fetch_product_data

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MemoryModule:
    """
    MemoryModule handles conversation history, recommendations, and dynamic tool execution.
    """
    def __init__(self, llm):
        # Initialize conversation history and recommendation store.
        self.conversation_history = []
        self.recommendations = []
        self.llm_chain = LLMChain(
            llm=llm,
            prompt=PromptTemplate(
                input_variables=["query", "history"],
                template=(
                    "User query: {query}\n"
                    "Conversation history: {history}\n"
                    "Reason about the query and respond appropriately."
                )
            )
        )
        self.tools = [fetch_product_data_tool()]
        self.agent = initialize_agent(
            tools=self.tools,
            llm=llm,
            agent="zero-shot-react-description",
            verbose=True
        )

    def add_to_history(self, query, response):
        """Store a query-response pair into the conversation history."""
        self.conversation_history.append({"query": query, "response": response})

    def get_history(self):
        """Return the conversation history as a formatted string."""
        if not self.conversation_history:
            return ""
        return "\n".join(
            f"Q: {item['query']}\nA: {item['response']}"
            for item in self.conversation_history
        )

    def add_recommendation(self, recommendation):
        """Store the given recommendation."""
        self.recommendations.append(recommendation)

    def get_past_recommendations(self):
        """Return the stored recommendations."""
        return self.recommendations

    def execute(self, plan, query=None):
        """
        Execute the plan and return the appropriate response.
        """
        if plan == "reasoning":
            history = self.get_history()
            response = self.llm_chain.run({"query": query, "history": history})
            self.add_to_history(query, response)
            return response

        if plan == "recommendation":
            preferences = self.get_past_recommendations()
            recommendation = fetch_product_data(preferences)  # Fetch based on preferences
            self.add_recommendation(recommendation)
            return f"Based on your preferences, here are some recommendations: {recommendation}"

        if plan == "avoid_repetition":
            return "You've already seen these recommendations. Let me find something new."

        if plan == "history":
            history = self.get_history()
            if not history:
                return "No conversation history found."
            return f"Here is your conversation history: {history}"

        if plan == "dynamic_tool":
            try:
                logger.info(f"Executing dynamic tool with query: {query}")
                response = self.agent.run(query)
                self.add_to_history(query, response)
                logger.info("Dynamic tool execution successful.")
                return response
            except Exception as e:
                logger.error(f"Error in dynamic tool execution: {e}")
                return "Sorry, an error occurred while processing your request."

        return "How can I assist you further?"