%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%{!?pgversion: %global pgversion 14}
%define installpath /usr/bin
%define pgpath /usr/pgsql-%{pgversion}
%global pkgname dbt2-pgsql_%{pgversion}
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       TPC-C benchmark kit - PostgreSQL extension and scripts
License:       The Artistic License
Source:        dbt2-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      postgresql%{pgversion}-server, llvm-libs, postgresql%{pgversion}, R, sysstat


%description
TPC-C benchmark kit - PostgreSQL extension and scripts

%prep
%setup -q -n dbt2-%{version}

%build
PATH=$PATH:%{pgpath}/bin cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/%{installpath}/.. -DDBMS=pgsql

%install
%{__install} -d %{buildroot}/%{installpath}
%{__install} -d %{buildroot}/%{pgpath}/share
%{__install} -c -m 644 storedproc/pgsql/pgsql/delivery.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/new_order.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/order_status.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/payment.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/stock_level.sql  %{buildroot}/%{pgpath}/share/.
PATH=$PATH:%{pgpath}/bin make -C storedproc/pgsql/c/ install DESTDIR=%{buildroot}
make install

%files
# PostgreSQL extension
%{pgpath}/share/delivery.sql
%{pgpath}/share/new_order.sql
%{pgpath}/share/order_status.sql
%{pgpath}/share/payment.sql
%{pgpath}/share/stock_level.sql
%{pgpath}/lib/dbt2.so
%{pgpath}/lib/bitcode/dbt2
%{pgpath}/lib/bitcode/dbt2.index.bc
%{pgpath}/share/extension/dbt2*.sql
%{pgpath}/share/extension/dbt2.control
# Scripts
%{installpath}/dbt2-pgsql-create-tables
%{installpath}/dbt2-pgsql-backup
%{installpath}/dbt2-pgsql-start-db
%{installpath}/dbt2-pgsql-init-db
%{installpath}/dbt2-pgsql-build-db
%{installpath}/dbt2-pgsql-stop-db
%{installpath}/dbt2-pgsql-drop-db
%{installpath}/dbt2-pgsql-check-db
%{installpath}/dbt2-pgsql-create-db
%{installpath}/dbt2-pgsql-load-db
%{installpath}/dbt2-pgsql-drop-tables
%{installpath}/dbt2-pgsql-load-stored-procs
%{installpath}/dbt2-pgsql-create-indexes
%{installpath}/dbt2-pgsql-destroy-installation
%{installpath}/dbt2-pgsql-install-source
%{installpath}/dbt2-pgsql-restore
%{installpath}/dbt2-pgsql-test
# Binaries
%{installpath}/dbt2-datagen
%{installpath}/dbt2-run-workload
%{installpath}/dbt2-get-os-info
%{installpath}/dbt2-run-workload-autoscale
%{installpath}/dbt2-post-process
# Stats
%{installpath}/dbt2-sysstats
%{installpath}/dbt2-pgsql-db-stat
%{installpath}/dbt2-pgsql-plans

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
