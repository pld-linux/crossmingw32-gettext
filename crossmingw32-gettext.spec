#
# Conditional build:
%bcond_without	asprintf	# without libasprintf (in C++)
#
%define		realname		gettext
Summary:	gettext libraries - cross mingw32 version
Summary(pl):	Biblioteki gettext - wersja skro¶na dla mingw32
Name:		crossmingw32-%{realname}
Version:	0.14.3
Release:	1
License:	LGPL
Group:		Libraries
Source0:	ftp://ftp.gnu.org/gnu/gettext/%{realname}-%{version}.tar.gz
# Source0-md5:	14c2644c2f3b0eb67d5db7ee389547de
Patch0:		%{realname}-info.patch
Patch1:		%{realname}-killkillkill.patch
Patch2:		%{name}.patch
URL:		http://www.gnu.org/software/gettext/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake >= 1:1.7.5
BuildRequires:	crossmingw32-gcc
%{?with_asprintf:BuildRequires:	crossmingw32-gcc-c++}
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

%build
# it's m4_included somewhere
install %{_aclocaldir}/libtool.m4 config/m4/libtool.m4
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd autoconf-lib-link
%{__aclocal} -I m4 -I ../config/m4
%{__autoconf}
%{__automake}
cd ../gettext-runtime
%{__aclocal} -I m4 -I ../autoconf-lib-link/m4 -I ../gettext-tools/m4 -I ../config/m4
%{__autoconf}
%{__automake}
cd ..

%configure \
	AR="%{target}-ar" \
	RANLIB="%{target}-ranlib" \
	--target=%{target} \
	--host=%{target_platform} \
	--disable-csharp \
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
%{_bindir}/libintl-3.dll
%if %{with asprintf}
%{_libdir}/libasprintf.a
%{_libdir}/libasprintf.la
%endif
%{_libdir}/libintl.dll.a
%{_libdir}/libintl.la
%{_includedir}/*.h
