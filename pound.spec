Summary:	Pound - reverse-proxy and load-balancer
Summary(pl):	Pound - reverse-proxy i load-balancer
Name:		pound
Version:	0.7
Release:	1
License:	GPL
Group:		Networking/Daemons
Vendor:		Robert Segall - roseg@apsis.ch
Source0:	http://www.apsis.ch/pound/Pound-%{version}.tgz
Source1:	%{name}.cfg
Source2:	%{name}.init
Patch0:		pound-getregexp.patch
URL:		http://www.apsis.ch/pound/
BuildRequires:	openssl-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Pound program is a reverse proxy, load balancer and HTTPS
front-end for Web server(s). Pound was developped to enable
distributing the load among several Web-servers and to allow for a
convenient SSL wrapper for those Web servers that do not offer it
natively. Pound is distributed under the GPL - no warranty, it's free
to use, copy and give away.

%prep
%setup -q -n pound
%patch0 -p0

%build
%{__make} F_CONF=%{_sysconfdir}/pound/pound.cfg

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man8,%{_sysconfdir}/{pound/,rc.d/init.d}}

install pound 	$RPM_BUILD_ROOT%{_bindir}
install pound.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pound/
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/%{name}

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
        %{_sysconfdir}/rc.d/init.d/%{name} restart 1>&2
else    
        echo "Run \"%{_sysconfdir}/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" -a -f %{_var}/lock/subsys/%{name} ]; then
        %{_sysconfdir}/rc.d/init.d/%{name} stop 1>&2
fi
/sbin/chkconfig --del %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%attr(644,root,root) %{_mandir}/man8/*
%attr( 644,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/pound/*
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/%{name}
%dir %{_sysconfdir}/pound/
