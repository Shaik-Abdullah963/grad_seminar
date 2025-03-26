from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

from langchain.chat_models import ChatOpenAI
from src.agents.memory import MemoryModule
from src.agents.action import ActionModule
from src.agents.profiling import ProfilingModule
from src.agents.planning import PlanningModule

app = FastAPI(
    title="Shopping Assistant API",
    description="A RESTful API for the shopping agent supporting multiple users.",
    version="1.0.0"
)

# Create a global ChatOpenAI instance (shared across sessions)
llm = ChatOpenAI(model="gpt-4o")  # Replace with your preferred chat model

# Dictionary to store per-user sessions.
user_sessions = {}

class UserSession:
    """
    Container for per-user agent modules.
    """
    def __init__(self):
        self.memory = MemoryModule(llm)
        self.profiling = ProfilingModule()
        self.planning = PlanningModule(memory=self.memory, profiling=self.profiling)
        self.action = ActionModule(self.memory, llm)

def get_user_session(user_id: str) -> UserSession:
    """
    Retrieve the session for the given user_id.
    If the session doesn't exist, create a new one.
    """
    if user_id not in user_sessions:
        user_sessions[user_id] = UserSession()
    return user_sessions[user_id]

# Request and Response Models
class QueryRequest(BaseModel):
    user_id: Optional[str]  # If not provided, a new user_id is generated.
    query: str

class QueryResponse(BaseModel):
    user_id: str
    direct_response: str
    plan: str
    response_based_on_plan: str
    recommendation: str
    conversation_history: str

class ProfileUpdate(BaseModel):
    name: Optional[str]
    preferences: Optional[list]

@app.post("/query", response_model=QueryResponse)
async def process_query(req: QueryRequest):
    # Generate or fetch the user session.
    user_id = req.user_id or str(uuid4())
    session = get_user_session(user_id)
    
    try:
        user_query = req.query
        
        # Direct execution branch: get a direct reasoning response.
        direct_response = session.action.execute(plan="reasoning", query=user_query)
        
        # Use PlanningModule to decide the best plan based on past interactions.
        plan = session.planning.plan(user_query)
        response_based_on_plan = session.action.execute(plan=plan, query=user_query)
        
        # Get product recommendations and conversation history.
        recommendation = session.action.execute(plan="recommendation")
        conversation_history = session.action.execute(plan="history")
        
        return QueryResponse(
            user_id=user_id,
            direct_response=direct_response,
            plan=plan,
            response_based_on_plan=response_based_on_plan,
            recommendation=recommendation,
            conversation_history=conversation_history
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{user_id}")
async def get_history(user_id: str):
    session = get_user_session(user_id)
    try:
        history = session.action.execute(plan="history")
        return {"user_id": user_id, "conversation_history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/profile/{user_id}")
async def update_profile(user_id: str, profile: ProfileUpdate):
    session = get_user_session(user_id)
    try:
        if profile.name is not None:
            session.profiling.update_profile("name", profile.name)
        if profile.preferences is not None:
            session.profiling.update_profile("preferences", profile.preferences)
        return {"user_id": user_id, "message": "Profile updated", "profile": session.profiling.get_profile()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reset/{user_id}")
async def reset_memory(user_id: str):
    session = get_user_session(user_id)
    try:
        session.memory.conversation_history.clear()
        session.memory.recommendations.clear()
        return {"user_id": user_id, "message": "Memory has been reset."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main_api:app", host="0.0.0.0", port=8000, reload=True)