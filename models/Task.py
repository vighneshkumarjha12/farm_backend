from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel ,Field
from typing import Union,Optional

class Task(BaseModel):
    title:str = Field(...)
    desc: str = Field(...)
    is_complete:Union[bool,None] = False
    created_at:datetime = Field(default=datetime.now())






#  UPDATE (PUT / PATCH)
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None
    is_complete: Optional[bool] = None