from flask import abort


ESTCODE_DB_BIND_MAP = {
    'ODGM01': 'cis_db_1',
    'ODGM02': 'cis_db_2',
    'ODGM03': 'cis_db_3',
    'ODGM04': 'cis_db_4',
}


def get_cis_bind(estcode: str) -> str:
    if not estcode:
        abort(400, "estcode is required")

    estcode = estcode.upper()

    bind = ESTCODE_DB_BIND_MAP.get(estcode)
    if not bind:
        abort(400, f"Invalid estcode: {estcode}")

    return bind


def get_cis_db_key(estcode: str) -> str:
    estcode = estcode.upper()
    if estcode not in ESTCODE_DB_BIND_MAP:
        raise ValueError(f"Invalid estcode: {estcode}")
    return ESTCODE_DB_BIND_MAP[estcode]
