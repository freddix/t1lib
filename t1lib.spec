Summary:	A library for character- and string-glyphs from Adobe Type 1 fonts
Name:		t1lib
Version:	5.1.2
Release:	3
License:	LGPL
Group:		Libraries
Source0:	ftp://sunsite.unc.edu/pub/Linux/libs/graphics/%{name}-%{version}.tar.gz
# Source0-md5:	a5629b56b93134377718009df1435f3c
Source1:	%{name}-fonts.Fontmap
Source2:	%{name}-fonts.fonts.scale
Source3:	%{name}config
Patch0:		%{name}-doc.patch
Patch1:		%{name}-config.patch
Patch2:		%{name}-KernMapSize.patch
Patch3:		%{name}-man.patch
Patch4:		%{name}-xglyph.patch
Patch5:		%{name}-link.patch
Patch6:		%{name}-aclocal.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	xorg-libXaw-devel
Requires(post):	fontpostinst
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_t1fontsdir	%{_fontsdir}/Type1
%define		_t1afmdir	%{_t1fontsdir}/afm
%define		_datadir	/etc

%description
t1lib is a library distributed under the GNU General Public Library
License for generating character- and string-glyphs from Adobe Type 1
fonts under UNIX. t1lib uses most of the code of the X11 rasterizer
donated by IBM to the X11-project. But some disadvantages of the
rasterizer being included in X11 have been eliminated.

%package fonts
Summary:	Type 1 fonts
Group:		Fonts
Requires(post,postun):	fontpostinst
Requires:	%{_fontsdir}/Type1

%description fonts
Type 1 fonts.

%package devel
Summary:	Development files for t1lib
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The files needed for developing applications using t1lib.

%package xglyph
Summary:	Test program for t1lib with X11 interface
Group:		X11/Applications
Requires:	%{name}-devel = %{version}-%{release}

%description xglyph
Test program for t1lib with X11 interface.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

rm -f ac-tools/aclocal.m4

%build
%{__libtoolize}
%{__aclocal} -I ac-tools
%{__autoconf}
%configure \
	--disable-static

%{__make} without_doc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_datadir},%{_bindir},%{_includedir}} \
	$RPM_BUILD_ROOT{%{_t1fontsdir},%{_t1afmdir}} \
	$RPM_BUILD_ROOT%{_mandir}/man{1,5,8}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -a Fonts/enc $RPM_BUILD_ROOT%{_datadir}/%{name}
install Fonts/afm/*.afm $RPM_BUILD_ROOT%{_t1afmdir}
install Fonts/type1/*.pfb $RPM_BUILD_ROOT%{_t1fontsdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_t1fontsdir}/Fontmap.%{name}-fonts
install %{SOURCE2} $RPM_BUILD_ROOT%{_t1fontsdir}/fonts.scale.%{name}-fonts
install %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}

> $RPM_BUILD_ROOT%{_datadir}/%{name}/FontDatabase

for sec in 1 5; do
	install debian/*.${sec} $RPM_BUILD_ROOT%{_mandir}/man${sec}
done

chmod +x $RPM_BUILD_ROOT%{_libdir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/sbin/ldconfig
fontpostinst Type1

%postun	-p /usr/sbin/ldconfig

%post fonts
fontpostinst Type1

%postun fonts
fontpostinst Type1

%files
%defattr(644,root,root,755)
%doc Changes README.t1*
%doc doc/*.{tex,eps,fig}

%attr(755,root,root) %{_bindir}/type1afm
%attr(755,root,root) %{_bindir}/t1libconfig
%attr(755,root,root) %ghost %{_libdir}/*.so.?
%attr(755,root,root) %{_libdir}/*.so.*.*

%dir %{_datadir}/%{name}
%{_datadir}/%{name}/enc

%ghost %{_datadir}/%{name}/t1lib.config
%ghost %{_datadir}/%{name}/FontDatabase

%{_mandir}/man[5]/*
%{_mandir}/man1/type1afm.1*

%files fonts
%defattr(644,root,root,755)
%{_t1fontsdir}/*.pfb
%{_t1afmdir}/*.afm
%{_t1fontsdir}/*.%{name}-fonts

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.la
%{_includedir}/*

%files xglyph
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xglyph
%{_mandir}/man1/xglyph.1*

