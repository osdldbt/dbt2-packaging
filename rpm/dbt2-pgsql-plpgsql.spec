%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%{!?pgversion: %global pgversion 14}
%define installpath /usr/share
%global pkgname dbt2-pgsql-plpgsql_%{pgversion}
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Fair Use TPC-C benchmark kit - PostgreSQL PL/pgsql Stored Functions
License:       The Artistic License
Source:        v%{version}.zip
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      postgresql%{pgversion}-server, llvm-libs, postgresql%{pgversion}


%description
Fair Use TPC-C benchmark kit - PostgreSQL PL/pgsql Stored Functions

%prep
%setup -q -n dbt2-%{version}

%install
mkdir -p %{buildroot}/%{installpath}
cp -p storedproc/pgsql/pgsql/delivery.sql %{buildroot}/%{installpath}/
cp -p storedproc/pgsql/pgsql/new_order.sql %{buildroot}/%{installpath}/
cp -p storedproc/pgsql/pgsql/order_status.sql %{buildroot}/%{installpath}/
cp -p storedproc/pgsql/pgsql/payment.sql %{buildroot}/%{installpath}/
cp -p storedproc/pgsql/pgsql/stock_level.sql %{buildroot}/%{installpath}/

%files
%{installpath}/delivery.sql
%{installpath}/new_order.sql
%{installpath}/order_status.sql
%{installpath}/payment.sql
%{installpath}/stock_level.sql

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
