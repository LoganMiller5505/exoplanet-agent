DROP VIEW IF EXISTS ps_default;
DROP VIEW IF EXISTS k2pandc;

CREATE VIEW ps_default AS
SELECT * FROM ps WHERE default_flag = 1;

CREATE VIEW k2pandc AS
SELECT * FROM ps WHERE default_flag = 1;