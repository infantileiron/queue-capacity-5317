# 云岫实验室 · 收样窗口容量预演

面向云岫检测中心20人收样组的容量讨论工作台：从到达间隔与单次服务时长估计输入率，使用Erlang-C解析与离散事件仿真比较窗口数、等待及忙碌比例，再由人员复核归档。全量资料为模拟匿名样本，不连接真实检测业务。

## 场景与一天的剧本

团队原来用Excel统计日均到达量，再凭经验增开窗口，存在高峰等待不可量化、利用率与等待混淆、方案不确定性缺失三项痛点。上游为收样窗口匿名计时记录；本项目替代样本口径核查、容量预演与报告复核；下游由收样组讨论人员配置，不自动生成排班或接收真实样本。

09:00分析员登录；09:03核查 yunxiu_intake_202611.json 的480条匿名观测和peak/offpeak时段；09:08选择全日或高峰，估计每分钟到达率λ与单窗口服务率μ；09:12保存3窗口、480分钟观测、120分钟预热、30次重复、seed2206的方案；09:15后台worker执行；09:18比较2/3/4窗口稳态条件与等待；09:20核对重复试验区间及服务时间轴；09:25记录高峰与指数假设的局限；09:28管理员批准归档；09:30只读账号下载30行重复试验CSV。

|角色|主要页面|权限与典型动作|
|---|---|---|
|admin|全部页面|创建实体与运行、人工复核、批准归档|
|analyst|收样观测、服务剖面、窗口方案、结果、复核|导入匿名观测、估计输入率、后台仿真、提交意见；无批准权|
|viewer|全部只读与归档下载|核对结果和CSV；写操作后端403|

## 快速启动

```sh
cp .env.example .env
docker compose up -d --build --wait
docker compose exec -T backend python -m scripts.seed_demo
```

前端 http://localhost:18215 ，后端文档 http://localhost:19215/docs ，MySQL映射17715。三个账号为admin@yunxiu.demo、analyst@yunxiu.demo、viewer@yunxiu.demo；演示密码均为 `Queue2026!`。JWT_SECRET为演示开发密钥，实际部署自行替换。

恰好frontend/backend/worker/db/redis五服务，全部healthcheck。backend依赖MySQL和Redis健康，worker额外等待backend完成种子启动，frontend等待backend健康。数据库、Redis AOF与worker产物为三个命名卷。结束演示：`docker compose down -v --remove-orphans`；此操作清除本项目演示数据。

## 核心实体与数据

ArrivalDataset保存匿名sample_id、时段、到达间隔和服务时长；ServiceProfile保存所选时段的均值、CV、λ/μ与校验码；CapacityScenario保存窗口数、率倍率、时域、预热、重复数与seed；SimulationRun保存真实队列状态及结果；CapacityReview保存人工意见；Report仅在最新人工意见接受后由管理员归档。报告按run唯一；源样本ID唯一，分数/个人身份等信息不被采集。

SEED_DEMO=true启动建表并幂等填充，固定自然键/种子ID，不重复插入也不覆盖用户修改。480条观测由seed2206生成，高峰/平峰采用不同到达间隔均值，单次服务均值12分钟；种子包含2/3/4窗口三方案和真实计算的3窗口结果及归档。所有输入仅为模拟；实际模型输入必须来自经过核查的时段样本。

## 两类算法

1. Erlang-C M/M/c。统一用分钟：λ=1/平均到达间隔，μ=1/平均单次服务时长，c为窗口数，ρ=λ/(cμ)。当ρ≥1明确返回stable=false，等待概率、Wq、系统时长、队长均为null，没有有限稳态值。稳定时用Erlang-B递推 `B0=1; Bk=a*B(k-1)/(k+a*B(k-1))`，a=λ/μ，再得 `C=Bc/(1-rho+rho*Bc)`、`Wq=C/(c*mu-lambda)`、`Lq=lambda*Wq`、`W=Wq+1/mu`。稳态要求泊松到达、独立指数服务、同质窗口、无限等候空间和先到先服务。
2. 离散事件仿真。固定seed+重复序号生成指数到达间隔与服务时长；最小堆选择最早空闲窗口，服务开始=max(到达,窗口空闲)，等待=开始-到达。从空系统开始，先运行warmup，再统计观测时域内的到达；这些任务服务可以延续至观测结束后。窗口忙碌比例按所有服务区间与观测期的交集积分，分母为c×观测分钟，不把提供负荷误作忙碌比例。多次重复报告均值、等待概率与 `mean ± 1.96*sd(rep_means)/sqrt(R)` 正态近似区间。最后一次重复保留前80个事件，UI绘制前35个真实服务事件。

