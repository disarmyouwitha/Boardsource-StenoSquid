# Prototype status

| Area | Status |
|---|---|
| KiCad | Routed plate-top WSON layout. ERC, DRC, open-net and schematic parity checks pass. |
| Host fit | Confirm slot and contact alignment, pin-1 offset, USB plug and keycap clearance, and stack height on the Choc plate. |
| Assembly | Review the WSON lands and stencil. Select bare pin length after measuring the stack. |
| Switched rail | Confirm P0.31 polarity, voltage under load, discharge and shared loads. Keep C2 and R2 unpopulated for the breadboard test. |
| Bluetooth | Identify the antenna and verify clearance. Compare host and split links with the module fitted and removed. |
| Firmware | Boardsource Studio-enabled left, logging left, right and flash probes passed CI. Hardware testing is pending. |

[Current KiCad and fit files](../draft-4/README.md) · [Electrical, mechanical and RF review](design-review.md) · [Firmware CI](https://github.com/disarmyouwitha/zmk-javelin-steno/actions/runs/43167852080)

Historical review records are available in the [original electrical review](claude-review-2026-11-11.md), [WSON follow-up](claude-review-draft-b-2026-11-11.md), and [plate and mounting notes](claude-plate-and-mounting-2026-11-12.md).
