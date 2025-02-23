#
# Conditional build:
%bcond_with	sse4		# SSE4.1 (obligatory) and optionally AVX+ instructions
#
Summary:	Fraunhofer Versatile Video Encoder (VVenC)
Summary(pl.UTF-8):	VVenC - koder obrazu Fraunhofer Versatile Video
Name:		vvenc
Version:	1.12.0
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/fraunhoferhhi/vvenc/releases
Source0:	https://github.com/fraunhoferhhi/vvenc/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	b0b0f7dde67b44f1e161d42a21717afe
Patch0:		%{name}-pc.patch
URL:		https://github.com/fraunhoferhhi/vvenc
BuildRequires:	cmake >= 3.13.0
# C++14
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	nlohmann-json-devel >= 3.10.2
BuildRequires:	rpmbuild(macros) >= 1.605
%if %{with sse4}
Requires:	cpuinfo(sse4_1)
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
VVenC, the Fraunhofer Versatile Video Encoder, is a fast and efficient
software H.266/VVC encoder implementation with the following main
features:
- Easy to use encoder implementation with five predefined
  quality/speed presets;
- Perceptual optimization to improve subjective video quality, based
  on the XPSNR visual model;
- Extensive frame-level and task-based parallelization with very good
  scaling;
- Frame-level single-pass and two-pass rate control supporting
  variable bit-rate (VBR) encoding.

%description -l pl.UTF-8
VVenC (Fraunhofer Versatile Video Encoder) to szybka i wydajna
programowa implementacja kodera H.266/VVC o następujących cechach:
- łatwa w użyciu implementacja kodera w pięcioma predefiniowanymi
  ustawieniami jakości/prędkości
- optymalizacja percepcyjna w celu poprawy subiektywnej jakości
  obrazu, oparta na modelu wizualnym XPSNR
- rozległy model na poziomie ramek, oparte na zadaniach zrównoleglenie
  z bardzo dobrym skalowaniem
- jedno- i dwuprzebiegowe sterowanie przepustowością na poziomie ramek
  z obsługą kodowania o zmiennej przepustowości (VBR)

%package devel
Summary:	Header files for VVenC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki VVenC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	libstdc++-devel >= 6:5

%description devel
Header files for VVenC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki VVenC.

%prep
%setup -q
%patch -P0 -p1

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_SKIP_INSTALL_RPATH=ON \
	%{!?with_sse4:-DVVENC_ENABLE_X86_SIMD=OFF} \
	-DVVENC_ENABLE_THIRDPARTY_JSON=OFF \
	-DVVENC_INSTALL_FULLFEATURE_APP=ON

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install -p build/source/App/vvencFFapp/vvencFFapp $RPM_BUILD_ROOT%{_bindir}
install -p build/source/App/vvencapp/vvencapp $RPM_BUILD_ROOT%{_bindir}
cp -dp build/source/Lib/vvenc/libvvenc.so* $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS.md LICENSE.txt README.md
%attr(755,root,root) %{_bindir}/vvencFFapp
%attr(755,root,root) %{_bindir}/vvencapp
%attr(755,root,root) %{_libdir}/libvvenc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libvvenc.so.1.12

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libvvenc.so
%{_libdir}/cmake/vvenc
%{_includedir}/vvenc
%{_pkgconfigdir}/libvvenc.pc
