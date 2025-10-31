"""
database.py

This module handles all interactions with the MongoDB database for the todo app.
It contains:
- The database connection setup (client, database, and collection).
- A helper function to serialize MongoDB documents into Python dictionaries.
- CRUD (Create, Read, Update, Delete) operations for todo items.

This approach separates database logic from the API routing logic (in main.py),
making the code cleaner and easier to maintain.
"""

import motor.motor_asyncio  # The asynchronous driver for MongoDB
from bson import ObjectId  # For handling MongoDB's unique '_id' field
from models import Todo, TodoUpdate  # Import our Pydantic models
import os            
from dotenv import load_dotenv  

# --- Database Configuration ---

# !! IMPORTANT: Replace with your actual MongoDB connection string.
# This could be from a local MongoDB server or a cloud-hosted one like MongoDB Atlas.
# For production, this should be loaded from an environment variable (.env file), not hardcoded.
load_dotenv() 

MONGO_DETAILS = os.getenv("MONGODB_URL")

# Create an asynchronous client to connect to MongoDB.
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# Access your specific database (e.g., "tododb").
# MongoDB will create this database if it doesn't exist upon first write.
database = client.tododb

# Access your specific collection (like a table in SQL, e.g., "todos").
todo_collection = database.get_collection("todos")


# --- Helper Function ---

def todo_helper(todo) -> dict:
    """
    Converts a MongoDB document (BSON) into a Python dictionary.

    MongoDB's '_id' is an ObjectId object, which isn't JSON serializable.
    This function converts '_id' to a string and formats the rest of the
    document to match our Pydantic model.

    Args:
        todo (dict): A todo document retrieved from MongoDB.

    Returns:
        dict: A dictionary representation of the todo with a string 'id'.
    """
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        # Use .get() for optional fields to avoid errors if the field doesn't exist
        "description": todo.get("description"),
        "completed": todo["completed"],
    }


# --- CRUD Database Operations ---

async def retrieve_todos() -> list[dict]:
    """
    Retrieves all todo items from the database.
    """
    todos = []
    # .find() returns a cursor. We must iterate over it asynchronously.
    async for todo in todo_collection.find():
        todos.append(todo_helper(todo))
    return todos


async def add_todo(todo_data: dict) -> dict:
    """
    Adds a new todo item to the database.

    Args:
        todo_data (dict): A dictionary containing the todo data,
                          validated by the Pydantic 'Todo' model.

    Returns:
        dict: The newly created todo item, converted by todo_helper.
    """
    # Insert the new todo document and get the result
    todo = await todo_collection.insert_one(todo_data)
    
    # Find the newly created document using its inserted_id
    new_todo = await todo_collection.find_one({"_id": todo.inserted_id})
    
    # Convert and return it
    return todo_helper(new_todo)


async def retrieve_todo(id: str) -> dict | None:
    """
    Retrieves a single todo item by its ID.

    Args:
        id (str): The string representation of the todo's ObjectId.

    Returns:
        dict or None: The matching todo item if found, otherwise None.
    """
    # We must convert the string 'id' back into a MongoDB 'ObjectId'
    # to query the database by '_id'.
    todo = await todo_collection.find_one({"_id": ObjectId(id)})
    
    if todo:
        return todo_helper(todo)
    return None  # Explicitly return None if no todo was found


async def update_todo(id: str, data: dict) -> dict | None:
    """
    Updates an existing todo item in the database.

    Args:
        id (str): The string ID of the todo to update.
        data (dict): A dictionary containing the fields to update,
                     validated by the Pydantic 'TodoUpdate' model.

    Returns:
        dict or None: The updated todo item if successful, otherwise None.
    """
    # The 'data' dict comes from the TodoUpdate model, which has optional fields.
    # We must remove any fields that were not provided (i.e., are None)
    # so we only update the fields the user actually sent.
    data = {k: v for k, v in data.items() if v is not None}

    # Only proceed if there is at least one field to update
    if len(data) >= 1:
        update_result = await todo_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        # Check if a document was actually modified
        if update_result.modified_count == 1:
            # If update was successful, find and return the new, updated document
            if (
                updated_todo := await todo_collection.find_one({"_id": ObjectId(id)})
            ) is not None:
                return todo_helper(updated_todo)

    # If no update happened (e.g., no data provided or ID not found),
    # try to return the existing, unchanged document.
    if (
        existing_todo := await todo_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return todo_helper(existing_todo)
        
    return None  # Return None if the ID doesn't exist at all


async def delete_todo(id: str) -> bool:
    """
    Deletes a todo item from the database.

    Args:
        id (str): The string ID of the todo to delete.

    Returns:
        bool: True if the delete was successful, False otherwise.
    """
    delete_result = await todo_collection.delete_one({"_id": ObjectId(id)})

    # Check if a document was actually deleted
    if delete_result.deleted_count == 1:
        return True
    return False