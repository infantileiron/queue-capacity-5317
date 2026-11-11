from pathlib import Path
import traceback,redis
from sqlalchemy import select
from src.config.settings import REDIS_URL
from src.config.database import Session
from src.models import SimulationRun,CapacityScenario,ServiceProfile
from src.services.analysis import analyze
client=redis.Redis.from_url(REDIS_URL)
heartbeat=Path("/artifacts/worker-heartbeat")
def execute(id):
 with Session() as db:
  run=db.get(SimulationRun,id)
  if not run or run.status not in ("queued","running"):return
  run.status="running";db.commit()
  try:
   scenario=db.get(CapacityScenario,run.scenario_id);profile=db.get(ServiceProfile,scenario.profile_id)
   run.result=analyze(profile,scenario);run.status="completed"
  except Exception as error:run.error=str(error);run.status="failed";traceback.print_exc()
  db.commit()
with Session() as db:
 for id in db.scalars(select(SimulationRun.id).where(SimulationRun.status.in_(["queued","running"]))):client.lpush("queue-capacity:jobs",id)
while True:
 heartbeat.touch();job=client.brpop("queue-capacity:jobs",timeout=1)
 if job:execute(job[1].decode())
