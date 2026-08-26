DROP VIEW IF EXISTS habitable;

CREATE VIEW habitable AS
SELECT *
FROM ps_default
WHERE pl_eqt BETWEEN 200 AND 350 AND default_flag = 1;