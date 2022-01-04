# Execution Environment

User's software runs in a persistent sandboxed execution environment on a Spire payload, which is a specific Linux computer on a satellite controlling specific hardware.  User software is uploaded to this sandbox environment through the Tasking API.  User software has access to it's own filesystem and various software libraries, the specifics of which depend on which payload the customer is scheduling operations on.  The file system is persistent between contacts, files saved to the user's filesystem will persist until they are deleted by the user.

The execution environment includes two top level directories used to manage incoming and outgoing data:

* `/inbox` - Spire generated files during a payload window will be placed into this folder. 
For example, IQ files captures during a PAYLOAD_SDR window will appear in this folder.  File names and types placed in this folder
will vary between window types, please consult the [Tasking API documentation](https://developers.spire.com/tasking-api-docs/) 
for details about a specific window.  Files placed in this folder should be handled during the window which they are generated.
* `/outbox` - Any files placed in this folder by user software will be queued for downlink.  Files placed here will be removed by the Spire Linux Agent after 
any payload window.

## Payload Specifications

Below are the list of specifications for each payload type accessible to Software in Space customers including the list of packages pre-installed on the payload.

## SDR

| Attribute    | Value                               |
| ------------ | ------------------------------------|
| SoC          | Xilinx Zynq UltraScale+ ZU4CG       |
| CPU          | 2x ARM Cortex A53 @ 1.3GHz (+ 2x ARM Cortex R5F @ 533Mhz)	|
| Memory       | 2GB                                 |
| OS           | Yocto Poky 2.5 (Sumo)               |
| Arch         | 64-bit armv8-hardfp	             |
| Kernel       | Linux 4.14.0                        |
| IP Address   | 10.2.1.8                            |
| Package List | [List](./assets/text/sdr_package_list.txt) |
| Utilities    | - [RF Collect](#rf-collect)<br> - [RF Transmit](#rf-transmit)<br> - [IQ Generator](#iq-generator) |
| Windows      | [`PAYLOAD_SDR`](https://developers.spire.com/tasking-api-docs/#payload_sdr-v2) |


## IPI

| Attribute    | Value                               |
| ------------ | ------------------------------------|
| SoC          | Xilinx Zynq UltraScale+ ZU4CG       |
| CPU          | 2x ARM Cortex A53 @ 1.3GHz (+ 2x ARM Cortex R5F @ 533Mhz)	|
| Memory       | 2GB                                 |
| OS           | Yocto Poky 2.5 (Sumo)               |
| Arch         | 64-bit armv8-hardfp	             |
| Kernel       | Linux 4.14.0                        |
| IP Address   | 10.2.1.16                            |
| Package List | [List](./text/ipi_package_list.txt) |
| Windows      | [`PAYLOAD_IPI`](https://developers.spire.com/tasking-api-docs/#payload_ipi) |


## Sabertooth

| Attribute    | Value                               |
| ------------ | ------------------------------------|
| SoC          | NVIDIA Tegra TX2i                   |
| CPU          | 4x ARM Cortex A57 @ 2GHz (+ 2x Denver 2 @ 2Ghz) |
| Memory       | 8GB                                 |
| OS           | Ubuntu 18.04.2 ([Jetpack 4.2.2](https://developer.nvidia.com/jetpack-422-archive)) |
| Arch         | 64-bit armv8-hardfp	             |
| Kernel       | Linux 4.9.140                       |
| IP Address   | 10.2.1.10                           |
| Package List | [List](./assets/text/sabertooth_package_list.txt) |
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
| Package List | [List](./assets/text/dexter_package_list.txt) |