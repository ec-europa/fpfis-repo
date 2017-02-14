#===============================================================================
# Copyright 2016 European Commission
# Name: aws-monitoring.spec
#-------------------------------------------------------------------------------
# $Id: aws-monitoring.spec,v 1.0 2016/10/19 rvanhoudt Exp $
#-------------------------------------------------------------------------------
# Purpose: RPM Spec file for AWS monitoring scripts
# Version 1.00:24 Oct 2016 Created.
#===============================================================================

# No debuginfo:
%define debug_package %{nil}

%define name      aws-monitoring
%define summary   AWS monitoring scripts
%define version   0.%(perl -e 'print time()')
%define release   Base
%define license   GPL
%define group     Scripts
%define source0   aws-monitoring.tar.gz
%define url       http://www.europa.eu
%define vendor    European Commission
%define packager  Rudi Van Houdt
#%define buildroot %{_tmppath}/%{name}-root
%define _prefix   /opt/aws-scripts-mon

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
Deploying scripts to send extra metrics to Cloud Watch

%changelog
* Wed Dec 14 2016 AWS Monitoring Scripts -European Commission
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
mkdir -p ${RPM_BUILD_ROOT}/%{_prefix}/%{name}-%{version}
cp -r %{name}-%{version}/aws-scripts-mon/ ${RPM_BUILD_ROOT}/%{_prefix}/%{name}-%{version}

%post
echo "--------------------------------------------------------"
echo "      Deploy %{name}-%{version} on the server"
echo "--------------------------------------------------------"

rm %{_prefix}/current
ln -s %{_prefix}/%{name}-%{version}/ %{_prefix}/current
cd %{_prefix}
ls -td1 aws-scripts* | tail -n +4 | xargs sudo rm -rf

%files
%{_prefix}/%{name}-%{version}/*