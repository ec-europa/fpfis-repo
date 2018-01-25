# IUS spec file for php71u-pecl-gnupg, forked from:
#
# Fedora spec file for php-pecl-gnupg
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%global pecl_name gnupg
%global with_zts  0%{?__ztsphp:1}
%global ini_name  40-%{pecl_name}.ini
%global php_base  php71e

Name:           %{php_base}-pecl-%{pecl_name}
Summary:        Wrapper around the gpgme library
Version:        1.4.0
Release:        1%{?dist}
Source0:        http://pecl.php.net/get/%{pecl_name}-%{version}.tgz
Source1:        %{pecl_name}.ini

License:        PHP
Group:          Development/Languages
URL:            http://pecl.php.net/package/gnupg

BuildRequires:  %{php_base}-devel
BuildRequires:  pecl >= 1.10.0
BuildRequires:  pcre-devel
BuildRequires:  gpgme-devel >= 1.1

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
This extension provides methods to interact with gnupg


%prep
%setup -qc
mv %{pecl_name}-%{version} NTS

sed -e '/LICENSE/s/role="doc"/role="src"/' -i package.xml

pushd NTS

# Sanity check, really often broken
extver=$(sed -n '/#define PHP_GNUPG_VERSION/{s/.* "//;s/".*$//;p}' php_gnupg.h)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi
popd

%if %{with_zts}
# duplicate for ZTS build
cp -pr NTS ZTS
%endif


%build
pushd NTS
%{_bindir}/phpize
%configure \
   --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}
popd

%if %{with_zts}
pushd ZTS
%{_bindir}/zts-phpize
%configure \
   --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}
popd
%endif


%install

%{__make} install INSTALL_ROOT=%{buildroot} -C NTS

# Install XML package description
install -Dpm 0644 package.xml %{buildroot}%{pecl_xmldir}/%{pecl_name}.xml

# Install config file
install -Dpm 0644 %{SOURCE1} %{buildroot}%{php_inidir}/%{ini_name}

%if %{with_zts}
%{__make} install INSTALL_ROOT=%{buildroot} -C ZTS

# Install config file
install -Dpm 0644 %{SOURCE1} %{buildroot}%{php_ztsinidir}/%{ini_name}
%endif

rm -rf %{buildroot}%{php_incldir}/ext/%{pecl_name}/
%if %{with_zts}
rm -rf %{buildroot}%{php_ztsincldir}/ext/%{pecl_name}/
%endif

%check
# simple module load test
php --no-php-ini \
    --define extension_dir=%{buildroot}%{php_extdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%if %{with_zts}
zts-php --no-php-ini \
    --define extension_dir=%{buildroot}%{php_ztsextdir} \
    --define extension=%{pecl_name}.so \
    --modules | grep %{pecl_name}
%endif

%post
%{pecl_install} %{pecl_xmldir}/%{pecl_name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ]; then
    %{pecl_uninstall} %{pecl_name} >/dev/null || :
fi


%files
%doc ZTS/LICENSE ZTS/README
%{php_extdir}/%{pecl_name}.so
%{pecl_xmldir}/%{pecl_name}.xml
%config(noreplace) %verify(not md5 mtime size) %{php_inidir}/%{ini_name}

%if %{with_zts}
%{php_ztsextdir}/%{pecl_name}.so
%config(noreplace) %verify(not md5 mtime size) %{php_ztsinidir}/%{ini_name}
%endif

%changelog
* Thu Jan 25 2018 Gregory Boddin <gregory@siwhine.net> - 1.4.0
- Initial module import
