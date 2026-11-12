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
 item=CapacityScenario(id=str(uuid.uuid4()),created_at=now(),stale=0,stale_reason="",**payload.model_dump());db.add(item);db.commit();return serialize(item)
def acknowledge(db,id):
 # 数据员确认方案按当前剖面继续有效；剖面重算失败时禁止确认，也就无法启动新预演。
 item=db.get(CapacityScenario,id)
 if not item:raise HTTPException(404,"方案不存在")
 profile=db.get(ServiceProfile,item.profile_id)
 if profile and profile.stale:raise HTTPException(409,"关联剖面重算失败（"+profile.last_error+"），不可确认或启动新预演")
 item.stale=0;item.stale_reason="";db.commit();return serialize(item)
