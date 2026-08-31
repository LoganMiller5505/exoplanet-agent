DROP VIEW IF EXISTS planet_classes;

CREATE VIEW planet_classes AS
SELECT
    pl_name,
    hostname,
    pl_rade,
    pl_bmasse,
    pl_orbper,
    CASE
        WHEN pl_rade < 1.25                     THEN 'terrestrial'
        WHEN pl_rade >= 1.25 AND pl_rade < 2.0  THEN 'super_earth'
        WHEN pl_rade >= 2.0  AND pl_rade < 4.0  THEN 'mini_neptune'
        WHEN pl_rade >= 4.0  AND pl_rade < 10.0 THEN 'neptune_like'
        WHEN pl_rade >= 10.0                    THEN 'gas_giant'
        ELSE NULL
    END AS size_class,
    CASE
        WHEN pl_rade >= 1.5 AND pl_rade < 2.0  THEN 1
        WHEN pl_rade IS NOT NULL                THEN 0
        ELSE NULL
    END AS in_radius_valley,
    CASE
        WHEN pl_bmasse < 2.0                            THEN 'earth_mass'
        WHEN pl_bmasse >= 2.0   AND pl_bmasse < 10.0    THEN 'super_earth_mass'
        WHEN pl_bmasse >= 10.0  AND pl_bmasse < 50.0    THEN 'neptune_mass'
        WHEN pl_bmasse >= 50.0  AND pl_bmasse < 500.0   THEN 'jupiter_mass'
        WHEN pl_bmasse >= 500.0                         THEN 'super_jupiter'
        ELSE NULL
    END AS mass_class,
    CASE
        WHEN pl_bmasse IS NULL                          THEN NULL
        WHEN pl_bmassprov IN ('Msini','Msin(i)/sin(i)') THEN 1
        ELSE 0
    END AS mass_is_lower_bound,
    CASE
        WHEN pl_orbper IS NULL                  THEN NULL
        WHEN pl_orbper < 1                      THEN 'ultra_short_period'
        WHEN pl_rade > 8    AND pl_orbper < 10  THEN 'hot_jupiter'
        WHEN pl_rade > 8    AND pl_orbper < 100 THEN 'warm_giant'
        WHEN pl_rade > 8                        THEN 'cold_giant'
        WHEN pl_orbper < 10                     THEN 'hot_small'
        ELSE 'other'
    END AS orbital_class,
    CASE
        WHEN st_teff IS NULL   THEN NULL
        WHEN st_teff >= 30000  THEN 'O'
        WHEN st_teff >= 10000  THEN 'B'
        WHEN st_teff >= 7500   THEN 'A'
        WHEN st_teff >= 6000   THEN 'F'
        WHEN st_teff >= 5200   THEN 'G'
        WHEN st_teff >= 3700   THEN 'K'
        WHEN st_teff >= 2400   THEN 'M'
        ELSE 'L/T/Y'
    END AS spectral_class,
    CASE
        WHEN pl_rade IS NULL and pl_bmasse IS NULL THEN NULL
        WHEN pl_rade > 8 OR pl_bmasse > 50 THEN 1
        ELSE 0
    END AS is_giant
FROM planets;