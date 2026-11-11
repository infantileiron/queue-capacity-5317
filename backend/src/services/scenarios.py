import uuid
from sqlalchemy import select
from fastapi import HTTPException
from src.models import CapacityScenario,ServiceProfile
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload):
 profile=db.get(ServiceProfile,payload.profile_id)
 if not profile:raise HTTPException(404,"服务剖面不存在")
 if profile.arrival_rate*payload.arrival_multiplier*(payload.duration_minutes+payload.warmup_minutes)>20000:raise HTTPException(422,"仿真事件预算过大，请缩短时域")
 if db.scalar(select(CapacityScenario).where(CapacityScenario.name==payload.name)):raise HTTPException(409,"方案名称已存在")
 item=CapacityScenario(id=str(uuid.uuid4()),created_at=now(),**payload.model_dump());db.add(item);db.commit();return serialize(item)
