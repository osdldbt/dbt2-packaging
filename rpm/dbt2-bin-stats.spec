%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%{!?pgversion: %global pgversion 14}
%global pkgname dbt2-pgsql-stats_%{pgversion}
%define installpath /usr/bin
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       TPC-C benchmark kit - statistics collection
License:       The Artistic License
Source:        dbt2-%{version}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      postgresql%{pgversion}, sysstat


%description
TPC-C benchmark kit - statistics collection binaries

%prep
%setup -q -n dbt2-%{version}

%build
PATH=$PATH:/usr/pgsql-%{pgversion}/bin cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/%{installpath}/.. -DDBMS=pgsql
make

%install
%{__install} -d %{buildroot}/%{installpath}
make install

%files
%{installpath}/dbt2-sysstats
%{installpath}/dbt2-pgsql-db-stat
%{installpath}/dbt2-pgsql-plans

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
