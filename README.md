<!-- Copyright 2024 Fleuria
     SPDX-License-Identifier: Apache-2.0 -->
# uki-profilify: Multi-profile UKI creation helper

**uki-profilify** is a tool that eases creation of multi-profile UKIs,
supporting multiple kernel presets. For more information, see the [man page][1].

[1]: doc/uki-profilify.1

## Example configuration

Generate a UKI at `/efi/EFI/Arch/linux.efi` for the `linux` mkinitcpio preset
with two profiles: default and fallback.

```toml
[uki]
output = "/efi/EFI/Arch/linux.efi"
initrd = "/boot/initramfs-linux.img"
cmdline = "root=PARTLABEL=arch rw quiet splash"

[[profiles]]
id = "default"
title = "Boot using default options"

[[profiles]]
id = "fallback"
title = "Boot using fallback initramfs"
[profiles.sections]
initrd = "/boot/initramfs-linux-fallback.img"
cmdline = "root=PARTLABEL=arch rw"
```
