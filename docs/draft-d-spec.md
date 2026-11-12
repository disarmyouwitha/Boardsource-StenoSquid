# Draft D design brief

Proposed 2026-11-12 by Claude, from the owner's decisions. Not built: Claude has no KiCad here, so nothing was generated, routed or checked. Codex builds it in KiCad and runs ERC and DRC. The scale drawing is [draft-d-plate-fit.svg](draft-d-plate-fit.svg). All plate sizes are estimates read from an image (about 4.79 pixels per mm, from the 19.05 mm key pitch), good to a millimetre or two.

## Decisions from the owner

- The squid lies flat against the top of the switch plate, with the **parts and the artwork facing up**.
- It mounts through the plate's header slot on extended header pins, into the Boardsource header holes.
- It fills the solid plate area right of the key block, as far as the plate allows.
- The Inkling is drawn on the top face, around the components.
- Choc switches. Pin map, WSON-8 flash (W25Q128JVPIQ) and all other parts as in Draft B, with **R2 and C2 fitted**.

## Orientation and pinout, checked against sources

Seen from above, on the left half, with the USB-C at the top: the contact row runs along the **bottom** edge of the squid, **pin 1 at the left**, pin 8 at the right, parts up.

Why this is right: the nice!view documentation shows five pin holes, left to right when the display faces up: MOSI, SCK, VCC, GND, CS. The Boardsource header maps pins 3 to 7 to P0.12 (MOSI), P0.23 (SCK), VCC, GND and P0.19 (CS). So the vendor's "left to right" is the view from above, parts up, and a nice!view occupies header pins 3 to 7 in the middle of the row.

Consequence for the layout: Drafts B and C have the row at the top of the board. Draft D needs it at the bottom with pin 1 still on the left. Rotating or mirroring Draft B does not do that, because the flash cannot be mirrored. Re-place and re-route. The net names and the pin map stay exactly as locked.

## Geometry

Frame: origin at the left end of the plate slot, on the slot's centre line. x to the right, y up, millimetres. The plate image is the left half seen from above.

| Feature | Value |
| --- | --- |
| Left limit of the solid area (right edge of the key holes) | x = −2.5 |
| Plate right edge | x = 21.9 |
| Plate top edge | y = 45.0 |
| Slot | x 0 to the plate edge (open at the right), y ±1.25 (2.5 mm tall) |
| USB-C notch, wide part | x 2.9 to 17.1, y 42.3 to 45.0 |
| USB-C notch, narrow part | x 5.2 to 14.8, y 35.2 to 40.6, with a step between |
| Key holes beside the area | about 14.4 mm square, pitch 19.05 mm |

A nice!view (36 × 14 mm) in the same place, with its pin row on the slot centre line, ends 34 mm above the row. That is just below the notch at y = 35.2, which is a good sign that the numbers are right.

## Outline

Option A, as requested, fills the area with a cut around the USB notch:

- x from −1.8 to 21.1 (22.9 mm wide), bottom edge at y = −1.92.
- Two ears run up each side of the notch, to y = 44.4 on the left and y = 43.0 on the right, with 0.8 mm clearance to the plate notch.
- The notch in the squid has a wide part, x 2.1 to 17.9 above y = 41.5, and a narrow part, x 4.4 to 15.6 down to y = 36.0.
- Overall about 22.9 × 46.3 mm. Corner radius at least 1 mm. The exact polygon is in the drawing.

Option B drops the ears: x −1.8 to 21.1, y −1.92 to 36.0. That is 22.9 × 37.9 mm, a wide nice!view-sized board, simpler and more robust. The ears add only artwork area.

Margins are 0.7 mm to the key holes and 0.8 mm to the plate edge. The row's position inside this width is set by the host and is not yet known (see below).

## Contact row

- 8 plated holes, 1.0 mm drill, 1.7 mm pads, 2.54 mm pitch, on y = 0. Square pad on pin 1.
- Pin 1 at x = 2.2 as a placeholder. Make it a parameter. The real value comes from measuring the host: pin 1 must be at least 1.5 mm from the slot's left end, so it lies between 1.5 and about 4.1.
- The underside pad ring and solder fillet must fit inside the 2.5 mm slot height, so they sit in the slot and the board lies flat.
- No plastic header body on the squid. Solder bare pins, using the header's body underneath as a jig, then slide it off the long ends.

## Parts

- U1 flash, C1, R1, C2 and R2, all fitted, top face.
- Parts zone: x ≥ 0 and y 0.9 to 14, close to the row so the QSPI traces stay short.
- Keep tall parts away from the key side: nothing taller than the bare board within 2.5 mm of the key holes (x < 0), because Choc keycaps overhang their holes. Parts reach 0.9 mm (C1) and 0.8 mm (flash) above a 1.0 mm board, about 1.9 mm above the plate.
- Keep the 0.4 mm VCC_SW track, the ground vias and the grounded flash pad from Draft B.

## Artwork

The Inkling goes on the top face between and around the parts: silkscreen in the free area (y 15 to 43 is clear), or exposed copper or gold over the ground pour (see `artwork/gold-eyes.svg`). Silkscreen cannot cover pads. The area is far larger than Draft B's, so the squid can be drawn about twice as large.

## Board

- 2 layers, 1.0 mm FR4, as before.
- Solder mask over the whole underside except the pin pads, in case the plate is conductive.
- The squid can be held down with double-sided tape. The plate carries it, and the pins locate it.

## Pins

Below the squid's underside the pins must pass the plate, the PCB-to-plate gap and the host PCB, and leave a tail. With assumed values that is about 1.2 (plate) + 3.0 (Choc gap, inferred from the vendor's 3 mm Choc battery height) + 1.6 (PCB) + 1.0 (tail) = 6.8 mm, plus about 1 mm above the squid for the solder joint. Order long-pin headers, at least 8 mm below the body, and trim after. Replace the assumptions with measurements.

## Measure on the delivered board

1. Position of host pin 1, relative to the left end of the plate slot, and the pitch.
2. Plate thickness, PCB thickness, and the PCB-to-plate gap.
3. Distance from the key holes to the plate edge, and the keycap overhang.
4. Whether the plate is conductive.
5. Where the antenna is. Neither the photos nor the docs show it, and a ground-pour board near it could hurt range.
6. The switched rail on pin 5: voltage on USB and battery, polarity of P0.31, how fast it falls when switched off.

## For Codex

Build Draft D in a new `draft-4` folder from the Draft B netlist, with the layout above. Run the checks with nothing ignored, and update `interface.json`, `validation.json`, the BOM (R2 and C2 fitted) and the README. Test-print the outline and the contact row at 1:1 and hold it against the plate before ordering.
