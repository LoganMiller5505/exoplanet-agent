-- NOTE: This view was generated with Claude Opus 5 to ensure accurate domain logic on what is considered the habitable zone for exoplanets.

-- habitable_zone: per-planet habitable zone analysis.
--
-- Replaces the old `habitable` view, which filtered on pl_eqt BETWEEN 200 AND 350.
-- That column is NULL for ~72% of planets, so the old view silently dropped most
-- real candidates rather than excluding them on the merits.
--
-- Boundaries follow Kopparapu et al. (2013), ApJ 765, 131 -- coefficients from the
-- 2014 erratum, for a 1 M(Earth) planet. The polynomial is only valid for host stars
-- with 2600 K <= st_teff <= 7200 K; outside that range every boundary column is NULL,
-- teff_in_valid_range = 0, and the in_hz_* flags are NULL rather than 0. This affects
-- real targets -- TRAPPIST-1 is 2566 K, just under the floor -- so callers must treat
-- NULL as "not evaluated", not as "no". The polynomial is not extrapolated past its
-- published range.
--
--   S_eff = S_eff_sun + a*T + b*T^2 + c*T^3 + d*T^4        where T = st_teff - 5780
--   distance_au = sqrt(L_star / S_eff)
--
--                        S_eff_sun        a            b            c             d
--   Recent Venus          1.7763    1.4335e-4    3.3954e-9   -7.6364e-12   -1.1950e-15
--   Runaway Greenhouse    1.0385    1.2456e-4    1.4612e-8   -7.6345e-12   -1.7511e-15
--   Maximum Greenhouse    0.3507    5.9578e-5    1.6707e-9   -3.0058e-12   -5.1925e-16
--   Early Mars            0.3207    5.4471e-5    1.5275e-9   -2.1709e-12   -3.8282e-16
--
-- This view does NOT filter to habitable planets. It returns every planet whose
-- boundaries are computable, with flags describing where it falls. Filter with
-- `WHERE in_hz_conservative = 1` at the call site.

DROP VIEW IF EXISTS habitable_zone;

