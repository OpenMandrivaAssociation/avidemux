%define filename %{name}_%{version}
%define _disable_ld_no_undefined 1
%define _disable_lto 1

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
Version:	2.7.1
Release:	1%{?extrarelsuffix}
License:	GPLv2+
Group:		Video
Url:		http://fixounet.free.fr/avidemux
Source0:	http://www.fosshub.com/Avidemux.html/avidemux_%{version}.tar.gz
#Source1:	ffmpeg-%{ffmpeg_version}.tar.bz2
Source100:	%{name}.rpmlintrc
Patch1:		avidemux-2.6.12-compile.patch
Patch2:		avidemux-2.5.1-opencore-check.patch
Patch3:		avidemux-jack-underlinking.patch
Patch4:		avidemux-fix-cmake.patch
Patch5:		avidemux-2.6.8-ffmpeg-1.2.12.patch
Patch6:		avidemux-2.7.0-c++.patch
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	imagemagick
BuildRequires:	nasm
BuildRequires:	xsltproc
BuildRequires:	yasm
BuildRequires:	gettext-devel
BuildRequires:	a52dec-devel
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5OpenGL)
BuildRequires:  pkgconfig(Qt5Script)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  qmake5
BuildRequires:  qt5-linguist-tools
BuildRequires:  qt5-qttools
BuildRequires:	%{_lib}qt5gui5-vnc
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(libva)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(mad)
BuildRequires:	pkgconfig(samplerate)
BuildRequires:	pkgconfig(sdl)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(xv)
BuildRequires:	pkgconfig(sqlite3)
# not packaged yet:
#BuildRequires:  libaften-devel
%if %with plf
BuildRequires:	libfaac-devel
BuildRequires:	libfaad2-devel
BuildRequires:	liblame-devel
BuildRequires:	libxvid-devel
BuildRequires:	pkgconfig(opencore-amrnb)
BuildRequires:	pkgconfig(opencore-amrwb)
BuildRequires:	pkgconfig(x264)
%endif
BuildRequires:	pkgconfig(glu)
Requires:	avidemux-ui

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

%package qt
Summary:	A free video editor - Qt5 GUI
Group:		Video
Requires:	%{name} = %{version}-%{release}
Provides:	avidemux-ui = %{version}-%{release}

%description qt
Avidemux is a free video editor. This package contains the
version with a graphical user interface based on Qt5.

%package cli
Summary:	A free video editor - command-line version
Group:		Video
Requires:	%{name} = %{version}-%{release}
Provides:	avidemux-ui = %{version}-%{release}

%description cli
Avidemux is a free video editor. This package contains the
version with a command-line interface.

%if %with plf
This package is in restricted because this build has support for codecs
covered by software patents.
%endif

%prep
%setup -qn %{filename}

dos2unix avidemux/common/ADM_render/CMakeLists.txt

#sed -i 's/set(FFMPEG_VERSION "2.7.6")/set(FFMPEG_VERSION "%{ffmpeg_version}")/' cmake/admFFmpegBuild.cmake
#rm -f avidemux_core/ffmpeg_package/ffmpeg-*.tar.bz2
#cp %{SOURCE1} avidemux_core/ffmpeg_package/

%apply_patches


%build
# Get rid of patch backups -- some CMake files in avidemux
# package all files in a directory as headers to be installed
# and included in the final package...
find . -name "*.*~" |xargs rm

%setup_compile_flags
export CFLAGS="%{optflags} -fno-strict-aliasing"
export CXXFLAGS="%{optflags} -fno-strict-aliasing"

export PATH=%{_libdir}/qt5/bin:$PATH

