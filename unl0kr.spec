Name:           unl0kr
Version:        {{{ git_dir_version }}}
Release:        1%{?dist}
Summary:        Framebuffer-based disk unlocker for the initramfs based on LVGL 
License:        GPLV3
URL:            https://gitlab.com/cherrypicker/unl0kr

BuildRequires:  git
BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(scdoc)

%description
Unl0kr is an osk-sdl clone written in LVGL and rendering directly to the Linux framebuffer. As a result, it doesn't depend on GPU hardware acceleration.

# Disable debug packages
%define debug_package %{nil}

%prep
git clone https://gitlab.com/cherrypicker/unl0kr.git
cd unl0kr
git submodule update --init --recursive

%build
cd unl0kr
%meson
%meson_build

%install
cd unl0kr
%meson_install

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license unl0kr/COPYING
%{_bindir}/%{name}
%{_sysconfdir}/%{name}.conf
%{_mandir}/man*/%{name}.*

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}
