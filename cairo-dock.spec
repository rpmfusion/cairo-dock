# For svn
# svn checkout http://svn.berlios.de/svnroot/repos/cairo-dock/trunk
# cd trunk
# tar cjf ../cairo-dock-sources-%%{tag}.tar.bz2 .

%define		released	1
# For now build only stable plugin
%define		build_other	1

%define		tarballver	svn1363_trunk
%define		mainver		1.6.3.1
%undefine		betaver		
%define		build_gecko	1


%if 0%{?released} < 1
%define		fedora_rel	0.2.%{tarballver}
%else
%define		fedora_rel	2%{?betaver:.%betaver}
%endif


# released tarball does not ship weblets
%if 0%{?released} >= 1
%define		build_other	0
%endif
%if %{build_other} < 1
%define		build_gecko	0
%endif


%if 0%{?fedora} >= 9
%define		gecko_ver	>= 1.9
%endif
%if 0%{?fedora} == 8
%define		gecko_ver	= 1.8.1.17
%endif

Name:		cairo-dock
Version:	%{mainver}
Release:	%{fedora_rel}%{?dist}
Summary:	Light eye-candy fully themable animated dock

Group:		User Interface/Desktops
License:	GPLv3+
URL:		http://www.cairo-dock.org/
%if 0%{?released} < 1
Source0:	%{name}-sources-%{tarballver}.tar.bz2
%else
Source0:	http://download.berlios.de/cairo-dock/%{name}-%{mainver}%{?betaver:-%betaver}.tar.bz2
Source1:	http://download.berlios.de/cairo-dock/%{name}-themes-%{mainver}%{?betaver:-%betaver}.tar.bz2
Source2:	http://download.berlios.de/cairo-dock/%{name}-plugins-%{mainver}%{?betaver:-%betaver}.tar.bz2
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	libtool

# For main package
BuildRequires:	dbus-glib-devel
BuildRequires:	gtk2-devel
BuildRequires:	glitz-glx-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXtst-devel
BuildRequires:	perl(XML::Parser)

# For plug-ins
BuildRequires:	alsa-lib-devel
BuildRequires:	gnome-menus-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gnutls-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libXxf86vm-devel
BuildRequires:	vte-devel

# For plug-ins-xfce
BuildRequires:	Thunar-devel

# For plug-ins-gecko
%if %{build_gecko} > 0
BuildRequires:	gecko-devel %{?gecko_ver: %{gecko_ver}}
%if 0%{?fedora} >= 9
BuildRequires:	gecko-devel-unstable
%endif
%endif

%description
An light eye-candy fully themable animated dock for any 
Linux desktop. It has a family-likeness with OSX dock,
but with more options.

%package	themes
Summary:	Additional themes for %{name}
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description	themes
This package contains a set of additional themes for %{name}.

%package	plug-ins
Summary:	Plug-ins files for %{name}
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}
%if %{build_gecko} == 0
Obsoletes:	%{name}-plug-ins-gecko < %{version}-%{release}
%endif

%description	plug-ins
This package contains plug-ins files for %{name}.

%package	plug-ins-xfce
Summary:	Plug-ins files for %{name} related to Xfce
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description	plug-ins-xfce
This package contains plug-ins files for %{name} related
to Xfce.

%package	plug-ins-gecko
Summary:	Plug-ins files for %{name} related to Gecko
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}
Requires:	gecko-libs %{?gecko_ver: %{gecko_ver}}

%description	plug-ins-gecko
This package contains plug-ins files for %{name} related
to Gecko.

%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries

Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig
Requires:	dbus-glib-devel
Requires:	gtk2-devel
Requires:	glitz-glx-devel
Requires:	librsvg2-devel
Requires:	libxml2-devel
Requires:	libXtst-devel

%description	devel
The %{name}-devel package contains libraries, build data, and header
files for developing applications that use %{name}.

%prep
%if 0%{released} < 1
%setup -q -c
%else

###
### This changed again....
%setup -q -c -a 1 -a 2
%{__ln_s} -f cairo-dock-%{mainver}%{?betaver:-%betaver} cairo-dock
%{__ln_s} -f cairo-dock-plugins-%{mainver}%{?betaver:-%betaver} plug-ins
%{__ln_s} -f cairo-dock-themes-%{mainver}%{?betaver:-%betaver} themes
%endif
###
###

