# IUS spec file for php71u-pecl-igbinary, forked from:
#
# Fedora spec file for php-pecl-igbinary
#
# Copyright (c) 2010-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pecl_name  igbinary
%global with_zts   0%{?__ztsphp:1}
%global ini_name   40-%{pecl_name}.ini
%global php_base   php71e

Summary:        Replacement for the standard PHP serializer
Name:           %{php_base}-pecl-%{pecl_name}
Version:        2.0.1
Release:        2%{?dist}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
License:        BSD
Group:          System Environment/Libraries

URL:            http://pecl.php.net/package/%{pecl_name}

BuildRequires:  %{php_base}-devel
BuildRequires:  pecl >= 1.10.0
BuildRequires:  %{php_base}-pecl-apcu-devel

Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

Requires(post): pecl >= 1.10.0
Requires(postun): pecl >= 1.10.0

# provide the stock name
Provides:       php-pecl-%{pecl_name} = %{version}
Provides:       php-pecl-%{pecl_name}%{?_isa} = %{version}

# provide the stock and IUS names without pecl
Provides:       php-%{pecl_name} = %{version}
Provides:       php-%{pecl_name}%{?_isa} = %{version}
Provides:       %{php_base}-%{pecl_name} = %{version}
Provides:       %{php_base}-%{pecl_name}%{?_isa} = %{version}

# provide the stock and IUS names in pecl() format
Provides:       php-pecl(%{pecl_name}) = %{version}
Provides:       php-pecl(%{pecl_name})%{?_isa} = %{version}
Provides:       %{php_base}-pecl(%{pecl_name}) = %{version}
Provides:       %{php_base}-pecl(%{pecl_name})%{?_isa} = %{version}

# conflict with the stock name
Conflicts:      php-pecl-%{pecl_name} < %{version}

%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}


%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
igbinary stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.


%package devel
Summary:        Igbinary developer files (header)
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{php_base}-devel%{?_isa}

Provides:       php-pecl-%{pecl_name}-devel = %{version}
Provides:       php-pecl-%{pecl_name}-devel%{?_isa} = %{version}
Conflicts:      php-pecl-%{pecl_name}-devel < %{version}


%description devel
These are the files needed to compile programs using Igbinary


%prep
%setup -q -c
mv %{pecl_name}-%{version} NTS

sed -e '/COPYING/s/role="doc"/role="src"/' -i package.xml

pushd NTS

# Check version
subdir="php$(%{__php} -r 'echo PHP_MAJOR_VERSION;')"
extver=$(sed -n '/#define PHP_IGBINARY_VERSION/{s/.* "//;s/".*$//;p}' src/$subdir/igbinary.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream version is ${extver}, expecting %{version}.
   exit 1
fi
popd

%if %{with_zts}
cp -r NTS ZTS
%endif

cat <<EOF | tee %{ini_name}
; Enable %{pecl_name} extension module
extension=%{pecl_name}.so

; Enable or disable compacting of duplicate strings
; The default is On.
;igbinary.compact_strings=On

; Use igbinary as session serializer
;session.serialize_handler=igbinary

; Use igbinary as APC serializer
;apc.serializer=igbinary
EOF


%build
pushd NTS
%{_bindir}/phpize
%configure --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}
popd

%if %{with_zts}
pushd ZTS
%{_bindir}/zts-phpize
%configure --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
popd
%endif


%install
make install -C NTS INSTALL_ROOT=%{buildroot}

install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml

install -D -m 644 %{ini_name} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ini_name} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
pushd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do [ -f $i       ] && install -Dpm 644 $i       %{buildroot}%{pecl_testdir}/%{pecl_name}/$i
   [ -f tests/$i ] && install -Dpm 644 tests/$i %{buildroot}%{pecl_testdir}/%{pecl_name}/tests/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{pecl_name}/$i
done
popd


