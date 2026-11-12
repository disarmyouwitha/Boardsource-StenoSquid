# Claude review implementation status

Updated 2026-11-11. The original notes are archived in [claude-review-2026-11-11.md](claude-review-2026-11-11.md). The current implementation is Draft B in draft-2.

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
| 14. Studio and host layout | Owner decisions recorded | Studio mode identity, behavior metadata and USB/memory integration fixes are still under discussion; host layout stays in Javelin Steno Tools |

The pin-map firmware is on [steno-squid/locked-pin-map](https://github.com/disarmyouwitha/zmk-javelin-steno/tree/steno-squid/locked-pin-map). The current baseline compiles with Studio disabled. The successful local builds verify the map update and do not establish the pending Studio integration.