TOP=`pwd`
touch previous.dirs
touch previous.files
mkdir build
cd build
for i in avidemux_core avidemux/qt4 avidemux/cli; do
	mkdir -p $i
	cd $i
	cmake $TOP/$i -DENABLE_QT5=True -DAVIDEMUX_SOURCE_DIR=$TOP -DFAKEROOT=$TOP/DEST -DCMAKE_INSTALL_PREFIX=%_prefix -DCMAKE_STRIP=/bin/true
	%make
	make install DESTDIR=$TOP/DEST
	cd -
	cd $TOP/DEST
	find . -type d >$TOP/current.dirs
	find . -type f >$TOP/current.files
	cat $TOP/previous.files $TOP/previous.files $TOP/current.files |sort |uniq -u >$TOP/build/$i/file.list
	cat $TOP/previous.dirs $TOP/previous.dirs $TOP/current.dirs |sort |uniq -u >$TOP/build/$i/dirs.list
	cat $TOP/previous.files $TOP/build/$i/file.list |sort >$TOP/tmp
	mv -f $TOP/tmp $TOP/previous.files
	cat $TOP/previous.dirs $TOP/build/$i/dirs.list |sort >$TOP/tmp
	mv -f $TOP/tmp $TOP/previous.dirs
	cd -
done
for i in COMMON QT4 CLI SETTINGS; do
	mkdir -p $i
	cd $i
	cmake $TOP/avidemux_plugins -DENABLE_QT5=True -DAVIDEMUX_SOURCE_DIR=$TOP -DFAKEROOT=$TOP/DEST -DCMAKE_INSTALL_PREFIX=%_prefix -DPLUGIN_UI=$i -DCMAKE_STRIP=/bin/true
	make
	make install DESTDIR=$TOP/DEST
	cd -
	cd $TOP/DEST
	find . -type d >$TOP/current.dirs
	find . -type f >$TOP/current.files
	cat $TOP/previous.files $TOP/previous.files $TOP/current.files |sort |uniq -u >$TOP/build/$i/file.list
	cat $TOP/previous.dirs $TOP/previous.dirs $TOP/current.dirs |sort |uniq -u >$TOP/build/$i/dirs.list
	cat $TOP/previous.files $TOP/build/$i/file.list |sort >$TOP/tmp
	mv -f $TOP/tmp $TOP/previous.files
	cat $TOP/previous.dirs $TOP/build/$i/dirs.list |sort >$TOP/tmp
	mv -f $TOP/tmp $TOP/previous.dirs
	cd -
done

%install
mkdir -p %{buildroot}
cp -a DEST/* %{buildroot}

# icons
install -d -m755 %{buildroot}%{_liconsdir}
install -d -m755 %{buildroot}%{_iconsdir}
install -d -m755 %{buildroot}%{_miconsdir}
convert avidemux_icon.png -resize 48x48 %{buildroot}%{_liconsdir}/%{name}.png
convert avidemux_icon.png -resize 32x32 %{buildroot}%{_iconsdir}/%{name}.png
convert avidemux_icon.png -resize 16x16 %{buildroot}%{_miconsdir}/%{name}.png

# menu
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}-qt.desktop << EOF
[Desktop Entry]
Name=Avidemux
Comment=A free video editor
Exec=%{_bindir}/%{name}3_qt5 %U
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=AudioVideo;Video;AudioVideoEditing;Qt;
EOF

%find_lang %{name} || touch %name.lang

# Workaround for identical build IDs in nonidentical files
# FIXME this should really get a proper fix inside gold some time soon
#__strip --strip-unneeded %buildroot%_bindir/*

find build -name file.list |xargs sed -i -e 's,^\.,,'
# Don't own standard dirs
find build -name dirs.list |xargs sed -i -e '/.\/usr\/bin$/d;/.\/usr\/share$/d;/.\/usr\/%_lib$/d;/.\/usr$/d;/.\/usr\/include$/d'
# Mark directories as such
find build -name dirs.list |xargs sed -i -e 's,^\.,%%dir ,'
find build -name dirs.list |while read r; do
	cat $r >>`dirname $r`/file.list
done

%files -f %{name}.lang -f build/avidemux_core/file.list,build/SETTINGS/file.list,build/COMMON/file.list
%_datadir/icons/*.png
%_datadir/icons/*/*

%files qt -f build/avidemux/qt4/file.list,build/QT4/file.list
%{_datadir}/applications/avidemux-qt.desktop

%files cli -f build/avidemux/cli/file.list,build/CLI/file.list
