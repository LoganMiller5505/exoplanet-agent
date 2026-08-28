DROP VIEW IF EXISTS candidates;

CREATE VIEW candidates AS
SELECT
    tid         AS object_id,
    'TESS'      AS survey,
    CASE
        WHEN tfopwg_disp IN ('CP','KP')                 THEN 'confirmed'
        WHEN tfopwg_disp IN ('PC','APC')                THEN 'candidate'
        WHEN tfopwg_disp IN ('FP','FA')  THEN 'false_positive'
        ELSE 'unknown'
    END         AS status,
    tfopwg_disp AS status_raw,
    null        AS pl_name, -- Will rely on planet_names view to be fixed (blocked by REGEXP_REPLACE issue)
    pl_orbper   AS period,
    pl_rade     AS radius,
    pl_eqt      AS equilibrium_temperature,
    pl_insol    AS insolation,
    pl_trandurh AS duration,
    pl_trandep  AS depth,
    st_teff     AS stellar_temperature
FROM toi

UNION ALL

SELECT
    kepid           AS object_id,
    'Kepler'        AS survey,
    CASE
        WHEN koi_disposition IN ('CONFIRMED')                 THEN 'confirmed'
        WHEN koi_disposition IN ('CANDIDATE')                THEN 'candidate'
        WHEN koi_disposition IN ('FALSE POSITIVE')  THEN 'false_positive'
        ELSE 'unknown'
    END             AS status,
    koi_disposition AS status_raw,
    null            AS pl_name, -- Will rely on planet_names view to be fixed (blocked by REGEXP_REPLACE issue)
    null            AS period,
    null            AS radius,
    null            AS equilibrium_temperature,
    null            AS insolation,
    null            AS duration,
    null            AS depth,
    null            AS stellar_temperature
FROM cumulative

UNION ALL

SELECT
    null            AS object_id, -- May need to derive an object_id from pl_name or something else (probably using planet_names view)
    'K2'            AS survey,
    CASE
        WHEN disposition IN ('CONFIRMED')                 THEN 'confirmed'
        WHEN disposition IN ('CANDIDATE')                THEN 'candidate'
        WHEN disposition IN ('FALSE POSITIVE','REFUTED')  THEN 'false_positive'
        ELSE 'unknown'
    END             AS status,
    disposition     AS status_raw,
    pl_name         AS pl_name,
    pl_orbper       AS period,
    pl_rade         AS radius,
    pl_eqt          AS equilibrium_temperature,
    pl_insol        AS insolation,
    null            AS duration,    -- Does not have transit data (investigate join to get here)
    null            AS depth,       -- Does not have transit data (investigate join to get here)
    st_teff         AS stellar_temperature
FROM k2pandc_default;