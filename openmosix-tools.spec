Summary:	The userland tools of the openMosix-system
Summary(pl):	Narzedzia przestrzeni uzytkownika dla openMosixa
Name:		openmosix-tools
Version:	0.3.4
Release:	0.1
License:	GPL
Source0:	http://dl.sourceforge.net/sourceforge/openmosix/%{name}-%{version}.tar.bz2
URL:		http://openmosix.sourceforge.net/
Group:		Base/Kernel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)


%description
openMosix is a Linux kernel extension for single-system image
clustering. This package contains the necessary user-land tools for an
openMosix cluster. It also contains openMosix versions of ps and top
(mps and mtop) that has an additional column which shows on what node
the processes are running.

%description -l pl


%prep

%setup -q

%build
./configure --enable-rpmbuild --bindir=/bin --sbindir=/sbin --includedir=%{_includedir} --mandir=%{_mandir} --libdir=/lib --with-kerneldir=%{_kernelsrcdir}-openmosix
%{__make} all

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%pre

%post
/sbin/ldconfig
chkconfig --add openmosix
if [ "$1" = "1" ] ; then  # first install
   # Add mosrun-commands in /etc/inittab
   perl -pi -e 's!:(/etc/rc.d/rc)!:/bin/mosrun -h $1!' /etc/inittab
   perl -pi -e 's!:(/sbin/update)!:/bin/mosrun -h $1!' /etc/inittab
   perl -pi -e 's!:(/sbin/shutdown)!:/bin/mosrun -h $1!' /etc/inittab
   # Add nolock-command in /etc/init.d/sshd
   perl -i -e 'local $/; $_ = <>; s!(start\(\)\s+{\n)!$1\ttest -f /proc/\$\$/lock && echo 0 \> /proc/\$\$/lock\n\n!; print' /etc/init.d/sshd
   # Add mfs to slocate.cron
   perl -pi -e 's!(/usr/bin/updatedb -f \"nfs)!$1,mfs!' /etc/cron.daily/slocate.cron
   # Tell user to edit mosix.map
   echo -e "\nEdit /etc/openmosix.map if you don't want to use the autodiscovery daemon.\n"
fi


%preun
if [ "$1" = "0" ] ; then # last uninstall
   # Remove links to startup-script
   chkconfig --del openmosix
   # Remove mosrun-commands in /etc/inittab
   perl -pi -e 's!:/bin/mosrun -h !:!' /etc/inittab
   # Remove nolock-command in /etc/rc.d/init.d/sshd
   perl -i -e 'local $/; $_ = <>; s!\ttest -f /proc/\$\$/lock && echo 0 \> /proc/\$\$/lock\n\n!!g; print' /etc/init.d/sshd
   # Remove mfs from slocate.cron
   perl -pi -e 's/mfs,//' /etc/cron.daily/slocate.cron
fi


%postun
/sbin/ldconfig


%files
%defattr(644,root,root,755)
%dir %{_sysconfdir}/openmosix
%config %{_sysconfdir}/openmosix.map
%config %{_sysconfdir}/openmosix/openmosix.config
%config %{_sysconfdir}/init.d/openmosix
%doc %{_mandir}/man1/*
/bin/*
/lib/*
/sbin/*
%{_includedir}/*
