## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%define 	add_to_doc_files()	\
	mkdir -p %{buildroot}%{_docdir}/%{name}-%{version} ||: ; \
	cp -p %1  %{buildroot}%{_docdir}/%{name}-%{version}/$(echo '%1' | sed -e 's!/!.!g')

## Optional build modifications...
## --with coverage: Enables compile-time checking of code coverage.
##	(Default: No)
##
## --with debug: Enable more verbose debugging. Makes runtime a bit slower.
##	Also disables the optimized memory allocator.
##	(Default: No)
##
## --with jit: Enable JIT ("just-in-time") JavaScript compiling support.
## 	Only supported on ix86 at this time, according to upstream.
##	(Default: No)
##	
## --with pango: Use Pango instead of freetype2 as the font renderer.
##	CJK support is functional only with the freetype2 backend.
##	(Default: No - use freetype2)
##
## --with svg: Experimental SVG support (filters)
##	(Default: No) 
##
## --with wml: Build support for WML
##	(Default: No)

%bcond_with 	coverage
%bcond_with 	debug
%bcond_with 	jit
%bcond_with 	pango
%bcond_with 	svg
%bcond_with 	wml

Name:		webkitgtk
Version:	1.1.4
Release:	1%{?dist}
Summary:	GTK+ Web content engine library

Provides:	WebKit-gtk = %{version}-%{release}
Obsoletes:	WebKit-gtk < %{version}-%{release}

Group:		Development/Libraries
License:	LGPLv2+ and BSD
URL:		http://www.webkitgtk.org/

Source0:	http://www.webkitgtk.org/webkit-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	geoclue-devel
BuildRequires:	gperf
BuildRequires:	gnome-keyring-devel
BuildRequires:	gstreamer-devel
BuildRequires:	gstreamer-plugins-base-devel
BuildRequires:	gtk2-devel
BuildRequires:	libsoup-devel >= 2.25.91
BuildRequires:	libicu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libtool
BuildRequires:	libxslt-devel
BuildRequires:	libXt-devel
BuildRequires:	pcre-devel
BuildRequires:	sqlite-devel

## Conditional dependencies...
%if %{with pango}
BuildRequires:	pango-devel
%else
BuildRequires:	cairo-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel
%endif

%description 
WebKitGTK+ is the port of the portable web rendering engine WebKit to the
GTK+ platform.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	gtk2-devel
Provides:	WebKit-gtk-devel = %{version}-%{release}
Obsoletes:	WebKit-gtk-devel < %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.


%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Provides:	WebKit-doc = %{version}-%{release}
Obsoletes:	WebKit-doc < %{version}-%{release}

%description	doc
This package contains the documentation for %{name}, including various
LICENSE, README, and AUTHORS files.


%prep
%setup -qn "webkit-%{version}"


%build
%configure							\
			--enable-gnomekeyring			\
			--enable-geolocation			\
%{?with_coverage:	--enable-coverage		}	\
%{?with_debug:		--enable-debug			}	\
%{?with_jit:		--enable-jit			}	\
%{?with_pango:		--with-font-backend=pango	}	\
%{?with_svg:		--enable-svg-filters		}	\
%{?with_wml:		--enable-wml			}
	
make %{?_smp_mflags}

# workaround for bug 488112
# Compile libJavaScriptCore.a with -fno-strict-aliasing
touch JavaScriptCore/AllInOneFile.cpp
make %{?_smp_mflags} CXXFLAGS="%{optflags} -fno-strict-aliasing"


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
install -d -m 755 %{buildroot}%{_libexecdir}/%{name}
install -m 755 Programs/GtkLauncher %{buildroot}%{_libexecdir}/%{name}

## Finally, copy over and rename the various files for %%doc inclusion.
%add_to_doc_files JavaScriptCore/icu/LICENSE
%add_to_doc_files WebKit/LICENSE
%add_to_doc_files WebCore/icu/LICENSE
%add_to_doc_files WebCore/LICENSE-APPLE
%add_to_doc_files WebCore/LICENSE-LGPL-2
%add_to_doc_files WebCore/LICENSE-LGPL-2.1

%add_to_doc_files JavaScriptCore/pcre/COPYING
%add_to_doc_files JavaScriptCore/COPYING.LIB

#add_to_doc_files JavaScriptCore/icu/README
#add_to_doc_files WebCore/icu/README

%add_to_doc_files JavaScriptCore/AUTHORS
%add_to_doc_files JavaScriptCore/pcre/AUTHORS   

%add_to_doc_files JavaScriptCore/THANKS


%clean
rm -rf %{buildroot}


%post	-p /sbin/ldconfig

