# Development Environments

Developers have a choice of C/C++ compilation environments based on need.

# C/C++ Cross Compiling

For compilations with few external package dependencies, cross-compiling may be the simplest option. Spire provides a complete cross-compiler for the SDR & IPI Linux payloads, but not the SABERTOOTH payload (see [below](#sabertooth)).

 * [Cross Compiling](./cross-compiling/)


# Payload Virtual Machine

The SDR & IPI payloads run on an ARM Cortex A53, with Yocto Poky 2.5 (Sumo) installed ([specs](https://developers.spire.com/space-services-user-guide/index.html#payload-specifications)). The sumo OS can be run in a QEMU VM.

 * [QUEMU Setup](./virtual-machine/)


# In-Orbit Compiling

Developers have the option to compile on the payloads, in-orbit. This option is not recommended because the environment will be untested by the developer.  For Python this requires additional steps:

 * [In-Orbit Python Setup](./in-orbit/)
 

# SABERTOOTH

The `SABERTOOTH` payload is an NVIDIA Tegra TX2i, which runs an ARM Cortex A57, and has [Jetpack 4.2.2](https://developer.nvidia.com/jetpack-422-archive) installed ([specs](https://developers.spire.com/space-services-user-guide/index.html#payload-specifications)). Developers may choose to purchase this (or the Nano 2) to perform development and/or integration testing of the environment.