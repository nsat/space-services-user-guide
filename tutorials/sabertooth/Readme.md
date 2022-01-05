# Sabertooth Python Build Environment Setup

|Complexity:|High|
|-|-|
|Payloads:|`SABERTOOTH`|
|Windows:|`PAYLOAD_SABERTOOTH`|

The `SABERTOOTH` payload is installed with the stock NVIDIA JETSON Ubuntu 18.04.2 Linux distro ([specs](../../ExecutionEnvironment.md#sabertooth)). The environment requires further setup if the user plans to deploy python modules. This walkthrough can be adapted for any linux distro package or python module. 

 A list of packages installed on the `SABERTOOTH` payload can be found [here](../../text/sabertooth_package_list.txt). 


 ## Packages

Let's say that we require the Python module `zfec`. The module has dependencies on the following packages which are not installed:

  - [Python 3.6.9 headers](http://ports.ubuntu.com/ubuntu-ports/pool/main/p/python3.6/libpython3.6-dev_3.6.9-1~18.04ubuntu1.6_arm64.deb) (43 MB)
  - [Python3 pip v21.3.1](https://pypi.org/project/pip/) (1.7 MB)
  - [Python3 setuptools v59.6.0](https://pypi.org/project/setuptools/) (952 KB)
  - [pyutil 3.3.0 Python module](https://pypi.org/project/pyutil/) (292 KB)
  - [zfec 1.5.1 Python module](https://pypi.org/project/zfec/) (70 KB)

These will need to be uploaded and installed, however uploading this much data will take too long, so we will need to extract only what is needed, and recompress with `xz`/`lzma` to minimize upload size.


## Create Deploy Package

Steps:

1. Download packages
1. Extract packages
1. Select minimal file set
1. Build `xz` compressed tarball
1. Append tarball to `install` script

See the [`create_package`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/sabertooth/create_package) script in [github](https://github.com/nsat/space-services-user-guide/tree/main/tutorials/sabertooth/).


## Install Script

Steps:

1. Locate tarball at end of file
1. Extract tarball to `CWD`
1. Recreate wheel packages for python
1. Move include files to `~/.local/include`
1. `pip install` modules

See the [`install.in`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/sabertooth/install.in) input script in [github](https://github.com/nsat/space-services-user-guide/tree/main/tutorials/sabertooth/).


## Deploy Script

TODO: upload
TODO: schedule payload_sabertooth
