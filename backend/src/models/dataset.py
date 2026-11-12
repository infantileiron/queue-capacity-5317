from sqlalchemy import String,Float,Integer,JSON,ForeignKey,Text
from sqlalchemy.orm import Mapped,mapped_column
from src.config.database import Base
class ArrivalDataset(Base):
 __tablename__="arrival_datasets"
 id:Mapped[str]=mapped_column(String(80),primary_key=True)
 name:Mapped[str]=mapped_column(String(160),unique=True)
 source:Mapped[str]=mapped_column(String(160))
 rows:Mapped[list]=mapped_column(JSON)
 revision:Mapped[int]=mapped_column(Integer,default=1)
 created_at:Mapped[str]=mapped_column(String(64))
class DatasetRevision(Base):
 __tablename__="dataset_revisions"
 id:Mapped[str]=mapped_column(String(80),primary_key=True)
 dataset_id:Mapped[str]=mapped_column(ForeignKey("arrival_datasets.id"))
 revision:Mapped[int]=mapped_column(Integer)
 added:Mapped[int]=mapped_column(Integer,default=0)
 corrected:Mapped[int]=mapped_column(Integer,default=0)
 withdrawn:Mapped[int]=mapped_column(Integer,default=0)
 checksum:Mapped[str]=mapped_column(String(80))
 actor:Mapped[str]=mapped_column(String(160))
 created_at:Mapped[str]=mapped_column(String(64))
