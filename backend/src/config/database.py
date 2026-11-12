from sqlalchemy import create_engine,inspect,text
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from src.config.settings import DATABASE_URL
class Base(DeclarativeBase): pass
engine=create_engine(DATABASE_URL,pool_pre_ping=True)
Session=sessionmaker(bind=engine,expire_on_commit=False)
def db_session():
 with Session() as db: yield db
# 版本化新增列：首次部署由 create_all 一并建成；已有库由 ensure_schema 幂等补齐。
ADDED_COLUMNS={
 "arrival_datasets":{"revision":"INTEGER NOT NULL DEFAULT 1"},
 "service_profiles":{"stale":"INTEGER NOT NULL DEFAULT 0","last_error":"TEXT NULL","dataset_revision":"INTEGER NOT NULL DEFAULT 1"},
 "capacity_scenarios":{"stale":"INTEGER NOT NULL DEFAULT 0","stale_reason":"VARCHAR(200) NOT NULL DEFAULT ''"},
 "simulation_runs":{"dataset_revision":"INTEGER NOT NULL DEFAULT 0","profile_checksum":"VARCHAR(80) NOT NULL DEFAULT ''","snapshot":"JSON NULL"},
}
def ensure_schema():
 inspector=inspect(engine)
 if not inspector.has_table("arrival_datasets"):return
 with engine.begin() as conn:
  for table,columns in ADDED_COLUMNS.items():
   existing={c["name"] for c in inspector.get_columns(table)}
   for name,ddl in columns.items():
    if name not in existing:conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {name} {ddl}"))
