import uuid
from sqlalchemy import select
from fastapi import HTTPException
from src.models import ServiceProfile
from src.services.datasets import require
from src.services.profiling import fit_profile
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload):
 dataset=require(db,payload.dataset_id)
 if db.scalar(select(ServiceProfile).where(ServiceProfile.name==payload.name)):raise HTTPException(409,"服务剖面名称已存在")
 try:fitted=fit_profile(dataset.rows,payload.period)
 except ValueError as e:raise HTTPException(422,str(e))
 item=ServiceProfile(id=str(uuid.uuid4()),created_at=now(),**payload.model_dump(),**fitted);db.add(item);db.commit();return serialize(item)
