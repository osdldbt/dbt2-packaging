#!/bin/bash -eux

export PKG_CONFIG_PATH="/usr/lib/pkgconfig"

# DBT2 version
VERSION="0.49.0"
TAG="v$VERSION"

yum -qy update
yum -qy install \
		bison \
		bzip2 \
		cmake \
		file \
		flex \
		gcc \
		libev-devel \
		libffi-devel \
		make \
		patch \
		perl \
		sqlite-devel \
		xz \
		zlib-devel
yum -qy clean all

mkdir -p /usr/local/AppDir
export LD_LIBRARY_PATH="/usr/local/lib64"

JULIAVER="1.8.5"
export JULIA_DEPOT_PATH="/usr/local/AppDir/opt/julia"
curl -o /tmp/julia-${JULIAVER}-linux-x86_64.tar.gz \
		-sOL https://julialang-s3.julialang.org/bin/linux/x64/1.8/julia-${JULIAVER}-linux-x86_64.tar.gz
tar -C /tmp -xf tmp/julia-${JULIAVER}-linux-x86_64.tar.gz
mv /tmp/julia-${JULIAVER} /usr/local/AppDir/usr
sed -i -e 's#/usr#././#g' /usr/local/AppDir/usr/bin/julia
/usr/local/AppDir/usr/bin/julia --quiet -C generic \
		-e 'import Pkg; Pkg.add("CSV"); Pkg.add("DataFrames");'

OPENSSLVER="1.1.1s"
curl -o /tmp/openssl-${OPENSSLVER}.tar.gz \
		-sOL https://www.openssl.org/source/openssl-${OPENSSLVER}.tar.gz
tar -C /usr/local/src -xf "/tmp/openssl-${OPENSSLVER}.tar.gz"
cd /usr/local/src/openssl-${OPENSSLVER}
./config -fPIC shared
make -s "-j$(nproc)"
make -s install

PYTHONVER="3.11.1"
curl -o "/tmp/Python-${PYTHONVER}.tgz" \
		-sOL https://www.python.org/ftp/python/${PYTHONVER}/Python-${PYTHONVER}.tgz
tar -C /usr/local/src -xf "/tmp/Python-${PYTHONVER}.tgz"
cd /usr/local/src/Python-${PYTHONVER}
./configure --silent --prefix=/usr/local/AppDir/usr \
		--with-openssl-rpath=/usr/local/lib64
make -s "-j$(nproc)"
make -s install
sed -i -e 's#/usr#././#g' /usr/local/AppDir/usr/bin/python3.11
/usr/local/AppDir/usr/bin/pip3 install docutils

# PostgreSQL 11 is the first release creating the pg_type_d.h include file for
# CockroachDB binary support.

PGVER="11.18"
curl -o "/tmp/postgresql-${PGVER}.tar.bz2" \
		-sOL https://ftp.postgresql.org/pub/source/v${PGVER}/postgresql-${PGVER}.tar.bz2
tar -C /usr/local/src -xf "/tmp/postgresql-${PGVER}.tar.bz2"
cd /usr/local/src/postgresql-${PGVER}
# I think it's simpler to install into the system's default paths and into a
# "clean" location for ease of building other software and generating the
# AppImage, resp.
./configure --silent --without-ldap --without-readline --without-zlib \
		--without-gssapi --with-openssl --prefix=/usr
make -s -j "$(nproc)" install
./configure --silent --without-ldap --without-readline --without-zlib \
		--without-gssapi --with-openssl --prefix=/usr/local/AppDir/usr
make -s -j "$(nproc)" install
sed -i -e 's#/usr#././#g' /usr/local/AppDir/usr/bin/psql
ldconfig

# Install DBT Tools

DBTTOOLSVER="0.3.2"
curl -o "/tmp/v${DBTTOOLSVER}.tar.gz" \
		-sOL https://github.com/osdldbt/dbttools/archive/refs/tags/v${DBTTOOLSVER}.tar.gz
tar -C /usr/local/src -xf "/tmp/v${DBTTOOLSVER}.tar.gz"
cd /usr/local/src/dbttools-${DBTTOOLSVER}
cmake -H. -Bbuilds/release -DCMAKE_INSTALL_PREFIX=/usr
(cd builds/release && make -s install DESTDIR=/usr/local/AppDir)
rm -f "/tmp/v${DBTTOOLSVER}.tar.gz"

cd /usr/local
curl -sOL https://github.com/AppImage/AppImageKit/releases/download/13/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage --appimage-extract
chmod 0755 squashfs-root
chmod 0755 squashfs-root/usr
chmod 0755 squashfs-root/usr/bin
chmod 0755 squashfs-root/usr/lib
chmod 0755 squashfs-root/usr/lib/appimagekit
chmod 0755 squashfs-root/usr/share

curl -o "/tmp/${TAG}.tar.gz" \
		-OL https://github.com/osdldbt/dbt2/archive/refs/tags/${TAG}.tar.gz
tar -C /workspace -xf "/tmp/${TAG}.tar.gz"
cd /workspace/dbt2-${VERSION}
patch -p1 < patches/bsd_vs_default.patch
patch -p1 < patches/cmake.patch
make -f Makefile.cmake appimage
