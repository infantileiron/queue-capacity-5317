import statistics,hashlib,json
def fit_profile(rows,period):
 sample=[r for r in rows if period=="all" or r["period"]==period]
 if len(sample)<20: raise ValueError("所选时段至少需要20条观测")
 arrivals=[r["interarrival_minutes"] for r in sample];services=[r["service_minutes"] for r in sample]
 a=statistics.mean(arrivals);s=statistics.mean(services)
 return {"arrival_rate":1/a,"service_rate":1/s,"statistics":{"n":len(sample),"mean_interarrival":a,"mean_service":s,"interarrival_cv":statistics.stdev(arrivals)/a,"service_cv":statistics.stdev(services)/s,"checksum":hashlib.sha256(json.dumps(sample,sort_keys=True).encode()).hexdigest()}}
