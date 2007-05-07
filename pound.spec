Summary:	Pound - reverse-proxy and load-balancer
Summary(pl.UTF-8):	Pound - reverse-proxy i load-balancer
Name:		pound
Version:	2.3.1
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://www.apsis.ch/pound/Pound-%{version}.tgz
# Source0-md5:	e5dc7677fe2491c3af50120b49f2dc50
Source1:	%{name}.cfg
Source2:	%{name}.init
URL:		http://www.apsis.ch/pound/
BuildRequires:	automake
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%build
cp -f /usr/share/automake/config.sub .
%configure

%{__make} \
	CC="%{__cc}" \
	F_CONF=%{_sysconfdir}/pound/pound.cfg

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/pound,/etc/rc.d/init.d}

install pound    $RPM_BUILD_ROOT%{_sbindir}
install poundctl $RPM_BUILD_ROOT%{_sbindir}
install pound.8  $RPM_BUILD_ROOT%{_mandir}/man8
install poundctl.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pound
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart "%{name} daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/*
%dir %{_sysconfdir}/pound
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pound/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/*
