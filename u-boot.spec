# -*- rpm-spec -*-
# spec file for the u-boot software
#
Summary:        u-boot software
Name:           u-boot
Version:        %{_u_boot_ver}
Release:        1
License:        GPL-2.0+
Group:          System Environment/Kernel
Vendor:         UniWest
AutoReqProv:    no

Provides: u-boot
Prefix: /

%description
U-Boot is a boot loader for Embedded boards.

%prep
rm -rf %{buildroot}/lib

%build
make

%install
mkdir -p $RPM_BUILD_ROOT/boot/
cp u-boot.imx %{buildroot}/boot/u-boot.imx

%clean
rm -rf %{buildroot}/lib
rm -rf %{buildroot}/boot

%post
dd if=/boot/u-boot.imx of=/dev/mmcblk0 seek=2 bs=512

%postun


%pre


%preun


%files
%defattr(-,root,root,-)
"/boot/u-boot.imx"

%changelog
