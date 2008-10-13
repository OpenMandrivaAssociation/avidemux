%define	name	avidemux
%define	Name	Avidemux
%define version 2.4.3
%define rel 1
%define pre 0
%if %pre
%define filename %{name}_%{version}_preview%pre
%define release %mkrel 0.preview%pre.%rel
%else 
%define filename %{name}_%version
%define release %mkrel %rel
%endif

%bcond_with plf

%if %with plf
%define distsuffix plf
%endif

%define	pkgsummary	A free video editor
%define build_mmx 1
%{?_with_mmx: %{expand: %%define build_mmx 1}}
%{?_without_mmx: %{expand: %%define build_mmx 0}}

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	%{pkgsummary}
Source0:	http://download.berlios.de/avidemux/%{filename}.tar.gz
Patch0:		avidemux_2.4.1-qt4.patch
Patch1:		avidemux-2.4-i18n.patch
Patch2:		avidemux-2.4-libdca.patch
License:	GPLv2+
Group:		Video
Url:		http://fixounet.free.fr/avidemux
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gtk+2-devel >= 2.6.0
BuildRequires:	qt4-devel qt4-linguist
BuildRequires:	SDL-devel
BuildRequires:	nasm
BuildRequires:	libxml2-devel
BuildRequires:	libmad-devel
BuildRequires:	liba52dec-devel
BuildRequires:	libarts-devel 
BuildRequires:	libvorbis-devel
BuildRequires:	esound-devel
BuildRequires:	libjack-devel
BuildRequires:	libpulseaudio-devel
BuildRequires:	libsamplerate-devel
BuildRequires:	gettext-devel
BuildRequires:	cmake
BuildRequires:	libxslt-proc
# not packaged yet:
#BuildRequires:  libaften-devel
%if %with plf
BuildRequires:	libxvid-devel
BuildRequires:	liblame-devel
BuildRequires:	libfaad2-devel
BuildRequires:	libfaac-devel
BuildRequires:	x264-devel
BuildRequires:  libamrnb-devel
BuildRequires:	libdca-devel
%endif
BuildRequires:	ImageMagick
Requires: avidemux-ui

%description
Avidemux is a free video editor designed for simple cutting,
filtering and encoding tasks.It supports many file types, including
AVI, DVD compatible MPEG files, MP4 and ASF, using a variety of
codecs. Tasks can be automated using projects, job queue and
powerful scripting capabilities.

%if %with plf
This package is in PLF because this build has support for codecs
covered by software patents.
%endif

%package gtk
Summary:	%{pkgsummary} - GTK GUI
Group:		Video
Requires: gtk+2.0 >= 2.6.0
Requires: %name >= %version
Provides: avidemux-ui

%description gtk
Avidemux is a free video editor. This package contains the
version with a graphical user interface based on GTK.

%package qt
Summary:	%{pkgsummary} - Qt4 GUI
Group:		Video
Requires: %name >= %version
Provides: avidemux-ui

%description qt
Avidemux is a free video editor. This package contains the
version with a graphical user interface based on Qt4.

%package cli
Summary:	%{pkgsummary} - command-line version
Group:		Video
Provides: avidemux-ui

%description cli
Avidemux is a free video editor. This package contains the
version with a command-line interface.

%if %with plf
This package is in PLF because this build has support for codecs
covered by software patents.
%endif

%prep
%setup -q -n %filename
%patch0 -p1
%patch1 -p1
%patch2 -p1 -b .libdca

%build
#gw FIXME: How do I disable MMX with cmake?
%cmake
%make

%install
rm -rf $RPM_BUILD_ROOT
cd build
%makeinstall_std
cd ..

# icons
install -d -m755 $RPM_BUILD_ROOT%{_liconsdir}
install -d -m755 $RPM_BUILD_ROOT%{_iconsdir}
install -d -m755 $RPM_BUILD_ROOT%{_miconsdir}
convert avidemux_icon.png -resize 48x48 $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert avidemux_icon.png -resize 32x32 $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert avidemux_icon.png -resize 16x16 $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

# menu
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}-gtk.desktop << EOF
[Desktop Entry]
Name=%{Name}
Comment=%{pkgsummary}
Exec=%{_bindir}/%{name}2_gtk %U
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Video;AudioVideoEditing;GTK;
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}-qt.desktop << EOF
[Desktop Entry]
Name=%{Name}
Comment=%{pkgsummary}
Exec=%{_bindir}/%{name}2_qt4 %U
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Video;AudioVideoEditing;Qt;
EOF

rm -rf %buildroot%_datadir/locale/klingon

%{find_lang} %{name}

%if %mdkversion <= 200710
# compatibility symlink
ln -s avidemux2_gtk %{buildroot}%{_bindir}/avidemux2
%endif

%if %mdkversion < 200900
%post gtk
%{update_menus}
%endif

%if %mdkversion < 200900
%postun gtk
%{clean_menus}
%endif

%if %mdkversion < 200900
%post qt
%{update_menus}
%endif

%if %mdkversion < 200900
%postun qt
%{clean_menus}
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL TODO History README
%if %mdkversion <= 200710
%{_bindir}/avidemux2
%endif
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files gtk
%defattr(-,root,root)
%{_bindir}/avidemux2_gtk
%_datadir/applications/mandriva-avidemux-gtk.desktop

%files qt
%defattr(-,root,root)
%{_bindir}/avidemux2_qt4
%_datadir/applications/mandriva-avidemux-qt.desktop
%dir %_datadir/%name
%dir %_datadir/%name/i18n
%_datadir/%name/i18n/*.qm


%files cli
%defattr(-,root,root)
%doc README
%{_bindir}/avidemux2_cli
