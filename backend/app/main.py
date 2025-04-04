from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import social_media

app = FastAPI(
    title="MibiTech Backend API",
    description="API backend for MibiTech website",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(social_media.router, prefix="/api/social-media", tags=["social-media"])

@app.get("/api/status")
async def status():
    return {"status": "ok"}