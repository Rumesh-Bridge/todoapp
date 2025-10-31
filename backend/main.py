# main.py

"""
Main application file.

This file:
1. Creates the main FastAPI application instance.
2. Configures CORS middleware.
3. Includes the API routers from the /routes directory.
4. Defines a root endpoint for health checks.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import todo  

# --- App Initialization ---
app = FastAPI(
    title="Todo API",
    description="A simple API for a Todo application, built with FastAPI and MongoDB.",
    version="1.0.0"
)

# --- CORS Configuration ---
origins = [
    "http://localhost:3000",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routers ---
# This is the key line. It tells the main app to include
# all the routes defined in the 'todo.router' from routes/todo.py.
app.include_router(todo.router)


# --- Root Endpoint ---
@app.get("/", tags=["Root"])
async def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"message": "Welcome to the Todo App API!"}