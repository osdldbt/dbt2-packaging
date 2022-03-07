%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%{!?pgversion: %global pgversion 14}
%global pkgname dbt2-db
%define installpath /usr/bin
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Fair Use TPC-C benchmark kit - Database Data Generator
License:       The Artistic License
Source:        v%{version}.zip
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Fair Use TPC-C benchmark kit - Database Data Generator

%prep
%setup -q -n dbt2-%{version}

%build
PKG_CONFIG_PATH="/usr/pgsql-%{pgversion}/lib/pkgconfig" PATH=$PATH:/usr/pgsql-%{pgversion}/bin cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}/%{installpath}/..
make

%install
%{__install} -d %{buildroot}/%{installpath}
make install

%files
# Binaries
%{installpath}/dbt2-datagen

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
