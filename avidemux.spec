%define libname		%mklibname %{name}
%define filename %{name}%{!?git:_%{version}}%{?git:2-master}
%define _disable_ld_no_undefined 1
#define _disable_lto 1
%define git 20251101

#define ffmpeg_version 2.7.7

#############################
# Hardcore PLF build
# bcond_with or bcond_without
%bcond_with plf
#############################

%if %with plf
%define distsuffix plf
# make EVR of plf build higher than regular to allow update, needed with rpm5 mkrel
%define extrarelsuffix plf
%endif

Summary:	A free video editor
Name:		avidemux
Version:	2.8.2%{?git:~%{git}}
Release:	2%{?extrarelsuffix}
License:	GPLv2+
Group:		Video
Url:		https://avidemux.sourceforge.net/
%if 0%{?git:1}
Source0:	https://github.com/mean00/avidemux2/archive/refs/heads/master.tar.gz#/%{name}-%{git}.tar.gz
%else
Source0:	https://jztkft.dl.sourceforge.net/project/avidemux/avidemux/%{version}/avidemux_%{version}.tar.gz
%endif
Source100:	%{name}.rpmlintrc
Patch7:		avidemux-compile.patch
BuildRequires:	cmake
BuildRequires: ninja
BuildRequires:	dos2unix
BuildRequires:	imagemagick
BuildRequires:	nasm
BuildRequires:	xsltproc
BuildRequires:	yasm
BuildRequires: which
BuildRequires:	gettext-devel
BuildRequires:	a52dec-devel
BuildRequires: lame-devel
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Gui)
BuildRequires:  pkgconfig(Qt6Network)
BuildRequires:  pkgconfig(Qt6OpenGL)
BuildRequires:  pkgconfig(Qt6OpenGLWidgets)
BuildRequires:  pkgconfig(Qt6Widgets)
BuildRequires:  qmake-qt6
BuildRequires:	pkgconfig(jack)
BuildRequires: pkgconfig(aom)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(sqlite3)
BuildRequires: pkgconfig(libass)
BuildRequires: pkgconfig(vapoursynth)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(twolame)
BuildRequires: pkgconfig(opus)	
%ifnarch %{armx} %{arm}
BuildRequires: pkgconfig(ffnvcodec)
%endif
# not packaged yet:
#BuildRequires:  libaften-devel
%if %with plf
BuildRequires:	libfaac-devel
BuildRequires:	libfaad2-devel
BuildRequires: pkgconfig(libdca)
BuildRequires:	libxvid-devel
BuildRequires:	pkgconfig(opencore-amrnb)
BuildRequires:	pkgconfig(opencore-amrwb)
BuildRequires:	pkgconfig(x264)
BuildRequires: pkgconfig(x265)
%endif
BuildRequires:	pkgconfig(glu)
Requires:	avidemux-qt

%description
Avidemux is a free video editor designed for simple cutting,
filtering and encoding tasks.It supports many file types, including
AVI, DVD compatible MPEG files, MP4 and ASF, using a variety of
codecs. Tasks can be automated using projects, job queue and
powerful scripting capabilities.

%if %with plf
This package is in restricted because this build has support for codecs
covered by software patents.
%endif

%package -n	%{libname}
Summary:	Shared libraries for %{name}

%description -n	%{libname}
Shared libraries for %{name}.

%package	devel
Summary:	Header files for %{name}
Requires:	%{libname} = %{version}
Obsoletes:	%{name}-qt-devel < %{version}-%{release}
Obsoletes:	%{name}-cli-devel < %{version}-%{release}

%description	devel
Header files for %{name}.

%package	cli
Summary:	Command line interface for %{name}
%rename		%{name}
Recommends:	%{name}-plugins
Recommends:	%{name}-cli-plugins

%description	cli
This package contains the command-line interface for %{name}.

%package	qt
Summary:	Qt graphical user interface for %{name}
%rename		%{name}
Recommends:	%{name}-plugins
Recommends:	%{name}-qt-plugins

%description	qt
This package contains the Qt graphical user interface for %{name}.

%package	plugins
Summary:	Plugins for %{name}

%description	plugins
This package contains the common plugins for %{name}.

%package	cli-plugins
Summary:	Plugins for %{name}-cli

%description	cli-plugins
This package contains the plugins for the %{name} command-line interface.

%package	qt-plugins
Summary:	Plugins for %{name}-qt

%description	qt-plugins
This package contains the plugins for the %{name} graphical user interface.

%if %with plf
This package is in restricted because this build has support for codecs
covered by software patents.
%endif

%prep
%autosetup -p1 -n %{filename}

#sed -i 's/set(FFMPEG_VERSION "2.7.6")/set(FFMPEG_VERSION "%{ffmpeg_version}")/' cmake/admFFmpegBuild.cmake
#rm -f avidemux_core/ffmpeg_package/ffmpeg-*.tar.bz2
#cp %{SOURCE1} avidemux_core/ffmpeg_package/


%build
%setup_compile_flags
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"

export PATH=%{_libdir}/qt5/bin:$PATH

bash bootStrap.bash \
     --with-core \
     --with-cli \
     --with-plugins \
     --with-system-liba52 \
     --with-system-libmad \
     --with-ninja || cat /tmp/logCmakebuildQt6

%install
cp -a install/* %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man1
install -m 644 man/avidemux.1 %{buildroot}%{_mandir}/man1
chrpath --delete %{buildroot}%{_libdir}/*.so*
chrpath --delete %{buildroot}%{_libdir}/ADM_plugins6/*/*.so
chrpath --delete %{buildroot}%{_bindir}/*
rm -rf %{buildroot}%{_datadir}/ADM6_addons


%files -n %{libname}
%{_libdir}/libADM_audio*.so
%{_libdir}/libADM_core*.so
%{_libdir}/libADM6*.so.*

%files devel
%{_includedir}/%{name}

%files cli
%{_mandir}/man1/avidemux.1*
%{_bindir}/avidemux3_cli
%{_libdir}/libADM_UI_Cli6.so
%{_libdir}/libADM_render6_cli.so

%files qt
%{_bindir}/avidemux3_qt6
%{_bindir}/avidemux3_jobs_qt6
%{_bindir}/vsProxy
%{_bindir}/vsProxy_gui_qt6
%{_libdir}/libADM_render6_QT6.so
%{_libdir}/libADM_UIQT66.so
%{_libdir}/libADM_openGLQT66.so
%{_datadir}/metainfo/org.avidemux.Avidemux.appdata.xml
%{_iconsdir}/hicolor/128x128/apps/org.avidemux.Avidemux.png
%{_datadir}/applications/org.avidemux.Avidemux.desktop

%files plugins
%dir %{_libdir}/ADM_plugins6
%dir %{_libdir}/ADM_plugins6/*
%{_libdir}/ADM_plugins6/*/*
%exclude %{_libdir}/ADM_plugins6/videoFilters/cli/*.so
%exclude %{_libdir}/ADM_plugins6/videoFilters/qt6/*.so

%files cli-plugins
%{_libdir}/ADM_plugins6/videoFilters/cli/*.so

%files qt-plugins
%{_libdir}/ADM_plugins6/videoFilters/qt6/*.so
