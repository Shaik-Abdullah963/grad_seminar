from langchain.chat_models import ChatOpenAI  # Updated import for ChatOpenAI
from src.agents.memory import MemoryModule
from src.agents.action import ActionModule
from src.agents.profiling import ProfilingModule
from src.agents.planning import PlanningModule

def main():
    # Initialize the LLM instance first.
    llm = ChatOpenAI(model="gpt-4o")  # Replace with your preferred model

    # Initialize modules with the LLM instance where needed.
    memory = MemoryModule(llm)
    profiling = ProfilingModule()
    planning = PlanningModule(memory=memory, profiling=profiling)
    action_module = ActionModule(memory, llm)

    # Example usage: obtain user query from input or preset.
    user_query = "Can you recommend a Pasta?"
    
    # Option 1: Direct action execution (existing functionality).
    response = action_module.execute(plan="reasoning", query=user_query)
    print("Direct Reasoning Response:", response)
    
    # Option 2: Use PlanningModule to decide the plan dynamically.
    plan = planning.plan(user_query)
    print("Plan decided:", plan)
    response = action_module.execute(plan=plan, query=user_query)
    print("Response based on plan:", response)
    
    # Add a recommendation and show the result.
    recommendation_response = action_module.execute(plan="recommendation")
    print("Recommendation Response:", recommendation_response)
    
    # Retrieve and print conversation history.
    history_response = action_module.execute(plan="history")
    print("Conversation History:", history_response)

if __name__ == "__main__":
    main()