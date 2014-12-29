# NOTE!
# Now for weblet plug-ins now cairo-dock uses WebKit, not Gecko.

# Now upstream VCS uses bazaar
# To gain the source codes from upstream VCS, use
# $ bzr branch <URL>
# , where the current URL is:
#
# For core:
# http://bazaar.launchpad.net/~cairo-dock-team/cairo-dock-core/2.1.x/
# For plug-ins:
# http://bazaar.launchpad.net/~cairo-dock-team/cairo-dock-plug-ins/2.1.x/

%global		released	1
%undefine		pre_release	
# Set the below to 1 when building unstable plug-ins
%global		build_other	1

%global		urlver		3.4
%global		mainver	3.4.0
#%%define		betaver	0rc1
#%%global		postver_c	2
#%%global		postver_p	2.1

%global		rpmver_c	%{mainver}%{?postver_c:.%postver_c}
%global		rpmver_p	%{mainver}%{?postver_p:.%postver_p}
%global		rpmrel		%{fedora_rel}%{?dist}

%global		build_webkit	1
%global		build_xfce	1

%global		fedora_main_rel	7


%global		fedora_rel	%{?pre_release:0.}%{fedora_main_rel}%{?betaver:.%betaver}

%if 0%{?released} >= 1
%global		build_other	0
%endif

# Bindings
%global	build_python		1
%global	build_python3		1

%global	build_ruby		1
%global	ruby_vendorlib		%(ruby -rrbconfig -e "puts Config::CONFIG['vendorlibdir']")
%global	build_vala		1
%global	build_unstable 1

# For debugging
%global	skip_main_build	0

Name:		cairo-dock
Version:	%{rpmver_c}
Release:	%{rpmrel}
Summary:	Light eye-candy fully themable animated dock

Group:		User Interface/Desktops
License:	GPLv3+
URL:		http://www.glx-dock.org/
%if 0%{?released} < 1
Source0:	%{name}-sources-%{betaver}.tar.bz2
%else
Source0:	http://launchpad.net/cairo-dock-core/%{urlver}/%{mainver}%{?betaver:-%betaver}/+download/cairo-dock-%{mainver}%{?postver_c:~%postver_c}%{?betaver:~%betaver}.tar.gz
Source2:	http://launchpad.net/cairo-dock-plug-ins/%{urlver}/%{mainver}%{?betaver:-%betaver}/+download/cairo-dock-plugins-%{mainver}%{?postver_p:~%postver_p}%{?betaver:~%betaver}.tar.gz
%endif
# Specify gem name to surely use ruby-dbus
# Applied as 006353cc067e789e50d85790fbdb6c25e1398a63
Patch0:	cairo-dock-plugins-3.4.0-ruby-specify-gemname.patch
# Ruby initialization fix
# Applied as b71aff98db0fe9d4a22ed1fb9c457da0c3023846
Patch1:	cairo-dock-plugins-3.4.0-ruby-initialization.patch
# Append soname for Vala interface
# Upstream: 2326408fb3ea63b78f0b0b5b13dcfa2070018e10
Patch2:	cairo-dock-plugins-3.4.0-vala-append-soname.patch

BuildRequires:	cmake

BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool

# For main package
BuildRequires:	dbus-glib-devel
BuildRequires:	gtk3-devel
BuildRequires:	libcurl-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libXrandr-devel
BuildRequires:	libXrender-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXtst-devel
BuildRequires:	libGLU-devel
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	perl(XML::Parser)

