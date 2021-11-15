%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%{!?pgversion: %global pgversion 14}
%global pkgname dbt2-pgsql-dbcreation_%{pgversion}
%define installpath /usr/bin
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       TPC-C benchmark kit - database creation
License:       The Artistic License
Source:        dbt2-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      postgresql%{pgversion}


%description
TPC-C benchmark kit - database creation binaries

%prep
%setup -q -n dbt2-%{version}

%build
PATH=$PATH:/usr/pgsql-%{pgversion}/bin cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/%{installpath}/.. -DDBMS=pgsql
make

%install
%{__install} -d %{buildroot}/%{installpath}
make install

%files
%{installpath}/dbt2-pgsql-create-tables
%{installpath}/dbt2-pgsql-start-db
%{installpath}/dbt2-pgsql-init-db
%{installpath}/dbt2-pgsql-build-db
%{installpath}/dbt2-pgsql-stop-db
%{installpath}/dbt2-pgsql-drop-db
%{installpath}/dbt2-pgsql-check-db
%{installpath}/dbt2-pgsql-create-db
%{installpath}/dbt2-pgsql-load-db
#%{installpath}/dbt2-pgsql-load-db-autoscale
#%{installpath}/dbt2-pgsql-create-tables-autoscale
%{installpath}/dbt2-pgsql-drop-tables
%{installpath}/dbt2-pgsql-load-stored-procs
%{installpath}/dbt2-pgsql-create-indexes

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
