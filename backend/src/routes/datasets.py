from fastapi import APIRouter,Depends
from sqlalchemy import select
from src.config.database import db_session
from src.controllers.auth import current_user,writer,admin
from src.models import ArrivalDataset
from src.schemas.dataset import DatasetInput,ObservationBatch
from src.services import datasets as service
from src.utils.serialization import rows
router=APIRouter(prefix="/datasets")
@router.get("")
def listing(db=Depends(db_session),user=Depends(current_user)):return rows(db.scalars(select(ArrivalDataset).order_by(ArrivalDataset.created_at.desc())))
@router.post("")
def create(payload:DatasetInput,db=Depends(db_session),user=Depends(writer)):return service.create(db,payload,user)
@router.post("/{id}/observations")
def update_observations(id:str,payload:ObservationBatch,db=Depends(db_session),user=Depends(writer)):return service.update_observations(db,id,payload,user)
@router.get("/{id}/revisions")
def revisions(id:str,db=Depends(db_session),user=Depends(current_user)):return service.revisions(db,id)
