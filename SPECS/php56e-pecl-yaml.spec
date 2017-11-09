# IUS spec file for php56u-pecl-yaml, forked from:
#
# Fedora spec file for php-pecl-yaml
#
# Copyright (c) 2010-2014 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#

%global extname   yaml
%global with_zts  0%{?__ztsphp:1}
%global ini_name  40-%{extname}.ini
%global php_base  php56e

Summary:        Replacement for the standard PHP serializer
Name:           %{php_base}-pecl-%{extname}
Version:        1.3.1 
Release:        1%{?dist}
Source0:        http://pecl.php.net/get/%{extname}-%{version}.tgz
Source1:        yaml.ini
License:        BSD
Group:          System Environment/Libraries
URL:            http://pecl.php.net/package/yaml
BuildRequires:  %{php_base}-pear
BuildRequires:  %{php_base}-devel
BuildRequires:  %{php_base}-pecl-apcu-devel >= 3.1.7

Requires(post): %{php_base}-pear
Requires(postun): %{php_base}-pear
Requires:       %{php_base}(zend-abi) = %{php_zend_api}
Requires:       %{php_base}(api) = %{php_core_api}

# provide the stock name
Provides:       php-pecl-%{extname} = %{version}
Provides:       php-pecl-%{extname}%{?_isa} = %{version}

# provide the stock and IUS names without pecl
Provides:       php-%{extname} = %{version}
Provides:       php-%{extname}%{?_isa} = %{version}
Provides:       %{php_base}-%{extname} = %{version}
Provides:       %{php_base}-%{extname}%{?_isa} = %{version}

# provide the stock and IUS names in pecl() format
Provides:       php-pecl(%{extname}) = %{version}
Provides:       php-pecl(%{extname})%{?_isa} = %{version}
Provides:       %{php_base}-pecl(%{extname}) = %{version}
Provides:       %{php_base}-pecl(%{extname})%{?_isa} = %{version}

# conflict with the stock name
Conflicts:      php-pecl-%{extname} < %{version}

%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_provides_in: %filter_provides_in %{php_ztsextdir}/.*\.so$}
%{?filter_setup}


%description
Igbinary is a drop in replacement for the standard PHP serializer.

Instead of time and space consuming textual representation, 
yaml stores PHP data structures in a compact binary form. 
Savings are significant when using memcached or similar memory
based storages for serialized data.


%package devel
Summary:        Igbinary developer files (header)
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{php_base}-devel%{?_isa}

# provide the stock name
Provides:       php-pecl-%{extname}-devel = %{version}
Provides:       php-pecl-%{extname}-devel%{?_isa} = %{version}

# provide the stock and IUS names without pecl
Provides:       php-%{extname}-devel = %{version}
Provides:       php-%{extname}-devel%{?_isa} = %{version}
Provides:       %{php_base}-%{extname}-devel = %{version}
Provides:       %{php_base}-%{extname}-devel%{?_isa} = %{version}

# conflict with the stock name
Conflicts:      php-pecl-%{extname}-devel < %{version}


%description devel
These are the files needed to compile programs using Igbinary


%prep
%setup -q -c

mv %{extname}-%{version} NTS

sed -e '/COPYING/s/role="doc"/role="src"/' -i package.xml

pushd NTS

# Check version
extver=$(sed -n '/#define PHP_IGBINARY_VERSION/{s/.* "//;s/".*$//;p}' src/php5/yaml.h)
if test "x${extver}" != "x%{version}%{?prever}"; then
   : Error: Upstream version is ${extver}, expecting %{version}%{?prever}.
   exit 1
fi
popd

%if %{with_zts}
cp -r NTS ZTS
%endif


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

install -D -m 644 package.xml %{buildroot}%{pecl_xmldir}/%{extname}.xml

install -D -m 644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

# Install the ZTS stuff
%if %{with_zts}
make install -C ZTS INSTALL_ROOT=%{buildroot}
install -D -m 644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

# Test & Documentation
pushd NTS
for i in $(grep 'role="test"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_testdir}/%{extname}/tests/$i
done
for i in $(grep 'role="doc"' ../package.xml | sed -e 's/^.*name="//;s/".*$//')
do install -Dpm 644 $i %{buildroot}%{pecl_docdir}/%{extname}/$i
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
    --define extension=%{buildroot}%{php_extdir}/%{extname}.so \
    --modules | grep %{extname}

: upstream test suite
pushd NTS
TEST_PHP_EXECUTABLE=%{__php} \
TEST_PHP_ARGS="-n $MOD -d extension=$PWD/modules/%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__php} -n run-tests.php --show-diff
popd

%if %{with_zts}
: simple ZTS module load test, without APC, as optional
%{__ztsphp} --no-php-ini \
    --define extension=%{buildroot}%{php_ztsextdir}/%{extname}.so \
    --modules | grep %{extname}

: upstream test suite
pushd ZTS
TEST_PHP_EXECUTABLE=%{__ztsphp} \
TEST_PHP_ARGS="-n $MOD -d extension=$PWD/modules/%{extname}.so" \
NO_INTERACTION=1 \
REPORT_EXIT_STATUS=1 \
%{__ztsphp} -n run-tests.php --show-diff
popd
%endif


%post
%{pecl_install} %{pecl_xmldir}/%{extname}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
    %{pecl_uninstall} %{extname} >/dev/null || :
fi


%files
%license NTS/COPYING
%doc %{pecl_docdir}/%{extname}
%config(noreplace) %{php_inidir}/%{ini_name}
%{php_extdir}/%{extname}.so
%{pecl_xmldir}/%{extname}.xml

%if %{with_zts}
%config(noreplace) %{php_ztsinidir}/%{ini_name}
%{php_ztsextdir}/%{extname}.so
%endif


%files devel
%doc %{pecl_testdir}/%{extname}
%{php_incldir}/ext/%{extname}

%if %{with_zts}
%{php_ztsincldir}/ext/%{extname}
%endif


%changelog
* Thu Nov 9 2017 Gregory Boddin <gregory@siwhine.net> 1.3.1
- initital RPM

