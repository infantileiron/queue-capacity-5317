from pydantic import BaseModel,Field,model_validator
from typing import Literal
class Observation(BaseModel):
 sample_id:str=Field(min_length=1,max_length=50)
 period:Literal["peak","offpeak"]
 interarrival_minutes:float=Field(gt=0,le=120,allow_inf_nan=False)
 service_minutes:float=Field(gt=0,le=180,allow_inf_nan=False)
class DatasetInput(BaseModel):
 name:str=Field(min_length=2,max_length=120)
 source:str=Field(default="arrivals.json",max_length=120)
 rows:list[Observation]=Field(min_length=20,max_length=5000)
 @model_validator(mode="after")
 def unique(self):
  if len({x.sample_id for x in self.rows})!=len(self.rows): raise ValueError("样本编号重复")
  return self
