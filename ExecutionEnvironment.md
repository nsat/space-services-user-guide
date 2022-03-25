# Execution Environment

Users software runs in a persistent sandboxed execution environment on a Spire payload, which is a specific Linux computer on a satellite controlling specific hardware.  User software is uploaded to this sandbox environment through the Tasking API.  User software has access to its own filesystem and various software libraries, the specifics of which depend on which payload the user is scheduling operations on.  The file system is persistent between contacts, files saved to the users filesystem will persist until they are deleted by the user.

## Filesystem

The execution environment includes two top level directories used to manage incoming and outgoing data:

* `/inbox` - Spire generated files during a payload window will be placed into this folder. 
For example, [IQ](#iq-generator) files captured during a PAYLOAD_SDR window will appear in this folder.  File names and types placed in this folder
will vary between window types, please consult the [Tasking API documentation](https://developers.spire.com/tasking-api-docs/) 
for details about a specific window.  Files placed in this folder should be handled by the user in the window which they are generated.
* `/outbox` - Any files placed in this folder by the user's software will be queued for downlink.  Files placed here will be removed by the Spire Linux Agent after 
any payload window.

The root filesystem is writable to the user. Common Linux directories have been bind-mounted read-only, e.g. `/bin`, `/usr`, `/proc`, `/var`, `/home` etc. The user's home directory `~` is ephemeral (not persisted between restarts) and may not be on the same path for each payload. The Tasking API executes user applications outside of a shell. For these reasons it recommended to:

1. Create a wrapper shell script & to add environment variables for `PATH` and other user requirements
1. Create and use `/persist` or similar directory name at the root of the filesystem, for files that should remain on the payload for future windows
   1. When installing, install to this directory
1. Treat all existing directories as read-only


### Wrapper Script

The Tasking API is used to deploy apps to payloads and execute them. It is helpful to use a wrapper script to provide a consistent environment between payloads, to set common environment variables and capture `stdout` and `stderr` to a log file for download at the end of the window. The wrapper script, named [`entry.sh`](https://github.com/nsat/space-services-user-guide/blob/main/dev-env/entry.sh) can be deployed to each payload at `/persist/bin/entry.sh` and used for all execution commands. All tutorials require `entry.sh` to be deployed. The script can be deployed to a payload by running [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/dev-env/deploy) in the [`dev-env`](https://github.com/nsat/space-services-user-guide/tree/main/dev-env) directory:


<aside class="notice">Replace [YOUR_AUTH_TOKEN]& [YOUR_SAT_ID] needed. [YOUR_PAYLOAD] can be one of `IPI`, `SDR` or `SABERTOOTH`.</aside>

```bash
$ dev-env/deploy "[YOUR_AUTH_TOKEN]" [YOUR_SAT_ID] [YOUR_PAYLOAD]
```


## Networking

Payloads have direct IP network access via ethernet to listen on ports above 10000, as well as make connections to those ports. TCP & UDP are supported. Payload modules with [overlapping windows](https://developers.spire.com/tasking-api-docs/#overlapping-windows) have IP routes available between them for the duration of the overlap. Users are expected to setup server and client on each module to facilitate communication.


### Inter-Satellite Links (ISL)

Inter-satellite data transfer is possible using ISL. In order to utilize inter-satellite data transfer, A `LEASE_ISL` windows must be scheduled concurrently with a `PAYLOAD_*` on each side satellite. One satellite is selected as a transmitter and the other as a receiver. A network gateway/route is available on the SABERTOOTH, LEMSDR & IPI payloads that routes IPv4 traffic via the ISL radio for SIMPLEX transmission to a receiving satellite. **UDP** transmission is possible over the SIMPLEX link.  The ISL network uses standard IP networking. Using NAT, the remote payloads are addressable on the
`172.16.0.x` subnet (The subnet `10.2.1.x` is replaced with `172.16.0.x` by the NAT router).


### IP Table

| Payload | Local IP Address | Remote (ISL) IP Address |
| - | - | - |
| SDR | 10.2.1.12 | 172.16.0.8 |
| SABERTOOTH | 10.2.1.10 | 172.16.0.10 |
| IPI | 10.2.1.16 | 172.16.0.16 |


## Payload Specifications

Below are the list of specifications for each payload type accessible to Software in Space users including the list of packages pre-installed on the payload.

## SDR

| Attribute    | Value                               |
| ------------ | ------------------------------------|
| SoC          | Xilinx Zynq UltraScale+ ZU4CG       |
| CPU          | 2x ARM Cortex A53 @ 1.3GHz (+ 2x ARM Cortex R5F @ 533Mhz [**](#note))	|
| Memory       | 2GB                                 |
| OS           | Yocto Poky 2.5 (Sumo)               |
| Arch         | 64-bit armv8-hardfp	              |
| Kernel       | Linux 4.14.0                        |
| IP Address   | 10.2.1.12                           |
| Package List | [List](./text/sdr_package_list.txt) |
| Utilities    | - [RF Collect](./Utilities.md#rf-collect)<br> - [RF Transmit](./Utilities.md#rf-transmit)<br> - [IQ Generator](./Utilities.md#iq-generator) |
| Windows      | [`PAYLOAD_SDR`](https://developers.spire.com/tasking-api-docs/#payload_sdr-v2) |


## IPI

| Attribute    | Value                               |
| ------------ | ------------------------------------|
| SoC          | Xilinx Zynq UltraScale+ ZU4CG       |
| CPU          | 2x ARM Cortex A53 @ 1.3GHz (+ 2x ARM Cortex R5F @ 533Mhz [**](#note))	|
| Memory       | 2GB                                 |
| OS           | Yocto Poky 2.5 (Sumo)               |
| Arch         | 64-bit armv8-hardfp	             |
| Kernel       | Linux 4.14.0                        |
| IP Address   | 10.2.1.16                            |
| Package List | [List](./text/ipi_package_list.txt) |
| Windows      | [`PAYLOAD_IPI`](https://developers.spire.com/tasking-api-docs/#payload_ipi) |


## SABERTOOTH

| Attribute    | Value                               |
| ------------ | ------------------------------------|
| SoC          | NVIDIA Tegra TX2i                   |
| CPU          | 4x ARM Cortex A57 @ 2GHz (+ 2x Denver 2 @ 2Ghz) |
| Memory       | 8GB                                 |
| OS           | Ubuntu 18.04.2 ([Jetpack 4.2.2](https://developer.nvidia.com/jetpack-422-archive)) |
| Arch         | 64-bit armv8-hardfp	             |
| Kernel       | Linux 4.9.140                       |
| IP Address   | 10.2.1.10                           |
| Package List | [List](./text/sabertooth_package_list.txt) |
| Windows      | [`PAYLOAD_SABERTOOTH`](https://developers.spire.com/tasking-api-docs/#compute-boards) |


## Dexter

| Attribute    | Value                               |
| ------------ | ------------------------------------|
| SoC          | Xilinx Zynq 7020                    |
| CPU          | 2x ARM Cortex A9 @ 866MHz	         |
| Memory       | 1GB                                 |
| OS           | Yocto Poky 2.3 (Pyro)               |
| Arch         | 32-bit armv7-hardfp	             |
| Kernel       | Linux 4.6.0-2016_R2                 |
| IP Address   | 10.2.1.9                            |
| Package List | [List](./text/dexter_package_list.txt) |
| Windows      | [`PAYLOAD_DEXTER`](https://developers.spire.com/tasking-api-docs/#payload_dexter) |

### NOTE

The ARM Cortex R5F real-time processors (RPUs) are only available with [Payload In Space](./PayloadInSpace.md) service.

## Next Steps

 - [Attitude Control](./AttitudeControl.md)
