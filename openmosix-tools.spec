Summary:	The userland tools of the openMosix-system
Summary(pl):	Narzêdzia przestrzeni u¿ytkownika dla openMosiksa
Name:		openmosix-tools
%define	ver	0.3.6
%define	subver	2
Version:	%{ver}.%{subver}
Release:	0.9
License:	GPL
Group:		Base/Kernel
Source0:	http://heanet.dl.sourceforge.net/openmosix/%{name}-%{ver}-%{subver}.tar.gz
# Source0-md5:	e947c622b945fda7f24a949b73ba5280
Source1:	openmosix.init
Source2:	openmosix.sysconfig
Patch0:		%{name}-source_path.patch
URL:		http://openmosix.sourceforge.net/
BuildRequires:	kernel-mosix-headers >= 2.4.22-4.1
BuildRequires:	ncurses-devel
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		kmosix_ver	2.4.22
%define		_kernelsrcdir	/usr/src/linux-%{kmosix_ver}
%define		_bindir		/bin
%define		_sbindir	/sbin
%define		_libdir		/%{_lib}

%description
openMosix is a Linux kernel extension for single-system image
clustering. This package contains the necessary user-land tools for an
openMosix cluster. It also contains openMosix versions of ps and top
(mps and mtop) that has an additional column which shows on what node
the processes are running.

%description -l pl
openMosix to rozszerzenie j±dra Linuksa o klastowanie odwzorowuj±ce
pojedynczy system. Ten pakiet zawiera narzêdzia przestrzeni
u¿ytkownika potrzebne dla klastrów openMosix. Zawiera tak¿e
openmosiksowe wersje narzêdzi ps i top (mps i mtop), maj±ce dodatkow±
kolumnê, w której pokazywany jest wêze³, na którym dzia³a proces.

%package devel
Summary:	openMosix headers files
Summary(pl):	Pliki nag³ówkowe openMosiksa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description devel
openMosix heades files.

%description devel -l pl
Pliki nag³ówkowe openMosiksa.

%package static
Summary:	Static openMosix libraries
Summary(pl):	Biblioteki statyczne do openMosiksa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static openMosix libraries.

%description static -l pl
Biblioteki statyczne do openMosiksa.

%prep
%setup -q -n %{name}-%{ver}-%{subver}

%patch0 -p1

%build
CPPFLAGS="-I/usr/include/ncurses"
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--enable-rpmbuild \
	--with-kerneldir=%{_kernelsrcdir} \
	--with-sysvdir=%{_initrddir}

%{__make} \
	all

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT/etc/rc.d/init.d/openmosix
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/openmosix
install -d $RPM_BUILD_ROOT/etc/sysconfig
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/openmosix

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
if [ "$1" = "1" ] ; then
	/sbin/chkconfig --add openmosix
	echo -e "\nEdit /etc/openmosix.map if you don't want to use the autodiscovery daemon.\n"
fi

%preun
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del openmosix
fi

%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/openmosix.map
%config(noreplace) %verify(not size mtime md5) /etc/sysconfig/openmosix
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
#%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(754,root,root) %{_initrddir}/openmosix
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*
%{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