%check
# drop extension load from phpt
sed -e '/^extension=/d' -i ?TS/tests/*phpt

# APC required for test 045
if [ -f %{php_extdir}/apcu.so ]; then
  MOD="-d extension=apcu.so"
fi

: simple NTS module load test, without APC, as optional
%{__php} --no-php-ini \
    --define extension=%{buildroot}%{php_extdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite
pushd NTS
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n $MOD -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
popd

%if %{with_zts}
: simple ZTS module load test, without APC, as optional
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{pecl_name}.so \
    --modules | grep %{pecl_name}

: upstream test suite
pushd ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $MOD -d extension=$PWD/modules/%{pecl_name}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
popd
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%license NTS/COPYING
%doc %{pecl_docdir}/%{pecl_name}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{pecl_name}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{pecl_name}.so
%endif


%files devel
%doc %{pecl_testdir}/%{pecl_name}
%{php_incldir}/ext/%{pecl_name}

%if %{with_zts}
%{php_ztsincldir}/ext/%{pecl_name}
%endif


%changelog
* Thu Dec 29 2016 Carl George <carl.george@rackspace.com> - 2.0.1-1.ius
- Latest upstream

* Sun Dec 11 2016 Carl George <carl.george@rackspace.com> - 2.0.0-2.ius
- Port from Fedora to IUS
- Build with pear1u (via "pecl" virtual provides)
- Re-add scriptlets (file triggers not yet available in EL)
- Install package.xml as %%{pecl_name}.xml, not %%{name}.xml
- Properly install license file

* Mon Nov 21 2016 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- update to 2.0.0

* Mon Nov 14 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.2.20161018git6a2d5b7
- refresh with sources from igbinary instead of old closed repo igbinary7
- rebuild for https://fedoraproject.org/wiki/Changes/php71

* Mon Jun 27 2016 Remi Collet <remi@fedoraproject.org> - 1.2.2-0.1.20151217git2b7c703
- update to 1.2.2dev for PHP 7
- ignore test results, 4 failed tests: igbinary_009.phpt, igbinary_014.phpt
  igbinary_026.phpt and igbinary_unserialize_v1_compatible.phpt
- session support not yet available

* Wed Feb 10 2016 Remi Collet <remi@fedoraproject.org> - 1.2.1-4
- drop scriptlets (replaced by file triggers in php-pear)
- cleanup

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- update to 1.2.0
- open https://github.com/igbinary/igbinary/pull/36

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.12.gitc35d48f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 19 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.11.gitc35d48f
- rebuild for https://fedoraproject.org/wiki/Changes/Php56

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.10.gitc35d48f
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.9.gitc35d48f
- add numerical prefix to extension configuration file

* Mon Mar 10 2014 Remi Collet <rcollet@redhat.com> - 1.1.2-0.8.gitc35d48f
- cleanups and drop SCL support
- install doc in pecl_docdir
- install tests in pecl_testdir (devel)

* Mon Jul 29 2013 Remi Collet <rcollet@redhat.com> - 1.1.2-0.7.gitc35d48f
- adapt for scl

* Sat Jul 27 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-0.6.gitc35d48f
- latest snapshot
- fix build with APCu
- spec cleanups

* Fri Mar 22 2013 Remi Collet <rcollet@redhat.com> - 1.1.2-0.5.git3b8ab7e
- rebuild for http://fedoraproject.org/wiki/Features/Php55

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.4.git3b8ab7e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-0.3.git3b8ab7e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Collet <remi@fedoraproject.org> - 1.1.2-0.2.git3b8ab7e
- enable ZTS extension

* Fri Jan 20 2012 Collet <remi@fedoraproject.org> - 1.1.2-0.1.git3b8ab7e
- update to git snapshot for php 5.4

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep 18 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-3
- fix EPEL-6 build, no arch version for php-devel

* Sat Sep 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-2
- clean spec, adapted filters

* Mon Mar 14 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- version 1.1.1 published on pecl.php.net
- rename to php-pecl-igbinary

* Mon Jan 17 2011 Remi Collet <rpms@famillecollet.com> 1.1.1-1
- update to 1.1.1

* Fri Dec 31 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-3
- updated tests from Git.

* Sat Oct 23 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-2
- filter provides to avoid igbinary.so
- add missing %%dist

* Wed Sep 29 2010 Remi Collet <rpms@famillecollet.com> 1.0.2-1
- initital RPM

