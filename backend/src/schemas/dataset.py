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
class ObservationChange(BaseModel):
 action:Literal["upsert","withdraw"]
 sample_id:str=Field(min_length=1,max_length=50)
 period:Literal["peak","offpeak"]|None=None
 interarrival_minutes:float|None=Field(default=None,gt=0,le=120,allow_inf_nan=False)
 service_minutes:float|None=Field(default=None,gt=0,le=180,allow_inf_nan=False)
 @model_validator(mode="after")
 def complete(self):
  if self.action=="upsert" and (self.period is None or self.interarrival_minutes is None or self.service_minutes is None):
   raise ValueError("补录或更正必须提供时段、到达间隔与服务时长")
  return self
class ObservationBatch(BaseModel):
 changes:list[ObservationChange]=Field(min_length=1,max_length=1000)
 @model_validator(mode="after")
 def unique(self):
  ids=[c.sample_id for c in self.changes]
  if len(set(ids))!=len(ids): raise ValueError("同批变更中样本编号重复，整批不生效")
  return self
