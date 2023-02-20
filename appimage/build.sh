#!/bin/bash -eux

export PKG_CONFIG_PATH="/usr/lib/pkgconfig"

# DBT2 version
VERSION="0.49.1"
TAG="v$VERSION"

curl -o "/tmp/${TAG}.tar.gz" \
		-OL https://github.com/osdldbt/dbt2/archive/refs/tags/${TAG}.tar.gz
tar -xf "/tmp/${TAG}.tar.gz"
cd dbt2-${VERSION}
container/prepare-appimage
container/build-appimage
