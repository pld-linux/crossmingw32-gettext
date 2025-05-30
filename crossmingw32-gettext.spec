%define		realname		gettext
Summary:	gettext libraries - cross MinGW32 version
Summary(pl.UTF-8):	Biblioteki gettext - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	0.25
Release:	2
License:	LGPL v2.1+
Group:		Development/Libraries
Source0:	https://ftp.gnu.org/gnu/gettext/%{realname}-%{version}.tar.lz
# Source0-md5:	7c1ab3685b9ec8da9b0d35f5caf75b2e
Patch0:		%{name}-kill_tools.patch
Patch1:		%{realname}-mingw32.patch
URL:		http://www.gnu.org/software/gettext/
BuildRequires:	autoconf >= 2.64
BuildRequires:	automake >= 1:1.13
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-gcc-c++
BuildRequires:	crossmingw32-libiconv
BuildRequires:	libtool >= 2:2
BuildRequires:	lzip
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo
Requires:	crossmingw32-libiconv
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++
%define		_ssp_cflags		%{nil}

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
gettext libraries - cross MinGW32 version.

%description -l pl.UTF-8
Biblioteki gettext - wersja skrośna dla MinGW32.

%package static
Summary:	Static gettext libraries (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczne biblioteki gettext (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static gettext libraries (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczne biblioteki gettext (wersja skrośna MinGW32).

%package dll
Summary:	DLL gettext libraries for Windows
Summary(pl.UTF-8):	Biblioteki DLL gettext dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-libiconv-dll
Requires:	wine

%description dll
DLL gettext libraries for Windows.

%description dll -l pl.UTF-8
Biblioteki DLL gettext dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch -P0 -p1
%patch -P1 -p1

%{__sed} -i \
	-e 's@m4_esyscmd(\[build-aux/git-version-gen \.tarball-version\])@[%{version}]@' \
	configure.ac
%{__sed} -i \
	-e 's@m4_esyscmd(\[\.\./build-aux/git-version-gen \.\./\.tarball-version\])@[%{version}]@' \
	gettext-runtime/configure.ac \
	gettext-tools/configure.ac

%build
# we can assume Vista to build with system locale_t support, but then build fails on missing LC_GLOBAL_LOCALE
#CPPFLAGS="%{rpmcppflags} -DWINVER=0x0600"
cd gettext-runtime
%{__libtoolize}
%{__aclocal} -I m4 -I ../m4 -I gnulib-m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd intl
%{__libtoolize}
%{__aclocal} -I ../../m4 -I ../m4 -I gnulib-m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../libasprintf
%{__aclocal} -I ../../m4 -I ../m4 -I gnulib-m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../../libtextstyle
%{__libtoolize}
%{__aclocal} -I m4 -I gnulib-m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../gettext-tools
%{__aclocal} -I m4 -I ../gettext-runtime/m4 -I ../m4 -I gnulib-m4 -I libgrep/gnulib-m4 -I libgettextpo/gnulib-m4 -I tests/gnulib-m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd examples
%{__aclocal} -I ../../gettext-runtime/m4 -I ../../m4
%{__autoconf}
%{__automake}
cd ../..
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-csharp \
	--disable-d \
	--disable-modula2 \
	--enable-static \
	--enable-threads=windows \
	--without-bzip2 \
	--without-git \
	--with-xz

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%{__rm} $RPM_BUILD_ROOT%{_bindir}/{{envsubst,gettext,ngettext}.exe,gettext.sh}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/{doc,gettext,locale,man}
%{__rm} -r $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libintl.dll.a
%{_libdir}/libintl.la
%{_libdir}/libasprintf.dll.a
%{_libdir}/libasprintf.la
%{_includedir}/autosprintf.h
%{_includedir}/libintl.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libintl.a
%{_libdir}/libasprintf.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libintl-8.dll
%{_dlldir}/libasprintf-0.dll
