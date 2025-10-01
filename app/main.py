from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="LiftPal Video Analysis API")

# Register routes
app.include_router(router)
