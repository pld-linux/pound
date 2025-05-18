# TODO: test and merge this branch to master
#
# Conditional build:
%bcond_without	tcmalloc	# tcmalloc allocator

%ifarch x32
%undefine       with_tcmalloc
%endif
Summary:	Pound - reverse-proxy and load-balancer
Summary(pl.UTF-8):	Pound - odwrotne proxy i load-balancer
Name:		pound
Version:	4.16
Release:	1
License:	GPL v3
Group:		Networking/Daemons
#Source0Download: https://github.com/graygnuorg/pound/releases
Source0:	https://github.com/graygnuorg/pound/releases/download/v%{version}/pound-%{version}.tar.gz
# Source0-md5:	b1b5a11e5480b611c5561125cab3600f
Source1:	%{name}.cfg
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source5:	%{name}.tmpfiles
Patch0:		%{name}-man.patch
Patch1:		%{name}-info.patch
URL:		https://github.com/graygnuorg/pound
%{?with_tcmalloc:BuildRequires:	libtcmalloc-devel}
BuildRequires:	openssl-devel >= 1.1
BuildRequires:	pcre-devel >= 7.8
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	texinfo
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
%setup -q
%patch -P0 -p1
%patch -P1 -p1

%build
%configure \
	ac_cv_lib_nsl_gethostbyaddr=no \
	ac_cv_lib_socket_socket=no \
	--disable-hoard \
	--enable-pcreposix \
	--enable-tcmalloc%{!?with_tcmalloc:=no} \
	--with-group=pound \
	--with-maxbuf=6144 \
	--with-owner=pound

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{sysconfig,rc.d/init.d}} \
	$RPM_BUILD_ROOT/var/run/%{name} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}
install -p %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
cp -p %{SOURCE3} $RPM_BUILD_ROOT/etc/sysconfig/%{name}
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 200 %{name}
%useradd -u 200 -d /var/lib/%{name} -g %{name} -c "Pound Daemon" %{name}

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c /usr/share/info > /dev/null 2>&1
/sbin/chkconfig --add %{name}
%service %{name} restart "Pound Daemon"

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c /usr/share/info > /dev/null 2>&1
if [ "$1" = "0" ]; then
	%userremove %{name}
	%groupremove %{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog ChangeLog.apsis NEWS README THANKS
%attr(755,root,root) %{_bindir}/poundctl
%attr(755,root,root) %{_sbindir}/pound
%{_datadir}/pound
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pound.cfg
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_infodir}/pound.info*
%{_mandir}/man5/poundctl.tmpl.5*
%{_mandir}/man8/pound.8*
%{_mandir}/man8/poundctl.8*
%{systemdtmpfilesdir}/%{name}.conf
%dir /var/run/%{name}
