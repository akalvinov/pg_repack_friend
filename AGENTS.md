# pg_repack assistant

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

System dependencies (not in venv): `psql`, `pg_repack`.

## Config

PostgreSQL clusters are listed in `config.yaml`. Each entry has `host`, `port`, `cluster`, `user`, `password`, and `db_list`. **This file contains secrets** — avoid leaking.

## Current state

`main.py` is a skeleton: it reads `config.yaml` and prints `host`/`port` per cluster but does **not** yet execute `pg_repack`. The real work (iterating databases, running `pg_repack -k` per DB) still needs implementation.

## No tests, no CI, no lint/typecheck config

If you add code that needs verification, add a check yourself (e.g., `pip install -e .` or a manual smoke run). There are no pre-existing test, lint, or typecheck commands.

## Conventions

- Uses `pydantic` for models (`PGCluster` with `BaseModel`)
- Uses `PyYAML` for config loading (`yaml.SafeLoader`)
- Requirements in `requirements.txt` (keep updated)
- `.gitignore` only ignores `venv/` — add entries if introducing new artifacts
