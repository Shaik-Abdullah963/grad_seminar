from src.agents.planning import PlanningModule
from src.agents.action import ActionModule
from src.agents.memory import MemoryModule
from src.agents.profiling import ProfilingModule
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

class ShoppingAssistant:
    def __init__(self):
        # Initialize modules; MemoryModule and ActionModule require an LLM instance.
        self.memory = MemoryModule(llm=self.initialize_llm())
        self.profiling = ProfilingModule()
        self.planning = PlanningModule(memory=self.memory, profiling=self.profiling)
        self.action = ActionModule(memory=self.memory, llm=self.initialize_llm())

    def initialize_llm(self):
        """Initialize the LLM with the desired model."""
        return OpenAI(model="gpt-4o")  # Replace with your preferred model

    def respond(self, query, plan="reasoning"):
        """
        Generate a response based on the query and plan.
        """
        # Retrieve user profile for context (if needed in the default case)
        user_profile = self.profiling.get_profile()

        # Route query based on specified plan
        if plan == "reasoning":
            return self.action.execute(plan="reasoning", query=query)

        if plan == "recommendation":
            return self.action.execute(plan="recommendation")

        if plan == "history":
            return self.action.execute(plan="history")

        if plan == "dynamic_tool":
            return self.action.execute(plan="dynamic_tool", query=query)

        # Default response using LangChain (if no specific plan is matched)
        response = self.action.llm_chain.run({"query": query, "profile": user_profile})
        self.memory.add_to_history(query, response)
        return response

    def clear_memory(self):
        """Clear conversation history and recommendations."""
        self.memory.clear_history()
        self.memory.clear_recommendations()
        
if __name__ == "__main__":
    # Example usage
    assistant = ShoppingAssistant()
    query = "Can you recommend a laptop?"
    
    # Using direct reasoning
    print("Direct Reasoning Response:", assistant.respond(query, plan="reasoning"))
    
    # Dynamically plan response
    plan = assistant.planning.plan(query)
    print("Plan decided:", plan)
    print("Response based on plan:", assistant.respond(query, plan=plan))
    
    # Get recommendations
    print("Recommendation Response:", assistant.respond(query, plan="recommendation"))
    
    # Retrieve history
    print("Conversation History:", assistant.respond("", plan="history"))