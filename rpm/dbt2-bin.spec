%global debug_package %{nil}
%global pkgname dbt2-pgsql-bin
%{!?pkgrevision: %global pkgrevision 1}
%define installpath /usr/bin

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       TPC-C benchmark kit - binaries
License:       The Artistic License
Source:        dbt2-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      libpq


%description
TPC-C benchmark kit - binaries

%prep
%setup -q -n dbt2-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/%{installpath}/.. -DDBMS=pgsql
make

%install
%{__install} -d %{buildroot}/%{installpath}
make install

%files
%{installpath}/dbt2-client
%{installpath}/dbt2-datagen
%{installpath}/dbt2-driver
%{installpath}/dbt2-rand
%{installpath}/dbt2-transaction-test
%{installpath}/dbt2-generate-report
%{installpath}/dbt2-get-os-info
%{installpath}/dbt2-plot-transaction-rate
%{installpath}/dbt2-post-process
%{installpath}/dbt2-run-workload
%{installpath}/dbt2-run-workload-autoscale
%{installpath}/dbt2-sysstats
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

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
