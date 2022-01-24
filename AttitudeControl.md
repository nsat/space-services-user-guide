# Attitude Control

Attitude is controlled by the Attitude Control and Determination System (ADCS). Attitude information can be set as part of a window, or at run-time, in-orbit when there is an ADCS lease window, via the [Satellite Bus API](https://developers.spire.com/satellite-bus-api/). The ADCS provides a way for the satellite to reorient itself, and report which way it is facing. Attitude information is always relative to an aperture/antenna. If none is provided then the X/S-BAND radio is assumed.


## Setting ADCS on windows

If the user knows ahead of time what the are of interest is (i.e. tracking a point on earth or facing a fixed direction) then this information can be provided in [`adcs_config`⤴](https://developers.spire.com/tasking-api-docs/#adcs_config) on the  payload window. For example, to take a photo of a location on earth, the user would schedule an [`PAYLOAD_IPI`⤴](https://developers.spire.com/tasking-api-docs/#payload_ipi) window to have the the `IPI` aperture track that location:

```json
{
    "type": "PAYLOAD_IPI",
    "parameters": {
            "adcs_config": {
              "mode": "TRACKING",
              "aperture": "IPI",
              "target_latitude_north": 25.5,
              "target_longitude_east": -71.5
            },
            "user_command": { /* take photo */ }
        }
    }
}
```

The [Tracking an Area Of Interest Tutorial](./tutorials/aio/) demonstrates this.


## Setting ADCS at Run-time

If the user plans to command the satellites attitude from the payload, a [`LEASE_ADCS`⤴](https://developers.spire.com/tasking-api-docs/index.html#lease_adcs) window must be scheduled which allows a payload window to call the [Satellite Bus API⤴](https://developers.spire.com/satellite-bus-api/) to control attitude in real-time. For example, this can be used by a user process running on a payload in-orbit that listens for ADS-B messages and directs a camera to take a photograph of the location reported within a specific ADS-B message. The location is not known at the time the window is scheduled, so the satellite must be commanded in real-time.

The [Leasing ADCS for Realtime Control](./tutorials/adcs-lease/) demonstrates this.



## Next Steps

 - [Tools & Utilities](./Utilities.md)
