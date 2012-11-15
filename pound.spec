Summary:	Pound - reverse-proxy and load-balancer
Summary(pl.UTF-8):	Pound - reverse-proxy i load-balancer
Name:		pound
Version:	2.6
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.apsis.ch/pound/Pound-%{version}.tgz
# Source0-md5:	8c913b527332694943c4c67c8f152071
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source4:	%{name}.logrotate
Source5:	%{name}.tmpfiles
Patch0:		%{name}-hash-UL.patch
Patch1:		%{name}-logfile.patch
Patch2:		%{name}-daemonize.patch
Patch3:		%{name}-log-notice.patch
Patch4:		%{name}-man.patch
URL:		http://www.apsis.ch/pound/
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	openssl-tools
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.644
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	pcre >= 7.8
Requires:	rc-scripts
Provides:	group(pound)
Provides:	user(pound)
Conflicts:	logrotate < 3.7-4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/pound

%description
The Pound program is a reverse proxy, load balancer and HTTPS
front-end for Web server(s). Pound was developped to enable
distributing the load among several Web-servers and to allow for a
convenient SSL wrapper for those Web servers that do not offer it
natively. Pound is distributed under the GPL - no warranty, it's free
to use, copy and give away.

%description -l pl.UTF-8
Program Pound jest odwrotnym proxy, load-balancerem i interfejsem
HTTPS do serwera(ów) WWW. Pount został stworzony by pozwolić na
rozdzielenie obciążenia na kilka serwerów WWW i pozwolić na wygodne
opakowanie SSL-em tych serwerów, które same nie obsługują SSL. Pound
jest rozpowszechniany na licencji GPL - bez gwarancji, z możliwością
swobodnego używania, kopiowania i rozdawania.

%prep
%setup -q -n Pound-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
cp -f /usr/share/automake/config.sub .
%configure \
	--with-maxbuf=2048
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir},/etc/{sysconfig,logrotate.d,rc.d/init.d}} \
	$RPM_BUILD_ROOT{/var/log/{%{name},archive/%{name}},/var/run/%{name}} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

install -p pound    $RPM_BUILD_ROOT%{_sbindir}
install -p poundctl $RPM_BUILD_ROOT%{_sbindir}
cp -p pound.8  $RPM_BUILD_ROOT%{_mandir}/man8
cp -p poundctl.8 $RPM_BUILD_ROOT%{_mandir}/man8
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE4} $RPM_BUILD_ROOT/etc/logrotate.d/%{name}

install %{SOURCE5} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 200 %{name}
%useradd -u 200 -d /var/lib/%{name} -g %{name} -c "Pound Daemon" %{name}

%post
for a in access.log pound.log; do
	if [ ! -f /var/log/%{name}/$a ]; then
		touch /var/log/%{name}/$a
		chown pound:pound /var/log/%{name}/$a
		chmod 644 /var/log/%{name}/$a
	fi
done
/sbin/chkconfig --add %{name}
%service %{name} restart "Pound Daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc README FAQ CHANGELOG z*.py
%attr(755,root,root) %{_sbindir}/pound
%attr(755,root,root) %{_sbindir}/poundctl
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pound.cfg
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/*
%{systemdtmpfilesdir}/%{name}.conf
%dir /var/run/%{name}
%dir %attr(751,root,root) /var/log/%{name}
%attr(750,root,root) %dir /var/log/archive/%{name}
