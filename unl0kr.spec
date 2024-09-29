%define dracutlibdir %{_prefix}/lib/dracut

Name:           unl0kr
Version:        3.2.0
Release:        1%{?dist}
Summary:        Framebuffer-based disk unlocker for the initramfs based on LVGL 
License:        GPLv3
URL:            https://gitlab.com/postmarketOS/buffybox

BuildRequires:  git
BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  wget
BuildRequires:  meson >= 0.55.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(scdoc)

Source1:        unl0kr-dracut-module-setup.sh
Source2:        unl0kr-ask-password.sh
Source3:        unl0kr-ask-password.path
Source4:        unl0kr-ask-password.service
Source5:        unl0kr.conf
Source6:        10-unl0kr.conf

# Patch0:         0001-Remove-newline-from-password-output.patch

# Disable debug packages
%define debug_package %{nil}

%description
Unl0kr is an osk-sdl clone written in LVGL and rendering directly to the Linux framebuffer. As a result, it doesn't depend on GPU hardware acceleration.

%package dracut
Summary: Integration of unl0kr and Dracut
Requires: %{name} = %{version}-%{release}
Requires: dracut

%description dracut
Provides a Dracut module that will ask for password with an on-screen-keyboard

%prep
wget -O buffybox.tar.gz https://gitlab.com/-/project/52322952/uploads/88ff83972a3c19d16d9d2560bfae8a7e/buffybox-%{version}.tar.gz
tar xavf buffybox.tar.gz
cd buffybox-%{version}/unl0kr
cp %{SOURCE5} unl0kr.conf

%build
cd buffybox-%{version}/unl0kr
%meson
%meson_build

%install
cd buffybox-%{version}/unl0kr
%meson_install
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/10unl0kr
install -p -m 0644 %{SOURCE1} %{buildroot}%{dracutlibdir}/modules.d/10unl0kr/module-setup.sh
install -p -m 0755 %{SOURCE2} %{buildroot}%{dracutlibdir}/modules.d/10unl0kr/unl0kr-ask-password.sh
mkdir -p %{buildroot}%{_unitdir}/sysinit.target.wants
install -p -m 0755 %{SOURCE3} %{buildroot}%{_unitdir}/unl0kr-ask-password.path
install -p -m 0755 %{SOURCE4} %{buildroot}%{_unitdir}/unl0kr-ask-password.service
ln -s ../unl0kr-ask-password.path %{buildroot}%{_unitdir}/sysinit.target.wants/
mkdir -p %{buildroot}%{_sysconfdir}/unl0kr.conf.d/
touch %{buildroot}%{_sysconfdir}/unl0kr.conf.d/dummy
mkdir -p %{buildroot}%{dracutlibdir}/dracut.conf.d/
cp %{SOURCE6} %{buildroot}%{dracutlibdir}/dracut.conf.d/10-unl0kr.conf

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license buffybox-%{version}/COPYING
%{_bindir}/unl0kr
%{_sysconfdir}/unl0kr.conf
%{_sysconfdir}/unl0kr.conf.d/*
%{_mandir}/man*/unl0kr.*

%files dracut
%{dracutlibdir}/modules.d/10unl0kr
%{dracutlibdir}/dracut.conf.d/10-unl0kr.conf
%{_unitdir}/unl0kr-ask-password.path
%{_unitdir}/unl0kr-ask-password.service
%{_unitdir}/sysinit.target.wants/unl0kr-ask-password.path

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
