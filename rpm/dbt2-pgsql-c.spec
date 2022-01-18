%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%{!?pgversion: %global pgversion 14}
%define installpath /usr/bin
%define pgpath /usr/pgsql-%{pgversion}
%global pkgname dbt2-pgsql-c_%{pgversion}
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Fair Use TPC-C benchmark kit - PostgreSQL C Stored Functions
License:       The Artistic License
Source:        v%{version}.zip
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      postgresql%{pgversion}-server, llvm-libs, postgresql%{pgversion}


%description
Fair Use TPC-C benchmark kit - PostgreSQL C Stored Functions

%prep
%setup -q -n dbt2-%{version}

%install
%{__install} -d %{buildroot}/%{installpath}
%{__install} -d %{buildroot}/%{pgpath}/share
PATH=$PATH:%{pgpath}/bin make -C storedproc/pgsql/c/ install DESTDIR=%{buildroot}

%files
%{pgpath}/lib/dbt2.so
%{pgpath}/lib/bitcode/dbt2
%{pgpath}/lib/bitcode/dbt2.index.bc
%{pgpath}/share/extension/dbt2*.sql
%{pgpath}/share/extension/dbt2.control

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
