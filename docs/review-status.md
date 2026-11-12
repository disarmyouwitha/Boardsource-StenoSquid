# Claude review implementation status

Updated 2026-11-12. The original notes are archived in [claude-review-2026-11-11.md](claude-review-2026-11-11.md). The current implementation is Draft B in draft-2.

| Review item | Status | Evidence or next input |
|---|---|---|
| 1. Power labels and back contact numbers | Complete | VCC, GND and 1–8 on both faces, back pin-1 marker; validation asserts the legends |
| 2. Host mating orientation and overhang | Physical check pending | Delivered PCB, battery, plate and case dimensions |
| 3 / 7. Low-profile WSON package | Implemented | W25Q128JVPIQ, grounded 3.4 × 4.3 mm EP, segmented paste, two-layer track/via keepout; assembler review pending |
| 4. Optional bleed resistor | Implemented | R2 100 kΩ DNP; population and value follow discharge measurements |
| 5. Flash identification | IQ variant retained | Expected EF 40 18; alternate IDs/quad procedures need separate driver work |
| 6. RGB | Deferred | All six signal contacts serve QSPI |
| 8. Flash lifecycle | Documented prototype limitation | Recheck ordering availability; larger runs need second-source qualification |
| 9. Locked pin map | Implemented across hardware and firmware | Six-net cross-check passed; firmware default and sleep selections agree |
| 10. Other switched-rail loads | Physical/schematic investigation pending | Identify host rail circuit and shared loads |
| 11. Local build evidence | Complete for pin-map revision | Left/right/probe/quad pass, compiler/commit/dependency hashes and UF2 SHA-256 recorded in firmware branch |
| 12. Ignored DRC categories | Complete | All five former ignores enabled; current DRC has no ignored categories and zero issues |
| 13. Artwork face | Pending orientation | Back squid remains a candidate until item 2 is resolved |
| 14. Studio and host layout | CI builds pass, hardware test pending | The left Studio targets on firmware main and the Boardsource branch pass CI. Host layout stays in Javelin Steno Tools |
| Draft B follow-up: local ground returns | Complete | Three stitching vias, two beside U1 and one beside C1. The WSON pad keepout is preserved |
| Draft B follow-up: switched power | Complete | 0.40 mm minimum, 39.48 mm total across 15 segments. Header contact 5 to C1 to U1 stays on the front |
| Draft B follow-up: current firmware map | Verified | All six active and sleep pin selections match Draft B at Boardsource firmware commit `80a1cae` |

Firmware `main` now builds its nice!nano left target with ZMK Studio enabled. GitHub Actions runs on code pushes, and the Boardsource firmware branch also passed `boardsource-left-studio`, `boardsource-left-logging`, `boardsource-right` and both flash probes. These builds verify compilation. The delivered board is still needed to confirm the mating face, qualify the P0.31 rail and test runtime behavior. [Main CI run](https://github.com/disarmyouwitha/zmk-javelin-steno/actions/runs/43167755597) · [Boardsource CI run](https://github.com/disarmyouwitha/zmk-javelin-steno/actions/runs/43167852080)
