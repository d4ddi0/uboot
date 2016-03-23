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
mkdir -p $RPM_BUILD_ROOT/etc/
mkdir -p $RPM_BUILD_ROOT/sbin/
cp u-boot.imx %{buildroot}/boot/u-boot.imx
cp tools/env/fw_printenv %{buildroot}/sbin/fw_printenv
cp tools/env/fw_printenv %{buildroot}/sbin/fw_setenv
echo "/dev/mmcblk0           0x80000       0x2000" > %{buildroot}/etc/fw_env.config
%clean
rm -rf %{buildroot}/lib
rm -rf %{buildroot}/boot

%post
# Post-install commands
ENGSN_UPPER="99"

#Make sure there is a valid serial number
if ! read INSTRSN < /etc/sn; then
    echo "Warning: could not read serial number, assuming newest hardware" >&2
    exit
fi

#Make sure the serial number is valid
if ! expr "${INSTRSN}" + "0" > /dev/null 2>&1; then
    echo "Warning: serial number is not an integer, assuming latest hardware" >&2
    exit
fi

is_reg_xg()
{
	XG_SNS="100 101 102 103 104 105 106 107 108 110 111 112 113 114 115 116 117 118 119"
	for SN in $XG_SNS;
	do
		[ $SN -eq $1 ] && return 0
	done
	return 1
}

dd if=/boot/u-boot.imx of=/dev/mmcblk0 seek=2 bs=512

# no need to check serial numbers for non engineering units
if [ "${INSTRSN}" -le "${ENGSN_UPPER}" ]; then
	/sbin/fw_setenv fdt_file imx6q-evi-revxf.dtb
elif is_reg_xg ${INSTRSN}; then
	/sbin/fw_setenv fdt_file imx6q-evi-revxg.dtb
else
	/sbin/fw_setenv fdt_file imx6q-evi.dtb
fi

%postun


%pre


%preun


%files
%defattr(-,root,root,-)
"/boot/u-boot.imx"
"/etc/fw_env.config"
"/sbin/fw_printenv"
"/sbin/fw_setenv"

%changelog