# For plug-ins
BuildRequires:	alsa-lib-devel
BuildRequires:	fftw3-devel
BuildRequires:	gnome-menus-devel
BuildRequires:	libexif-devel
BuildRequires:	libical-devel
BuildRequires:	libxklavier-devel
BuildRequires:	libXxf86vm-devel
BuildRequires:	libzeitgeist-devel
BuildRequires:	pulseaudio-libs-devel
#BuildRequires:	qt4-devel
BuildRequires:	upower-devel
BuildRequires:	vte3-devel
BuildRequires:	libetpan-devel
BuildRequires:	lm_sensors-devel
BuildRequires:	pkgconfig(indicator3-0.4)
BuildRequires:	pkgconfig(dbusmenu-glib-0.4)
BuildRequires:	pkgconfig(dbusmenu-gtk3-0.4)
# For plug-ins-xfce
%if %{build_xfce} > 0
BuildRequires:	Thunar-devel
%endif
%if %{build_webkit} > 0
# For plug-ins-webkit
# Now using webkit, not gecko
BuildRequires:	webkitgtk3-devel
%endif

# Bindings
%if %{build_python}
BuildRequires:	python2-devel
%endif
%if %{build_python3}
BuildRequires:	python3-devel
%endif
%if %{build_ruby}
BuildRequires:	ruby(release)
BuildRequires:	ruby-devel
%endif
%if %{build_vala}
BuildRequires:	vala
%endif

# This is a meta package to install cairo-dock-core and
# cairo-dock-plug-ins
Requires:	%{name}-core = %{rpmver_c}-%{rpmrel}
Requires:	%{name}-plug-ins = %{rpmver_p}-%{rpmrel}

%description
This is a metapackage for installing all default packages
related to cairo-dock.

%package	core
Summary:	Core files for %{name}
Version:	%{rpmver_c}
Release:	%{rpmrel}
Group:		User Interface/Desktops
# Requires related to commands used internally
# in cairo-dock
Requires:	findutils
Requires:	curl
Requires:	xterm

# Obsoletes moved to main package
# Switch to Webkit, always obsolete gecko (and _not_ provide it)
Obsoletes:	%{name}-plug-ins-gecko < %{rpmver_p}-%{rpmrel}
%if %{build_webkit} == 0
Obsoletes:	%{name}-plug-ins-webkit < %{rpmver_p}-%{rpmrel}
%endif
%if %{build_xfce} == 0
Obsoletes:	%{name}-plug-ins-xfce < %{rpmver_p}-%{rpmrel}
%endif
# cairo-dock-themes is obsoleted
Obsoletes:	%{name}-themes < %{rpmver_c}-%{rpmrel}

%description	core
An light eye-candy fully themable animated dock for any 
Linux desktop. It has a family-likeness with OSX dock,
but with more options.

This is the core package of cairo-dock.

%package	plug-ins
Summary:	Plug-ins files for %{name}
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core = %{rpmver_c}-%{rpmrel}
# rpmfusion bug 3470
# cairo-dock-launcher-API-daemon is written in python,
# so for now make this depending on python
Requires:	%{name}-python%{?_isa} = %{rpmver_p}-%{rpmrel}

%description	plug-ins
This package contains plug-ins files for %{name}.

%package	plug-ins-xfce
Summary:	Plug-ins files for %{name} related to Xfce
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}

%description	plug-ins-xfce
This package contains plug-ins files for %{name} related
to Xfce.

%package	plug-ins-kde
Summary:	Plug-ins files for %{name} related to KDE
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}

%description	plug-ins-kde
This package contains plug-ins files for %{name} related
to KDE.

%package	plug-ins-webkit
Summary:	Plug-ins files for %{name} related to Gecko
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}

%description	plug-ins-webkit
This package contains plug-ins files for %{name} related
to webkit.

%package	plug-ins-unstable
Summary:	Unstable plug-ins not installed by default
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}

%description	plug-ins-unstable
This package contains unstable and experimental
plug-ins not installed by default.

%package	python
Summary:	Python binding for %{name}
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}
Requires:	pygobject2
Requires:	dbus-python

%description	python
This package contains Python binding files for %{name}

%package	python3
Summary:	Python3 binding for %{name}
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}
Requires:	pygobject3
Requires:	python3-dbus

%description	python3
This package contains Python3 binding files for %{name}

