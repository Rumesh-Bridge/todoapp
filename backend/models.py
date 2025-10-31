# models.py

from pydantic import BaseModel, Field
from typing import Optional, Any
from bson import ObjectId
from pydantic_core import core_schema
from pydantic.json_schema import GetJsonSchemaHandler  


class PyObjectId(ObjectId):
    """
    Custom Pydantic type for MongoDB's ObjectId.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, info: Any) -> ObjectId:
        """Validate that the input is a valid ObjectId."""
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        core_schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler 
    ) -> dict[str, Any]:
        """
        This is the new Pydantic v2 method to update the JSON schema.
        We are telling Swagger/OpenAPI that this field should be treated
        as a plain string.
        """
        return {"type": "string"}


class Todo(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config: 
        """
        Pydantic model configuration.
        """
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None