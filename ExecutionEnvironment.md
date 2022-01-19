# Execution Environment

Users software runs in a persistent sandboxed execution environment on a Spire payload, which is a specific Linux computer on a satellite controlling specific hardware.  User software is uploaded to this sandbox environment through the Tasking API.  User software has access to its own filesystem and various software libraries, the specifics of which depend on which payload the user is scheduling operations on.  The file system is persistent between contacts, files saved to the users filesystem will persist until they are deleted by the user.

The execution environment includes two top level directories used to manage incoming and outgoing data:

* `/inbox` - Spire generated files during a payload window will be placed into this folder. 
For example, [IQ](#iq-generator) files captured during a PAYLOAD_SDR window will appear in this folder.  File names and types placed in this folder
will vary between window types, please consult the [Tasking API documentation](https://developers.spire.com/tasking-api-docs/) 
for details about a specific window.  Files placed in this folder should be handled by the user in the window which they are generated.
* `/outbox` - Any files placed in this folder by the user's software will be queued for downlink.  Files placed here will be removed by the Spire Linux Agent after 
any payload window.

## Filesystem

The root filesystem is writable to the user. Common Linux directories have been bind-mounted read-only, i.e. `/bin`, `/usr`, `/proc`, `/var` etc. The user's home directory `~` may not be on the same path for each payload. The Tasking API executes user applications outside of a shell. For these reasons it recommended to:

1. Create a wrapper shell script to add environment variables
1. Create and use `/persist` or similar directory name at the root of the filesystem, for files that should remain on the payload for future windows
   1. When installing, install to this directory
1. Treat all existing directories as read-only


## Wrapper Script

The Tasking API is used to deploy apps to payloads and execute them. It is helpful to use a wrapper script to provide a consistent environment between payloads, to set common environment variables and capture `stdout` and `stderr` to a log file for download at the end of the window. The wrapper script, named [`entry.sh`](https://github.com/nsat/space-services-user-guide/blob/main/dev-env/entry.sh) should be deployed to each payload at `/persist/bin/entry.sh` and used for all execution commands. All tutorials require `entry.sh` to be deployed. The script can be deployed with:


```bash
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SATELLITE_ID="satellite_id=YOUR_SAT_ID"

curl -o entry.sh "https://github.com/nsat/space-services-user-guide/blob/main/dev-env/entry.sh"
HOST="https://api.orb.spire.com"
DESTINATION_PATH="destination_path=/persist/bin/entry.sh"
EXECUTABLE="executable=true"
```

```bash
PAYLOAD="payload=SDR"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"
curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@entry.sh"
```

```bash
PAYLOAD="payload=SABERTOOTH"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"
curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@entry.sh"
```

```bash
PAYLOAD="payload=IPI"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"
curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@entry.sh"
```

## Payload Specifications

Below are the list of specifications for each payload type accessible to Software in Space users including the list of packages pre-installed on the payload.

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
| Package List | [List](./text/sdr_package_list.txt) |
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


## Next Steps

 - [Attitude Control](./AttitudeControl.md)
