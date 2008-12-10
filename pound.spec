Summary:	Pound - reverse-proxy and load-balancer
Summary(pl.UTF-8):	Pound - reverse-proxy i load-balancer
Name:		pound
Version:	2.4.3
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.apsis.ch/pound/Pound-%{version}.tgz
# Source0-md5:	2de4c2ac1023b420b74a1bc08fb93b8a
Patch0:		%{name}-overquote.patch
Patch1:		%{name}-hash-UL.patch
Patch2:		%{name}-logfile.patch
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.sysconfig
URL:		http://www.apsis.ch/pound/
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Requires:	rc-scripts
Provides:	group(pound)
Provides:	user(pound)
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

%build
cp -f /usr/share/automake/config.sub .
%configure \
	--with-maxbuf=2048
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir},/etc/{sysconfig,rc.d/init.d}} \
	$RPM_BUILD_ROOT{/var/log/{%{name},archive/%{name}},/var/run/%{name}}

install pound    $RPM_BUILD_ROOT%{_sbindir}
install poundctl $RPM_BUILD_ROOT%{_sbindir}
install pound.8  $RPM_BUILD_ROOT%{_mandir}/man8
install poundctl.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 200 %{name}
%useradd -u 200 -d /var/lib/%{name} -g %{name} -c "Pound Daemon" %{name}

%post
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
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pound.cfg
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/*
%dir /var/run/%{name}
%dir %attr(751,root,root) /var/log/%{name}
%attr(750,root,root) %dir /var/log/archive/%{name}
