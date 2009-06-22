# NOTE!
# Now for weblet plug-ins now cairo-dock uses WebKit, not Gecko.

# For svn
# svn checkout http://svn.berlios.de/svnroot/repos/cairo-dock/trunk
# cd trunk
# tar cjf ../cairo-dock-sources-%%{tag}.tar.bz2 .

%global		released	0
%define		pre_release	1
# Set the below to 1 when building unstable plug-ins
%global		build_other	1

%global		mainver		2.0.6
%define		betaver		svn1832_trunk

%global		build_themes	0

%global		build_webkit	1
%global		build_xfce	1

%global		fedora_main_rel	1


%global		fedora_rel	%{?pre_release:0.}%{fedora_main_rel}%{?betaver:.%betaver}

%if 0%{?released} >= 1
%global		build_other	0
%endif
# Now WebKit plug-in is (will be) included in released tarball
%if %{build_other} < 1
%global		build_webkit	1
%endif


Name:		cairo-dock
Version:	%{mainver}
Release:	%{fedora_rel}%{?dist}
Summary:	Light eye-candy fully themable animated dock

Group:		User Interface/Desktops
License:	GPLv3+
URL:		http://www.cairo-dock.org/
%if 0%{?released} < 1
Source0:	%{name}-sources-%{betaver}.tar.bz2
%else
Source0:	http://download.berlios.de/cairo-dock/%{name}-%{mainver}%{?betaver:-%betaver}.tar.bz2
%if %{build_themes} 
Source1:	http://download.berlios.de/cairo-dock/%{name}-themes-%{mainver}%{?betaver:-%betaver}.tar.bz2
%endif
Source2:	http://download.berlios.de/cairo-dock/%{name}-plugins-%{mainver}%{?betaver:-%betaver}.tar.bz2
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# plug-ins specific patches
Patch100:	cairo-dock-rev1677-stacks.patch
#Patch200:	xorg-x11-proto-devel-workaround-bz505774.patch

%if ! %{released}
BuildRequires:	automake
BuildRequires:	intltool
BuildRequires:	libtool
%endif
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

# For main package
BuildRequires:	dbus-glib-devel
BuildRequires:	glitz-glx-devel
BuildRequires:	gtk2-devel
BuildRequires:	gtkglext-devel
BuildRequires:	librsvg2-devel
BuildRequires:	libXcomposite-devel
BuildRequires:	libXinerama-devel
BuildRequires:	libXrender-devel
BuildRequires:	libxml2-devel
BuildRequires:	libXtst-devel
BuildRequires:	perl(XML::Parser)

# For plug-ins
BuildRequires:	alsa-lib-devel
BuildRequires:	gnome-menus-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	libexif-devel
BuildRequires:	libgnomeui-devel
BuildRequires:	libxklavier-devel
BuildRequires:	libXxf86vm-devel
BuildRequires:	vte-devel
# Not shown in .pc files
BuildRequires:	libetpan-devel
# For plug-ins-xfce
%if %{build_xfce} > 0
BuildRequires:	Thunar-devel
%endif
%if %{build_webkit} > 0
# For plug-ins-webkit
# Now using webkit, not gecko
BuildRequires:	WebKit-gtk-devel
%endif
# Requires related to commands used internally
# in cairo-dock
Requires:	findutils
Requires:	wget
Requires:	xterm

# Obsoletes moved to main package
# Switch to Webkit, always obsolete gecko (and _not_ provide it)
Obsoletes:	%{name}-plug-ins-gecko < %{version}-%{release}
%if %{build_webkit} == 0
Obsoletes:	%{name}-plug-ins-webkit < %{version}-%{release}
%endif
%if %{build_xfce} == 0
Obsoletes:	%{name}-plug-ins-xfce < %{version}-%{release}
%endif
# cairo-dock-themes is obsoleted
%if ! %{build_themes}
Obsoletes:	%{name}-themes < %{version}-%{release}
%endif

%description
An light eye-candy fully themable animated dock for any 
Linux desktop. It has a family-likeness with OSX dock,
but with more options.

%package	themes
# Kill AutoProv to remove unwilling desktop prov
AutoProv:	No
BuildArch:	noarch
Summary:	Additional themes for %{name}
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description	themes
This package contains a set of additional themes for %{name}.

%package	plug-ins
Summary:	Plug-ins files for %{name}
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description	plug-ins
This package contains plug-ins files for %{name}.

