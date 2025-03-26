# Grad Seminar – Shopping Assistant AI Agent

This project implements a shopping assistant that uses a Large Language Model (LLM) for generating personalized product recommendations. It is designed to support multiple users via a RESTful API built with FastAPI. Each user’s conversation history, profile, and recommendations are maintained in separate sessions.

## Project Structure

```
grad_seminar/
├── data/
│   └── data_loader.py              # Data loading and preprocessing utilities.
├── src/
│   ├── agents/
│   │   ├── action.py               # Contains the ActionModule – execution logic for queries.
│   │   ├── memory.py               # Implements MemoryModule that stores conversation history and recommendations.
│   │   ├── planning.py             # Implements PlanningModule to decide action plans.
│   │   ├── profiling.py            # Implements ProfilingModule to handle user profile.
│   │   ├── shopping_agent.py       # High-level agent integrating all modules.
│   │   └── __pycache__/
│   ├── api/
│   │   ├── main_api.py             # The FastAPI application entry point.
│   │   └── __pycache__/
│   ├── recommender/
│   │   └── collaborative_filtering.py  # (Optional) Alternative recommendation strategies.
│   └── utils/
│       └── helpers.py              # Helper functions (e.g., for fetching product data).
└── tests/
    └── test_agents.py             # Unit tests for agent modules.
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- LangChain
- Other required packages as listed in your `requirements.txt` (if available).

## Setup and Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/YourUsername/grad_seminar.git
   cd grad_seminar
   ```

2. **Create a virtual environment and install dependencies:**
   On Mac:
   ```
   python3 -m venv grad_seminar_venv
   source grad_seminar_venv/bin/activate
   pip install -r requirements.txt
   ```
   Ensure that your `requirements.txt` contains FastAPI, Uvicorn, langchain, and any additional dependencies.

## Running the API

The API is implemented in `src/api/main_api.py`. To run the FastAPI server, use the following command from your project root:

```
uvicorn src.api.main_api:app --host 0.0.0.0 --port 8000 --reload
```

This will start the API server at [http://localhost:8000](http://localhost:8000).

## API Endpoints

Once the server is running, you can interact with your API endpoints:

### 1. **Query Endpoint**
- **Endpoint:** `POST /query`
- **Description:** Process a user query and return a structured response including direct reasoning, the chosen plan, product recommendations, and conversation history.
- **Example Request:**
  ```json
  {
      "query": "Can you recommend some pasta?"
  }
  ```
  Optionally, include a `"user_id"` to continue a session:
  ```json
  {
      "user_id": "existing-user-id",
      "query": "Can you recommend a laptop?"
  }
  ```
- **Response:** JSON object with fields:
  - `user_id`
  - `direct_response`
  - `plan`
  - `response_based_on_plan`
  - `recommendation`
  - `conversation_history`

### 2. **Get History**
- **Endpoint:** `GET /history/{user_id}`
- **Description:** Retrieve the conversation history for the specified user.
- **Example Request:**
  ```
  GET http://localhost:8000/history/your-user-id
  ```

### 3. **Update Profile**
- **Endpoint:** `PUT /profile/{user_id}`
- **Description:** Update the user's profile, for example, updating their name or preferences.
- **Example Request:**
  ```json
  {
      "name": "Jane Doe",
      "preferences": ["budget-friendly", "gaming"]
  }
  ```

### 4. **Reset Memory**
- **Endpoint:** `POST /reset/{user_id}`
- **Description:** Clear the conversation history and recommendations for the given user.
- **Example Request:**
  ```
  POST http://localhost:8000/reset/your-user-id
  ```

## Interacting with the API

There are several ways to interact with the API:

- **Swagger UI:**  
  Visit [http://localhost:8000/docs](http://localhost:8000/docs) to use the interactive API documentation provided by FastAPI.

- **Curl:**  
  Use curl commands from your terminal (examples provided above) to test the endpoints.

- **Postman or Other HTTP Clients:**  
  You can also use Postman to prepare and send HTTP requests and inspect responses.

## Additional Notes

- **Session Management:**  
  Each user session is maintained in memory. In production, consider using a database or caching system (e.g., Redis) for persistence.

- **Customization:**  
  You can extend the agent’s functionalities in `src/agents/shopping_agent.py` and modify the logic in the agent modules located in `src/agents/`.

- **Testing:**  
  Unit tests for the agent components are located in the `tests/` folder. Use pytest to run tests:
  ```
  pytest tests/
  ```

## License
[Your License Information]

## Author
Abdullah Shaik