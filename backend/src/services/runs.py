import uuid,redis
from fastapi import HTTPException
from src.models import SimulationRun,CapacityScenario,ServiceProfile
from src.config.settings import REDIS_URL
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,scenario_id):
 scenario=db.get(CapacityScenario,scenario_id)
 if not scenario:raise HTTPException(404,"方案不存在")
 if scenario.stale:raise HTTPException(409,"方案已失效："+(scenario.stale_reason or"源观测已更新，请先确认"))
 profile=db.get(ServiceProfile,scenario.profile_id)
 if profile and profile.stale:raise HTTPException(409,"关联剖面重算失败（"+profile.last_error+"），已保留上次可用结果，不可启动新预演")
 # 快照当时的剖面与方案参数：此后源数据再变，本次运行仍按提交时口径复现。
 snapshot={};dataset_revision=0;profile_checksum=""
 if profile:
  dataset_revision=profile.dataset_revision
  profile_checksum=profile.statistics.get("checksum","")
  snapshot={"profile":{"id":profile.id,"name":profile.name,"period":profile.period,"arrival_rate":profile.arrival_rate,"service_rate":profile.service_rate,"statistics":profile.statistics},"scenario":{"id":scenario.id,"name":scenario.name,"windows":scenario.windows,"arrival_multiplier":scenario.arrival_multiplier,"service_multiplier":scenario.service_multiplier,"duration_minutes":scenario.duration_minutes,"warmup_minutes":scenario.warmup_minutes,"replications":scenario.replications,"seed":scenario.seed}}
 item=SimulationRun(id=str(uuid.uuid4()),scenario_id=scenario_id,status="queued",result={},error="",dataset_revision=dataset_revision,profile_checksum=profile_checksum,snapshot=snapshot,created_at=now());db.add(item);db.commit()
 try:redis.Redis.from_url(REDIS_URL).lpush("queue-capacity:jobs",item.id)
 except redis.RedisError:
  item.status="failed";item.error="后台队列不可用，请重试";db.commit();raise HTTPException(503,item.error)
 return serialize(item)
def require_completed(db,id):
 item=db.get(SimulationRun,id)
 if not item:raise HTTPException(404,"运行不存在")
 if item.status!="completed":raise HTTPException(409,"运行尚未完成")
 return item
