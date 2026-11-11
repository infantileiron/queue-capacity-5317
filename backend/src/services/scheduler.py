import heapq,math
def schedule(arrivals,services,windows):
 if len(arrivals)!=len(services) or windows<1: raise ValueError("到达与服务长度须一致，窗口数须为正")
 if any(not math.isfinite(x) or x<0 for x in arrivals) or any(not math.isfinite(x) or x<=0 for x in services): raise ValueError("到达须有限非负、服务须有限正数")
 if any(a>b for a,b in zip(arrivals,arrivals[1:])): raise ValueError("到达时间须递增")
 servers=[(0.0,i+1) for i in range(windows)];heapq.heapify(servers);events=[]
 for i,(arrival,service) in enumerate(zip(arrivals,services)):
  free,server=heapq.heappop(servers);start=max(arrival,free);end=start+service
  events.append({"job":i+1,"arrival":arrival,"service":service,"start":start,"end":end,"wait":start-arrival,"server":server})
  heapq.heappush(servers,(end,server))
 return events
