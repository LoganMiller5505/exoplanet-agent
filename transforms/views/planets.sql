DROP VIEW IF EXISTS planets;

CREATE VIEW planets AS
SELECT
    psd.*,
    psc.*
FROM ps_default AS psd
LEFT JOIN pscomppars AS psc ON psd.pl_name = psc.pl_name;