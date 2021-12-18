Inter-Satellite LinksTracking an Area Of Interest Tutorial

|Complexity:|High|
|-|-|
|Payloads:|2 satellites with ISL: `SDR` & `SABERTOOTH`|
|Windows:|`LEASE_ISL`, `PAYLOAD_SDR` & `PAYLOAD_SABERTOOTH`|

Inter-Satellite Links (ISL) are enabled for some satellites. ISL links can be made between 2 satellites following the same orbit so that they can be in contact at any time, and there is little relative motion between them. Satellites that are in intermittent contact when their orbits overlap may also be used for ISL contacts, so long as their direction is similar enough for meaningful contact time as well as low doppler-shift.

For this example we will be assuming that the satellites are in synchronous orbit to simplify calculating when to schedule the windows.


1. Schedule an ISL between 2 satellites
1. Upload listener and client to satellites
1. Schedule the `SDR` on the transmitting satellite to send data
1. Schedule the `SABERTOOTH` on the receiving satellite to listen for & downlink data
1. Review


## Schedule LEASE_ISL

The `LEASE_ISL` is used to configure a one-way S-BAND ISL, providing a simplex IP link between the satellites. UDP is used for data transfer as the protocol has no return acknowledgment.

A single call to the Tasking API creates a `LEASE_ISL` in both satellites. For this example satellites `FM1` and `FM2` are scheduled for 5 minutes. Everything is scheduled 24 hours out when there are no conflicts with existing down-link contact windows.


```bash
HOST="https://api.orb.spire.com"
AUTH_HEADER="Authorization: Bearer YOUR_AUTH_TOKEN"
START=$(( `date -u +'%s'` + 86400 ))

curl -X POST ${HOST}/tasking/window \
-H "${AUTH_HEADER}" \
-H "Content-Type: application/json" \
-d @- << EOF
{
    "type": "LEASE_ISL",
    "satellite_id": "FM1",
    "start": ${START},
    "duration": 300,
    "parameters": {
        "user_isl_receive_satellite_id": "FM2"
    }
}
EOF
```


## Upload Listener & Client



.