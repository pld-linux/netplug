# TODO
# - pld initscript
Summary:	Daemon that responds to network cables being plugged in and out
Summary(pl.UTF-8):	Demon reagujący na podłączenia/odłączenie kabla ethernetowego
Name:		netplug
Version:	1.2.9.2
Release:	1
License:	GPL
Group:		Networking
Source0:	http://www.red-bean.com/~bos/netplug/%{name}-%{version}.tar.bz2
# Source0-md5:	1d6db99536bdf875ce441f2c0e45ebf2
Patch0:		%{name}-opt.patch
URL:		http://www.red-bean.com/~bos/
Requires(post,preun):	/sbin/chkconfig
Requires:	iproute2 >= 2.4.7
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sysconfig	/etc/sysconfig/network-scripts
%define		_sbindir	/sbin

%description
netplug is a daemon that manages network interfaces in response to
link-level events such as cables being plugged in and out. When a
cable is plugged into an interface, the netplug daemon brings that
interface up. When the cable is unplugged, the daemon brings that
interface back down.

This is extremely useful for systems such as laptops, which are
constantly being unplugged from one network and plugged into another,
and for moving systems in a machine room from one switch to another
without a need for manual intervention.

%description -l pl.UTF-8
netplug jest demonem zarządzającym interfejsami sieciowymi w reakcji
na zdarzenia poziomu połączeniowego (link-level), takie jak
podłączenie/odłączenia kabla. Przy podłączaniu kabla do karty
sieciowej demon netplug podnosi dany interfejs. Przy odłączaniu kabla
demon ponownie wyłącza ten interfejs.

Najbardziej przydaje się to komputerach typu laptop, które są ciągle
wyłączane z jednej sieci i włączane do innej oraz w komputerach
przenoszonych w serwerowni z jednego switcha do drugiego bez potrzeby
ręcznej interwencji.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	install_opts= \
	prefix=$RPM_BUILD_ROOT \
	initdir=$RPM_BUILD_ROOT/etc/rc.d/init.d \
	mandir=$RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add netplugd

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del netplugd
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README TODO
%attr(755,root,root) %{_sbindir}/netplugd
%dir %{_sysconfdir}/netplug
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/netplug/netplugd.conf
%dir %{_sysconfdir}/netplug.d
%attr(755,root,root) %{_sysconfdir}/netplug.d/netplug
%attr(754,root,root) /etc/rc.d/init.d/netplugd
%{_mandir}/man?/*
