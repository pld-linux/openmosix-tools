Summary:	The userland tools of the openMosix-system
Summary(pl):	Narzêdzia przestrzeni u¿ytkownika dla openMosiksa
Name:		openmosix-tools
Version:	0.3.4
Release:	0.2
License:	GPL
Group:		Base/Kernel
Source0:	http://dl.sourceforge.net/openmosix/%{name}-%{version}.tar.bz2
# Source0-md5:	f9c9cee038aa95004a77907b226ff006
URL:		http://openmosix.sourceforge.net/
BuildRequires:	kernel-mosix-headers >= 2.4.22-1
BuildRequires:	ncurses-devel
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		/bin
%define		_sbindir	/sbin
%define		_libdir		/lib

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
Summary:        openMosix headers files
Summary(pl):    openMosix pliki nag³ókowe
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}
                                                                                
%description devel
openMosix heades files.
                                                                                
%description devel -l pl
openMosix pliki nag³ókowe.

%package static
Summary:        Static openMosix libraries
Summary(pl):    Biblioteki statyczne do openMosix'a
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}
                                                                                
%description static
Static openMosix libraries.
                                                                                
%description static -l pl
Biblioteki statyczne do openMosix.

%prep
%setup -q

%build
CPPFLAGS="-I/usr/include/ncurses"
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
%config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/openmosix/openmosix.config
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%dir %{_sysconfdir}/openmosix
%attr(754,root,root) %{_initrddir}/openmosix
%{_mandir}/man1/*

%files devel
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_includedir}/*.h

%files static
%{_libdir}/lib*.a
