from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import base_router
from .routers.listings import router as listings_router

app = FastAPI(title="My Fullstack App")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(base_router)
app.include_router(listings_router)

@app.get("/")  
async def root():  
    return {"message": "Hello from FastAPI!"}  