%if 0
find . -type d -name \.svn | sort -r | xargs %{__rm} -rf
find . -type d -name \*CVS\* | sort -r | xargs %{__rm} -rf
%endif

pushd .
# A. main
cd cairo-dock
# temporary fix
#%%{__sed} -i.inline -e 's|^inline ||' src/cairo-dock-icons.*

# permission
for dir in */
	do
	find $dir -type f | xargs %{__chmod} 0644
done
%{__chmod} 0644 [A-Z]*

# Makefile issue
%{__sed} -i.debuglevel -e '/-O3/d' \
%if 0%{?released} > 0
	src/Makefile.in
%else
	src/Makefile.am

autoreconf -i -f
%endif

# B. themes
cd ../themes

%if 0%{?released} < 1
autoreconf -i -f
%endif

# C. plug-ins
cd ../plug-ins

#
# Note:
# * gnome-integration requires gio-2.0.pc, which is in F-9+ glib2-devel
# * weblets is gecko related, needs investigating
# * mail plug-ins is GPLv2 only, 
#   however source codes include "cairo-dock.h", which includes "cairo-dock-log.h",
#   which is GPLv3+, which makes license conflict.
#

# permission
%if 0%{?released} < 1
%{__chmod} 0644 Applets.stable
%endif
find . -name \*.h -or -name \*.c | xargs %{__chmod} 0644

# source code fix

# mail: license conflict
%{__rm} -rf mail/

# stacks: directory fix
%if 0%{?released} < 1
sed -i.dir -e '/stacksdatadir/s|pluginsdir|pluginsdatadir|' \
	stacks/configure.ac
%endif

# template: upstream says this is not needed
%{__rm} -rf template/

# weblets
%if %{build_gecko} > 0
cd weblets/
%{__sed} -i.gecko \
%if 0%{?fedora} < 9
	-e 's|xulrunner-gtkmozembed|firefox-gtkmozembed|' \
%else
	-e 's|xulrunner-gtkmozembed|mozilla-gtkmozembed|' \
%endif
	configure.ac

## NEED INVESTIGATING
sed -i.dir \
	-e 's|docshell/nsIScrollable.h|nsIScrollable.h|' \
	src/applet-widget-itf.cpp

cd ..
%else
%{__rm} -rf weblets/
%endif

# First deal with subdirs in topdir configure.ac, then else
Subdirs_1=$(%{__sed} -n -e '\@SUBDIR@,\@^.*[^\\]$@p' Makefile.am | sed -e 's|\\$||' | tail -n +2)
%{__sed} -n -e '\@_dir=@p' Makefile.am > eval.sh

. eval.sh
Subdirs=$(eval echo ${Subdirs_1})

# gnome-integration: needs F-9+
%if 0%{?fedora} < 9
Subdirs="${Subdirs} gnome-integration"
%endif

# Register Subdirs
echo $Subdirs > Subdirs.list

for dir in */
	do
	skip=0
	for ddir in $Subdirs
		do
		if [ $dir == ${ddir}/ ] ; then skip=1; fi
	done
	for ddir in autom* po translations
		do
		if [ $dir == ${ddir}/ ] ; then skip=2 ; fi
	done
	if [ $skip == 2 ] ; then continue ; fi
	cd $dir

	%{__sed} -i.error \
		-e 's|-O3|-O2|' \
		-e 's|-Werror\\|\\|' \
		-e 's|-Werror$||' \
%if 0%{?released} > 0
		src/Makefile.in
%else
		src/Makefile.am
%endif
	if [ $skip == 1 ] ; then 
		cd ..
		continue
	fi
%if %{build_other} > 0
	autoreconf -i -f
%endif
	cd ..
done

%if %{released} < 1
autoreconf -f -i
%endif

popd # from opt/cairo-dock/trunk/cairo-dock

%build
status=0

# A. main
pushd cairo-dock

%configure
%{__make} %{?_smp_mflags} -k || status=$((status+1))

