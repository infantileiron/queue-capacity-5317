from sqlalchemy import String,Float,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class CapacityReview(Base):
 __tablename__="capacity_reviews"
 id:Mapped[str]=mapped_column(String(80),primary_key=True)
 run_id:Mapped[str]=mapped_column(ForeignKey("simulation_runs.id"))
 note:Mapped[str]=mapped_column(Text)
 decision:Mapped[str]=mapped_column(String(30))
 author:Mapped[str]=mapped_column(String(160))
 created_at:Mapped[str]=mapped_column(String(64))
