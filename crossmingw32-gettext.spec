
%define		realname		gettext
%define		snapshot		2003.02.01-1
Summary:	iconv
Name:		crossmingw32-%{realname}
Version:	0.11.5
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/mingw/%{realname}-%{version}-%{snapshot}-src.tar.bz2
URL:		http://www.gnu.org/software/gettext/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc >= 0.9-4
BuildRequires:	libtool
BuildRequires:	rpm-build >= 4.1-8.2
BuildRequires:	crossmingw32-iconv
BuildRoot:	%{tmpdir}/%{realname}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32
%define		arch			%{_prefix}/%{target}
%define		gccarch			%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib			%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%description
gettext

%prep
%setup -q -n %{realname}-%{version}

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB

#rm -f missing
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}

%configure \
	--target=%{target} \
	--host=%{target_platform} \
	--prefix=%{arch} \
	--disable-static \
	--bindir=%{arch}/bin \
	--libdir=%{arch}/lib \
	--includedir=%{arch}/include
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_mandir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{arch}