%package	plug-ins-xfce
Summary:	Plug-ins files for %{name} related to Xfce
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description	plug-ins-xfce
This package contains plug-ins files for %{name} related
to Xfce.

%package	plug-ins-webkit
Summary:	Plug-ins files for %{name} related to Gecko
Group:		User Interface/Desktops
Requires:	%{name} = %{version}-%{release}

%description	plug-ins-webkit
This package contains plug-ins files for %{name} related
to webkit.

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
%if %{build_themes}
%setup -q -c -a 1 -a 2
%else
%setup -q -c -a 2
%endif
%{__ln_s} -f cairo-dock-%{mainver}%{?betaver:-%betaver} cairo-dock
%if %{build_themes}
%{__ln_s} -f cairo-dock-themes-%{mainver}%{?betaver:-%betaver} themes
%endif
%{__ln_s} -f cairo-dock-plugins-%{mainver}%{?betaver:-%betaver} plug-ins
%endif
###

%if 0
find . -type d -name \.svn | sort -r | xargs %{__rm} -rf
find . -type d -name \*CVS\* | sort -r | xargs %{__rm} -rf
%endif

pushd .

%if 0
####
# Workaround for bz 506656
mkdir -p .%{_includedir}/X11/extensions
pushd .%{_includedir}/X11/extensions
cp -p %{_includedir}/X11/extensions/XTest.h .
%patch200 -p4
popd

%global optflags_ %{optflags}
%global optflags %{optflags_} -I%{_builddir}/%{name}-%{version}/%{_includedir}
####
%endif

# A. main
cd cairo-dock

# Patch

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

# desktop file
%{__sed} -i.icon \
	-e 's|Icon=\*|Icon=cairo-dock|' \
	data/cairo-dock*.desktop

# B. themes
%if %{build_themes}
cd ../themes

%if 0%{?released} < 1
autoreconf -i -f
%endif
%endif

# C. plug-ins
cd ../plug-ins

# permission
%if 0%{?released} < 1
%{__chmod} 0644 Applets.stable
%endif
find . -name \*.h -or -name \*.c | xargs %{__chmod} 0644

# source code fix

# dialog-rendering
find dialog-rendering -type f \
	\( -not -path '*/.svn/*' -and -not -name \*.png \) \
	| xargs %{__sed} -i -e 's|\r||'

# stacks: directory fix
%if 0%{?released} < 1
%patch100 -p0 -b .compile
%{__sed} -i.dir -e '/stacksdatadir/s|pluginsdir|pluginsdatadir|' \
	stacks/configure.ac
%endif

# template: upstream says this is not needed
%{__rm} -rf template/


# First deal with subdirs in configure.ac of topdir, then else
if [ -f Makefile.am ] ; then
	Subdirs_1=$(%{__sed} -n -e '\@SUBDIR@,\@^.*[^\\]$@p' Makefile.am | sed -e 's|\\$||' | tail -n +2)
	%{__sed} -n -e '\@_dir=@p' Makefile.am > eval.sh

# Now bash 4.0 "source" command does not search for the current
# directory when executed as "sh" (in posix mode)
	. ./eval.sh
	Subdirs=$(eval echo ${Subdirs_1})

# Register Subdirs
	echo $Subdirs > Subdirs.list
else
	rm -f Subdirs.list
	for ddir in */ ; do echo $ddir >> Subdirs.list ; done
	%{__sed} -i.1 -e '\@po/@d' Subdirs.list
fi

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
%global	__make	\
	%{_bindir}/make -k GMSGFMT="%{_bindir}/msgfmt --statistics"

# A. main
pushd cairo-dock

# --enable-glitz cannot be set because cairo-glitz.h is missing
# (Fedora cairo does not support glitz)
%configure

# Workaround to avoid endless loop on po/
touch po/stamp-it

%{__make} %{?_smp_mflags} || status=$((status+1))

# For plug-ins & themes
unlink cairo-dock || :
ln -sf src cairo-dock
export CFLAGS="%optflags -I$(pwd) -I$(pwd)/cairo-dock"
export CPPFLAGS="%optflags -I$(pwd) -I$(pwd)/cairo-dock"
export PKG_CONFIG_PATH=$(pwd):${PKG_CONFIG_PATH}

# B themes
%if %{build_themes}
cd ../themes

%configure
%{__make} %{?_smp_mflags} || status=$((status+1))
%endif

# C plug-ins
cd ../plug-ins

# First deal with subdirs in topdir configure.ac, then else

