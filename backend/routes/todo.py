# routes/todo.py

"""
This module defines the API routes for all Todo-related operations.

It uses an APIRouter to group these endpoints, which are then
included by the main FastAPI app instance in main.py.
"""

from fastapi import APIRouter, Body, HTTPException, status, Response
from typing import List
import database  # Absolute import from the project root (backend folder)
from models import Todo, TodoUpdate  # Absolute import from the project root

# Create a new APIRouter instance
# prefix="/todos": All routes in this file will be prepended with /todos
# tags=["Todos"]: All routes will be grouped under "Todos" in the Swagger docs
router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

# --- Todo Endpoints ---

@router.post(
    "/",  # The path is now "/" because of the prefix
    response_description="Add a new todo",
    response_model=Todo,
    status_code=status.HTTP_201_CREATED
)
async def create_todo(todo: Todo = Body(...)):
    """
    Create a new todo item and store it in the database.
    """
    todo_data = todo.model_dump(by_alias=True, exclude=["id"])
    new_todo = await database.add_todo(todo_data)
    return new_todo


@router.get(
    "/",  # The path is now "/" because of the prefix
    response_description="List all todos",
    response_model=List[Todo]
)
async def list_todos():
    """
    Retrieve all todo items from the database.
    """
    todos = await database.retrieve_todos()
    return todos


@router.get(
    "/{id}",  # The path is now just "/{id}"
    response_description="Get a single todo by its ID",
    response_model=Todo
)
async def get_todo(id: str):
    """
    Retrieve a single todo item by its unique ID.
    """
    todo = await database.retrieve_todo(id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {id} not found"
        )
    return todo


@router.put(
    "/{id}",
    response_description="Update an existing todo",
    response_model=Todo
)
async def update_todo_data(id: str, req: TodoUpdate = Body(...)):
    """
    Update one or more fields of an existing todo item.
    """
    req_data = req.model_dump(exclude_unset=True)
    updated_todo = await database.update_todo(id, req_data)
    if updated_todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {id} not found"
        )
    return updated_todo


@router.delete(
    "/{id}",
    response_description="Delete a todo",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_todo_data(id: str):
    """
    Delete a todo item from the database by its ID.
    """
    deleted = await database.delete_todo(id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with ID {id} not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)