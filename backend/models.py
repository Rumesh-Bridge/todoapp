from optparse import Option
from pydantic import BaseModel, Field
from typing import Optional

from pydantic.warnings import ArbitraryTypeWarning
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid Object")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, feild_schema):
        feild_schema.update(type="string")
    
class Todo(BaseModel):
    id:Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    description: Optional[str] = None
    completed: bool = False

    class Config: 
        allow_population_feild_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId:str}

class TodoUpdate(BaseModel):
    title:Optional[str]
    description: Optional[str]
    completed:Optional[bool]