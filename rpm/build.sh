#!/bin/bash -eux

# DBT2 version
VERSION="0.44.0"
TAG="v$VERSION"

dnf update -y
dnf install rpm-build redhat-rpm-config yum-utils curl unzip -y
dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
dnf -qy module disable postgresql
dnf install -y postgresql14-server postgresql14-devel postgresql14-libs
dnf install -y postgresql13-server postgresql13-devel postgresql13-libs
dnf install -y postgresql12-server postgresql12-devel postgresql12-libs
dnf install -y postgresql11-server postgresql11-devel postgresql11-libs
dnf install cmake gcc make postgresql-devel postgresql-libs  -y

cp /workspace/rpm/*.patch /workspace/

yum-builddep -y /workspace/rpm/dbt2-client-pgsql.spec
yum-builddep -y /workspace/rpm/dbt2-db.spec
yum-builddep -y /workspace/rpm/dbt2-driver.spec
yum-builddep -y /workspace/rpm/dbt2-exec.spec
yum-builddep -y /workspace/rpm/dbt2-pgsql-c.spec
yum-builddep -y /workspace/rpm/dbt2-pgsql-plpgsql.spec
yum-builddep -y /workspace/rpm/dbt2-scripts.spec

(cd /workspace && curl -OL https://github.com/osdldbt/dbt2/archive/refs/tags/${TAG}.zip)

for PGVERSION in 11 12 13 14; do
	rpmbuild \
		--clean \
		--define "pgversion ${PGVERSION}" \
		--define "pkgversion ${VERSION}" \
		--define "_topdir ${PWD}/tmp/rpm" \
		--define "_sourcedir ${PWD}/workspace" \
		-bb /workspace/rpm/dbt2-pgsql-c.spec
done;

# PostgreSQL PL/pgsql stored functions
rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-pgsql-plpgsql.spec

# Binaries for the client
rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-client-cockroachdb.spec

rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-client-pgsql.spec

# Binary for the DB
rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-db.spec

# Binary for the driver
rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-driver.spec

# Execution scripts
rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-exec.spec

# Helper scripts
rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-scripts.spec

rm /workspace/${TAG}.zip
mkdir -p ${PWD}/workspace/rpm/build/
cp ${PWD}/tmp/rpm/RPMS/*/*.rpm ${PWD}/workspace/rpm/build/.
chown ${1}:${2} -R ${PWD}/workspace/rpm/build/
ls -lha ${PWD}/workspace/rpm/build/*.rpm
