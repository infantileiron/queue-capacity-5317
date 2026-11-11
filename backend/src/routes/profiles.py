from fastapi import APIRouter,Depends
from sqlalchemy import select
from src.config.database import db_session
from src.controllers.auth import current_user,writer,admin
from src.models import ServiceProfile
from src.schemas.profile import ProfileInput
from src.services import profiles as service
from src.utils.serialization import rows
router=APIRouter(prefix="/profiles")
@router.get("")
def listing(db=Depends(db_session),user=Depends(current_user)):return rows(db.scalars(select(ServiceProfile).order_by(ServiceProfile.created_at.desc())))
@router.post("")
def create(payload:ProfileInput,db=Depends(db_session),user=Depends(writer)):return service.create(db,payload)
