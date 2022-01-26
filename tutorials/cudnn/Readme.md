# Sabertooth cuDNN Tutorial

|Complexity:|Low|
|-|-|
|Payloads:|`SABERTOOTH`|
|Windows:|`PAYLOAD_SABERTOOTH`|


This tutorial demonstrates [CuDNN v7.5.0](https://developer.nvidia.com/rdp/cudnn-archive) by running [the samples that come shipped with it](https://github.com/mmmn143/cudnn_samples_v7).

## Overview

The tutorial comes with 2 scripts:

1. [`cudnn_demo`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy) - runs in-orbit on the Sabertooth to demonstrate cuDNN running
1. [`deploy`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy) - run by the user on the ground to upload `cudnn_demo` and schedule it to execute in a `PAYLOAD_SABERTOOTH` window


## cudnn_demo Script

[`cudnn_demo`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy) builds & runs 3 of the CUDA samples:

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
<pre id="cudnn_demo_output" class="highlight">
Linking agains cublasLt = false
CUDA VERSION: 10000
TARGET ARCH: aarch64
HOST_ARCH: aarch64
TARGET OS: linux
SMS: 30 35 50 53 60 61 62 70 72 75
/usr/local/cuda/bin/nvcc -ccbin g++ -I/usr/local/cuda/include -IFreeImage/include  -m64    -gencode arch=compute_30,code=sm_30 -gencode arch=compute_35,code=sm_35 -gencode arch=compute_50,code=sm_50 -gencode arch=compute_53,code=sm_53 -gencode arch=compute_60,code=sm_60 -gencode arch=compute_61,code=sm_61 -gencode arch=compute_62,code=sm_62 -gencode arch=compute_70,code=sm_70 -gencode arch=compute_72,code=sm_72 -gencode arch=compute_75,code=sm_75 -gencode arch=compute_75,code=compute_75 -o fp16_dev.o -c fp16_dev.cu
g++ -I/usr/local/cuda/include -IFreeImage/include   -o fp16_emu.o -c fp16_emu.cpp
g++ -I/usr/local/cuda/include -IFreeImage/include   -o mnistCUDNN.o -c mnistCUDNN.cpp
/usr/local/cuda/bin/nvcc -ccbin g++   -m64      -gencode arch=compute_30,code=sm_30 -gencode arch=compute_35,code=sm_35 -gencode arch=compute_50,code=sm_50 -gencode arch=compute_53,code=sm_53 -gencode arch=compute_60,code=sm_60 -gencode arch=compute_61,code=sm_61 -gencode arch=compute_62,code=sm_62 -gencode arch=compute_70,code=sm_70 -gencode arch=compute_72,code=sm_72 -gencode arch=compute_75,code=sm_75 -gencode arch=compute_75,code=compute_75 -o mnistCUDNN fp16_dev.o fp16_emu.o mnistCUDNN.o -I/usr/local/cuda/include -IFreeImage/include  -LFreeImage/lib/linux/aarch64 -LFreeImage/lib/linux -lcudart -lcublas -lcudnn -lfreeimage -lstdc++ -lm
FreeImage/lib/linux/aarch64/libfreeimage.a(strenc.o): In function `StrIOEncInit':
strenc.c:(.text+0x1294): warning: the use of `tmpnam' is dangerous, better use `mkstemp'

cudnnGetVersion() : 7500 , CUDNN_VERSION from cudnn.h : 7500 (7.5.0)
Host compiler version : GCC 7.4.0
There are 1 CUDA capable devices on your machine :
device 0 : sms  1  Capabilities 5.3, SmClock 921.6 Mhz, MemSize (Mb) 1980, MemClock 12.8 Mhz, Ecc=0, boardGroupID=0
Using device 0

Testing single precision
Loading image data/one_28x28.pgm
Performing forward propagation ...
Testing cudnnGetConvolutionForwardAlgorithm ...
Fastest algorithm is Algo 1
Testing cudnnFindConvolutionForwardAlgorithm ...
^^^^ CUDNN_STATUS_SUCCESS for Algo 0: 0.251667 time requiring 0 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 2: 0.382813 time requiring 57600 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 4: 2.635729 time requiring 207360 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 5: 12.472500 time requiring 203008 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 7: 12.811354 time requiring 2057744 memory
Resulting weights from Softmax:
0.0000000 0.9999399 0.0000000 0.0000000 0.0000561 0.0000000 0.0000012 0.0000017 0.0000010 0.0000000
Loading image data/three_28x28.pgm
Performing forward propagation ...
Resulting weights from Softmax:
0.0000000 0.0000000 0.0000000 0.9999288 0.0000000 0.0000711 0.0000000 0.0000000 0.0000000 0.0000000
Loading image data/five_28x28.pgm
Performing forward propagation ...
Resulting weights from Softmax:
0.0000000 0.0000008 0.0000000 0.0000002 0.0000000 0.9999820 0.0000154 0.0000000 0.0000012 0.0000006

Result of classification: 1 3 5

Test passed!

Testing half precision (math in single precision)
Loading image data/one_28x28.pgm
Performing forward propagation ...
Testing cudnnGetConvolutionForwardAlgorithm ...
Fastest algorithm is Algo 1
Testing cudnnFindConvolutionForwardAlgorithm ...
^^^^ CUDNN_STATUS_SUCCESS for Algo 1: 0.171354 time requiring 3464 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 0: 0.206354 time requiring 0 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 2: 0.319636 time requiring 28800 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 4: 2.538021 time requiring 207360 memory
^^^^ CUDNN_STATUS_SUCCESS for Algo 5: 12.519062 time requiring 203008 memory
Resulting weights from Softmax:
0.0000001 1.0000000 0.0000001 0.0000000 0.0000563 0.0000001 0.0000012 0.0000017 0.0000010 0.0000001
Loading image data/three_28x28.pgm
Performing forward propagation ...
Resulting weights from Softmax:
0.0000000 0.0000000 0.0000000 1.0000000 0.0000000 0.0000714 0.0000000 0.0000000 0.0000000 0.0000000
Loading image data/five_28x28.pgm
Performing forward propagation ...
Resulting weights from Softmax:
0.0000000 0.0000008 0.0000000 0.0000002 0.0000000 1.0000000 0.0000154 0.0000000 0.0000012 0.0000006

Result of classification: 1 3 5

Test passed!
<pre>
</details>


## Upload & Deploy

Run [`deploy <AUTH_TOKEN> <SAT_ID>`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/cuda/deploy) substituting `<AUTH_TOKEN>` and `<SAT_ID>` per the [getting started guide](../../GettingStarted.md). The script uploads `cudnn_demo` and schedules it's execution in 24 hours.

## Review

Once the window has completed and enough time has passed for the log to download, it can be reviewed in AWS S3 (see [Hello World tutorial](../hello_world/#review)).
