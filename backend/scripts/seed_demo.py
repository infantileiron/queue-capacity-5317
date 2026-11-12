import random,json
from sqlalchemy import select,func
from src.config.database import Base,engine,Session
from src.models import User,ArrivalDataset,DatasetRevision,ServiceProfile,CapacityScenario,SimulationRun,CapacityReview,Report
from src.services.profiling import fit_profile
from src.services.analysis import analyze
from src.services.datasets import rows_checksum
from src.utils.time import now
from src.utils.security import hash_password
def seed():
 Base.metadata.create_all(engine)
 with Session() as db:
  for role in ("admin","analyst","viewer"):
   if not db.get(User,role):db.add(User(id=role,email=role+"@yunxiu.demo",password=hash_password("Queue2026!"),role=role))
  rng=random.Random(2206);rows=[]
  for i in range(480):
   peak=i%120<50
   rows.append({"sample_id":f"YX-{i+1:04}","period":"peak" if peak else "offpeak","interarrival_minutes":round(max(.05,rng.expovariate(1/(3.5 if peak else 7.2))),3),"service_minutes":round(max(.1,rng.expovariate(1/12)),3)})
  if not db.get(ArrivalDataset,"demo-data"):
   db.add(ArrivalDataset(id="demo-data",name="云岫收样·11月匿名时长观测",source="yunxiu_intake_202611.json",rows=rows,revision=1,created_at=now()));db.flush()
  if not db.get(DatasetRevision,"demo-revision-1"):
   db.add(DatasetRevision(id="demo-revision-1",dataset_id="demo-data",revision=1,added=len(rows),corrected=0,withdrawn=0,checksum=rows_checksum(rows),actor="seed",created_at=now()));db.flush()
  if not db.get(ServiceProfile,"demo-profile"):db.add(ServiceProfile(id="demo-profile",name="全日均值·单窗口服务剖面",dataset_id="demo-data",period="all",stale=0,last_error="",dataset_revision=1,created_at=now(),**fit_profile(rows,"all")));db.flush()
  for c in (2,3,4):
   id=f"demo-scenario-{c}"
   if not db.get(CapacityScenario,id):db.add(CapacityScenario(id=id,name=f"{c}窗口·全日容量预演",profile_id="demo-profile",windows=c,arrival_multiplier=1,service_multiplier=1,duration_minutes=480,warmup_minutes=120,replications=30,seed=2206,stale=0,stale_reason="",created_at=now()))
  db.flush()
  if not db.get(SimulationRun,"demo-run"):
   profile=db.get(ServiceProfile,"demo-profile");scenario=db.get(CapacityScenario,"demo-scenario-3")
   snapshot={"profile":{"id":profile.id,"name":profile.name,"period":profile.period,"arrival_rate":profile.arrival_rate,"service_rate":profile.service_rate,"statistics":profile.statistics},"scenario":{"id":scenario.id,"name":scenario.name,"windows":scenario.windows,"arrival_multiplier":scenario.arrival_multiplier,"service_multiplier":scenario.service_multiplier,"duration_minutes":scenario.duration_minutes,"warmup_minutes":scenario.warmup_minutes,"replications":scenario.replications,"seed":scenario.seed}}
   db.add(SimulationRun(id="demo-run",scenario_id="demo-scenario-3",status="completed",result=analyze(profile,scenario),error="",dataset_revision=1,profile_checksum=profile.statistics["checksum"],snapshot=snapshot,created_at=now()));db.flush()
  if not db.get(CapacityReview,"demo-review"):db.add(CapacityReview(id="demo-review",run_id="demo-run",note="全日均值不能代替高峰到达率；已记录指数独立假设与输入估计误差，建议另行复核高峰时段。",decision="accepted",author="analyst@yunxiu.demo",created_at=now()));db.flush()
  if not db.get(Report,"demo-report"):db.add(Report(id="demo-report",run_id="demo-run",title="收样窗口·全日容量复核",published_by="admin@yunxiu.demo",created_at=now()))
  db.commit()
  return {m.__tablename__:db.scalar(select(func.count()).select_from(m)) for m in (User,ArrivalDataset,DatasetRevision,ServiceProfile,CapacityScenario,SimulationRun,CapacityReview,Report)}
if __name__=="__main__":print(json.dumps(seed(),ensure_ascii=False))