%package	ruby
Summary:	Ruby binding for %{name}
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}
Requires:	ruby(release)
Requires:	rubygem(ruby-dbus)
Requires:	rubygem(parseconfig)

%description	ruby
This package contains Ruby binding files for %{name}

%package	vala
Summary:	Vala binding for %{name}
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		User Interface/Desktops
Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}
Requires:	vala

%description	vala
This package contains Vala binding files for %{name}

%package	vala-devel
Summary:	Development files for Vala binding for %{name}
Version:	%{rpmver_p}
Release:	%{rpmrel}
Group:		Development/Libraries
Requires:	%{name}-vala%{?_isa} = %{rpmver_p}-%{rpmrel}

%description vala-devel
This package contains development files for Vala
binding for %{name}.

%package	devel
Summary:	Development files for %{name}
Version:	%{rpmver_c}
Release:	%{rpmrel}
Group:		Development/Libraries

Requires:	%{name}-core%{?_isa} = %{rpmver_c}-%{rpmrel}

%description	devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%prep
%setup -q -c -a 2
ln -s -f cairo-dock-%{mainver}* cairo-dock
ln -s -f cairo-dock-plugins-%{mainver}* plug-ins

%if 0
find . -type d -name \.svn | sort -r | xargs rm -rf
find . -type d -name \*CVS\* | sort -r | xargs rm -rf
%endif

TOPDIR=$(pwd)
pushd .

# A. main
cd cairo-dock

## Patch

## permission
for dir in */
do
	find $dir -type f | xargs chmod 0644
done
chmod 0644 [A-Z]*
chmod 0755 */

## cmake issue
sed -i.debuglevel \
	-e '\@add_definitions@s|-O3|-O2|' \
	CMakeLists.txt
sed -i.libdir \
	-e '\@set.*libdir@s|lib64|lib\${LIB_SUFFIX}|' \
	CMakeLists.txt
sed -i.stat \
	-e 's|\${MSGFMT_EXECUTABLE}|\${MSGFMT_EXECUTABLE} --statistics|' \
	po/CMakeLists.txt

## desktop file
sed -i.icon \
	-e 's|Icon=\*|Icon=cairo-dock|' \
	data/cairo-dock*.desktop

# C. plug-ins
cd ../plug-ins

# Patch
%patch0 -p1 -b .gem
%patch1 -p1 -b .rubyinit
%patch2 -p1 -b .valasoname

## permission
for dir in */
do
	find $dir -type f | xargs chmod 0644
done
chmod 0644 [A-Z]*
chmod 0755 */

## cmake issue
sed -i.debuglevel \
	-e '\@add_definitions@s|-O3|-O2|' \
	CMakeLists.txt
sed -i.stat \
	-e 's|\${MSGFMT_EXECUTABLE}|\${MSGFMT_EXECUTABLE} --statistics|' \
	po/CMakeLists.txt

## source code fix
## Bindings
# Ruby
sed -i.site \
	-e "s|CONFIG\['rubylibdir'\]|CONFIG['vendorlibdir']|" \
	CMakeLists.txt
# ????
sed -i.installdir \
	-e '\@REGEX REPLACE.*RUBY@d' \
	-e '\@set.*RUBY_LIB_DIR.*CMAKE_INSTALL_PREFIX.*RUBY_LIB_DIR_INSTALL@d' \
	CMakeLists.txt
# Python

popd # from opt/cairo-dock/trunk/cairo-dock

%build
status=0
TOPDIR=$(pwd)

%global	__make	\
	%{_bindir}/make -k VERBOSE=true

# A. main
pushd cairo-dock

%if %{skip_main_build} < 1

# ZZZ GLib inclusion
# From GLib 2.31, _some_ Glib headers were made not to be included
# directly, however still gi18n.h, gstdio.h and so on have to be
# included separately
%if 0%{?fedora} >= 17
export CFLAGS="%optflags -DGLIB_COMPILATION"
export CXXFLAGS="%optflags -DGLIB_COMPILATION"
%else
export CFLAGS="%optflags"
export CXXFLAGS="%optflags"
%endif

