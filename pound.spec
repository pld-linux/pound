# NOTE: pound 3.x has been withdrawn; for pound 4.x (based on fork from pound 2.8)
# see pound-4 branch - to be tested and merged
#
# Conditional build:
%bcond_without	tcmalloc	# tcmalloc allocator

%ifarch x32
%undefine       with_tcmalloc
%endif
Summary:	Pound - reverse-proxy and load-balancer
Summary(pl.UTF-8):	Pound - odwrotne proxy i load-balancer
Name:		pound
Version:	3.0.2
Release:	4
License:	GPL v3
Group:		Networking/Daemons
Source0:	http://www.apsis.ch/pound/Pound-%{version}.tgz
# Source0-md5:	c0f5af4cd6aa184c00f4848ae1c4536a
Source1:	%{name}.yaml
Source2:	%{name}.init
Source3:	%{name}.sysconfig
Source5:	%{name}.tmpfiles
Patch0:		tcmalloc.patch
Patch1:		pound-man.patch
Patch2:		mbedtls3.patch
URL:		https://github.com/graygnuorg/pound
BuildRequires:	cmake >= 3.0
%{?with_tcmalloc:BuildRequires:	libtcmalloc-devel}
BuildRequires:	mbedtls-devel
BuildRequires:	nanomsg-devel
BuildRequires:	pcre2-8-devel
BuildRequires:	pcre2-posix-devel
BuildRequires:	rpmbuild(macros) >= 1.644
BuildRequires:	yaml-devel
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
%setup -q -n Pound-%{version}
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

%build
install -d build
cd build
%cmake .. \
	%{?with_tcmalloc:-DWANT_TCMALLOC:BOOL=ON}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir},/etc/{sysconfig,rc.d/init.d}} \
	$RPM_BUILD_ROOT/var/run/%{name} \
	$RPM_BUILD_ROOT%{systemdtmpfilesdir}

install -p build/pound $RPM_BUILD_ROOT%{_sbindir}
cp -p man/pound.8  $RPM_BUILD_ROOT%{_mandir}/man8
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
%doc README.md
%attr(755,root,root) %{_sbindir}/pound
%dir %{_sysconfdir}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pound.yaml
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%{_mandir}/man8/pound.8*
%{systemdtmpfilesdir}/%{name}.conf
%dir /var/run/%{name}
