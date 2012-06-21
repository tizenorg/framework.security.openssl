%define soversion 1.0.0

Name:           openssl
Version:        1.0.0f
Release:        1
Summary:        A general purpose cryptography library with TLS implementation

Source:         openssl-%{version}.tar.gz
Source1001:     packaging/openssl.manifest

License:        OpenSSL
Url:            http://www.openssl.org/
Group:          System/Libraries
BuildRequires:  mktemp,
BuildRequires:  sed,
BuildRequires:  util-linux
BuildRequires:  zlib-devel,
Requires:       /bin/mktemp

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package devel
Summary:        Files for development of applications which will use OpenSSL
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       pkgconfig
Requires:       zlib-devel

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
./Configure shared \
	--prefix=%{_prefix} --install-prefix=%{buildroot} linux-generic32 -ldl no-asm no-idea no-camellia enable-md2

make depend
make all

%install

# Install OpenSSL.
make INSTALL_PREFIX=%{buildroot} install

rm -rf %{buildroot}%{_prefix}/ssl/man
rm -rf %{buildroot}%{_prefix}/lib/*.a
rm -rf %{buildroot}%{_prefix}/ssl/misc/*.pl
rm -rf %{buildroot}%{_prefix}/ssl/misc/tsget
rm -rf %{buildroot}%{_bindir}/c_rehash

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest openssl.manifest
%{_bindir}/*
%{_prefix}/ssl
%{_libdir}/engines/*.so
%{_libdir}/libcrypto.so.%{soversion}
%{_libdir}/libssl.so.%{soversion}

%files devel
%manifest openssl.manifest
%{_includedir}/openssl/*
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc


