# NOTE:
# - manifest url https://commondatastorage.googleapis.com/nativeclient-mirror/nacl/nacl_sdk/naclsdk_manifest.json
#   rev 6757 matches pepper_15, r1239
#   rev 6941 matches pepper_16, r1344
# - libdir mixed up for 32/64 bit. do we care? upstream confused about it too
# - /bin/sh in some wrappers:
#   cat i686-nacl-as
#   #!/bin/bash
#%define		nacl_revision	6757
#%define		nacl_revision	6869
%define		nacl_revision	6941
%define		binutils_ver	2.20.1
%define		gcc_ver			4.4.3
%define		newlib_ver		1.18.0
Summary:	Native Client newlib-based toolchain (only for compiling IRT)
Name:		nacl-toolchain-newlib
Version:	0.%{nacl_revision}
Release:	0.3
License:	BSD (NaCL), GPL v3/LGPL v3 (binutils), GPL v3+ (gcc), GPL v2(newlib)
Group:		Applications
Source0:	http://gsdview.appspot.com/nativeclient-archive2/x86_toolchain/r%{nacl_revision}/nacltoolchain-buildscripts-r%{nacl_revision}.tar.gz
# Source0-md5:	884acc20fb43fd6f399e4bb693bf5750
Source1:	ftp://sources.redhat.com/pub/newlib/newlib-%{newlib_ver}.tar.gz
# Source1-md5:	3dae127d4aa659d72f8ea8c0ff2a7a20
Source2:	http://ftp.gnu.org/gnu/binutils/binutils-%{binutils_ver}.tar.bz2
# Source2-md5:	2b9dc8f2b7dbd5ec5992c6e29de0b764
Source3:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{gcc_ver}/gcc-%{gcc_ver}.tar.bz2
# Source3-md5:	fe1ca818fc6d2caeffc9051fe67ff103
Patch0:		http://gsdview.appspot.com/nativeclient-archive2/x86_toolchain/r%{nacl_revision}/naclbinutils-%{binutils_ver}-r%{nacl_revision}.patch.bz2
# Patch0-md5:	dbcd40f49c9bd6624ed6b78056ab906b
Patch1:		http://gsdview.appspot.com/nativeclient-archive2/x86_toolchain/r%{nacl_revision}/naclnewlib-%{newlib_ver}-r%{nacl_revision}.patch.bz2
# Patch1-md5:	f433a45f24fc97f0b2ecc6ac1458b578
Patch2:		http://gsdview.appspot.com/nativeclient-archive2/x86_toolchain/r%{nacl_revision}/naclgcc-%{gcc_ver}-r%{nacl_revision}.patch.bz2
# Patch2-md5:	581d51e531d50566cb30235611faeed6
URL:		http://code.google.com/chrome/nativeclient/
BuildRequires:	binutils >= 2.15.94
BuildRequires:	bison >= 1.875
BuildRequires:	cloog-ppl-devel
BuildRequires:	flex >= 2.5.4
BuildRequires:	gettext-devel
BuildRequires:	iconv
BuildRequires:	libart_lgpl-devel >= 2.1
BuildRequires:	libmpc-devel
BuildRequires:	m4
BuildRequires:	ncurses-devel >= 5.2
BuildRequires:	ppl-devel
BuildRequires:	sed >= 4
BuildRequires:	texinfo >= 4.8
BuildRequires:	unzip
BuildRequires:	yacc
BuildRequires:	zip
Requires:	glibc >= 6:2.8/v8
Requires:	gmp >= 5.0.2
Requires:	mpfr >= 3.0.1
Requires:	zlib >= 1.1.4
ExclusiveArch:	%{x8664} %{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		target		x86_64-nacl
%define		arch		%{_prefix}/%{target}-newlib
%define		_datadir	%{arch}/share
%define		_mandir		%{_datadir}/man
%define		_infodir	%{_datadir}/info
%define		_includedir	%{arch}/%{target}/include
%define		_libexecdir	%{arch}/libexec

%define     gccarch     %{_libexecdir}/gcc/%{target}
%define     gcclib      %{gccarch}/%{gcc_ver}

%description
Native Client newlib-based toolchain (only for compiling IRT).

%prep
%setup -qc -a1 -a2 -a3
mkdir -p SRC
mv binutils-%{binutils_ver} SRC/binutils
mv newlib-%{newlib_ver} SRC/newlib
mv gcc-%{gcc_ver} SRC/gcc

cd SRC
%patch0 -p0
%patch1 -p0
%patch2 -p0

%build
%{__make} build-with-newlib \
	PREFIX="$(pwd)/out" \
	CANNED_REVISION="yes"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}
cp -a out/* $RPM_BUILD_ROOT%{arch}

%{__rm} $RPM_BUILD_ROOT%{arch}/COPYING*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%{__rm} $RPM_BUILD_ROOT%{arch}/%{target}/lib/*.la
%{__rm} $RPM_BUILD_ROOT%{arch}/%{target}/lib32/*.la

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_mandir}
rm -rf $RPM_BUILD_ROOT%{_infodir}
rm -rf $RPM_BUILD_ROOT%{arch}/info
rm -rf $RPM_BUILD_ROOT%{arch}/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%dir %{arch}

# binutils
%dir %{arch}/bin
%attr(755,root,root) %{arch}/bin/*

# libc
%dir %{_datadir}
%{_datadir}/iconv_data

# gcc
%dir %{arch}/lib
%dir %{arch}/lib/gcc
%dir %{arch}/lib/gcc/x86_64-nacl
%{arch}/lib/gcc/x86_64-nacl/%{gcc_ver}

%dir %{_libexecdir}
%dir %{_libexecdir}/gcc
%dir %{gccarch}
%dir %{gcclib}
%attr(755,root,root) %{gcclib}/cc1
%attr(755,root,root) %{gcclib}/collect2
%attr(755,root,root) %{gcclib}/cc1obj
%attr(755,root,root) %{gcclib}/cc1plus

%dir %{gcclib}/install-tools
%attr(755,root,root) %{gcclib}/install-tools/*

%dir %{arch}/%{target}

# toolchain symlinks
%dir %{arch}/%{target}/bin
%{arch}/%{target}/bin/ar
%{arch}/%{target}/bin/as
%{arch}/%{target}/bin/c++
%{arch}/%{target}/bin/g++
%{arch}/%{target}/bin/gcc
%{arch}/%{target}/bin/ld
%{arch}/%{target}/bin/nm
%{arch}/%{target}/bin/objcopy
%{arch}/%{target}/bin/objdump
%{arch}/%{target}/bin/ranlib
%{arch}/%{target}/bin/strip

# libc-devel
%dir %{_includedir}
%{_includedir}/*.h
%{_includedir}/machine
%{_includedir}/sys
%{_includedir}/bits

# libstdc++-devel
%dir %{_includedir}/c++
%{_includedir}/c++/%{gcc_ver}

# binutils
%dir %{arch}/%{target}/lib
%dir %{arch}/%{target}/lib/32
%{arch}/%{target}/lib/crt0.o
%{arch}/%{target}/lib/ldscripts

# binutils-devel
%{arch}/%{target}/lib/libc.a
%{arch}/%{target}/lib/libcrt_common.a
%{arch}/%{target}/lib/libg.a
%{arch}/%{target}/lib/libiberty.a
%{arch}/%{target}/lib/libm.a
%{arch}/%{target}/lib/libobjc.a
%{arch}/%{target}/lib/libstdc++.a
%{arch}/%{target}/lib/libsupc++.a

%dir %{arch}/%{target}/lib32
%{arch}/%{target}/lib32/crt0.o
%{arch}/%{target}/lib32/libc.a
%{arch}/%{target}/lib32/libcrt_common.a
%{arch}/%{target}/lib32/libg.a
%{arch}/%{target}/lib32/libiberty.a
%{arch}/%{target}/lib32/libm.a
%{arch}/%{target}/lib32/libobjc.a
%{arch}/%{target}/lib32/libstdc++.a
%{arch}/%{target}/lib32/libsupc++.a
%{arch}/%{target}/lib64
