Name:           fpfis-repo
Version:        7 
Release:        1%{?dist} 
Summary:        FPFIS Packages for Enterprise Linux repository configuration

Group:          System Environment/Base
License:        GPLv2

# This is a FPFIS maintained package which is specific to
# our distribution.  Thus the source is only available from
# within this srpm.

URL:            https://github.com/ec-europa/fpfis-repo
Source0:        fpfis-repo-7.repo
Source1:        FPFIS-REPO-kEY 
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}%{version}

%description
This package contains the FPFIS Packages for Enterprise Linux (EL) repository
GPG key as well as configuration for yum.

%prep
%setup  -c -T

%build


%install
rm -rf %{buildroot} 

#GPG Key
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_sysconfdir}/pki/rpm-gpg/FPFIS-REPO-KEY

# yum
install -dm 755 %{buildroot}%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0}  \
    %{buildroot}%{_sysconfdir}/yum.repos.d/fpfis.repo

%clean
rm -rf %{buildroot} 

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/yum.repos.d/*
%{_sysconfdir}/pki/rpm-gpg/*

%changelog
* Tue Dec 20 2016 Gregory Boddin <gregory@siwhine.net> - 7-1
- Created package for easy install on RHELs
 
* Mon Dec 16 2013 Dennis Gilmore <dennis@ausil.us> - 6-0.1
- initial epel 6 build. 

