import uuid,hashlib,json
from fastapi import HTTPException
from sqlalchemy import select
from src.models import ArrivalDataset,DatasetRevision
from src.utils.time import now
from src.utils.serialization import serialize,rows
def rows_checksum(data):return hashlib.sha256(json.dumps(data,sort_keys=True).encode()).hexdigest()
def create(db,payload,user):
 if db.scalar(select(ArrivalDataset).where(ArrivalDataset.name==payload.name)):raise HTTPException(409,"样本名称已存在")
 data=[r.model_dump() for r in payload.rows]
 item=ArrivalDataset(id=str(uuid.uuid4()),name=payload.name,source=payload.source,rows=data,revision=1,created_at=now())
 db.add(item);db.flush()
 db.add(DatasetRevision(id=str(uuid.uuid4()),dataset_id=item.id,revision=1,added=len(data),corrected=0,withdrawn=0,checksum=rows_checksum(data),actor=user["email"],created_at=now()))
 db.commit();return serialize(item)
def require(db,id):
 item=db.get(ArrivalDataset,id)
 if not item:raise HTTPException(404,"样本不存在")
 return item
def update_observations(db,id,payload,user):
 # 整批校验通过后一次性生效；任一条出错抛异常，事务不提交，整批不生效。
 dataset=require(db,id)
 current={r["sample_id"]:dict(r) for r in dataset.rows}
 added=corrected=withdrawn=0
 for change in payload.changes:
  if change.action=="withdraw":
   if change.sample_id not in current:raise HTTPException(422,f"样本编号 {change.sample_id} 不存在，无法撤回；整批未生效")
   del current[change.sample_id];withdrawn+=1
  else:
   row={"sample_id":change.sample_id,"period":change.period,"interarrival_minutes":change.interarrival_minutes,"service_minutes":change.service_minutes}
   if change.sample_id in current:corrected+=1
   else:added+=1
   current[change.sample_id]=row
 if len(current)<20:raise HTTPException(422,"更新后观测不足20条，整批未生效")
 data=list(current.values())
 dataset.rows=data
 dataset.revision+=1
 db.add(DatasetRevision(id=str(uuid.uuid4()),dataset_id=dataset.id,revision=dataset.revision,added=added,corrected=corrected,withdrawn=withdrawn,checksum=rows_checksum(data),actor=user["email"],created_at=now()))
 from src.services.profiles import recompute
 recompute(db,dataset)
 db.commit();return serialize(dataset)
def revisions(db,id):
 require(db,id)
 return rows(db.scalars(select(DatasetRevision).where(DatasetRevision.dataset_id==id).order_by(DatasetRevision.revision.desc())))
