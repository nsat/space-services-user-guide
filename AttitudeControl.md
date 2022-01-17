# Attitude Control

Attitude is controlled in-orbit by the Attitude Control And Determination System (ADCS). Attitude information can be configured as part of a window, or at run-time/in-orbit with an ADCS lease. ADCS provides a way for the satellite to reorient itself, and report which way it is facing. Attitude information is always relative to an aperture. If none is provided then the X/S-BAND radio is assumed.


## Modes

Documentation on how to set the mode can be found [here](https://developers.spire.com/tasking-api-docs/#adcs_config).


### Nadir

Nadir means to point the chosen aperture directly below the satellite relative to the earth.


### Target-Tracking

The satellite is continually adjusted to ensure the aperture is pointed directly at the provided lat/lon on the ground as the satellite passes. This is useful for directional antennas and imaging equipment.


### NOOP

This mode defers ADCS control, allowing for another payload window, ADCS lease, ISL, solar charging, or station-keeping to take control.


## Next Steps

 - [Tools & Utilities](./Utilities.md)
