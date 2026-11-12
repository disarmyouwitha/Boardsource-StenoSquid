# Claude review of Draft B

Reviewed 2026-11-11 at commit `0f327c3`, from `draft-2/steno-squid.kicad_pcb`, `interface.json`, `BOM.csv`, `validation.json` and the previews. The board file was parsed with a script. KiCad was not run, so the ERC and DRC results are the ones recorded in `draft-2/checks`.

## Confirmed

- **Pin map.** Header contacts 1 to 8 carry CS_N, IO0, IO3, IO1, VCC_SW, GND, CLK and IO2, and reach flash pads 1, 5, 7, 2, 8, 4, 6 and 3. This matches the locked map.
- **Package.** U1 is the WSON-8 6 × 5 mm footprint. The 3.4 × 4.3 mm centre pad is on GND and its paste is split into four windows. Signal pads are 1.15 × 0.6 mm at ±2.825 mm, which covers the package leads with toe to spare.
- **Labels.** VCC, GND and 1 to 8 are on both faces, with a pin-1 marker on the back.
- **Bleed resistor.** R2, 100 kΩ, from VCC_SW to GND, not fitted by default.
- **Passives.** C1 100 nF and C2 1 µF (not fitted) across VCC_SW and GND. R1 10 kΩ pulls CS_N up to VCC_SW.

## Change before ordering

1. **Add ground vias.** The board has no vias on GND. The top and bottom ground pours meet only at the plated hole of header contact 6. Add two to four vias beside U1 pad 4 and the centre pad, and one beside C1 pad 2, so the decoupling capacitor has a short return path to the bottom pour.
2. **Widen and shorten the power track.** VCC_SW is 0.2 mm wide and about 46 mm long, in 54 segments, on a 22 mm board. It will carry the current, but 0.4 mm or wider on a more direct route costs nothing. Keep C1 between the header and U1 pad 8.
3. **Update `docs/review-status.md`.** Its closing paragraph says the firmware baseline compiles with Studio disabled and points at `steno-squid/locked-pin-map`. Firmware `main` now builds with ZMK Studio on by default for the left half, and GitHub Actions builds every push.

## Minor

- The 3D model path for U1 names a WDFN part with a 3.4 × 4 mm pad. It only affects the render.
- A WSON has no exposed leads. Hand assembly needs solder paste and hot air or a hotplate. Assembly by the board house avoids that.

## Still open

- Which face mates with the Boardsource, the overhang direction and the header height.
- The P0.31 rail: polarity, voltage, shared loads and discharge time, which also decides whether R2 is fitted.
- The firmware `qspi.dtsi` for the Boardsource has not been checked against firmware `main` since the Studio and flash changes were merged.
