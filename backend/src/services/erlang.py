import math
def erlang_c(arrival_rate,service_rate,windows):
 if not math.isfinite(arrival_rate) or not math.isfinite(service_rate) or arrival_rate<=0 or service_rate<=0: raise ValueError("到达率与单窗口服务率必须为有限正数，单位均为每分钟")
 if not isinstance(windows,int) or windows<1: raise ValueError("窗口数须为正整数")
 offered=arrival_rate/service_rate;rho=offered/windows
 base={"arrival_rate":arrival_rate,"service_rate":service_rate,"windows":windows,"rho":rho,"stable":rho<1}
 if rho>=1:return {**base,"p_wait":None,"mean_wait_minutes":None,"mean_system_minutes":None,"mean_queue_length":None}
 # Erlang-B recursion avoids factorial/power overflow; C=B/(1-rho+rho*B).
 b=1.0
 for k in range(1,windows+1):b=offered*b/(k+offered*b)
 p_wait=b/(1-rho+rho*b)
 wq=p_wait/(windows*service_rate-arrival_rate)
 return {**base,"p_wait":p_wait,"mean_wait_minutes":wq,"mean_system_minutes":wq+1/service_rate,"mean_queue_length":arrival_rate*wq}
