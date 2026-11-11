import uuid
from fastapi import HTTPException
from sqlalchemy import select
from src.models import ArrivalDataset
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload):
 if db.scalar(select(ArrivalDataset).where(ArrivalDataset.name==payload.name)):raise HTTPException(409,"样本名称已存在")
 item=ArrivalDataset(id=str(uuid.uuid4()),name=payload.name,source=payload.source,rows=[r.model_dump() for r in payload.rows],created_at=now());db.add(item);db.commit();return serialize(item)
def require(db,id):
 item=db.get(ArrivalDataset,id)
 if not item:raise HTTPException(404,"样本不存在")
 return item
