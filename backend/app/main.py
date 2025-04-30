from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import base_router
from .routers.listings import router as listings_router

app = FastAPI(title="HouseHackCalc API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(base_router)
app.include_router(listings_router)

@app.get("/")
async def root():
    return {"message": "Welcome to HouseHackCalc API"}  