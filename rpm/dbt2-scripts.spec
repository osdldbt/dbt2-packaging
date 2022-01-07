%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%{!?pgversion: %global pgversion 14}
%global pkgname dbt2-scripts
%define installpath /usr/bin
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Fair Use TPC-C benchmark kit - Scripts
License:       The Artistic License
Source:        v%{version}.zip
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      coreutils, procps-ng, sysstat


%description
TPC-C benchmark kit

%prep
%setup -q -n dbt2-%{version}

%build
PATH=$PATH:/usr/pgsql-%{pgversion}/bin cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/%{installpath}/.. -DDBMS=pgsql
make

%install
%{__install} -d %{buildroot}/%{installpath}
make install

%files
# General Scripts
%{installpath}/dbt2-get-os-info
%{installpath}/dbt2-sysstats
# PostgreSQL Scripts
%{installpath}/dbt2-pgsql-backup
%{installpath}/dbt2-pgsql-build-db
%{installpath}/dbt2-pgsql-check-db
%{installpath}/dbt2-pgsql-create-db
%{installpath}/dbt2-pgsql-create-indexes
%{installpath}/dbt2-pgsql-create-tables
%{installpath}/dbt2-pgsql-db-stat
%{installpath}/dbt2-pgsql-destroy-installation
%{installpath}/dbt2-pgsql-drop-db
%{installpath}/dbt2-pgsql-drop-tables
%{installpath}/dbt2-pgsql-init-db
%{installpath}/dbt2-pgsql-install-source
%{installpath}/dbt2-pgsql-load-db
%{installpath}/dbt2-pgsql-load-stored-procs
%{installpath}/dbt2-pgsql-plans
%{installpath}/dbt2-pgsql-restore
%{installpath}/dbt2-pgsql-start-db
%{installpath}/dbt2-pgsql-stop-db
%{installpath}/dbt2-pgsql-test
# Binaries
%{installpath}/dbt2-rand

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
