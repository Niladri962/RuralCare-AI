from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from app.api.voice import router as voice_router
from app.graph.workflow import healthcare_graph
from app.services.session import (
    get_conversation,
    add_message,
    clear_conversation,
)

# Create FastAPI app FIRST
app = FastAPI(
    title="RuralCare AI",
    version="0.6.0",
    description="Healthcare Triage Assistant"
)

# Serve frontend files
app.mount("/static", StaticFiles(directory="frontend"), name="static")


# Home page
@app.get("/")
async def home():
    return FileResponse("frontend/index.html")

app.include_router(
    voice_router
)