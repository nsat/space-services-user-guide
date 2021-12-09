# Fundamentals

In simple terms, applications are deployed to the satellite, time is scheduled to run the applications, and the output is downloaded to AWS S3. Applications have access to satellite hardware and telemetry.

Everything happens as time windows on a schedule. The schedule holds all upcoming contact windows with the ground (and other satellites), and all reservation windows made by customers. Customers reserve specific hardware over a time window on a satellite. The schedule is synchronized with the satellite at each contact.

## Lifecycle

1. **Develop** code to run on the satellite 
1. **Deploy** applications and data to the satellite
1. **Schedule** application to run at a specific time window
1. **Wait** for window to complete & results downloaded
1. **Analyze** received data

## Execution Environment
The satellite hosts multiple Linux computers ("payloads") with each managing specific hardware (i.e. cameras, transceivers or GPUs). Spire provides a persistent isolated execution environment for the customer to upload files to and run applications. An inbox and output provide a way to uplink and downlink files. A local agent provides a REST API to interact with the satellite bus (i.e. for telemetry or attitude control), as well as an SDK. 


## Satellite Bus
The satellite bus is a broad name given to the many systems on the satellite that support a customers activities.  Spire maintains the satellite bus, which includes powering systems on and off, charging batteries, station-keeping, communicating with the ground (and other satellites), running the schedule, and executing customer applications on the payloads. 


## Window
A window is a reserved period of time on a specific satellite for an activity. Windows are placed in the schedule. Different window types reserve different hardware and require exclusive access to different things, i.e. attitude control. Customer reservations are represented as types of windows too.


### Contact Window
A contact is a type of window, and is a one or two-way radio transmission between a satellite and a ground-station, or between two satellites (inter-satellite links). The purpose of a contacts is broad, but includes time for maintenance, schedule synchronization and the transfer of data, logs and telemetry. Spire schedules contacts for its exclusive use - customer code is not made aware of these contacts. Customers may schedule their own contacts between satellites. 


## Satellite Schedule
The list of windows for each satellite is held in a schedule. The schedule contains all windows, both for contacts and customer activities. The schedule is synchronized with the satellite at each contact. 


## Scheduling Time on a Payload
A window is inserted into the schedule with the [Tasking API](). The window type controls what payload is reserved. A window accepts attitude control information to enable directional control of antennas, apertures, cameras etc. 


## Uploading, Downloading & Sharing Files
The [Tasking API]() provides an `upload` endpoint for up-linking files to a specific satellite payload. Files are cached on the ground and queued for upload at subsequent contacts, managed by Spire.


## Spire Linux Agent
Each Linux payload runs a local agent to provide a RESTful interface to interact with the satellite bus. The services provided by the daemon are numerous, and include file inbox/outbox, telemetry, and attitude control.


## Inter-payload Networking
When windows on a satellite overlap, ethernet is provided for IP networking, Ping and UDP & TCP ports 10,000+ are enabled. This allows application code to communicate, i.e. listen on a port for requests from a different payload.


## Inter-satellite Networking
Inter-satellite-links (ISL) lease windows can be scheduled for customer use. They are requested with the [Tasking API]() and create a Tx window on one satellite and Rx window on the other, as the link is simplex/one-way. ISL leases require a satellite pair in synchronous orbit.  An ISL lease window opens up a route to payloads on the remote/Rx satellite. To make use of the ISL network, windows on the sending a receiving satellites would be scheduled concurrently. Destination ports of 10,000+ are routed across the link. The simplex link means that TCP can not be "acknowledged" - UDP is supported.


## Power
The satellite bus manages power consumption and collection of solar energy. In the unlikely event that there is not enough power to maintain the health of the satellite bus, a payload window may be aborted or not attempted at all. 


## Antennas & Apertures (Cameras)
Various antennas are made available on the Software Defined Radio (SDR) payload.  Some antennas allow for Tx/Rx while others are Rx only. Spire provides utilities for RF capture and receive.

The Imaging Payload Interface (IPI) payload provides customer with access to one or more cameras. Spire provides an SDK and utilities for managing and acquiring images.


## Attitude Control
The orientation (attitude) of the satellite is controlled by an Attitude Determination and Control System (ADCS). Attitude control supports a range of modes including nadir and target tracking.


### Ground Based
When a window is scheduled, attitude can be provided. The satellites attitude is set before the start of the window.


### In-orbit - Realtime
Additionally, a window can be scheduled to allow in-orbit control of attitude from one or more payloads. This allows payloads to respond to events in real-time by pointing directional antennas and/or apertures at areas of interest. Attitude control is provided via REST API to the local agent. 


## Telemetry
Various metrics are captured on the satellite bus and made available on the ground to customers. This telemetry includes power levels and attitude data. 


## Ground Station
Spire maintains ground-stations around the globe. The location & capabilities of each ground-station affect when a customer can expect their data to be uplinked or downlinked. Ground stations are fitted with some combination of UHF, S-BAND and X-BAND transceivers.
