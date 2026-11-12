from sqlalchemy import String,Float,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ServiceProfile(Base):
 __tablename__="service_profiles"
 id:Mapped[str]=mapped_column(String(80),primary_key=True)
 name:Mapped[str]=mapped_column(String(160),unique=True)
 dataset_id:Mapped[str]=mapped_column(ForeignKey("arrival_datasets.id"))
 period:Mapped[str]=mapped_column(String(30))
 arrival_rate:Mapped[float]=mapped_column(Float)
 service_rate:Mapped[float]=mapped_column(Float)
 statistics:Mapped[dict]=mapped_column(JSON)
 stale:Mapped[int]=mapped_column(Integer,default=0)
 last_error:Mapped[str]=mapped_column(Text,default="")
 dataset_revision:Mapped[int]=mapped_column(Integer,default=1)
 created_at:Mapped[str]=mapped_column(String(64))
