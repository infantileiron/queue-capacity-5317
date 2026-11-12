from sqlalchemy import String,Float,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class CapacityScenario(Base):
 __tablename__="capacity_scenarios"
 id:Mapped[str]=mapped_column(String(80),primary_key=True)
 name:Mapped[str]=mapped_column(String(160),unique=True)
 profile_id:Mapped[str]=mapped_column(ForeignKey("service_profiles.id"))
 windows:Mapped[int]=mapped_column(Integer)
 arrival_multiplier:Mapped[float]=mapped_column(Float)
 service_multiplier:Mapped[float]=mapped_column(Float)
 duration_minutes:Mapped[int]=mapped_column(Integer)
 warmup_minutes:Mapped[int]=mapped_column(Integer)
 replications:Mapped[int]=mapped_column(Integer)
 seed:Mapped[int]=mapped_column(Integer)
 stale:Mapped[int]=mapped_column(Integer,default=0)
 stale_reason:Mapped[str]=mapped_column(String(200),default="")
 created_at:Mapped[str]=mapped_column(String(64))
