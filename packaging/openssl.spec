%define soversion 1.0.0

Summary: A general purpose cryptography library with TLS implementation
Name: openssl
Version: 1.0.0f
Release: 1

Source: openssl-%{version}.tar.gz

License: OpenSSL
Group: System/Libraries
URL: http://www.openssl.org/
BuildRequires: mktemp, sed, zlib-devel, util-linux-ng
Requires: /bin/mktemp

%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

%package devel
Summary: Files for development of applications which will use OpenSSL
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, zlib-devel
Requires: pkgconfig

%description devel
OpenSSL is a toolkit for supporting cryptography. The openssl-devel
package contains include files needed to develop applications which
support various cryptographic algorithms and protocols.

%prep
%setup -q

%build 

# ia64, x86_64, ppc, ppc64 are OK by default
# Configure the build tree.  Override OpenSSL defaults with known-good defaults
# usable on all platforms.  The Configure script already knows to use -fPIC and
# RPM_OPT_FLAGS, so we can skip specifiying them here.
./Configure shared \
	--prefix=%{_prefix} --install-prefix=$RPM_BUILD_ROOT linux-generic32 -ldl -no-asm

make depend
make all

%install
rm -rf $RPM_BUILD_ROOT

# Install OpenSSL.
make INSTALL_PREFIX=$RPM_BUILD_ROOT install

rm -rf %{buildroot}/usr/ssl/man
rm -rf %{buildroot}/usr/lib/*.a
rm -rf %{buildroot}/usr/ssl/misc/CA.pl

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files 
%{_prefix}/bin
%{_prefix}/ssl
%{_libdir}/engines/*.so
%{_libdir}/libcrypto.so.%{soversion}
%{_libdir}/libssl.so.%{soversion}

%files devel
/usr/include/openssl/*
%attr(0755,root,root) %{_libdir}/*.so
%attr(0644,root,root) %{_libdir}/pkgconfig/*.pc


