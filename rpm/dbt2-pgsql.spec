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
Summary:       Fair Use TPC-C benchmark kit - PostgreSQL Stored Functions
License:       The Artistic License
Source:        v%{version}.zip
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      postgresql%{pgversion}-server, llvm-libs, postgresql%{pgversion}


%description
TPC-C benchmark kit - PostgreSQL extension and scripts

%prep
%setup -q -n dbt2-%{version}

%install
%{__install} -d %{buildroot}/%{installpath}
%{__install} -d %{buildroot}/%{pgpath}/share
%{__install} -c -m 644 storedproc/pgsql/pgsql/delivery.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/new_order.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/order_status.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/payment.sql  %{buildroot}/%{pgpath}/share/.
%{__install} -c -m 644 storedproc/pgsql/pgsql/stock_level.sql  %{buildroot}/%{pgpath}/share/.
PATH=$PATH:%{pgpath}/bin make -C storedproc/pgsql/c/ install DESTDIR=%{buildroot}

%files
# pl/pgsql stored functions
%{pgpath}/share/delivery.sql
%{pgpath}/share/new_order.sql
%{pgpath}/share/order_status.sql
%{pgpath}/share/payment.sql
%{pgpath}/share/stock_level.sql
# PostgreSQL extension
%{pgpath}/lib/dbt2.so
%{pgpath}/lib/bitcode/dbt2
%{pgpath}/lib/bitcode/dbt2.index.bc
%{pgpath}/share/extension/dbt2*.sql
%{pgpath}/share/extension/dbt2.control

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