# For plug-ins & themes
unlink cairo-dock || :
ln -sf src cairo-dock
export CFLAGS="%optflags -I$(pwd) -I$(pwd)/cairo-dock"
export CPPFLAGS="%optflags -I$(pwd) -I$(pwd)/cairo-dock"
export PKG_CONFIG_PATH=$(pwd):${PKG_CONFIG_PATH}

# B themes
cd ../themes

%configure
%{__make} %{?_smp_mflags} -k || status=$((status+1))

# C plug-ins
cd ../plug-ins

# First deal with subdirs in topdir configure.ac, then else
%configure \
%if 0%{?fedora} < 9
	--disable-gnome-integration \
%else
	--enable-gio \
%endif

# Parallel make fails some times, but it is gerenally fast
# so do parallel make anyway first
%{__make} %{?_smp_mflags} -k || :
%{__make} -k || status=$((status+1))

%if %{build_other} >= 1
Subdirs=$(cat Subdirs.list)
for dir in */
	do
	skip=0
	for ddir in $Subdirs autom* po translations
		do
		if [ $dir == ${ddir}/ ] ; then skip=1 ; fi
	done
	if [ $skip == 1 ] ; then continue ; fi
	cd $dir

	%configure
	# Parallel make fails some times, but it is gerenally fast
	# so do parallel make anyway first
	%{__make} %{?_smp_mflags} -k || :
	%{__make} -k || status=$((status+1))

	cd ..
done
%endif

popd # from opt/cairo-dock/trunk/cairo-dock
if [ $status -gt 0 ] ; then exit 1 ; fi

%install
%{__rm} -rf $RPM_BUILD_ROOT
TOPDIR=$(pwd)

# A. main
pushd cairo-dock
export PKG_CONFIG_PATH=$(pwd):${PKG_CONFIG_PATH}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -p"
%{__chmod} 0755 $RPM_BUILD_ROOT%{_bindir}/*.sh

# desktop files
if [ ! -f data/%{name}.desktop ] ; then
	cat > data/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Exec=cairo-dock
Icon=cairo-dock
Terminal=false

Name=Cairo-Dock
Name[fr]=Cairo-Dock

GenericName=Multi-purpose Dock
GenericName[fr]=Dock multi-usage
Categories=System;
EOF
fi

desktop-file-install \
	--dir $RPM_BUILD_ROOT%{_datadir}/applications \
	--vendor fedora \
	data/%{name}.desktop
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/pixmaps
%{__install} -cpm 644 data/%{name}.svg \
	$RPM_BUILD_ROOT%{_datadir}/pixmaps/

# documents
%{__rm} -rf $TOPDIR/documents/main
%{__mkdir} -p $TOPDIR/documents/main

## ???????
## NEEDFIX
for f in \
%if 0%{?released} < 1
	LICENSE \
%endif
	data/ChangeLog.txt \
%if 0%{?released} < 1
	doc/HOW-TO__applets.txt \
	doc/dox.config \
%endif
	
	do
	%{__cp} -pr $f $TOPDIR/documents/main/
done

%find_lang %{name}
%{__mv} -f %{name}.lang $TOPDIR

# B. themes
cd ../themes
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -p"

# clean up
pushd $RPM_BUILD_ROOT%{_datadir}/%{name}/themes
# no...
%{__rm} -rf ./_Ubuntu_/
popd # from $RPM_BUILD_ROOT

# C plug-ins
%{__rm} -rf $TOPDIR/{lang-plug-ins,lang-gecko}
%{__mkdir} -p $TOPDIR/{lang-plug-ins,lang-gecko}

cd ../plug-ins
# First deal with subdirs in topdir configure.ac, then else
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -p"

Subdirs=$(cat Subdirs.list)
for dir in */
	do
	skip=0
	for ddir in $Subdirs
		do
		if [ $dir == ${ddir}/ ] ; then skip=1 ; fi
	done
	# don't skip here
	# if [ $skip == 1 ] ; then continue ; fi

	for ddir in autom* po translations
		do
		if [ $dir == ${ddir}/ ] ; then skip=2 ; fi
	done
	if [ $skip == 2 ] ; then continue ; fi

	cd $dir

%if %{build_other} >= 1
	[ $skip != 1 ] && \
		%{__make} install \
		DESTDIR=$RPM_BUILD_ROOT \
		INSTALL="%{__install} -p"
%endif

	# read GETTEXT_PACKAGE
	if [ ! -r po/Makefile.in ] ; then
		cd ..
		continue
	fi

	GETTEXT_MO_PACKAGES=`sed -n -e 's|^GETTEXT_PACKAGE *= *||p' po/Makefile.in`
	case $GETTEXT_MO_PACKAGES in
		*weblet* )
			%find_lang $GETTEXT_MO_PACKAGES && \
				%{__mv} -f ${GETTEXT_MO_PACKAGES}.lang \
				$TOPDIR/lang-gecko/
				;;
		* )
			%find_lang $GETTEXT_MO_PACKAGES && \
				%{__mv} -f ${GETTEXT_MO_PACKAGES}.lang \
				$TOPDIR/lang-plug-ins/
				;;
	esac
	cd ..
done

# Temporary hack
find $RPM_BUILD_ROOT%{_libdir}/cairo-dock/ -name \*.so | xargs %{__chmod} 0755
find $RPM_BUILD_ROOT%{_libdir}/cairo-dock -name \*.so.* | xargs %{__rm} -f

# documents
%if 0%{?released} < 1
%{__cp} -p Applets.stable $TOPDIR/documents/main/
%endif

# lang files
cat $TOPDIR/lang-plug-ins/*.lang > $TOPDIR/lang-plug-ins.lang
%if %{build_gecko} > 0
cat $TOPDIR/lang-gecko/*.lang > $TOPDIR/lang-gecko.lang
%endif

popd # from opt/cairo-dock/trunk/cairo-dock

# final clean up
# remove all unneeded files
pushd $RPM_BUILD_ROOT
%{__rm} -f ./%{_datadir}/%{name}/{ChangeLog.txt,License}
find .%{_libdir}/%{name} -name \*.la | xargs %{__rm} -f

# just to suppress rpmlint...
for f in \
	`find ./%{_datadir}/%{name} -name \*.desktop` \
	`find . -name \*.conf`
	do
	echo > $f.tmp
	cat $f >> $f.tmp
	touch -r $f $f.tmp
	%{__mv} -f $f.tmp $f
done

set +x
for f in .%{_datadir}/%{name}/plug-ins/*/*
	do
	if head -n 1 $f 2>/dev/null | grep -q /bin/ ; then 
		set -x
		%{__chmod} 0755 $f
		set +x
	fi
done
set -x

popd # from $RPM_BUILD_ROOT

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc	documents/main/*

%{_bindir}/*%{name}*
%{_datadir}/applications/fedora-%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg

%dir	%{_datadir}/%{name}/
%{_datadir}/%{name}/*.conf
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%{_datadir}/%{name}/*view
%{_datadir}/%{name}/emblems/
%{_datadir}/%{name}/explosion/
%{_datadir}/%{name}/gauges/
%dir	%{_datadir}/%{name}/themes/
%dir	%{_datadir}/%{name}/plug-ins/
%{_datadir}/%{name}/themes/_default_/
# only directory
%dir	%{_libdir}/%{name}/

%files	themes
%defattr(-,root,root,-)
%{_datadir}/%{name}/themes/_[A-Z]*/

%files	plug-ins -f lang-plug-ins.lang
%defattr(-,root,root,-)
%{_libdir}/%{name}/*
%{_datadir}/%{name}/plug-ins/*
%if %{build_gecko}
%exclude	%{_libdir}/%{name}/*weblet*
%exclude	%{_datadir}/%{name}/plug-ins/*weblet*
%endif
%exclude	%{_libdir}/%{name}/*xfce*
%exclude	%{_datadir}/%{name}/plug-ins/*xfce*

%files	plug-ins-xfce
%defattr(-,root,root,-)
%{_libdir}/%{name}/*xfce*
%{_datadir}/%{name}/plug-ins/*xfce*

%if %{build_gecko} > 0
%files	plug-ins-gecko -f lang-gecko.lang
%defattr(-,root,root,-)
%{_libdir}/%{name}/*weblet*
%{_datadir}/%{name}/plug-ins/*weblet*
%endif

%files	devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue May 19 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1.6.3.1-2
- Rebuild on rpmfusion

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

