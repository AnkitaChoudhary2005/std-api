
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


# Data received when creating or updating a student
class StudentCreate(BaseModel):

   name: str = Field(min_length=1, max_length=100)

   age: int = Field(gt=0)

class StudentUpdate(BaseModel):
        
        name: Optional[str] = Field(
    
                        default=None,
                        min_length=1,
                        max_length=100
                                            )
        age: Optional[int]= Field(
                default=None,
                gt=0)


# Data returned by the API

class StudentResponse(BaseModel):

    id: int

    name: str

    age: int

    model_config = ConfigDict(from_attributes=True)
