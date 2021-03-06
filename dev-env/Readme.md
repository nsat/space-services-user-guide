# Development Environments

Native applications, including scripted languages with native components (e.g. NumPy) must be compiled to the ARM 8 architecture. A Linux cross-compiler is provided for this purpose.


# C/C++ Cross Compiling

For compilations with few external package dependencies, cross-compiling may be the simplest option. Spire provides a complete cross-compiler for the SDR & IPI Linux payloads, but not the `SABERTOOTH` payload (see [below](#sabertooth))



# Virtual Machine

The SDR & IPI payloads run on an ARM Cortex A53, with Yocto Poky 2.5 (Sumo) installed ([specs](../#payload-specifications)). The Yocto Poky sumo OS can be run in a QEMU VM.

 * [QUEMU Setup](./vm/)


# In-Orbit Compiling

All payloads include the software and libraries to compile C & C++ applications. This environment is not well suited to the iterative process usually needed due to the time taken to upload files, schedule activities, and wait for the results to appear in the bucket. Where dependent packages are needed, large uploads will require additional time to upload.

Developers should consider using the cross compiler if possible.

An example is provided for installing the `zfec` Python module which includes a native C library built at install time:

 * [In-Orbit Python Setup](./in-orbit/)


# SABERTOOTH

The `SABERTOOTH` payload is an NVIDIA Tegra TX2i, which runs an ARM Cortex A57, and has [Jetpack 4.2.2](https://developer.nvidia.com/jetpack-422-archive) installed ([specs](../ExecutionEnvironment.md#sabertooth)). Developers may choose to purchase this hardware (or the Nano 2) to perform development, compilation, or integration testing.
