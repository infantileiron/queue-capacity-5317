-- 002-versioning: 观测版本化、失效传播与运行快照。
-- backend 启动时由 src/config/database.py 的 ensure_schema 幂等执行等价 ALTER；
-- 本文件供人工审阅，dataset_revisions 新表由 SQLAlchemy create_all 建立。
ALTER TABLE arrival_datasets ADD COLUMN revision INTEGER NOT NULL DEFAULT 1;
ALTER TABLE service_profiles
  ADD COLUMN stale INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN last_error TEXT NULL,
  ADD COLUMN dataset_revision INTEGER NOT NULL DEFAULT 1;
ALTER TABLE capacity_scenarios
  ADD COLUMN stale INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN stale_reason VARCHAR(200) NOT NULL DEFAULT '';
ALTER TABLE simulation_runs
  ADD COLUMN dataset_revision INTEGER NOT NULL DEFAULT 0,
  ADD COLUMN profile_checksum VARCHAR(80) NOT NULL DEFAULT '',
  ADD COLUMN snapshot JSON NULL;
