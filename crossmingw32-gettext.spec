#
%bcond_with     bootstrap       # use system GLib
#
Summary:	gettext libraries - cross mingw32 version
Summary(pl.UTF-8):	Biblioteki gettext - wersja skrośna dla mingw32
%define		realname		gettext
Name:		crossmingw32-%{realname}
Version:	0.17
Release:	1
License:	LGPL v2+
Group:		Development/Libraries
Source0:	http://ftp.gnu.org/gnu/gettext/%{realname}-%{version}.tar.gz
# Source0-md5:	58a2bc6d39c0ba57823034d55d65d606
Patch0:		%{realname}-info.patch
Patch1:		%{realname}-libintl_by_gcj.patch
Patch2:		%{realname}-removed_macros.patch
Patch3:		%{name}-kill_tools.patch
URL:		http://www.gnu.org/software/gettext/
BuildRequires:	autoconf >= 2.60
BuildRequires:	automake >= 1:1.10
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-gcc-c++
# just to shorten build (libgettextlib is not packaged anyway)
%{!?with_bootstrap:BuildRequires:	crossmingw32-glib2 >= 2.0}
BuildRequires:	crossmingw32-libiconv
BuildRequires:	libtool
BuildRequires:	texinfo
Requires:	crossmingw32-libiconv
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
gettext libraries - cross mingw32 version.

%description -l pl.UTF-8
Biblioteki gettext - wersja skrośna dla mingw32.

%package static
Summary:	Static gettext libraries (cross mingw32 version)
Summary(pl.UTF-8):	Statyczne biblioteki gettext (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static gettext libraries (cross mingw32 version).

%description static -l pl.UTF-8
Statyczne biblioteki gettext (wersja skrośna mingw32).

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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%{__libtoolize}
cd autoconf-lib-link
%{__aclocal} -I m4 -I ../m4
%{__autoconf}
%{__automake}
cd ../gettext-runtime
%{__libtoolize}
%{__aclocal} -I m4 -I gnulib-m4 -I ../autoconf-lib-link/m4 -I ../m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd libasprintf
%{__aclocal} -I ../m4 -I ../../m4
%{__autoconf}
%{__autoheader}
%{__automake}
cd ../..
%{__aclocal}
%{__autoconf}
%{__automake}

%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-csharp \
	--enable-static

%{__make} \
	SHELL=bash

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias
rm -rf $RPM_BUILD_ROOT%{_datadir}/{aclocal,doc,gettext,locale,man}
rm -rf $RPM_BUILD_ROOT%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libintl.dll.a
%{_libdir}/libintl.la
%{_libdir}/libasprintf.dll.a
%{_libdir}/libasprintf.la
%{_includedir}/*.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libintl.a
%{_libdir}/libasprintf.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libintl-8.dll
%{_dlldir}/libasprintf-0.dll
