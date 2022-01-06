# Sabertooth Python Build Environment Setup

|Complexity:|High|
|-|-|
|Payloads:|`SABERTOOTH`|
|Windows:|`PAYLOAD_SABERTOOTH`|

The `SABERTOOTH` payload is installed with the stock NVIDIA JETSON Ubuntu 18.04.2 Linux distro ([specs](../../ExecutionEnvironment.md#sabertooth)). The environment requires further setup if the user plans to deploy python modules. This walkthrough can be adapted for any Linux distro package or python module.

 A list of packages installed on the `SABERTOOTH` payload can be found [here](../../text/sabertooth_package_list.txt). 


 ## Packages

The ISL tutorial requires the python module `zfec`. The following instructions demonstrate deploying this module and it's dependencies:

  - [Python 3.6.9 headers](http://ports.ubuntu.com/ubuntu-ports/pool/main/p/python3.6/libpython3.6-dev_3.6.9-1~18.04ubuntu1.6_arm64.deb) (43 MB)
  - [Python3 pip v21.3.1](https://pypi.org/project/pip/) (1.7 MB)
  - [Python3 setuptools v59.6.0](https://pypi.org/project/setuptools/) (952 KB)
  - [pyutil 3.3.0 Python module](https://pypi.org/project/pyutil/) (292 KB)
  - [zfec 1.5.1 Python module](https://pypi.org/project/zfec/) (70 KB)

Uploading each package would take quite a while. To reduce the time required to upload the packages the following steps are taken:

1. Remove any files in packages that are not needed
1. Re-pack all packages into a single archive for better compression
1. Use `xz`/`lzma` compression to further reduce the size


## Install Script

Steps:

1. Locate tarball at end of `install` file
1. Extract the tarball to `CWD`
1. Recreate wheel packages for python
1. Move include files to `~/.local/include`
1. `pip install` modules

See the [`install.in`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/sabertooth/install.in) input script in [github](https://github.com/nsat/space-services-user-guide/tree/main/tutorials/sabertooth/).


## Create Deploy Package

Steps:

1. Download packages locally
1. Extract package contents
1. Select minimal file set
1. Build a single `xz` compressed tarball
1. Append the tarball to a `bash` install script


See the [`create_package`](https://github.com/nsat/space-services-user-guide/blob/main/tutorials/sabertooth/create_package) script in [github](https://github.com/nsat/space-services-user-guide/tree/main/tutorials/sabertooth/).


## Deploy Script

Deployment is a 2-step process of uploading the install file and executing it on the `SABERTOOTH`.


### Upload Script

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"

SATELLITE_ID="satellite_id=FM1"
PAYLOAD="payload=SDR"
DESTINATION_PATH="destination_path=/py-install"
EXECUTABLE="executable=true"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"

curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@install"
```

Since the file is a non-trivial size of around 1.7 MB, multiple contacts will likely be needed.


### Run Script


Add a [`PAYLOAD_SABERTOOTH`](https://developers.spire.com/tasking-api-docs/#payload_sabertooth) window to the schedule for in 24 hours. 24 hours was chosen to give the install script enough time to upload.

```bash
START=$(( `date -u +'%s'` + 86400 ))

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SABERTOOTH",
    "satellite_id": "FM1",
    "start": ${START},
    "duration": 60,
    "parameters": {
        "user_command": {
            "executable": "/py-install"
        }
    }
}
EOF
```


## Review Deploy Log

```bash
aws s3 ls --recursive s3://customer-s3-bucket/a/directory/FM1/downlink/
```

Response:

```bash
2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       2568 2021/09/06/20210906T043229Z_py-install.log
```