复现：相同观测JSON校验码、剖面时段、窗口数、倍率、时域、warmup、重复数与seed产生相同结果。输入有限正时长、至少20条最多5000条；窗口1—12、重复5—100、观测60—1440分钟、预热0—1440分钟，率倍率0.2—3。预期事件超过20000拒绝，实际单次超过50000事件拒绝，避免过大请求。

失败态：所选时段不足20条、样本编号重复、时长非正/非有限、无到达事件、队列不可用或无效窗口均有服务端错误；运行失败保留error并可新建运行重试。ρ≥1属于可计算的过载场景，解析值无稳态，有限期仿真继续并明确标识暂态。

## 界面与工程

六业务页：容量总览、收样观测、服务剖面、窗口方案、等待与负荷、复核归档（含操作留痕）；另有登录页。黛绿实验室板书视觉，双字体Noto Sans SC / ZCOOL XiaoWei，oklch色板与有实际数据的窗口对照、重复图、服务时间轴。Google Fonts不可访问时回退浏览器衬线/无衬线，功能保持可用。

|部分|技术|
|---|---|
|前端|Vue3.5、TypeScript5.7、Vite6、Nginx1.28|
|后端|Python3.11、FastAPI、SQLAlchemy、PyJWT|
|持久化|MySQL8.4，JSON列保存样本和计算结果|
|后台|Redis7.4持久化队列，独立Python worker与心跳|

目录frontend/src包含api/stores/types/components/common/hooks/pages/router/utils/constants；backend/src包含routes/controllers/services/models/schemas/middlewares/utils/constants/config；backend/scripts含seed，backend/migrations说明初次建表方式。测试、日志、截图及报告在批次test-artifacts/gb-2206，未混入源码。

本地开发：在backend安装requirements.txt，配置DATABASE_URL、REDIS_URL、JWT_SECRET后执行`uvicorn src.main:app --reload`，另开`python -m src.worker`；frontend执行`npm install && npm run dev`，Vite已将/api代理到本机19215并去除前缀。Docker由Nginx执行同样代理。

环境：COMPOSE_PROJECT_NAME=queue-capacity、FRONTEND_PORT=18215、BACKEND_PORT=19215、DB_PORT=17715、JWT_SECRET、SEED_DEMO；DATABASE_URL和REDIS_URL在Compose服务中配置。`.env`忽略，`.env.example`供复制。

共享枚举：Role与RunStatus、Period在backend/src/constants/enums.py；对应前端ROLES/RUN_STATUS/PERIODS在frontend/src/constants/enums.ts，权限消费位于controllers/auth.py、App.vue；状态变更位于services/runs.py和worker.py，Status.vue展示；period验证在schemas/profile.py、schemas/dataset.py，Profiles.vue与Datasets.vue消费。复核decision在schemas/review.py和frontend/constants/enums.ts，Reviews.vue使用。

## 适用边界

全日混合高峰和平峰不能保证泊松稳态。CV只描述变异程度，不是指数分布或独立性检验；warmup缓解空初态，不保证收敛。95%区间只反映固定模型的重复试验误差，不含输入估计误差。ρ≥1的有限期等待有暂态数值，但不能用该数值论证长期稳定。单worker演示队列支持启动时恢复queued/running任务，未实现分布式租约或多worker去重。初次数据库由SQLAlchemy建表，未提供生产迁移回滚。数据页预览40条，计算使用所选时段全量。

MIT License。
