DROP VIEW IF EXISTS systems;

CREATE VIEW systems AS
WITH agg AS (
    SELECT
        pl.hostname,
        COUNT(pl.pl_name)                           AS num_planets,
        MAX(pl.sy_pnum)                             AS sy_pnum,
        MAX(pl.sy_snum)                             AS sy_snum,
        MAX(pl.sy_dist)                             AS sy_dist,
        MAX(pl.st_teff)                             AS st_teff,
        MAX(pl.st_rad)                              AS st_rad,
        MAX(pl.st_mass)                             AS st_mass,
        MAX(pl.st_lum)                              AS st_lum,
        MAX(pl.st_spectype)                         AS st_spectype,
        MAX(pl.st_age)                              AS st_age,
        MAX(pl.st_met)                              AS st_metfe,
        MIN(pl.pl_orbper)                           AS min_orbper,
        MAX(pl.pl_orbper)                           AS max_orbper,
        MIN(hz.orbsmax_au)                          AS innermost_au,
        MAX(hz.orbsmax_au)                          AS outermost_au,
        SUM(
            CASE
                WHEN hz.in_hz_conservative = 1 THEN 1
                ELSE 0
            END
        )                                           AS n_in_hz_conservative,
        SUM(
            CASE
                WHEN hz.in_hz_optimistic = 1 THEN 1
                ELSE 0
            END
        )                                           AS n_in_hz_optimistic,
        SUM(
            CASE 
                WHEN hz.is_rocky_candidate = 1 THEN 1
                ELSE 0 
            END
        )                                           AS n_rocky_candidates,
        SUM(pl.pl_bmasse)                           AS total_detected_mass_earth,
        SUM(
            CASE
                WHEN pl.pl_bmasse IS NOT NULL THEN 1
                ELSE 0
            END
        )                                           AS n_planets_with_mass,
        MIN(pl.pl_rade)                             AS min_rade,
        MAX(pl.pl_rade)                             AS max_rade,
        MIN(pl.disc_year)                           AS first_discovery_year,
        MAX(pl.disc_year)                           AS last_discovery_year,
        GROUP_CONCAT(DISTINCT pl.discoverymethod)   AS discovery_methods
    FROM planets                AS pl
    LEFT JOIN habitable_zone    AS hz
        ON pl.pl_name = hz.pl_name
    GROUP BY pl.hostname
)
SELECT
    *,
    CASE WHEN sy_pnum > 1               THEN 1 ELSE 0 END AS is_multi_planet,
    CASE WHEN sy_snum > 1               THEN 1 ELSE 0 END AS is_multi_star,
    CASE WHEN innermost_au > 0          THEN outermost_au / innermost_au END AS orbital_span_ratio,
    CASE WHEN n_in_hz_conservative > 0  THEN 1 ELSE 0 END AS has_habitable_planet,
    CASE WHEN num_planets <> sy_pnum    THEN 1 ELSE 0 END AS pnum_disagrees
FROM agg;