
Summary: A music file player for Apple Airport Express
Name: raop_play
Version: 0.5.1
Release: %mkrel 1
Source0: http://puzzle.dl.sourceforge.net/sourceforge/raop-play/raop_play-%{version}.tar.gz
Source1: alsa_raoppcm-dkms.conf
Patch0:	 alsa_raoppcm-new-kernels.patch
License: GPL
Group: System/Kernel and hardware
URL: http://raop-play.sourceforge.net/
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: fltk-devel
BuildRequires: openssl-devel
BuildRequires: libsamplerate-devel

%description
raop_play is a music file player for Apple Airport Express,
the main functionalities are as follows:
* Make AEX become your 2'nd sound card device. http://raop-play.sourceforge.net/alsa_raoppcm.html
* Discover Airport Express by Apple Rendezvous
* Browse music files
 (Supported music file format: m4a(alac or aac), wav, mp3, ogg, flac, aac, pls, raw pcm)
* Send selected files to the Airport Express
* Play mp3 stream data (filename started with "http://")


%package -n dkms-alsa_raoppcm
Group: System/Kernel and hardware
Summary: Dkms module for the Apple Airport Express
Requires(post): dkms
Requires(preun): dkms

%description -n dkms-alsa_raoppcm
A music file player for Apple Airport Express.
This package contains the kernel module.

%prep
%setup -q
%patch0 -p1
perl -p -e 's/\@VERSION@/%{version}/' < %{SOURCE1} > dkms.conf

%build
%configure
perl -e 's/aexcl//g' -pi Makefile
perl -e 's/rendezvous//g' -pi Makefile
%make

%install
rm -rf $RPM_BUILD_ROOT
# install by hand
# make install DESDIR=$RPM_BUILD_ROOT

# ah! - install bny hand :-(
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp raop_play/raop_play $RPM_BUILD_ROOT%{_bindir}/raop_play
# Is APSL compatible with mandriva?
# cp rendezvous/mDNSClient $RPM_BUILD_ROOT%{_bindir}/mDNSClient
# cp aexcl/aexcl_play $RPM_BUILD_ROOT%{_bindir}/aexcl_play

# install dkms
mkdir -p $RPM_BUILD_ROOT/usr/src/alsa_raoppcm-%{version}-%{release}/
cp -r drivers/* $RPM_BUILD_ROOT/usr/src/alsa_raoppcm-%{version}-%{release}/
install -m 644 dkms.conf $RPM_BUILD_ROOT/usr/src/alsa_raoppcm-%{version}-%{release}/dkms.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_bindir}/*
%doc COPYING README CHANGELOG

%files -n dkms-alsa_raoppcm
%defattr(-,root,root)
%attr(0755,root,root) /usr/src/alsa_raoppcm-%{version}-%{release}/

%post -n dkms-alsa_raoppcm
set -x
/usr/sbin/dkms --rpm_safe_upgrade add -m alsa_raoppcm -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade build -m alsa_raoppcm -v %{version}-%{release}
/usr/sbin/dkms --rpm_safe_upgrade install -m alsa_raoppcm -v %{version}-%{release}

%preun -n dkms-alsa_raoppcm
set -x
/usr/sbin/dkms --rpm_safe_upgrade remove -m alsa_raoppcm -v %{version}-%{release} --all


