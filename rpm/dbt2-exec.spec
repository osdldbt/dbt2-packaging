%global debug_package %{nil}
%{!?pkgrevision: %global pkgrevision 1}
%global pkgname dbt2-exec
%define installpath /usr/bin
%define _unpackaged_files_terminate_build 0

Name:          %{pkgname}
Version:       %{pkgversion}
Release:       %{pkgrevision}%{?dist}
Summary:       Fair Use TPC-C benchmark kit - Execution and reporting scripts
License:       The Artistic License
Source:        v%{version}.zip
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:      dbttools, R-core, dbt2-driver, gawk, openssh-clients, psmisc, rsync


%description
Fair Use TPC-C benchmark kit - Execution and reporting scripts

%prep
%setup -q -n dbt2-%{version}

%install
mkdir -p %{buildroot}/%{installpath}
cp -p src/scripts/dbt2-generate-report %{buildroot}/%{installpath}/
cp -p src/scripts/dbt2-plot-transaction-rate %{buildroot}/%{installpath}/
cp -p src/scripts/dbt2-post-process %{buildroot}/%{installpath}/
cp -p src/scripts/dbt2-run-workload %{buildroot}/%{installpath}/

%files
%{installpath}/dbt2-generate-report
%{installpath}/dbt2-plot-transaction-rate
%{installpath}/dbt2-post-process
%{installpath}/dbt2-run-workload

%changelog
* Fri Oct 15 2021 Julien Tachoires <julmon@gmail.com> - master-1
- Initial packaging
