Summary:	Pound - reverse-proxy and load-balancer
Summary(pl):	Pound - reverse-proxy i load-balancer
Name:		pound
Version:	1.10
Release:	1
License:	GPL
Group:		Networking/Daemons
Vendor:		Robert Segall <roseg@apsis.ch>
Source0:	http://www.apsis.ch/pound/Pound-%{version}.tgz
# Source0-md5:	5792fd804907cc617e37607c6783d5f7
Source1:	%{name}.cfg
Source2:	%{name}.init
URL:		http://www.apsis.ch/pound/
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7d
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

%description -l pl
Program Pound jest odwrotnym proxy, load-balancerem i interfejsem
HTTPS do serwera(ów) WWW. Pount zosta³ stworzony by pozwoliæ na
rozdzielenie obci±¿enia na kilka serwerów WWW i pozwoliæ na wygodne
opakowanie SSL-em tych serwerów, które same nie obs³uguj± SSL. Pound
jest rozpowszechniany na licencji GPL - bez gwarancji, z mo¿liwo¶ci±
swobodnego u¿ywania, kopiowania i rozdawania.

%prep
%setup -q -n Pound-%{version}

%build
cp -f %{_datadir}/libtool/config.sub .
%configure

%{__make} \
	F_CONF=%{_sysconfdir}/pound/pound.cfg

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man8,%{_sysconfdir}/pound,/etc/rc.d/init.d}

install pound 	$RPM_BUILD_ROOT%{_bindir}
install pound.8 $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pound
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" -a -f %{_var}/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} stop 1>&2
fi
/sbin/chkconfig --del %{name}

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%dir %{_sysconfdir}/pound
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pound/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/*
