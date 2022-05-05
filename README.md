# DBT2 packaging

This repository contains scripts, relying on `docker-compose`, used to build
`dbt2` packages with Postgres support (no MySQL nor SQLite3 support). Only the
RPM format for RHEL 8 based distros is supported.

## Package building

Execute the following `make` command to build the packages:
```console
$ make -C rpm
```

Generated packages are located into the `rpm/build/` directory.
