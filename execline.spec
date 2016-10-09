# TODO
# - split -libs?
# - check/cleanup/handle "/command/" paths
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries

Summary:	A non-interactive scripting language similar to SH
Name:		execline
Version:	2.1.5.0
Release:	0.1
License:	ISC
Group:		Libraries
Source0:	http://www.skarnet.org/software/execline/%{name}-%{version}.tar.gz
# Source0-md5:	cc3271375b89a0e3e4ed7e4b659fefe4
URL:		http://www.skarnet.org/software/execline/
BuildRequires:	make >= 4.0
BuildRequires:	sed >= 4.0
BuildRequires:	skalibs-devel >= 2.3.10.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# FIXME. temporarily disable. fix this later
%define		skip_post_check_so	libexecline.so.%{version}

%description
execline is a (non-interactive) scripting language, like sh; but its
syntax is quite different from a traditional shell syntax. The
execlineb program is meant to be used as an interpreter for a text
file; the other commands are essentially useful inside an execlineb
script.

execline is as powerful as a shell: it features conditional loops,
getopt-style option handling, filename globbing, and more. Meanwhile,
its syntax is far more logic and predictable than the shell's syntax,
and has no security issues.

%package devel
Summary:	Header files for %{name} library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{name} library.

%prep
%setup -q

sed -i "s~tryldflag LDFLAGS_AUTO -Wl,--hash-style=both~:~" configure

%build
%configure \
	--enable-shared \
	--disable-static \
	--disable-allstatic \
	--bindir=%{_bindir} \
	--sbindir=%{_sbindir} \
	--dynlibdir=%{_libdir} \
	--libdir=%{_libdir} \
	--datadir=%{_sysconfdir} \
	--sysdepdir=%{_libdir}/skalibs \
	--dynlibdir=%{_libdir} \
	--with-lib=%{_libdir}/skalibs \
	--with-sysdeps=%{_libdir}/skalibs \
	%{nil}

%if 0
echo "%{__cc} %{rpmcflags} -Wall" > conf-compile/conf-cc
echo "%{__cc} %{rpmldflags}" > conf-compile/conf-dynld
echo %{_libdir}/%{name} > conf-compile/conf-install-library
echo %{_libdir}/%{name} > conf-compile/conf-install-library.so
echo "%{__cc} %{rpmldflags}" > conf-compile/conf-ld
rm -f conf-compile/flag-slashpackage
echo > conf-compile/stripbins
echo > conf-compile/striplibs
echo %{_libdir}/skalibs/sysdeps > conf-compile/import
echo %{_includedir}/skalibs > conf-compile/path-include
echo %{_libdir} > conf-compile/path-library
echo %{_libdir} > conf-compile/path-library.so
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# SONAME: libexecline.so.2.1
# so this is junk
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libexecline.so.2.1.5

# file %{_bindir}/import from install of execline-2.1.5.0-0.1.x86_64 conflicts with file from package ImageMagick-6.9.5.2-1.x86_64
%{__rm} $RPM_BUILD_ROOT%{_bindir}/import

%if 0
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_libdir},%{_bindir},%{_includedir}/%{name}}
install -p command/* $RPM_BUILD_ROOT%{_bindir}
cp -a library.so/*  $RPM_BUILD_ROOT%{_libdir}
cp -a etc/* $RPM_BUILD_ROOT%{_sysconfdir}
cp -a include/* $RPM_BUILD_ROOT%{_includedir}

%if %{with static_libs}
cp -p library/* $RPM_BUILD_ROOT%{_libdir}
%endif

%{__rm} $RPM_BUILD_ROOT%{_libdir}/libexecline.so.1.2
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc doc/*
%if 0
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/execline-shell
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/execline-startup
%endif
%attr(755,root,root) %{_bindir}/background
%attr(755,root,root) %{_bindir}/backtick
%attr(755,root,root) %{_bindir}/cd
%attr(755,root,root) %{_bindir}/define
%attr(755,root,root) %{_bindir}/dollarat
%attr(755,root,root) %{_bindir}/elgetopt
%attr(755,root,root) %{_bindir}/elgetpositionals
%attr(755,root,root) %{_bindir}/elglob
%attr(755,root,root) %{_bindir}/emptyenv
%attr(755,root,root) %{_bindir}/exec
#%attr(755,root,root) %{_bindir}/execline
%attr(755,root,root) %{_bindir}/execlineb
%attr(755,root,root) %{_bindir}/exit
%attr(755,root,root) %{_bindir}/export
%attr(755,root,root) %{_bindir}/fdblock
%attr(755,root,root) %{_bindir}/fdclose
%attr(755,root,root) %{_bindir}/fdmove
%attr(755,root,root) %{_bindir}/fdreserve
%attr(755,root,root) %{_bindir}/fdswap
#%attr(755,root,root) %{_bindir}/for
#%attr(755,root,root) %{_bindir}/forbacktick
%attr(755,root,root) %{_bindir}/forbacktickx
%attr(755,root,root) %{_bindir}/foreground
%attr(755,root,root) %{_bindir}/forstdin
%attr(755,root,root) %{_bindir}/forx
%attr(755,root,root) %{_bindir}/getcwd
%attr(755,root,root) %{_bindir}/getpid
%attr(755,root,root) %{_bindir}/heredoc
%attr(755,root,root) %{_bindir}/homeof
%attr(755,root,root) %{_bindir}/if
%attr(755,root,root) %{_bindir}/ifelse
%attr(755,root,root) %{_bindir}/ifte
%attr(755,root,root) %{_bindir}/ifthenelse
#%attr(755,root,root) %{_bindir}/import
%attr(755,root,root) %{_bindir}/importas
#%attr(755,root,root) %{_bindir}/loopwhile
%attr(755,root,root) %{_bindir}/loopwhilex
%attr(755,root,root) %{_bindir}/multidefine
%attr(755,root,root) %{_bindir}/multisubstitute
%attr(755,root,root) %{_bindir}/pipeline
%attr(755,root,root) %{_bindir}/piperw
%attr(755,root,root) %{_bindir}/redirfd
%attr(755,root,root) %{_bindir}/runblock
%attr(755,root,root) %{_bindir}/shift
%attr(755,root,root) %{_bindir}/trap
%attr(755,root,root) %{_bindir}/tryexec
%attr(755,root,root) %{_bindir}/umask
%attr(755,root,root) %{_bindir}/unexport
%attr(755,root,root) %{_bindir}/wait
%attr(755,root,root) %{_bindir}/withstdinas

# -libs
%attr(755,root,root) %{_libdir}/libexecline.so.*.*.*.*
%ghost %{_libdir}/libexecline.so.2.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/execline
%{_libdir}/libexecline.so