%configure \
	--enable-gio-in-gmenu \


# Workaround to avoid endless loop on po/
touch po/stamp-it

# Parallel make fails some times, but it is gerenally fast
# so do parallel make anyway first
retry=0
%{__make} %{?_smp_mflags} || retry=1
if [ $retry == 1 ] ; then
	%{__make} || status=$((status+1))
fi

%if %{build_other} >= 1
Subdirs=$(cat Subdirs.list)
for dir in */
do
	unset CONFIGURE_OPTS
	skip=0
	for ddir in $Subdirs autom* po translations
		do
		if [ $dir == ${ddir}/ ] ; then skip=1 ; fi
	done
	if [ $skip == 1 ] ; then continue ; fi
	cd $dir

	%configure $CONFIGURE_OPTS
	# Parallel make fails some times, but it is gerenally fast
	# so do parallel make anyway first
	%{__make} %{?_smp_mflags} || :
	%{__make} || status=$((status+1))

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
# debian file, not useful
%{__rm} -f $RPM_BUILD_ROOT%{_bindir}/cairo-dock-update.sh

for f in $RPM_BUILD_ROOT%{_datadir}/applications/*desktop
do
	desktop-file-validate $f
done
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/pixmaps
%{__install} -cpm 644 data/%{name}.svg \
	$RPM_BUILD_ROOT%{_datadir}/pixmaps/

# documents
%{__rm} -rf $TOPDIR/documents/main
%{__mkdir} -p $TOPDIR/documents/main

for f in \
	LICENSE \
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
%if %{build_themes}
cd ../themes
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -p"

# clean up
pushd $RPM_BUILD_ROOT%{_datadir}/%{name}/themes
# no...
%{__rm} -rf ./_Ubuntu_/
popd # from $RPM_BUILD_ROOT
%endif

# C plug-ins
%{__rm} -rf $TOPDIR/{lang-plug-ins,lang-webkit}
%{__mkdir} -p $TOPDIR/{lang-plug-ins,lang-webkit}

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
				$TOPDIR/lang-webkit/
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
find $TOPDIR/lang-plug-ins/ -name '*.lang' | xargs cat > $TOPDIR/lang-plug-ins.lang
%if %{build_webkit} > 0
find $TOPDIR/lang-webkit/ -name '*.lang' | xargs cat > $TOPDIR/lang-webkit.lang
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

# For now these are not needed
rm -f %{buildroot}%{_libdir}/libcairo-dock.*

%clean
%{__rm} -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc	documents/main/*

%{_bindir}/*%{name}*
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/pixmaps/%{name}.svg

%dir	%{_datadir}/%{name}/
%{_datadir}/%{name}/*.conf
%{_datadir}/%{name}/*.png
%{_datadir}/%{name}/*.svg
%{_datadir}/%{name}/*.xpm
%{_datadir}/%{name}/*view
%{_datadir}/%{name}/emblems/
%{_datadir}/%{name}/explosion/
%{_datadir}/%{name}/gauges/
%dir	%{_datadir}/%{name}/themes/
%dir	%{_datadir}/%{name}/plug-ins/
%{_datadir}/%{name}/themes/_default_/
# only directory
%dir	%{_libdir}/%{name}/

%if %{build_themes}
%files	themes
%defattr(-,root,root,-)
%{_datadir}/%{name}/themes/_[A-Z]*/
%endif

%files	plug-ins -f lang-plug-ins.lang
%defattr(-,root,root,-)
%{_libdir}/%{name}/*
%{_datadir}/%{name}/plug-ins/*
%if %{build_webkit} > 0
%exclude	%{_libdir}/%{name}/*weblet*
%exclude	%{_datadir}/%{name}/plug-ins/*weblet*
%endif
%if %{build_xfce} > 0
%exclude	%{_libdir}/%{name}/*xfce*
%exclude	%{_datadir}/%{name}/plug-ins/*xfce*
%endif

%if %{build_xfce} > 0
%files	plug-ins-xfce
%defattr(-,root,root,-)
%{_libdir}/%{name}/*xfce*
%{_datadir}/%{name}/plug-ins/*xfce*
%endif

%if %{build_webkit} > 0
%files	plug-ins-webkit -f lang-webkit.lang
%defattr(-,root,root,-)
%{_libdir}/%{name}/*weblet*
%{_datadir}/%{name}/plug-ins/*weblet*
%endif

%files	devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jun 23 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- rev 1832
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

