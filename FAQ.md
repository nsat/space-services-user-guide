# FAQ


## What is ECEF?

Earth-centered, Earth-fixed coordinate system. ECEF data is provided with TFRS from the [Satellite Bus API](https://developers.spire.com/satellite-bus-api/).

More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system).


## What is TFRS

Time-Frequency Reference System. Provides a highly accurate clock and position reading. TFRS data is provided from the [Satellite Bus API](https://developers.spire.com/satellite-bus-api/).


## What is an IQ File?

**I**n-phase and **Q**uadrature. The IQ file format comprises unsigned 16-bit pairs of imaginary and quadrature numbers. The file format is used to store samples from, or played into a Software Defined Radio (SDR).

More information can be found on [Wikipedia](https://en.wikipedia.org/wiki/In-phase_and_quadrature_components).


## How do I transmit and receive using the software-defined-radio (SDR)?

The software-defined-radio is on the [`SDR`](./ExecutionEnvironment.html#sdr) Linux payload. The radio is operated via the command-line tools [rf_collect](./Utilities.md#rf-collect) & [rftransmit](./Utilities.md#rf-transmit).


## How do I control the orientation of the satellite?

The satellites orientation (attitude) can be controlled from the ground by including [`adcs_config`](https://developers.spire.com/tasking-api-docs/#adcs_config) in the payload window, or while in orbit using an [`LEASE_ADCS`](https://developers.spire.com/tasking-api-docs/index.html#lease_adcs) and the [Satellite Bus API](https://developers.spire.com/satellite-bus-api/).


## Payload In Space, Software In Space - What's the difference?

With Payload In Space the customer owns the payload computer/hardware and has root access, regardless of whether Spire or the customer provided the hardware. Software In Space customers do not own the hardware; For this case the customer has the flexibility of different payload types and satellites available. Payload In Space is a specific case of Software In Space, where all the same APIs are available to the customer, along with the [Signaling API](https://developers.spire.com/payload-signaling-api-docs/) which is only for Payload In Space customers, and is required to allow Spire to notify the customer's payload of various events.


## How do I reduce file transfer latency?

When it's time to transmit data in a contact, file transmission begins, and continues until the end of the contact window. At the end of the window if a file transfer is in progress, the file is only partially transferred, and the transfer is resumed at next contact, which could be minutes, or hours later. The partial file is never delivered. It follows that smaller files are more likely to be delivered on the first available contact. More information on downlink and uplink can be found [here](https://developers.spire.com/tasking-api-docs/#total-daily-download-volume).
