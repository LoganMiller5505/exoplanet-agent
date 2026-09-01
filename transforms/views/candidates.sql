DROP VIEW IF EXISTS candidates;

CREATE VIEW candidates AS
SELECT
    toi.tid                 AS object_id,
    'TESS'                  AS survey,
    CASE
        WHEN toi.tfopwg_disp IN ('CP','KP')     THEN 'confirmed'
        WHEN toi.tfopwg_disp IN ('PC','APC')    THEN 'candidate'
        WHEN toi.tfopwg_disp IN ('FP','FA')     THEN 'false_positive'
        ELSE 'unknown'
    END                     AS status,
    toi.tfopwg_disp         AS status_raw,
    psd.pl_name             AS pl_name,
    toi.pl_orbper           AS period,
    toi.pl_rade             AS radius,
    toi.pl_eqt              AS equilibrium_temperature,
    toi.pl_insol            AS insolation,
    toi.pl_trandurh         AS duration,
<<<<<<< HEAD
    (toi.pl_trandep*100000) AS depth,
=======
    toi.pl_trandep          AS depth,
>>>>>>> origin/main
    toi.st_teff             AS stellar_temperature
FROM toi
LEFT JOIN ps_default as psd
    ON psd.tid_ic = 'TIC ' || toi.tid
    AND ABS(toi.pl_orbper - psd.pl_orbper) < 0.01 --Match on an individual planet level so stars with multiple planets don't get expanded

UNION ALL

SELECT
    kepid           AS object_id,
    'Kepler'        AS survey,
    CASE
        WHEN koi_disposition IN ('CONFIRMED')       THEN 'confirmed'
        WHEN koi_disposition IN ('CANDIDATE')       THEN 'candidate'
        WHEN koi_disposition IN ('FALSE POSITIVE')  THEN 'false_positive'
        ELSE 'unknown'
    END             AS status,
    koi_disposition AS status_raw,
    kepler_name     AS pl_name,
    koi_period      AS period,
    koi_prad        AS radius,
    koi_teq         AS equilibrium_temperature,
    koi_insol       AS insolation,
    koi_duration    AS duration,
    koi_depth       AS depth,
    koi_steff       AS stellar_temperature
FROM cumulative

UNION ALL

SELECT
    coalesce(epic_candname, pl_name)    AS object_id,
    'K2'                                AS survey,
    CASE
        WHEN disposition IN ('CONFIRMED')                   THEN 'confirmed'
        WHEN disposition IN ('CANDIDATE')                   THEN 'candidate'
        WHEN disposition IN ('FALSE POSITIVE','REFUTED')    THEN 'false_positive'
        ELSE 'unknown'
    END                                 AS status,
    disposition                         AS status_raw,
    pl_name                             AS pl_name,
    pl_orbper                           AS period,
    pl_rade                             AS radius,
    pl_eqt                              AS equilibrium_temperature,
    pl_insol                            AS insolation,
    pl_trandur                          AS duration, --Archive metadata labels this 'day', but the values are hours: 355 rows would otherwise transit for longer than their whole orbit
    (pl_trandep*10000)                  AS depth, --Source is percent; 1% = 10,000 ppm
    st_teff                             AS stellar_temperature
FROM k2pandc_default;