import random,statistics,math
from src.services.scheduler import schedule
def simulate(arrival_rate,service_rate,windows,duration,warmup,replications,seed):
 if arrival_rate<=0 or service_rate<=0 or windows<1 or duration<=0 or warmup<0 or replications<2:raise ValueError("无效仿真参数")
 if arrival_rate*(duration+warmup)>20000:raise ValueError("预期到达超过20000条，请缩短时域或降低负荷")
 results=[];last_events=[];end=warmup+duration
 for rep in range(replications):
  rng=random.Random(seed+rep);arrivals=[];services=[];t=0
  while True:
   t+=rng.expovariate(arrival_rate)
   if t>=end:break
   arrivals.append(t);services.append(rng.expovariate(service_rate))
   if len(arrivals)>50000:raise ValueError("单次仿真事件超过50000条")
  events=schedule(arrivals,services,windows);observed=[e for e in events if e["arrival"]>=warmup]
  if not observed:raise ValueError("观测时域没有到达，请增大时域")
  waits=[e["wait"] for e in observed]
  busy=sum(max(0,min(e["end"],end)-max(e["start"],warmup)) for e in events)
  results.append({"replication":rep+1,"arrivals":len(observed),"mean_wait_minutes":statistics.mean(waits),"p_wait":sum(x>1e-9 for x in waits)/len(waits),"max_wait_minutes":max(waits),"busy_fraction":busy/(windows*duration)})
  last_events=observed[:80]
 means=[r["mean_wait_minutes"] for r in results];mean=statistics.mean(means);se=statistics.stdev(means)/math.sqrt(replications)
 return {"mean_wait_minutes":mean,"mean_wait_ci95":[max(0,mean-1.96*se),mean+1.96*se],"p_wait":statistics.mean(r["p_wait"] for r in results),"busy_fraction":statistics.mean(r["busy_fraction"] for r in results),"replications":results,"timeline":last_events,"duration_minutes":duration,"warmup_minutes":warmup,"seed":seed,"ci_method":"重复试验均值的正态近似95%区间（1.96×重复均值标准误）"}
