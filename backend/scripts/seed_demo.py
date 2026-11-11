import random,json
from sqlalchemy import select,func
from src.config.database import Base,engine,Session
from src.models import User,ArrivalDataset,ServiceProfile,CapacityScenario,SimulationRun,CapacityReview,Report
from src.services.profiling import fit_profile
from src.services.analysis import analyze
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
  if not db.get(ArrivalDataset,"demo-data"):db.add(ArrivalDataset(id="demo-data",name="云岫收样·11月匿名时长观测",source="yunxiu_intake_202611.json",rows=rows,created_at=now()));db.flush()
  if not db.get(ServiceProfile,"demo-profile"):db.add(ServiceProfile(id="demo-profile",name="全日均值·单窗口服务剖面",dataset_id="demo-data",period="all",created_at=now(),**fit_profile(rows,"all")));db.flush()
  for c in (2,3,4):
   id=f"demo-scenario-{c}"
   if not db.get(CapacityScenario,id):db.add(CapacityScenario(id=id,name=f"{c}窗口·全日容量预演",profile_id="demo-profile",windows=c,arrival_multiplier=1,service_multiplier=1,duration_minutes=480,warmup_minutes=120,replications=30,seed=2206,created_at=now()))
  db.flush()
  if not db.get(SimulationRun,"demo-run"):
   db.add(SimulationRun(id="demo-run",scenario_id="demo-scenario-3",status="completed",result=analyze(db.get(ServiceProfile,"demo-profile"),db.get(CapacityScenario,"demo-scenario-3")),error="",created_at=now()));db.flush()
  if not db.get(CapacityReview,"demo-review"):db.add(CapacityReview(id="demo-review",run_id="demo-run",note="全日均值不能代替高峰到达率；已记录指数独立假设与输入估计误差，建议另行复核高峰时段。",decision="accepted",author="analyst@yunxiu.demo",created_at=now()));db.flush()
  if not db.get(Report,"demo-report"):db.add(Report(id="demo-report",run_id="demo-run",title="收样窗口·全日容量复核",published_by="admin@yunxiu.demo",created_at=now()))
  db.commit()
  return {m.__tablename__:db.scalar(select(func.count()).select_from(m)) for m in (User,ArrivalDataset,ServiceProfile,CapacityScenario,SimulationRun,CapacityReview,Report)}
if __name__=="__main__":print(json.dumps(seed(),ensure_ascii=False))
