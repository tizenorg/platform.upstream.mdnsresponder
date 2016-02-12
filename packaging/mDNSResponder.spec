Name:          mdnsresponder
Summary:       DNS Service Discovery
Version:       576.30.4
Release:       1
Source:       %{name}-%{version}.tar.gz
License:       Apache-2.0
Group:         System/Network
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires: bison
BuildRequires: flex
Requires(post):	/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
The DNS Service Discovery API is part of Bonjour, Apple's implementation of
zero-configuration networking(ZEROCONF).

%package devel
Summary:  DNS Service Discovery (Development)
Group:    System/Network
Provides: libdns_sd.so
Requires: %{name} = %{version}-%{release}

%description devel
The DNS Service Discovery API is part of Bonjour, Apple's implementation of
zero-configuration networking(ZEROCONF).

%prep
%setup -q

%build
cd mDNSPosix
make os=tizen %{?_smp_mflags}

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_sbindir}/
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_libdir}/pkgconfig/
mkdir -p %{buildroot}%{_libdir}/systemd/system/
cp mdnsd.service %{buildroot}%{_libdir}/systemd/system/mdnsd.service
mkdir -p %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/
ln -s mdnsd.service %{buildroot}%{_libdir}/systemd/system/multi-user.target.wants/mdnsd.service
mkdir -p %{buildroot}%{_includedir}/
cd mDNSPosix
make install os=tizen DESTDIR=%{buildroot} LIBDIR=/%{?_lib}
ln -sf %{_libdir}/libdns_sd.so.1 %{buildroot}%{_libdir}/libdns_sd.so

%post -p /sbin/ldconfig
%post devel -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%{_sbindir}/mdnsd
%{_bindir}/dns-sd
%{_libdir}/libdns_sd.so*
%attr(644,-,-) %{_libdir}/pkgconfig/*.pc
%attr(644,-,-) %{_libdir}/systemd/system/mdnsd.service
%attr(644,-,-) %{_libdir}/systemd/system/multi-user.target.wants/mdnsd.service

%files devel
%attr(644,-,-) %{_includedir}/*.h
%{_libdir}/libdns_sd.so*