CREATE VIEW habitable_zone AS
WITH resolved AS (
    -- Resolve stellar luminosity and semi-major axis, each with a fallback.
    -- The *_source columns let callers say "derived" rather than quoting an
    -- estimate as if it were a catalog measurement.
    SELECT
        pl_name,
        hostname,
        pl_letter,
        discoverymethod,
        disc_year,
        sy_dist,
        pl_rade,
        pl_bmasse,
        pl_eqt,
        pl_insol,
        pl_orbper,
        pl_orbeccen,
        pl_controv_flag,
        st_spectype,
        st_teff,
        st_rad,
        st_mass,
        st_lum,
        pl_tsm,
        pl_esm,

        -- Luminosity in solar units. st_lum is stored as log10(L/Lsun), NOT linear.
        -- Fallback is Stefan-Boltzmann: L/Lsun = (R/Rsun)^2 * (T/Tsun)^4, Tsun = 5772 K.
        CASE
            WHEN st_lum IS NOT NULL
                THEN pow(10.0, st_lum)
            WHEN st_rad IS NOT NULL AND st_teff IS NOT NULL
                THEN st_rad * st_rad * pow(st_teff / 5772.0, 4.0)
        END AS lum_solar,
        CASE
            WHEN st_lum IS NOT NULL THEN 'measured'
            WHEN st_rad IS NOT NULL AND st_teff IS NOT NULL THEN 'derived'
        END AS lum_source,

        -- Semi-major axis in AU. Fallback is Kepler's third law:
        -- a^3 = M_star * P^2, with P in years and M_star in solar masses.
        CASE
            WHEN pl_orbsmax IS NOT NULL
                THEN pl_orbsmax
            WHEN pl_orbper IS NOT NULL AND st_mass IS NOT NULL AND st_mass > 0
                THEN pow(st_mass * pow(pl_orbper / 365.25, 2.0), 1.0 / 3.0)
        END AS orbsmax_au,
        CASE
            WHEN pl_orbsmax IS NOT NULL THEN 'measured'
            WHEN pl_orbper IS NOT NULL AND st_mass IS NOT NULL AND st_mass > 0 THEN 'derived'
        END AS orbsmax_source
    FROM planets
),
tshift AS (
    -- T = st_teff - 5780, guarded to the polynomial's valid range.
    SELECT
        resolved.*,
        CASE
            WHEN st_teff BETWEEN 2600.0 AND 7200.0 THEN st_teff - 5780.0
        END AS ts
    FROM resolved
),
seff AS (
    -- Effective stellar flux at each boundary.
    SELECT
        tshift.*,
        1.7763 + 1.4335e-4 * ts + 3.3954e-9 * ts * ts
               + -7.6364e-12 * ts * ts * ts + -1.1950e-15 * ts * ts * ts * ts
            AS seff_recent_venus,
        1.0385 + 1.2456e-4 * ts + 1.4612e-8 * ts * ts
               + -7.6345e-12 * ts * ts * ts + -1.7511e-15 * ts * ts * ts * ts
            AS seff_runaway_greenhouse,
        0.3507 + 5.9578e-5 * ts + 1.6707e-9 * ts * ts
               + -3.0058e-12 * ts * ts * ts + -5.1925e-16 * ts * ts * ts * ts
            AS seff_maximum_greenhouse,
        0.3207 + 5.4471e-5 * ts + 1.5275e-9 * ts * ts
               + -2.1709e-12 * ts * ts * ts + -3.8282e-16 * ts * ts * ts * ts
            AS seff_early_mars
    FROM tshift
),
bounds AS (
    -- Convert each flux boundary to an orbital distance in AU.
    -- Inner boundaries take the larger S_eff, so they land closer to the star.
    SELECT
        seff.*,
        sqrt(lum_solar / seff_recent_venus)        AS hz_optimistic_inner_au,
        sqrt(lum_solar / seff_runaway_greenhouse)  AS hz_conservative_inner_au,
        sqrt(lum_solar / seff_maximum_greenhouse)  AS hz_conservative_outer_au,
        sqrt(lum_solar / seff_early_mars)          AS hz_optimistic_outer_au
    FROM seff
    WHERE lum_solar IS NOT NULL
      AND lum_solar > 0
      AND orbsmax_au IS NOT NULL
)
SELECT
    pl_name,
    hostname,
    pl_letter,
    discoverymethod,
    disc_year,
    sy_dist,
    pl_rade,
    pl_bmasse,
    pl_eqt,
    pl_insol,
    pl_orbper,
    pl_orbeccen,
    pl_controv_flag,
    st_spectype,
    st_teff,
    st_rad,
    st_mass,
    st_lum,
    pl_tsm,
    pl_esm,

    lum_solar,
    lum_source,
    orbsmax_au,
    orbsmax_source,

    hz_optimistic_inner_au,
    hz_conservative_inner_au,
    hz_conservative_outer_au,
    hz_optimistic_outer_au,

    -- Stellar flux the planet actually receives, in Earth units. Reported alongside
    -- the boundaries so a caller can see how far inside or outside the zone it sits.
    lum_solar / (orbsmax_au * orbsmax_au) AS insol_earth,

    CASE WHEN st_teff IS NULL THEN NULL WHEN st_teff BETWEEN 2600.0 AND 7200.0 THEN 1 ELSE 0 END AS teff_in_valid_range,

    -- Runaway greenhouse to maximum greenhouse: the defensible zone.
    -- NULL, not 0, when the boundaries could not be computed -- "we cannot evaluate
    -- this star" and "this planet is not habitable" are different answers, and
    -- collapsing them is the bug this view was written to replace.
    CASE
        WHEN hz_conservative_inner_au IS NULL THEN NULL
        WHEN orbsmax_au >= hz_conservative_inner_au
         AND orbsmax_au <= hz_conservative_outer_au
        THEN 1 ELSE 0
    END AS in_hz_conservative,

    -- Recent Venus to early Mars: the empirical zone, wider at both ends.
    CASE
        WHEN hz_optimistic_inner_au IS NULL THEN NULL
        WHEN orbsmax_au >= hz_optimistic_inner_au
         AND orbsmax_au <= hz_optimistic_outer_au
        THEN 1 ELSE 0
    END AS in_hz_optimistic,

    -- Where the planet sits relative to the conservative zone: 0.0 at the inner
    -- edge, 1.0 at the outer edge. Negative means too hot, >1 means too cold.
    (orbsmax_au - hz_conservative_inner_au)
        / (hz_conservative_outer_au - hz_conservative_inner_au) AS hz_position,

    -- 1.8 R(Earth) is the radius valley -- above it, planets are almost always
    -- volatile-rich rather than rocky. Combined with conservative HZ membership,
    -- this is the actual question behind "find me habitable planets".
    -- NULL when radius is unknown or the zone is uncomputable, for the same reason.
    CASE
        WHEN hz_conservative_inner_au IS NULL OR pl_rade IS NULL THEN NULL
        WHEN orbsmax_au >= hz_conservative_inner_au
         AND orbsmax_au <= hz_conservative_outer_au
         AND pl_rade < 1.8
        THEN 1 ELSE 0
    END AS is_rocky_candidate
FROM bounds;