## rpath issue needs investigating
%cmake -DCMAKE_SKIP_RPATH:BOOL=ON .
%{__make} %{?_smp_mflags} || status=$((status+1))

## Once install
rm -rf TMPINSTDIR
%{__make} install \
	DESTDIR=$TOPDIR/TMPINSTDIR \
	INSTALL="install -p" \
	|| status=$((status+1))

%endif

%if 1
export CFLAGS="$CFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock"
export CFLAGS="$CFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock/cairo-dock"
export CFLAGS="$CFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock/icon-factory"
export CFLAGS="$CFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock/gldit"
export CXXFLAGS="$CFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock"
export CXXFLAGS="$CXXFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock/cairo-dock"
export CXXFLAGS="$CXXFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock/icon-factory"
export CXXFLAGS="$CXXFLAGS -I$TOPDIR/TMPINSTDIR%{_includedir}/cairo-dock/gldit"
%endif
export LD_LIBRARY_PATH=$TOPDIR/TMPINSTDIR%{_libdir}
export PKG_CONFIG_PATH=$TOPDIR/TMPINSTDIR%{_libdir}/pkgconfig:${PKG_CONFIG_PATH}

chmod 0755 $TOPDIR/TMPINSTDIR%{_libdir}/lib*.so.*

# C plug-ins
cd ../plug-ins

# Create pseudo executable files
test -d TMPBINDIR || mkdir TMPBINDIR
export PATH=$(pwd)/TMPBINDIR:$PATH

cd TMPBINDIR
# Ruby: not ready
%if %{build_ruby} < 1
ln -sf /bin/false ruby
%endif
cd ..

rm -f CMakeCache.txt
%cmake \
%if 0%{?build_unstable} >= 1
	-Denable-disks=TRUE \
	-Denable-doncky=TRUE \
	-Denable-global-menu=TRUE \
	-Denable-network-monitor=TRUE \
	-Denable-scooby-do=TRUE \
%endif
	.

## Parallel make fails some times, but it is gerenally fast
## so do parallel make anyway first
retry=0
%{__make} %{?_smp_mflags} || retry=1
if [ $retry == 1 ] ; then
	%{__make} || status=$((status+1))
fi

%{__make} install \
	DESTDIR=$TOPDIR/TMPINSTDIR \
	INSTALL="install -p" \
	|| status=$((status+1))

popd ## from opt/cairo-dock/trunk/cairo-dock

## exit abnormally if some failure occurred 
if [ $status -gt 0 ] ; then exit 1 ; fi

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
TOPDIR=$(pwd)

# First copy all
cp -a ./TMPINSTDIR/* $RPM_BUILD_ROOT/

# Main package handling
## Desktop files
for f in $RPM_BUILD_ROOT%{_datadir}/applications/*desktop
do
	desktop-file-validate $f
done

## Cleanups
rm -f $RPM_BUILD_ROOT%{_datadir}/%{name}/ChangeLog.txt

## gettext .mo
%find_lang %{name}

## documents
rm -rf $TOPDIR/documents/main
mkdir -p $TOPDIR/documents/main

pushd cairo-dock
install -cpm 644 \
	ChangeLog \
	LGPL-2 \
	LICENSE \
	copyright \
	data/ChangeLog*.txt \
	$TOPDIR/documents/main/

popd # from cairo-dock


# plug-ins
## lang
%find_lang %{name}-plugins

# documents
rm -rf $TOPDIR/documents/plug-ins/
mkdir -p $TOPDIR/documents/plug-ins/

pushd plug-ins
install -cpm 0644 \
	ChangeLog \
	LGPL-2 \
	LICENSE \
	copyright \
	$TOPDIR/documents/plug-ins/
mkdir -p $TOPDIR/documents/plug-ins/Dbus
cp -a Dbus/demos \
	$TOPDIR/documents/plug-ins/Dbus/

popd # from plug-ins

# Final clean up
## remove all unneeded files
pushd $RPM_BUILD_ROOT

find .%{_libdir}/%{name} -name \*.la | xargs %{__rm} -f
# just to suppress rpmlint...
for f in \
	`find ./%{_datadir}/%{name} -name \*.desktop` \
	`find . -name \*.conf`
	do
	echo > $f.tmp
	cat $f >> $f.tmp
	touch -r $f $f.tmp
	mv -f $f.tmp $f
done

set +x
for f in .%{_datadir}/%{name}/plug-ins/*/*
	do
	if head -n 1 $f 2>/dev/null | grep -q /bin/ ; then 
		set -x
		chmod 0755 $f
		set +x
	fi
done
set -x

popd # from $RPM_BUILD_ROOT


%post core -p /sbin/ldconfig
%postun core -p /sbin/ldconfig
%if %{build_vala} >= 0
%post vala -p /sbin/ldconfig
%postun vala -p /sbin/ldconfig
%endif


%files
%defattr(-,root,root,-)

%files core -f %{name}.lang
%defattr(-,root,root,-)
%doc	documents/main/*

%{_bindir}/*%{name}*
%{_libdir}/libgldi.so.3*
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/pixmaps/%{name}.svg

%dir	%{_datadir}/%{name}/
%{_datadir}/%{name}/*.conf
%{_datadir}/%{name}/*.desktop
%{_datadir}/%{name}/*.svg
%{_datadir}/%{name}/images/
%{_datadir}/%{name}/*view
#%%{_datadir}/%{name}/emblems/
%{_datadir}/%{name}/explosion/
%{_datadir}/%{name}/gauges/
%{_datadir}/%{name}/icons/
%{_datadir}/%{name}/scripts/
%dir	%{_datadir}/%{name}/themes/
%dir	%{_datadir}/%{name}/plug-ins/
%{_datadir}/%{name}/themes/Default-Panel/
%{_datadir}/%{name}/themes/Default-Single/
%dir	%{_libdir}/%{name}/
%{_libdir}/%{name}/libcd-Help.so

%{_mandir}/man1/%{name}.1*

%files	plug-ins -f %{name}-plugins.lang
%defattr(-,root,root,-)
%doc	documents/plug-ins/*

%{_libdir}/%{name}/*
%exclude	%{_libdir}/%{name}/libcd-Help.so

%{_datadir}/%{name}/plug-ins/*
%if %{build_webkit} > 0
%exclude	%{_libdir}/%{name}/*weblet*
%exclude	%{_datadir}/%{name}/plug-ins/*weblet*
%endif
%if %{build_xfce} > 0
%exclude	%{_libdir}/%{name}/*xfce*
%exclude	%{_datadir}/%{name}/plug-ins/*xfce*
%endif
%exclude	%{_libdir}/%{name}/*kde*
%exclude	%{_datadir}/%{name}/plug-ins/*kde*
%if 0%{?build_unstable} >= 1
%exclude	%{_libdir}/%{name}/appmenu-registrar
%exclude	%{_libdir}/%{name}/libcd-Global-Menu.so
%exclude	%{_libdir}/%{name}/libcd-disks.so
%exclude	%{_libdir}/%{name}/libcd-doncky.so
%exclude	%{_libdir}/%{name}/libcd-network-monitor.so
%exclude	%{_libdir}/%{name}/libcd-scooby-do.so
%exclude	%{_datadir}/%{name}/plug-ins/Disks/
%exclude	%{_datadir}/%{name}/plug-ins/Doncky/
%exclude	%{_datadir}/%{name}/plug-ins/Global-Menu/
%exclude	%{_datadir}/%{name}/plug-ins/Network-Monitor/
%exclude	%{_datadir}/%{name}/plug-ins/Scooby-Do/
%endif

%if 0%{?build_unstable} >= 1
%files	plug-ins-unstable
%defattr(-,root,root,-)
%{_libdir}/%{name}/appmenu-registrar
%{_libdir}/%{name}/libcd-Global-Menu.so
%{_libdir}/%{name}/libcd-disks.so
%{_libdir}/%{name}/libcd-doncky.so
%{_libdir}/%{name}/libcd-network-monitor.so
%{_libdir}/%{name}/libcd-scooby-do.so
%{_datadir}/%{name}/plug-ins/Disks/
%{_datadir}/%{name}/plug-ins/Doncky/
%{_datadir}/%{name}/plug-ins/Global-Menu/
%{_datadir}/%{name}/plug-ins/Network-Monitor/
%{_datadir}/%{name}/plug-ins/Scooby-Do/
%endif

%if %{build_xfce} > 0
%files	plug-ins-xfce
%defattr(-,root,root,-)
%{_libdir}/%{name}/*xfce*
%{_datadir}/%{name}/plug-ins/*xfce*
%endif

%files	plug-ins-kde
%defattr(-,root,root,-)
%{_libdir}/%{name}/*kde*
%{_datadir}/%{name}/plug-ins/*kde*

%if %{build_webkit} > 0
%files	plug-ins-webkit
%defattr(-,root,root,-)
%{_libdir}/%{name}/*weblet*
%{_datadir}/%{name}/plug-ins/*weblet*
%endif

%if %{build_python} > 0
%files	python
%defattr(-,root,root,-)
%{python_sitelib}/CairoDock.py*
%{python_sitelib}/CDApplet.py*
%{python_sitelib}/CDBashApplet.py*
%{python_sitelib}/*.egg-info
%endif

%if %{build_python3} > 0
%files	python3
%defattr(-,root,root,-)
%{python3_sitelib}/CairoDock.py*
%{python3_sitelib}/CDApplet.py*
%{python3_sitelib}/CDBashApplet.py*
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/__pycache__/
%endif

%if %{build_ruby} > 0
%files	ruby
%defattr(-,root,root,-)
%{ruby_vendorlib}/CDApplet.rb
%endif

%if %{build_vala} > 0
%files vala
%{_libdir}/libCDApplet.so.1*
%{_datadir}/vala/vapi/CDApplet.*

%files vala-devel
%{_libdir}/libCDApplet.so
%{_libdir}/pkgconfig/CDApplet.pc
%endif


%files	devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/libgldi.so
%{_libdir}/pkgconfig/gldi.pc

%changelog
* Mon Dec 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-7
- Build unstable plug-ins (except for KDE experimental)
  (not installed by default option)

* Mon Dec 29 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-6
- Enable vala interface

* Sat Dec 20 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-5
- Make plug-ins depending on python(2), due to cairo-dock-launcher-API-daemon
  dependency (bug 3470)

* Fri Dec 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-4
- Add Dbus demos

* Fri Dec 19 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-3
- Build ruby

* Fri Dec 12 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-2
- Build Messaging-Menu, Status-Notifier

* Mon Dec  1 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.0-1
- 3.4.0

* Sun Aug 24 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-3
- F-21: rebuild against new upower

* Mon Jun 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-2
- Fix build with upower 0.99

* Mon Jun 16 2014 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.3.2-1
- Update to 3.3.2

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 3.2.1-2.1
- Rebuilt for libgcrypt

* Mon Jul  8 2013 Mamoru TASAKA <mtasaka@fedoraproject.org>
- F-20: rebuid against new libical

* Mon Apr 15 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1

* Fri Apr 12 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.2.0-1
- Update to 3.2.0

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.0.2-2.1
- Mass rebuilt for Fedora 19 Features

* Thu Dec 21 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.0.2-2
- Update plug-ins to 2.1

* Mon Dec 12 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.4.0.2-1
- 2.4.0-2

* Tue Nov  8 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0.3-3
- Rebuilt

* Wed Sep 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0.3-2.1
- Rebuilt for libgnome-menu

* Sun Jul 24 2011 Mamoru Tasaka <mtasaka@fedoraproject.org>
- Rebuild against new libetpan

* Tue Jun 28 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0.3-1
- 2.3.0-3

* Sun Jun  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0.2.1-2
- core 2.3.0~2.1

* Tue May  3 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0.2-1
- 2.3.0~2

* Sat Mar  5 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0-0.2.0rc1
- Add BR: lm_sensors-devel for Sensors support

* Fri Mar  4 2011 Mamoru Tasaka <mtasaka@fedoraproject.org> - 2.3.0-0.1.0rc1
- 2.3.0 0rc1
- Dbus interface: enable python, disable python, disable vala for now

* Thu Dec  9 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.2.0.4-1
- 2.2.0-4

* Sat Jul  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against new webkitgtk

* Fri Jun 11 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.9-3
- Fix for "GMenu does not handle desktop file exec strings properly"
  (Lauchpad 526138, rpmfusion 1265)

* Wed May 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rebuild against new libetpan

* Thu Apr 22 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.9-1
- 2.1.3-9

* Wed Apr  7 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.8-1
- 2.1.3-8

* Thu Apr  1 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.7-2
- Try to enable Network-Monitor and Scooby-do (while the codes say that
  this will be enabled from 2.1.4) (bug 578393)

* Sun Mar 14 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.7-1
- 2.1.3-7
- Some packaging changes out of requests from the upstream
  * rename %%name package to -core, make %%name be a metapkg for
    pulling -core and -plug-ins
  * split kde related files from -plug-ins
- Change R: wget -> curl

* Wed Mar  3 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.6-1
- 2.1.3-6

* Fri Feb 26 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.5-1
- 2.1.3-5

* Thu Feb 18 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.3-1
- 2.1.3-3

* Fri Feb 12 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.3.2-1
- 2.1.3-2

* Sun Jan 17 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-13: Rebuild for libxklavier soname bump

* Fri Dec 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.2.4-1
- 2.1.2-4

* Sat Nov  6 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.1.2-1
- 2.1.1-2

* Sat Oct 10 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.1.0-1
- 2.1.0

* Wed Sep 30 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.8.2-1
- 2.0.8.2

* Sun Jul 12 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.8-1
- 2.0.8

* Fri Jul  3 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.7-1
- 2.0.7

* Thu Jul  2 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-12: rebuild against new libxklavier

* Sat Jun 27 2009 Mamoru Tasaka <mtaaska@ioa.s.u-tokyo.ac.jp> - 2.0.6-1
- 2.0.6

* Thu Jun 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1833
- Remove workaround for bug 506656

* Thu Jun 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1825
- Remove debugedit workaround as bug 505774 is solved.
- Workaround for X11/extensions/XTest.h bug 506656

* Mon Jun 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1821
- Compile with -gdwarf-2 until bug 505774 is resolved.

* Thu Jun 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.5-1
- 2.0.5

* Tue Jun  9 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.4-1
- 2.0.4

* Mon May 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-2
- Workaround to avoid endless loop on po/ directory

* Sun May 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.3-1
- 2.0.3

* Tue May 19 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.2-1
- 2.0.2

* Sun May 17 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.1-1
- 2.0.1

* Mon May 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-2.respin1
- Tarballs respun

* Sun May 10 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-1
- 2.0.0 release

* Wed Apr 29 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-0.7.rc5
- 2.0.0 rc5

* Mon Apr 27 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-0.6.svn1689_trunk
- Kill AutoProv on -themes subpackage to avoid unneeded desktop prov
- Build -themes subpackage as noarch

* Sat Apr 18 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.0.0-0.4.rc3
- 2.0.0 rc3
- Move to rpmfusion
- Enable mail plugin, license is now changed to GPL+
- borrow some missing files from svn trunk for rc3
- Drop "fedora-" prefix from desktop file

* Wed Feb 11 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1527

* Thu Jan 22 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1496
- Include Wanda directory in Cairo-Penguin plug-in again

* Thu Jan 15 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1484
- Trademarked icons under plug-ins/Cairo-Penguin/data/themes are
  removed.

* Thu Dec 25 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1451
- Remove icons maybe under non-free copyright/license from Cairo-Penguin plugin
  (need ask)

* Sat Dec 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1444
- Support xfce plugin again because dependency on hal-devel
  is resoved

* Wed Dec 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Trial fix to compile motion-blur plugin on rev 1439

* Sun Dec  7 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1429
- Try 2.0.0 development branch
- Build weblet plugin with WebKit, switching from Gecko,
  rename weblet related plugin
- Disable xfce related plugin for now until hal-devel is properly
  rebuilt

* Wed Nov 12 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3.1-1
- 1.6.3.1

* Wed Nov  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-1
- 1.6.3

* Wed Oct 29 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-0.3.rc2
- 1.6.3 rc2

* Tue Oct 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-0.3.rc1
- 1.6.3 rc1

* Thu Oct 16 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3-0.2.svn1353_trunk
- GMenu plugin needs gnome-menus-devel

* Wed Sep 24 2008 Christopher Aillon <caillon@redhat.com> - 1.6.2.3-1.1
- Rebuild against newer gecko (F-9/8)

* Tue Sep  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2.3-1
- 1.6.2.3

* Thu Sep  4 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2.2-1
- 1.6.2.2

* Sat Aug 30 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2.1-1
- 1.6.2.1

* Thu Aug 28 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-1
- 1.6.2

* Tue Aug 26 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.6.RC4
- 1.6.2 RC4
- Temporary fix for stack/ plugin

* Sat Aug 23 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.3.RC2
- 1.6.2 RC2

* Sun Aug 10 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.2.svn1235_trunk
- Enable unstable plugins again

* Sun Aug 10 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.2-0.1.svn1235_trunk
- Patch to fix infinite loop of function call (this patch is needed
  for rev. 1235 and the released 1.6.1.2)
  (Fixed in svn 1241)

* Sat Aug  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Build only stable plug-ins for now

* Thu Jul 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.1.2-1
- 1.6.1.2

* Tue Jul 15 2008 Christopher Aillon <caillon@redhat.com>
- F-8: Rebuild against newer gecko

* Tue Jul 15 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.1.1-1
- 1.6.1.1

* Thu Jul  3 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- F-8: rebuild against new gecko

* Sat Jun 21 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0.2-1.date20080621
- 1.6.0.2

* Fri Jun 20 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0.1-2.date20080619
- Revert XCompositeRedirectSubwindows() part in 
  cairo-dock-X-utilities.c - fixed in rev. 1142

* Thu Jun 19 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0.1-1.date20080619
- 1.6.0.1

* Wed Jun 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-0.2.svn1089_trunk
- Fix possibly unsafe tmpfile creation

* Thu Jun  5 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.0-0.1.svn1080_trunk
- Prepare for using unified configure script on plug-ins directory
- Install desktop icon

* Wed May 27 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.6-1.date20080528
- 1.5.6

* Sat May 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-5.svn990_trunk
- Update to svn 990
- 2 issues fixed in upstream
  * plug-in directory moved to %%_libdir/%%name
  * %%name.pc fixed

* Sat May 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-4.date20080506
- F-10: don't build weblets plugin until xulrunner BR dependency is solved

* Sat May 17 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-3.date20080506
- Misc cleanup
- Remove template, upstream says this is not needed

* Sun May 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-2.date20080506
- Remove mail plug-in for now as there is license conflict
- Enable weblet plug-in

* Fri May  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.4-1.date20080506
- 1.5.5.4

* Thu May  1 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.5.5.3-1.date20080501
- Initial packaging
- remove Ubuntu related themes
- plugin dir is moved to %%_libdir/%%name/plug-in

