#!/bin/bash -eux

# DBT2 version
VERSION="0.42"
TAG="v0.42"

dnf update -y
dnf install rpm-build redhat-rpm-config yum-utils -y
dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm
dnf -qy module disable postgresql
dnf install -y postgresql14-server postgresql14-devel postgresql14-libs
dnf install -y postgresql13-server postgresql13-devel postgresql13-libs
dnf install -y postgresql12-server postgresql12-devel postgresql12-libs
dnf install -y postgresql11-server postgresql11-devel postgresql11-libs
dnf install git cmake gcc make postgresql-devel postgresql-libs  -y

yum-builddep -y /workspace/rpm/dbt2-bin.spec

git clone https://git.code.sf.net/p/osdldbt/dbt2 /tmp/dbt2
cd /tmp/dbt2
git archive --format=tar.gz --prefix=dbt2-${VERSION}/ ${TAG} > /workspace/dbt2-${VERSION}.tar.gz
cd /

for PGVERSION in 11 12 13 14; do
	# Stats collection packages for all supported Postgres version
	rpmbuild \
		--clean \
		--define "pgversion ${PGVERSION}" \
		--define "pkgversion ${VERSION}" \
		--define "_topdir ${PWD}/tmp/rpm" \
		--define "_sourcedir ${PWD}/workspace" \
		-bb /workspace/rpm/dbt2-bin-stats.spec
	# Database creation packages for all supported Postgres version
	rpmbuild \
		--clean \
		--define "pgversion ${PGVERSION}" \
		--define "pkgversion ${VERSION}" \
		--define "_topdir ${PWD}/tmp/rpm" \
		--define "_sourcedir ${PWD}/workspace" \
		-bb /workspace/rpm/dbt2-bin-dbcreation.spec
	# Test execution package
	rpmbuild \
		--clean \
		--define "pgversion ${PGVERSION}" \
		--define "pkgversion ${VERSION}" \
		--define "_topdir ${PWD}/tmp/rpm" \
		--define "_sourcedir ${PWD}/workspace" \
		-bb /workspace/rpm/dbt2-bin-exec.spec
	# PostgreSQL extension
	rpmbuild \
		--clean \
		--define "pgversion ${PGVERSION}" \
		--define "pkgversion ${VERSION}" \
		--define "_topdir ${PWD}/tmp/rpm" \
		--define "_sourcedir ${PWD}/workspace" \
		-bb /workspace/rpm/dbt2-ext.spec
done;
# Report generation
rpmbuild \
	--clean \
	--define "pkgversion ${VERSION}" \
	--define "_topdir ${PWD}/tmp/rpm" \
	--define "_sourcedir ${PWD}/workspace" \
	-bb /workspace/rpm/dbt2-bin-report.spec

rm /workspace/dbt2-${VERSION}.tar.gz
mkdir -p ${PWD}/workspace/rpm/build/
cp ${PWD}/tmp/rpm/RPMS/*/*.rpm ${PWD}/workspace/rpm/build/.
ls -lha ${PWD}/workspace/rpm/build/*.rpm
