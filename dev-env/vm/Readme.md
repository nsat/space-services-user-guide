# Yocto Poky sumo QEMU VM

|Complexity:|High - UNSUPPORTED|
|-|-|
|Payloads:|`SDR`, `IPI`|

This method creates a VM provided by [The Yocto Project⤴](http://www.yoctoproject.org/). It is unsupported.

The SDR & IPI payloads run on an ARM Cortex A53, with Yocto Poky 2.5 (Sumo) installed ([specs](../#payload-specifications)). The Yocto Poky sumo OS can be run in a QEMU VM.

There are significant differences between the packages installed in the image published by Yocto and the packages on the `SDR` & `IPI`. Please read more on the [Execution Environment](../ExecutionEnvironment.md), especially about the [filesystem](../ExecutionEnvironment.md#filesystem) to understand where to place files. A helper script is provided in the [Getting Started Guide](../../GettingStarted.md).


 * [QEMU⤴](https://www.qemu.org/) - may be installed with a package manager, i.e. `apt` or `apk`
 * [Download Yocto Poky sumo VM images⤴](http://downloads.yoctoproject.org/releases/yocto/yocto-2.5/machines/qemu/qemuarm64/)

Start VM:

```
qemu-system-aarch64 -cpu cortex-a57 -nographic -machine virt -kernel Image-qemuarm64.bin -m 2G -smp 6 -drive id=disk0,file=core-image-sato-sdk-qemuarm64.ext4,if=none,format=raw -device virtio-blk-device,drive=disk0 -append root=/dev/vda console=ttyS0 -device virtio-net-device,netdev=net0 -netdev user,id=net0,hostfwd=tcp::5555-:22`
```

Connect:

```
ssh -P 5555 root@localhost
```