%postun	-p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc
%exclude %{_libdir}/*.la
%{_bindir}/jsc
%{_libdir}/libwebkit-1.0.so.*
%{_libexecdir}/%{name}/

%files	devel
%defattr(-,root,root,-)
%{_datadir}/webkit-1.0
%{_includedir}/webkit-1.0
%{_libdir}/libwebkit-1.0.so
%{_libdir}/pkgconfig/webkit-1.0.pc

%files	doc
%defattr(-,root,root,-)
%{_docdir}/%{name}-%{version}/


%changelog
* Tue Apr 07 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.4-1
- Update to new upstream release (1.1.4)
- Enable building with geolocation support.
- Add build-time conditional for enabling code coverage checking (coverage).
- Remove html5video conditional and update dependencies accordingly. (HTML5
  video embedding support is now enabled by default by upstream.)

* Sun Mar 15 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.3-1
- Rename from WebKit-gtk and friends to WebKitGTK and subpackages.
- Update to new upstream release (1.1.3)
- Clean up the add_to_doc_files macro usage.

* Sat Mar 07 2009 Peter Gordon <peter@thecodergeek.com> - 1.1.1-1
- Update to new upstream release (1.1.1), includes a soname bump.
- Enable gnome-keyring support.

* Wed Mar  4 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.1.0-0.21.svn41071
- Compile libJavaScriptCore.a with -fno-strict-aliasing to
  do workaround for #488112

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.20.svn41071
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Peter Gordon <peter@thecodergeek.com> 1.1.0-0.19.svn41071
- Update to new upstream snapshot (SVN 41071).
- Drop libsoup build conditional. Use libsoup as default HTTP backend instead
  of cURL, following upstream's default.

* Fri Jan 30 2009 Peter Gordon <peter@thecodergeek.com> 1.1.0-0.18.svn40351
- Fix ownership of doc directory...this time without the oops (#473619).
- Bump package version number to match that used in the configure/build
  scripts. (Thanks to Martin Sourada for the bug report via email.)

* Thu Jan 29 2009 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.17.svn40351
- Update to new upstream snapshot (SVN 40351): adds the WebPolicyDelegate
  implementaton and related API (#482739).
- Drop Bison 2.4 patch (fixed upstream):
  - bison24.patch
- Fixes CVE-2008-6059: Sensitive information disclosure from cookies via
  XMLHttpRequest calls (#484197).

* Sat Nov 29 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.16.svn39370
- Update to new upstream snapshot (SVN 39370)
- Fix ownership of %%_docdir in the doc subpackage. 
- Resolves: bug 473619 (WebKit : Unowned directories).
- Adds webinspector data to the gtk-devel subpackage.
- Add patch from upstream bug 22205 to fix compilation errors with Bison 2.4:
  + bison24.patch
- Add build-time conditional for WML support.

* Thu Oct 23 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.15.svn37790
- Update to new upstream snapshot (SVN 37790).
- Default to freetype font backend for improved CJK/Unicode support. (#448693)
- Add some notes to the build options comments block.
- Add a build-time conditional for jit

* Sun Aug 24 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.14.svn35904
- Update to new upstream snapshot (SVN 35904)

* Fri Jul 04 2008 Peter Gordon <peter@thecodergeek.com>
- Remove outdated and unnecessary GCC 4.3 patch:
  - gcc43.patch
- Fix the curl-devel BuildRequire conditional. (It is only needed when building
  against curl instead of libsoup.)

* Thu Jun 12 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.13.svn34655
- Update to new upstream snapshot (SVN 34655)
- Add some build-time conditionals for non-default features: debug, 
  html5video, libsoup, pango, svg. 

* Tue Jun  3 2008 Caolán McNamara <caolanm@redhat.com> - 1.0.0-0.12.svn34279
- rebuild for new icu

* Tue Jun  3 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.0-0.11.svn34279
- Update to new upstream snapshot (SVN 34279) anyway
- Add BR: libXt-devel

* Tue Apr 29 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.10.svn32531
- Remove the -Qt subpackage stuff. QtWebKit is now included in Qt proper, as
  of qt-4.4.0-0.6.rc1. (We no longer need separate build-qt and build-gtk
  subdirectories either.)
- Reference: bug 442200 (RFE: WebKit Migration)
- Add libjpeg dependency (was previously pulled in by the qt4-devel dependency
  tree).

* Mon Apr 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.0.0-0.9.svn32531
- Update to new upstream snapshot (SVN 32531).
- Fix bug 443048 and hopefully fix bug 444445
- Modify the process of building GTK+ port a bit
- on qt port WebKit/qt/Plugins is not built for qt >= 4.4.0

* Sat Apr 12 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.8.svn31787
- Update to new upstream snapshot (SVN 31787).
- Resolves: CVE-2008-1010 (bug 438532: Arbitrary code execution) and
  CVE-2008-1011 (bug 438531: Cross-Site Scripting).
- Switch to using autotools for building the GTK+ port.

* Wed Mar 05 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.7.svn30667
- Fix the WebKitGtk pkgconfig data (should depend on gtk+-2.0). Resolves
  bug 436073 (Requires: gtk+-2.0 missing from WebKitGtk.pc).
- Thanks to Mamoru Tasaka for helping find and squash these many bugs. 
  
* Sat Mar 01 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.6.svn30667
- Fix include directory naming. Resolves: bug 435561 (Header file <> header
  file location mismatch)
- Remove qt4-devel runtime dependency and .prl file from WebKit-gtk-devel.
  Resolves: bug 433138 (WebKit-gtk-devel has a requirement on qt4-devel) 

* Fri Feb 29 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.5.svn30667
- Update to new upstream snapshot (SVN 30667)
- Add some build fixes for GCC 4.3:
  + gcc43.patch

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-0.5.svn29336
- Autorebuild for GCC 4.3

* Wed Jan 09 2008 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.4.svn29336
- Update to new upstream snapshot (SVN 29336).
- Drop TCSpinLock pthread workaround (fixed upstream):
  - TCSpinLock-use-pthread-stubs.patch

* Thu Dec 06 2007 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.3.svn28482
- Add proper %%defattr line to qt, qt-devel, and doc subpackages.
- Add patch to forcibly build the TCSpinLock code using the pthread
  implementation:
  + TCSpinLock-use-pthread-stubs.patch

* Thu Dec 06 2007 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.2.svn28482
- Package renamed from WebKitGtk.
- Update to SVN 28482.
- Build both the GTK and Qt ports, putting each into their own respective
  subpackages.
- Invoke qmake-qt4 and make directly (with SMP build flags) instead of using
  the build-webkit script from upstream.
- Add various AUTHORS, README, and LICENSE files (via the doc subpackage). 

* Tue Dec 04 2007 Peter Gordon <peter@thecodergeek.com> 1.0.0-0.1.svn28383
- Initial packaging for Fedora.
