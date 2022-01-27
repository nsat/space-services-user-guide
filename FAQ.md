# FAQ


## What is ECEF?

Earth-centered, Earth-fixed coordinate system. ECEF data is provided with TFRS from the [Satellite Bus API⤴](https://developers.spire.com/satellite-bus-api/).

More information can be found on [Wikipedia⤴](https://en.wikipedia.org/wiki/Earth-centered,_Earth-fixed_coordinate_system).


## What is TFRS

Time-Frequency Reference System. Provides a highly accurate clock and position reading. TFRS data is provided from the [Satellite Bus API⤴](https://developers.spire.com/satellite-bus-api/).


## What is an IQ File?

**I**n-phase and **Q**uadrature. The IQ file format comprises unsigned 16-bit pairs of imaginary and quadrature numbers. The file format is used to store samples from, or played into a Software Defined Radio (SDR).

More information can be found on [Wikipedia⤴](https://en.wikipedia.org/wiki/In-phase_and_quadrature_components).


## How do I transmit and receive using the software-defined-radio (SDR)?

The software-defined-radio is on the [`SDR`](./ExecutionEnvironment.html#sdr) Linux payload. The radio is operated via the command-line tools [rf_collect](./Utilities.md#rf-collect) & [rftransmit](./Utilities.md#rf-transmit).


## How do I control the orientation of the satellite?

The satellites orientation (attitude) can be controlled from the ground by including [`adcs_config`⤴](https://developers.spire.com/tasking-api-docs/#adcs_config) in the payload window, or while in orbit using an [`LEASE_ADCS`⤴](https://developers.spire.com/tasking-api-docs/index.html#lease_adcs) and the [Satellite Bus API⤴](https://developers.spire.com/satellite-bus-api/).
