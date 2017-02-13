#===============================================================================
# Copyright 2016 European Commission
# Name: cli53.spec
#-------------------------------------------------------------------------------
# $Id: aws-monitoring.spec,v 1.0 2016/10/19 rvanhoudt Exp $
#-------------------------------------------------------------------------------
# Purpose: RPM Spec file for AWS route53 scripts
# Version 1.00:24 Jan 2017 Created.
#===============================================================================

# No debuginfo:
%define debug_package %{nil}

%define name      cli53
%define summary   cli53 scripts
%define version   0.%(perl -e 'print time()')
%define release   Base
%define license   GPL
%define group     Scripts
%define source0   cli53.tar.gz
%define url       http://www.europa.eu
%define vendor    European Commission
%define packager  Rudi Van Houdt
#%define _binaries_in_noarch_packages_terminate_build   0
#%define buildroot %{_tmppath}/%{name}-root
%define _prefix   /opt/cli53

Name:      %{name}
Summary:   %{summary}
Version:   %{version}
Release:   %{release}
License:   %{license}
Group:     %{group}
Source0:   %{source0}
BuildArch: noarch
Requires:  filesystem, bash, grep, perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https
Provides:  %{name}
URL:       %{url}
Buildroot: %{buildroot}

%description
Deploying scripts to add DNS entries to route53

%changelog
* Tue Jan 17 2017 Route 53 scripts - European Commission
+ initial creation

%{summary}.

%prep
%setup -c -n %{name}-%{version}
%build

%install
rm -rf ${RPM_BUILD_ROOT}
install -d ${RPM_BUILD_ROOT}/%{_prefix}
cd ..
pwd
mkdir -p ${RPM_BUILD_ROOT}/%{_prefix}/
cp -r %{name}-%{version}/ ${RPM_BUILD_ROOT}/%{_prefix}

%post
echo "--------------------------------------------------------"
echo "      Deploy %{name}-%{version} on the server"
echo "--------------------------------------------------------"

rm %{_prefix}/current
ln -s %{_prefix}/%{name}-%{version}/ %{_prefix}/current
cd %{_prefix}
ls -td1 cli53* | tail -n +4 | xargs sudo rm -rf
cd current

tar -xvvf cli53.tar
rm cli53.tar

rm /usr/local/bin/cli53
rm /usr/local/bin/update_route53.sh
ln -s %{_prefix}/current/cli53 /usr/local/bin/cli53
ln -s %{_prefix}/current/update_route53.sh /usr/local/bin/update_route53.sh

%files
%{_prefix}/%{name}-%{version}/*

