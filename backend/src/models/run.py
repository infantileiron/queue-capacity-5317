from sqlalchemy import String,Float,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class SimulationRun(Base):
 __tablename__="simulation_runs"
 id:Mapped[str]=mapped_column(String(80),primary_key=True)
 scenario_id:Mapped[str]=mapped_column(ForeignKey("capacity_scenarios.id"))
 status:Mapped[str]=mapped_column(String(30))
 result:Mapped[dict]=mapped_column(JSON,default=dict)
 error:Mapped[str]=mapped_column(Text,default="")
 dataset_revision:Mapped[int]=mapped_column(Integer,default=0)
 profile_checksum:Mapped[str]=mapped_column(String(80),default="")
 snapshot:Mapped[dict]=mapped_column(JSON,default=dict)
 created_at:Mapped[str]=mapped_column(String(64))
