# Hardware and Vendor Adapter Strategy

NMRT separates vendor support from scientific processing. A Delsys, National Instruments, CED, or other adapter converts vendor-specific streams into the same canonical `Recording` object.

## Delsys

Planned support:
- HPF import through the user's locally installed/licensed Delsys conversion library
- exported CSV/text formats
- explicit ordered channel maps
- expected EMG vs ACC sampling-rate QC
- deep QC for missing/unequal streams
- no bundled proprietary Delsys DLLs

## National Instruments

Planned support:
- DAQ discovery
- arbitrary analog input channels
- differential/RSE/NRSE terminal configuration where supported
- engineering scale + offset
- independent live channel displays in the GUI
- UTC-aware recording metadata
- hardware/software trigger configuration
- raw voltage preservation plus calibrated derived signals

## CED / Spike2

Planned support:
- `.smr`/`.smrx` import through open libraries where technically supported
- continuous waveform channels
- event/marker channels
- preservation of sample rates and original timing
- clear fallback instructions to export from Spike2 when native parsing is incomplete

## ADInstruments / LabChart

Initial strategy:
- support exported text, CSV, MATLAB and other open representations
- map flow, pressure, spirometry and analog channels explicitly
- do not reverse-engineer or redistribute proprietary components

## Synchronization

The synchronization subsystem should support:
- shared hardware TTL pulses
- analog trigger channels
- digital event markers
- UTC/system timestamps
- manual alignment anchors
- lag estimation for diagnostic use
- drift estimation across clocks

Software timestamps alone must never be represented as equivalent to validated hardware synchronization.
