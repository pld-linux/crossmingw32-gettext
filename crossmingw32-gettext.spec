
%define		realname		gettext
%define		snapshot		2003.02.01-1
Summary:	iconv
Name:		crossmingw32-%{realname}
Version:	0.12.1
Release:	1
License:	LGPL
Group:		Libraries
#Source0:	http://dl.sourceforge.net/mingw/%{realname}-%{version}-%{snapshot}-src.tar.bz2
# Source0-md5:	5d4bddd300072315e668247e5b7d5bdb
Source0:	ftp://ftp.gnu.org/pub/gnu/gettext/%{realname}-%{version}.tar.gz
#Patch0:		crossmingw32-gettext.patch
Patch0:		%{realname}-info.patch
Patch1:		%{realname}-aclocal.patch
Patch2:		%{realname}-killkillkill.patch
Patch3:		%{realname}-pl.po-update.patch
Patch4:		%{realname}-no_docs.patch
URL:		http://www.gnu.org/software/gettext/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gtk-doc >= 0.9-4
BuildRequires:	libtool
BuildRequires:	rpm-build >= 4.1-8.2
BuildRequires:	crossmingw32-libiconv
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
CC=%{target}-gcc ; export CC
CXX=%{target}-g++ ; export CXX
LD=%{target}-ld ; export LD
AR=%{target}-ar ; export AR
AS=%{target}-as ; export AS
CROSS_COMPILE=1 ; export CROSS_COMPILE
CPPFLAGS="-I%{arch}/include" ; export CPPFLAGS
RANLIB=%{target}-ranlib ; export RANLIB

rm -f aclocal.m4 missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
cd gettext-runtime
rm -f aclocal.m4 missing
%{__libtoolize}
%{__aclocal} -I m4 -I ../gettext-tools/m4 -I ../autoconf-lib-link/m4
%{__autoconf}
%{__automake}

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
