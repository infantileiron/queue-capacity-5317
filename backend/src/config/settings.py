import os
DATABASE_URL=os.getenv("DATABASE_URL","mysql+pymysql://queue:queue-demo@db/queue?charset=utf8mb4")
REDIS_URL=os.getenv("REDIS_URL","redis://redis:6379/0")
JWT_SECRET=os.getenv("JWT_SECRET","queue-development-secret-replace-32chars")
SEED_DEMO=os.getenv("SEED_DEMO","true").lower()=="true"
