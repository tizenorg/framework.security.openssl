%define soversion 1.0.0
%define _unpackaged_files_terminate_build 0

Name:           openssl
Version:        1.0.1s
Release:        1
Summary:        A general purpose cryptography library with TLS implementation

Source:         openssl-%{version}.tar.gz
Source1001:     packaging/openssl.manifest

License:        OpenSSL
Url:            http://www.openssl.org/
Group:          System/Libraries

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package devel
Summary:        Files for development of applications which will use OpenSSL
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.


%prep
%setup -q

%build
cp %{SOURCE1001} .
# ia64, x86_64, ppc, ppc64 are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.

# Build the "Fips capable" openssl libraries.
cd openssl-fips/

chmod +x ./config
./config no-asm
make
make install INSTALLTOP=$PWD/../fips
cd ..

BINARY_FORMAT=armv4

%ifarch %{ix86}
BINARY_FORMAT=generic32
%endif

%ifarch x86_64
BINARY_FORMAT=x86_64
%endif

# Build the "Fips capable" openssl libraries.
./Configure fips shared \
    --with-fipsdir=$PWD/fips --prefix=%{_prefix} --libdir=%{_lib} --install-prefix=$RPM_BUILD_ROOT linux-$BINARY_FORMAT -ldl no-asm enable-md2 no-idea no-camellia no-rc5

make depend

# add '-g' flag to make debug symbol
find -name "Makefile" -exec sed -i "s#\-O[0-3]#& -g#g" {} \;

make all

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
# Install OpenSSL.
make INSTALL_PREFIX=$RPM_BUILD_ROOT install
rm -rf %{buildroot}/usr/ssl/man
rm -rf %{buildroot}/usr/share/
mkdir -p %{buildroot}/usr/share/license
cp LICENSE %{buildroot}/usr/share/license/%{name}

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest openssl.manifest
%defattr(-,root,root,-)
%{_prefix}/bin/openssl
%{_prefix}/ssl
%{_libdir}/engines/*.so
%{_libdir}/libcrypto.so.%{soversion}
%{_libdir}/libssl.so.%{soversion}
/usr/share/license/%{name}

%files devel
%manifest openssl.manifest
%defattr(-,root,root,-)
%{_prefix}/include/openssl
%attr(0644,root,root) %{_libdir}/*.a
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc

