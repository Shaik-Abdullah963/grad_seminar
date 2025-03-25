from langchain.chains import LLMChain
from langchain.prompts.chat import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

class PlanningModule:
    def __init__(self, memory, profiling):
        self.memory = memory
        self.profiling = profiling
        # Use the ChatOpenAI instance here.
        self.llm = ChatOpenAI(model="gpt-4o")  # Use your chat model
        # Create a ChatPromptTemplate for the planning chain.
        chat_prompt = ChatPromptTemplate.from_messages([
            HumanMessagePromptTemplate.from_template(
                "User query: {query}\n"
                "Conversation history: {history}\n"
                "User profile: {profile}\n"
                "Based on the above information, decide the best plan. Options: reasoning, recommendation, history, dynamic_tool."
            )
        ])
        self.planning_chain = LLMChain(llm=self.llm, prompt=chat_prompt)

    def plan(self, query):
        history = self.memory.get_history()
        profile = self.profiling.get_profile()
        # Run the chain using the chat prompt
        plan = self.planning_chain.run({
            "query": query,
            "history": history,
            "profile": profile
        })
        return plan.strip()