-- TODO: Need to find sqlite way to do a REGEXP_REPLACE
DROP VIEW IF EXISTS planet_names;

CREATE VIEW planet_names AS
SELECT
    pl_name         AS alias,
    REGEXP_REPLACE(
        LOWER(pl_name),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'planet_name'   AS alias_type,
    'planet'        AS resolves_to,
    pl_name         AS pl_name,
    hostname        AS hostname
FROM ps_default
WHERE pl_name IS NOT NULL

UNION
SELECT
    hostname        AS alias,
    REGEXP_REPLACE(
        LOWER(hostname),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'hostname'      AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM ps_default
WHERE hostname IS NOT NULL

UNION
SELECT
    hd_name         AS alias,
    REGEXP_REPLACE(
        LOWER(hd_name),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'hd'            AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM ps_default
WHERE hd_name IS NOT NULL

UNION
SELECT
    hip_name        AS alias,
    REGEXP_REPLACE(
        LOWER(hip_name),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'hip'           AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM ps_default
WHERE hip_name IS NOT NULL

UNION
SELECT
    tic_id         AS alias,
    REGEXP_REPLACE(
        LOWER(tic_id),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'tic'           AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM ps_default
WHERE tic_id IS NOT NULL

UNION
SELECT
    gaia_dr3_id     AS alias,
    REGEXP_REPLACE(
        LOWER(gaia_dr3_id),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'gaia'          AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM ps_default
WHERE gaia_dr3_id IS NOT NULL

UNION
SELECT
    kn.kepler_name  AS alias,
    REGEXP_REPLACE(
        LOWER(kn.kepler_name),
        '[^a-z0-9]+$',
        '',
        '',
        1,
        'i'
    )               AS alias_norm,
    'kepler_name'   AS alias_type,
    'planet'        AS resolves_to,
    kn.pl_name      AS pl_name,
    psd.hostname    AS hostname
FROM keplernames AS kn
LEFT JOIN ps_default AS psd ON kn.pl_name = psd.pl_name
WHERE kepler_name IS NOT NULL

UNION
SELECT
    kn.koi_name       AS alias,
    REGEXP_REPLACE(
        LOWER(kn.koi_name),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'koi_name'      AS alias_type,
    'planet'        AS resolves_to,
    kn.pl_name         AS pl_name,
    psd.hostname            AS hostname
FROM keplernames AS kn
LEFT JOIN ps_default AS psd ON kn.pl_name = psd.pl_name
WHERE koi_name IS NOT NULL

UNION
SELECT
    k2n.k2_name        AS alias,
    REGEXP_REPLACE(
        LOWER(k2n.k2_name),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'k2_name'       AS alias_type,
    'planet'        AS resolves_to,
    k2n.pl_name         AS pl_name,
    psd.hostname            AS hostname
FROM k2names AS k2n
LEFT JOIN ps_default AS psd ON k2n.pl_name = psd.pl_name
WHERE k2_name IS NOT NULL

UNION
SELECT
    epic_id        AS alias,
    REGEXP_REPLACE(
        LOWER(epic_id),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'epic_name'     AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM k2names
WHERE epic_id IS NOT NULL

UNION
SELECT
    epic_candname   AS alias,
    REGEXP_REPLACE(
        LOWER(epic_candname),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'epic_name'     AS alias_type,
    'planet'        AS resolves_to,
    pl_name         AS pl_name,
    hostname        AS hostname
FROM k2pandc_default
WHERE epic_candname IS NOT NULL

UNION
SELECT
    epic_hostname   AS alias,
    REGEXP_REPLACE(
        LOWER(epic_hostname),
        '[^a-z0-9]+$',
        '',
        1,
        'i'
    )               AS alias_norm,
    'epic_name'     AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM k2pandc_default
WHERE epic_hostname IS NOT NULL;