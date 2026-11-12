import uuid
from sqlalchemy import select
from fastapi import HTTPException
from src.models import ServiceProfile,CapacityScenario
from src.services.datasets import require
from src.services.profiling import fit_profile
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload):
 dataset=require(db,payload.dataset_id)
 if db.scalar(select(ServiceProfile).where(ServiceProfile.name==payload.name)):raise HTTPException(409,"服务剖面名称已存在")
 try:fitted=fit_profile(dataset.rows,payload.period)
 except ValueError as e:raise HTTPException(422,str(e))
 item=ServiceProfile(id=str(uuid.uuid4()),created_at=now(),stale=0,last_error="",dataset_revision=dataset.revision,**payload.model_dump(),**fitted);db.add(item);db.commit();return serialize(item)
def recompute(db,dataset):
 # 源观测更新后重算关联剖面：成功则刷新率与校验码；失败保留上次可用结果并标记失效。
 # 引用这些剖面的方案一律标记失效，须人工确认新剖面后才能再次运行。
 for profile in db.scalars(select(ServiceProfile).where(ServiceProfile.dataset_id==dataset.id)):
  try:fitted=fit_profile(dataset.rows,profile.period)
  except ValueError as e:
   profile.stale=1;profile.last_error=str(e)
  else:
   profile.arrival_rate=fitted["arrival_rate"];profile.service_rate=fitted["service_rate"];profile.statistics=fitted["statistics"]
   profile.dataset_revision=dataset.revision;profile.stale=0;profile.last_error=""
  for scenario in db.scalars(select(CapacityScenario).where(CapacityScenario.profile_id==profile.id)):
   scenario.stale=1;scenario.stale_reason=f"源观测已更新至 r{dataset.revision}，请确认新剖面后再运行"
