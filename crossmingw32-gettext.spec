%define		realname		gettext
Summary:	gettext libraries - cross mingw32 version
Summary(pl):	Biblioteki gettext - wersja skro¶na dla mingw32
Name:		crossmingw32-%{realname}
Version:	0.13.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnu.org/pub/gnu/gettext/%{realname}-%{version}.tar.gz
# Source0-md5:	b3477289185e7781527345c14a4565de
Patch0:		%{realname}-info.patch
Patch1:		%{realname}-killkillkill.patch
Patch2:		%{realname}-pl.po-update.patch
Patch3:		%{realname}-am18.patch
Patch4:		%{name}.patch
URL:		http://www.gnu.org/software/gettext/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1.7.5
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-libiconv
BuildRequires:	libtool
Requires:	crossmingw32-libiconv
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}

%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
gettext libraries - cross mingw32 version.

%description -l pl
Biblioteki gettext - wersja skro¶na dla mingw32.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd gettext-runtime
%{__libtoolize}
%{__aclocal} -I m4 -I ../autoconf-lib-link/m4 -I ../gettext-tools/m4 -I ../config/m4
%{__autoconf}
%{__automake}
cd ..

%configure \
	AR="%{target}-ar" \
	RANLIB="%{target}-ranlib" \
	--target=%{target} \
	--host=%{target_platform} \
	--disable-static
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_bindir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_bindir}/libintl-2.dll
#%{_libdir}/libasprintf.a
#%{_libdir}/libasprintf.la
%{_libdir}/libintl.dll.a
%{_libdir}/libintl.la
%{_includedir}/*.h
