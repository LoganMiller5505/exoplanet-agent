DROP VIEW IF EXISTS planet_names CASCADE;

CREATE VIEW planet_names AS
SELECT
    pl_name         AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(pl_name),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'planet_name'   AS alias_type,
    'planet'        AS resolves_to,
    pl_name         AS pl_name,
    hostname        AS hostname
FROM stg_ps
WHERE pl_name IS NOT NULL

UNION
SELECT
    hostname        AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(hostname),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'hostname'      AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM stg_ps
WHERE hostname IS NOT NULL

UNION
SELECT
    hd_name         AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(hd_name),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'hd'            AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM stg_ps
WHERE hd_name IS NOT NULL

UNION
SELECT
    hip_name        AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(hip_name),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'hip'           AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM stg_ps
WHERE hip_name IS NOT NULL

UNION
SELECT
    tic_id         AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(tic_id),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'tic'           AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM stg_ps
WHERE tic_id IS NOT NULL

UNION
SELECT
    gaia_dr3_id     AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(gaia_dr3_id),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'gaia'          AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM stg_ps
WHERE gaia_dr3_id IS NOT NULL

UNION
SELECT
    kn.kepler_name  AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(kn.kepler_name),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'kepler_name'   AS alias_type,
    'planet'        AS resolves_to,
    kn.pl_name      AS pl_name,
    psd.hostname    AS hostname
FROM src_keplernames AS kn
LEFT JOIN stg_ps AS psd ON kn.pl_name = psd.pl_name
WHERE kepler_name IS NOT NULL

UNION
SELECT
    kn.koi_name       AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(kn.koi_name),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'koi_name'      AS alias_type,
    'planet'        AS resolves_to,
    kn.pl_name         AS pl_name,
    psd.hostname            AS hostname
FROM src_keplernames AS kn
LEFT JOIN stg_ps AS psd ON kn.pl_name = psd.pl_name
WHERE koi_name IS NOT NULL

UNION
SELECT
    k2n.k2_name        AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(k2n.k2_name),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'k2_name'       AS alias_type,
    'planet'        AS resolves_to,
    k2n.pl_name         AS pl_name,
    psd.hostname            AS hostname
FROM src_k2names AS k2n
LEFT JOIN stg_ps AS psd ON k2n.pl_name = psd.pl_name
WHERE k2_name IS NOT NULL

UNION
SELECT
    k2n.epic_id     AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(k2n.epic_id),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'epic_name'     AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    psd.hostname    AS hostname
FROM src_k2names AS k2n
LEFT JOIN stg_ps AS psd ON k2n.pl_name = psd.pl_name
WHERE k2n.epic_id IS NOT NULL

UNION
SELECT
    epic_candname   AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(epic_candname),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'epic_name'     AS alias_type,
    'planet'        AS resolves_to,
    pl_name         AS pl_name,
    hostname        AS hostname
FROM stg_k2pandc
WHERE epic_candname IS NOT NULL

UNION
SELECT
    epic_hostname   AS alias,
    REPLACE(
        REPLACE(
            REPLACE(
                REPLACE(
                    REPLACE(
                        LOWER(epic_hostname),
                        '.',
                        ''
                    ),
                    '''',
                    ''
                ),
                ' ',
                ''
            ),
            '-',
            ''
        ),
        '+',
        ''
    )               AS alias_norm,
    'epic_name'     AS alias_type,
    'star'          AS resolves_to,
    null            AS pl_name,
    hostname        AS hostname
FROM stg_k2pandc
WHERE epic_hostname IS NOT NULL;