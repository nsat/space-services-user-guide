# In-Orbit Python Environment Setup

|Complexity:|High|
|-|-|
|Payloads:|`SABERTOOTH`, `SDR`, `IPI`|


All payloads include the software and libraries to compile C & C++ applications. This environment is not well suited to the iterative process usually needed due to the time taken to upload files, schedule activities, and wait for the results to appear in the bucket. Where dependent packages are needed, large uploads will require additional time to upload.

Developers should consider using the [cross compiler](../cross-compiling/) if possible.

The [ISL tutorial](../../tutorials/isl/) requires the python module `zfec`. This module has a native C library that is built at installation time by `setuptools`. The `SABERTOOTH`, `SDR`, `IPI` payloads require further setup if the developer plans to deploy python modules that have a C/C++ native build step. This walkthrough can be adapted for any Linux distro package or python module.


## Packages

  - [Python 3.6.9 headers](http://ports.ubuntu.com/ubuntu-ports/pool/main/p/python3.6/libpython3.6-dev_3.6.9-1~18.04ubuntu1.6_arm64.deb) (43 MB)
  - [Python3 pip v20.3.4](https://pypi.org/project/pip/) (1.7 MB)
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
1. Move include files to `/persist/usr/include`
1. `pip install` modules

See the [`install.in`](https://github.com/nsat/space-services-user-guide/blob/main/dev-env/in-orbit/install.in) input script in [github](https://github.com/nsat/space-services-user-guide/tree/main/dev-env/in-orbit/).


## Create Deploy Package

Steps:

1. Download packages locally
1. Extract package contents
1. Select minimal file set
1. Build a single `xz` compressed tarball
1. Append the tarball to a `bash` install script


See the [`create_package`](https://github.com/nsat/space-services-user-guide/blob/main/dev-env/in-orbit/create_package) script in [github](https://github.com/nsat/space-services-user-guide/tree/main/dev-env/in-orbit/).


## Deploy Script

Deployment is a 2-step process of uploading the install file and executing it on the payload. Below are the steps for the `SABERTOOTH` payload. All steps should be repeated for the `SDR` and `IPI` if required.


### Upload Script

<aside class="notice">Replace [YOUR_AUTH_TOKEN] & [YOUR_SAT_ID] as needed.</aside>

```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
SAT_ID="YOUR_SAT_ID"

SATELLITE_ID="satellite_id=SAT_ID"
PAYLOAD="payload=SABERTOOTH"
DESTINATION_PATH="destination_path=/persist/bin/py-install"
EXECUTABLE="executable=true"
QUERY_PARAMS="${SATELLITE_ID}&${PAYLOAD}&${DESTINATION_PATH}&${EXECUTABLE}"

curl -X POST ${HOST}/tasking/upload?${QUERY_PARAMS} \
-H "${AUTH_HEADER}"  \
-F "file=@install"
```

Since the file is a non-trivial size of around 1.7 MB, multiple contacts will likely be needed.


### Run Script


Add a [`PAYLOAD_SABERTOOTH`](https://developers.spire.com/tasking-api-docs/#payload_sabertooth) window to the schedule for in 24 hours (86400 seconds). 24 hours was chosen to give the install script enough time to upload.

```bash
START=$(( `date -u +'%s'` + 86400 ))

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "PAYLOAD_SABERTOOTH",
    "satellite_id": "${SAT_ID}",
    "start": ${START},
    "duration": 60,
    "parameters": {
        "user_command": {
            "executable": "/persist/bin/py-install",
            "executable_arguments": ["/persist"]
        }
    }
}
EOF
```


## Review Deploy Log

```
$ aws s3 ls --recursive s3://user-s3-bucket/a/directory/${SAT_ID}/downlink/

$ aws s3 cp s3://user-s3-bucket/a/directory/${SAT_ID}/downlink/2021/09/06/20210906T043229Z_py-install-2022_01_06_15_02_05.log -
```

Response:

```
2021-09-06 04:32:29          0 2021/
2021-09-06 04:32:29          0 2021/09/
2021-09-06 04:32:29          0 2021/09/06/
2021-09-06 04:32:29       5131 2021/09/06/20210906T043229Z_py-install-2022_01_06_15_02_05.log

<install log contents....>
```
