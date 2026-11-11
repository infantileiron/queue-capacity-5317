from sqlalchemy import String,Float,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ArrivalDataset(Base):
 __tablename__="arrival_datasets"
 id:Mapped[str]=mapped_column(String(80),primary_key=True)
 name:Mapped[str]=mapped_column(String(160),unique=True)
 source:Mapped[str]=mapped_column(String(160))
 rows:Mapped[list]=mapped_column(JSON)
 created_at:Mapped[str]=mapped_column(String(64))
