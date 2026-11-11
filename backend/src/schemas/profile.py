from pydantic import BaseModel,Field
from typing import Literal
class ProfileInput(BaseModel):
 name:str=Field(min_length=2,max_length=120)
 dataset_id:str
 period:Literal["all","peak","offpeak"]="all"
