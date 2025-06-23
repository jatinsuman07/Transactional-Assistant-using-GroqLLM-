from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from utils_tools import call_llm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class InvokeRequest(BaseModel):
    input: str
    config: Optional[List[Dict[str, Any]]] = None
    kwargs: Optional[Dict[str, Any]] = None

@app.get("/")
def read_root():
    return {"message": "Welcome to the Transactional System - BankMitra"}

@app.post("/customer-service/invoke")
async def invoke(request: InvokeRequest):
    try:
        response = call_llm(request.input)  # Modify if needed
        print(response)
        return {"output": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
