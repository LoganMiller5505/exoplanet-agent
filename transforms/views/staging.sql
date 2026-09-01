DROP VIEW IF EXISTS stg_ps CASCADE;
DROP VIEW IF EXISTS stg_k2pandc CASCADE;

CREATE VIEW stg_ps AS
SELECT * FROM src_ps WHERE default_flag = 1;

CREATE VIEW stg_k2pandc AS
SELECT * FROM src_k2pandc WHERE default_flag = 1;