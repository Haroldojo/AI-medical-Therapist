# Step1: Setup FastAPI Backend
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from .aiagent import graph,SYSTEM_PROMPT,parse_response


app = FastAPI()

# Setp2: Receive and validate Request from frontend
class Query(BaseModel):
    message: str

@app.post("/ask")
async def ask(query: Query):
    #AI agent
    # Step3: Send response to frontend
    inputs = {"messages":[("system", SYSTEM_PROMPT), ("user", query.message)]}
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)
    return {"response":final_response,"tool_called":tool_called_name}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

