# SABERTOOTH CUDA Tutorial

|Complexity:|Low|
|-|-|
|Payloads:|`SABERTOOTH`|
|Windows:|`PAYLOAD_SABERTOOTH`|


This tutorial demonstrates CUDA v10.0 by running [the samples that come shipped with NVIDIA CUDA v10.0](https://docs.nvidia.com/cuda/archive/10.0/cuda-installation-guide-linux/index.html#compiling-examples).


## Prerequisites

All tutorials require the steps outlined in the [Getting Started Guide](../../GettingStarted.md). 


## Overview

The tutorial comes with 2 scripts:

1. [`cuda_demo`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy) - runs in-orbit on the SABERTOOTH to demonstrate CUDA running
1. [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy) - run by the user on the ground to upload `cuda_demo` and schedule it to execute in a `PAYLOAD_SABERTOOTH` window


## cuda_demo Script

[`cuda_demo`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy) builds & runs 3 of the CUDA samples:

1. [`deviceQuery`](https://docs.nvidia.com/cuda/archive/10.0/demo-suite/index.html#deviceQuery)
1. [`bandwidthTest`](https://docs.nvidia.com/cuda/archive/10.0/demo-suite/index.html#bandwidthTest)
1. [`transpose`](https://docs.nvidia.com/cuda/archive/10.0/cuda-samples/index.html#matrix-transpose)


First, the CUDA compiler is checked for availability:

```bash
/usr/local/cuda/bin/nvcc -V
```

Next, the CUDA samples source is copied to `~/` as the system location is not writable:

```bash
cp -a /usr/local/cuda/samples ~/
```

Finally some of the CUDA samples are built & run. Here are the commands for building & running `deviceQuery`:

```bash
cd ~/samples/1_Utilities/deviceQuery &&
make &&
./deviceQuery
```


<details>
  <summary style="padding-left:20px;display:list-item;">Example Output</summary>
  <br/>
<pre id="cuda_demo_output" class="highlight">
+ cd /home/spire/samples/1_Utilities/deviceQuery
+ make
/usr/local/cuda-10.0/bin/nvcc -ccbin g++ -I../../common/inc  -m64    -gencode arch=compute_30,code=sm_30 -gencode arch=compute_32,code=sm_32 -gencode arch=compute_53,code=sm_53 -gencode arch=compute_61,code=sm_61 -gencode arch=compute_62,code=sm_62 -gencode arch=compute_70,code=sm_70 -gencode arch=compute_72,code=sm_72 -gencode arch=compute_75,code=sm_75 -gencode arch=compute_75,code=compute_75 -o deviceQuery.o -c deviceQuery.cpp
/usr/local/cuda-10.0/bin/nvcc -ccbin g++   -m64      -gencode arch=compute_30,code=sm_30 -gencode arch=compute_32,code=sm_32 -gencode arch=compute_53,code=sm_53 -gencode arch=compute_61,code=sm_61 -gencode arch=compute_62,code=sm_62 -gencode arch=compute_70,code=sm_70 -gencode arch=compute_72,code=sm_72 -gencode arch=compute_75,code=sm_75 -gencode arch=compute_75,code=compute_75 -o deviceQuery deviceQuery.o
mkdir -p ../../bin/aarch64/linux/release
cp deviceQuery ../../bin/aarch64/linux/release
+ ./deviceQuery
./deviceQuery Starting...

 CUDA Device Query (Runtime API) version (CUDART static linking)

Detected 1 CUDA Capable device(s)

Device 0: "NVIDIA Tegra X1"
  CUDA Driver Version / Runtime Version          10.0 / 10.0
  CUDA Capability Major/Minor version number:    5.3
  Total amount of global memory:                 1980 MBytes (2076352512 bytes)
  ( 1) Multiprocessors, (128) CUDA Cores/MP:     128 CUDA Cores
  GPU Max Clock rate:                            922 MHz (0.92 GHz)
  Memory Clock rate:                             13 Mhz
  Memory Bus Width:                              64-bit
  L2 Cache Size:                                 262144 bytes
  Maximum Texture Dimension Size (x,y,z)         1D=(65536), 2D=(65536, 65536), 3D=(4096, 4096, 4096)
  Maximum Layered 1D Texture Size, (num) layers  1D=(16384), 2048 layers
  Maximum Layered 2D Texture Size, (num) layers  2D=(16384, 16384), 2048 layers
  Total amount of constant memory:               65536 bytes
  Total amount of shared memory per block:       49152 bytes
  Total number of registers available per block: 32768
  Warp size:                                     32
  Maximum number of threads per multiprocessor:  2048
  Maximum number of threads per block:           1024
  Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
  Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
  Maximum memory pitch:                          2147483647 bytes
  Texture alignment:                             512 bytes
  Concurrent copy and kernel execution:          Yes with 1 copy engine(s)
  Run time limit on kernels:                     Yes
  Integrated GPU sharing Host Memory:            Yes
  Support host page-locked memory mapping:       Yes
  Alignment requirement for Surfaces:            Yes
  Device has ECC support:                        Disabled
  Device supports Unified Addressing (UVA):      Yes
  Device supports Compute Preemption:            No
  Supports Cooperative Kernel Launch:            No
  Supports MultiDevice Co-op Kernel Launch:      No
  Device PCI Domain ID / Bus ID / location ID:   0 / 0 / 0
  Compute Mode:
     < Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) >

deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 10.0, CUDA Runtime Version = 10.0, NumDevs = 1
Result = PASS
<pre>
</details>


## Upload & Deploy

Run [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy). The script uploads `cuda_demo` and schedules it's execution in 24 hours.

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
$ ./deploy "[YOUR_AUTH_TOKEN]" [YOUR_SAT_ID]
```


## Review

Once the window has completed and enough time has passed for the log to download, it can be reviewed in AWS S3 (see [Hello World tutorial](../hello_world/#review)).


## Next Steps

 - [SABERTOOTH cuDNN Tutorial](../cudnn/) 
