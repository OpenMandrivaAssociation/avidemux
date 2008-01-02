%define	name	avidemux
%define	Name	Avidemux
%define version 2.4
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
License:	GPL
Group:		Video
Url:		http://fixounet.free.fr/avidemux
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	gtk+2-devel >= 2.6.0
BuildRequires:	SDL-devel
BuildRequires:	nasm
BuildRequires:	libxml2-devel
BuildRequires:	libmad-devel
BuildRequires:	liba52dec-devel
BuildRequires:	libarts-devel 
BuildRequires:	libvorbis-devel
BuildRequires:	esound-devel
BuildRequires:	gettext-devel
# not packaged yet:
#BuildRequires:  libaften-devel
%if %with plf
BuildRequires:	libxvid-devel
BuildRequires:	liblame-devel
BuildRequires:	libfaad2-devel
BuildRequires:	libfaac-devel
BuildRequires:	x264-devel
BuildRequires:  libamrnb-devel
BuildRequires:	dtsdec-devel > 0.0.2-4
%endif
BuildRequires:	automake1.8
BuildRequires:	ImageMagick
Requires: gtk+2.0 >= 2.6.0

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

%package cli
Summary:	%{pkgsummary} - command-line version
Group:		Video

%description cli
Avidemux is a free video editor. This package contains the
version with a command-line interface.

%if %with plf
This package is in PLF because this build has support for codecs
covered by software patents.
%endif

%prep
%setup -q -n %filename

%build
sh admin/cvs.sh cvs
%configure2_5x --disable-warnings \
%if %with plf
	--enable-twolame \
	--enable-amr_nb \
%endif
%if ! %build_mmx
	--disable-mmx
%endif

# parallel build broken as of 2.3-0.preview2
make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

# icons
install -d -m755 $RPM_BUILD_ROOT%{_liconsdir}
install -d -m755 $RPM_BUILD_ROOT%{_iconsdir}
install -d -m755 $RPM_BUILD_ROOT%{_miconsdir}
convert avidemux_icon.png -resize 48x48 $RPM_BUILD_ROOT%{_liconsdir}/%{name}.png
convert avidemux_icon.png -resize 32x32 $RPM_BUILD_ROOT%{_iconsdir}/%{name}.png
convert avidemux_icon.png -resize 16x16 $RPM_BUILD_ROOT%{_miconsdir}/%{name}.png

# menu
install -d -m 755 $RPM_BUILD_ROOT%{_menudir}
cat >$RPM_BUILD_ROOT%{_menudir}/%{name} <<EOF
?package(%{name}): \
	command="%{_bindir}/%{name}2_gtk"\
	needs="X11"\
	section="Multimedia/Video"\
	icon="%{name}.png"\
	title="%{Name}"\
	longtitle="%{pkgsummary}" xdg="true"
EOF
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=%{Name}
Comment=%{pkgsummary}
Exec=%{_bindir}/%{name}2_gtk %U
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Video;AudioVideoEditing;X-MandrivaLinux-Multimedia-Video;GTK;
EOF
rm -rf %buildroot%_datadir/locale/klingon

%{find_lang} %{name}

%if %mdkversion <= 200710
# compatibility symlink
ln -s avidemux2_gtk %{buildroot}%{_bindir}/avidemux2
%endif

%post
%{update_menus}

%postun
%{clean_menus}

%clean 
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL TODO History README
%if %mdkversion <= 200710
%{_bindir}/avidemux2
%endif
%{_bindir}/avidemux2_gtk
%{_menudir}/%{name}
%_datadir/applications/mandriva-*
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png

%files cli -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/avidemux2_cli
