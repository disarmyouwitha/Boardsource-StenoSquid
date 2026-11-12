# Plate, mounting and rail notes

Claude, 2026-11-12. For Codex and the owner. Nothing here was measured on hardware.

Sources: the owner's photos of both faces of the Boardsource PCB, the owner's switch plate image, and [Boardsource's Wireless Corne docs](https://boardsource.xyz/blogs/guides/wireless-smt-corne-docs). Sizes below are read from the images at about 4.8 to 5.1 pixels per mm, using the 19.05 mm key spacing the vendor states. They are good to a millimetre or two. Replace them with measurements.

## What the PCB and plate show

- **The notch in the PCB is the battery cutout.** The vendor gives the maximum battery as 30 × 17 × 3 mm for Choc and 30 × 17 × 6 mm for MX, "for fitting in the PCB battery cutout under a switch plate". The notch measures roughly 27 × 37 mm in the photos.
- **The plate is a switch plate above the PCB.** It is solid over the battery cutout, about 23 × 34 mm, with a U-shaped notch above it for the USB-C connector.
- **A slot in the plate, about 19 × 2.5 mm, lines up with the 8-contact row.** Eight pins at 2.54 mm pitch span about 18 mm. This reads as the pass-through for a display's header pins. A header's plastic body, about 20 mm long, does not fit the slot and must stay above the plate.
- **The PCB contacts look like plain plated holes.** One face shows a row of 8 round holes along the notch edge, and the other face shows 8 rectangular pads in the same place. Nothing looks castellated. The pitch looks consistent with 2.54 mm but is not verified.
- **Flat mounting in the PCB notch is ruled out.** The module would sit under the solid plate with the battery and could not be reached.

## Mounting plan

Owner intent: the squid lies flush on top of the plate, with its pins passing down through the slot. Choc switches. The PCB-to-plate gap is probably about 3 mm, inferred from the vendor's Choc battery height. Measure it.

What that implies:

1. **Parts face up.** Lying flush, parts on the plate side (Draft C) would press against the plate. The parts reach 0.9 mm (C1) and 0.8 mm (flash) plus solder. Draft C needs a spacer of at least about 1.2 mm to be usable. The Draft B layout, parts and header body on the top face, matches a flush mount.
2. **Artwork goes on the parts face.** The underside is hidden against the plate. Use silkscreen in the free areas between the parts, or exposed copper or gold on the ground pour (see `artwork/gold-eyes.svg`). Silkscreen cannot cover pads, and the free area is small, so the Inkling will need to shrink or be trimmed.
3. **Width.** The solid plate area is about 23 mm wide with a switch hole beside it. The module is 22 mm wide. Trim to about 20 mm. The 8 contacts need about 19 to 20 mm. Depth is fine: about 33 mm is available above the slot and the module needs 17 mm.
4. **Contact row over the slot.** The row's pads are 1.7 mm wide, narrower than the 2.5 mm slot, so the underside solder fillets sit inside the slot and the board can lie flat. The board edge past the row can overhang the plate strip below the slot by about 1 mm.
5. **Pin length.** The pins must pass the squid (1.0 mm), the plate (typically 1.2 mm for Choc, confirm), the PCB-to-plate gap (about 3 mm), the host PCB (about 1.6 mm, confirm) and leave a solder tail. That is about 8 to 10 mm below the squid's underside. Standard headers have 3 mm and 6 mm sides, so use a long-pin header, or pins held by a plastic body slid up to the top face.

## Rail, R2 and C2

- **Update 2026-11-12: leave R2 and C2 unfitted** for now, to avoid R2's continuous draw. If the breadboard test shows a slow fall, fit a larger R2 (470 kΩ to 1 MΩ) with C2 off. C2 alone makes the rail fall more slowly. The figures below are for the case with both fitted.
- With both fitted the time constant is about 100 kΩ × 1.1 µF ≈ 110 ms, and the rail needs about 0.26 s to fall below 0.3 V. R2 costs about 33 µA while the rail is on.
- Firmware: the pause with the rail off between flash start-up retries is now 500 ms, in `claude/review-fixes` (`86a30ae`). It was 100 ms.
- To measure on the host: rail voltage on USB and on battery (the flash is specified for roughly 2.7 to 3.6 V), the polarity of P0.31 (the vendor does not state it, and the firmware assumes high is on), how fast the rail falls when P0.31 switches it off, and what else loads it.

## Still unknown

- The antenna position. Neither the photos nor the vendor docs show it. Ask Boardsource, or look at the delivered board, and keep the module out of its keep-out zone.
- The PCB thickness, plate thickness and PCB-to-plate gap on the real parts.
- Whether the host contact holes are edge-cut.

## Asks for Codex

Superseded by the [Draft D design brief](draft-d-spec.md), which fills the whole solid plate area instead of the 20 mm trim suggested here, and uses pins without a plastic body. The actual plate file (DXF, SVG or STEP), if the owner can supply it, would replace the estimates with exact sizes.
