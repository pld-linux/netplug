Summary:	Daemon that responds to network cables being plugged in and out
Summary(pl):	Demon reaguj±cy na pod³±czenia/od³±czenie kabla ethernetowego
Name:		netplug
Version:	1.2.9
Release:	2
License:	GPL
Vendor:		Key Research, Inc. <http://www.keyresearch.com/>
Group:		Networking
Source0:	http://www.red-bean.com/~bos/netplug/%{name}-%{version}.tar.bz2
# Source0-md5:	3bc8062d8033e3f897b015f2889ce5a9
Patch0:		%{name}-opt.patch
URL:		http://www.red-bean.com/~bos/
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
Requires(post):	diffutils
Requires(post,postun):	fileutils
Requires(post):	grep
Requires(post,postun):	sed
Requires:	iproute2 >= 2.4.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sysconfig	/etc/sysconfig/network-scripts

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

%description -l pl
netplug jest demonem zarz±dzaj±cym interfejsami sieciowymi w reakcji
na zdarzenia poziomu po³±czeniowego (link-level), takie jak
pod³±czenie/od³±czenia kabla. Przy pod³±czaniu kabla do karty
sieciowej demon netplug podnosi dany interfejs. Przy od³±czaniu kabla
demon ponownie wy³±cza ten interfejs.

Najbardziej przydaje siê to komputerach typu laptop, które s± ci±gle
wy³±czane z jednej sieci i w³±czane do innej oraz w komputerach
przenoszonych w serwerowni z jednego switcha do drugiego bez potrzeby
rêcznej interwencji.

%prep
%setup -q
%patch -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	install_opts= \
	prefix=$RPM_BUILD_ROOT \
	initdir=$RPM_BUILD_ROOT%{_initrddir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog NEWS README TODO
%attr(755,root,root) /sbin/netplugd
%dir %{_sysconfdir}/netplug
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/netplug/netplugd.conf
%dir %{_sysconfdir}/netplug.d
%attr(644,root,root) %{_sysconfdir}/netplug.d/netplug
%attr(754,root,root) /etc/rc.d/init.d/netplugd
%{_mandir}/man?/*

%post
/sbin/chkconfig --add netplugd

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del netplugd
fi
