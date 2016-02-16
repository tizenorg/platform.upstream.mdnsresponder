Name:       mdnsresponder
Summary:    DNS Service Discovery service with dns-sd library
Version:    576.30.4
Release:    1
Group:      System/Network
License:    Apache-2.0
Source0:    %{name}-%{version}.tar.gz
Source1001:    mdnsresponder.manifest
Source1002:    libdns_sd.manifest
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires: bison
BuildRequires: flex
Requires(post):	/sbin/ldconfig
Requires(postun):	/sbin/ldconfig

%description
The DNS Service Discovery is part of Bonjour, Apple's implementation of
zero-configuration networking(ZEROCONF).

%package -n libdns_sd
Summary:    DNS-SD - client libraries
Requires:   mdnsresponder = %{version}-%{release}

%description -n libdns_sd
Client libraries for DNS-SD: synchronous and asynchronous

%package devel
Summary:  DNS Service Discovery (Development)
Requires:   libdns_sd = %{version}-%{release}
Requires: pkgconfig

%description devel
DNS-SD development files

%prep
%setup -q
cp -a %{SOURCE1001} .
cp -a %{SOURCE1002} .

%build
%if "%{?_lib}" == "lib64"
CONFIG_TIZEN_64BIT=y; export CONFIG_TIZEN_64BIT
%endif

cd mDNSPosix
make os=tizen %{?_smp_mflags}

%install
MAJORVER=`echo %{version} | awk 'BEGIN {FS="."}{print $1}'`

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
%if "%{?_lib}" == "lib64"
CONFIG_TIZEN_64BIT=y; export CONFIG_TIZEN_64BIT
%endif
cd mDNSPosix
make install os=tizen DESTDIR=%{buildroot} LIBDIR=/%{?_lib}
ln -sf %{_libdir}/libdns_sd.so.%{version} %{buildroot}%{_libdir}/libdns_sd.so.576
ln -sf %{_libdir}/libdns_sd.so.%{version} %{buildroot}%{_libdir}/libdns_sd.so

%post
systemctl daemon-reload

if [ $1 = 1 ]; then
    systemctl enable mdnsd.service
fi

systemctl restart mdnsd.service

%preun
if [ $1 = 0 ]; then
    # unistall
    systemctl stop mdnsd.service
fi

%post -n libdns_sd -p /sbin/ldconfig

%postun -n libdns_sd -p /sbin/ldconfig

%files
%manifest mdnsresponder.manifest
%license LICENSE
%attr(755,root,root) %{_sbindir}/mdnsd
%attr(-,root,root) %{_libdir}/systemd/system/mdnsd.service
%attr(-,root,root) %{_libdir}/systemd/system/multi-user.target.wants/mdnsd.service

%files devel
%{_includedir}/*.h
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files -n libdns_sd
%manifest libdns_sd.manifest
%license LICENSE
%{_libdir}/libdns_sd.so*
