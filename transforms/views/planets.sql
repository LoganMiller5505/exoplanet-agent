DROP VIEW IF EXISTS planets;

CREATE VIEW planets AS
SELECT
    psd.*,
    psc.pl_tsm,
    psc.pl_esm,
    psc.pl_angsep,
    psc.pl_nobs_jwst_tran,
    psc.pl_nobs_jwst_e,
    psc.pl_nobs_jwst_pc,
    psc.pl_nobs_jwst_di
FROM ps_default AS psd
LEFT JOIN pscomppars AS psc ON psd.pl_name = psc.pl_name;