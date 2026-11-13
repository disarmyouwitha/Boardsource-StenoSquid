# Draft D design brief

Proposed 2026-11-12 by Claude, from the owner's decisions. The routed [Draft D KiCad layout](../draft-4/README.md) uses Option A and has its own [actual-size template](../draft-4/previews/plate-fit-1to1.svg). The original scale drawing is [draft-d-plate-fit.svg](draft-d-plate-fit.svg). All plate sizes are estimates read from an image (about 4.79 pixels per mm, from the 19.05 mm key pitch), good to a millimetre or two.

## Decisions from the owner

- The squid lies flat against the top of the switch plate, with the **parts and the artwork facing up**.
- It mounts through the plate's header slot on extended header pins, into the Boardsource header holes.
- It fills the solid plate area right of the key block, as far as the plate allows.
- The Inkling is drawn on the top face, around the components.
- Choc switches. Pin map, WSON-8 flash (W25Q128JVPIQ) and all other parts as in Draft B. **R2 and C2 are footprints only, not fitted**, until the breadboard test says the switched rail falls too slowly (see Rail bleed).

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

- U1 flash, C1 and R1 fitted, top face. C2 and R2 have pads but are not fitted (DNP).
- Parts zone: x ≥ 0 and y 0.9 to 14, close to the row so the QSPI traces stay short.
- Keep tall parts away from the key side: nothing taller than the bare board within 2.5 mm of the key holes (x < 0), because Choc keycaps overhang their holes. Parts reach 0.9 mm (C1) and 0.8 mm (flash) above a 1.0 mm board, about 1.9 mm above the plate.
- Keep the 0.4 mm VCC_SW track, the ground vias and the grounded flash pad from Draft B.

## Rail bleed (open)

The owner does not want R2's continuous draw (about 33 µA at 100 kΩ while the rail is on) unless it is needed. The breadboard test with the Adafruit breakout measures how fast the switched rail falls. If it is too slow, fit a larger R2 (470 kΩ to 1 MΩ, 3 to 7 µA) with C2 left off: against C1 alone that gives a time constant of 50 to 100 ms. Keep both footprints.

## Antenna (suspected, unverified)

From the owner's close-up photo of the host board's centre edge, a narrow white ceramic strip on each module's inner edge looks like the antenna. This is a visual inference only. No Boardsource RF drawing or part identification has been found. On the left half it lies about 4 mm below the header row (scale from the hole pitch, roughly 25 px per mm) and lines up with header pins 7 and 8, near the plate's right edge. The squid sits above the row, over the battery cutout, so there is little overlap seen from above. The one place it reaches is the bottom-right corner, 1.92 mm below the row and 3 to 4 mm from the antenna in plan.

Rules until the antenna is identified:

1. Keep the artwork area free of copper on both layers where possible. Draw the Inkling in silkscreen. Exposed gold or copper artwork (`artwork/gold-eyes.svg`) waits for a passing Bluetooth test.
2. Keep the ground pour compact, around the flash, the passives and the contact row. Do not fill the whole board with ground.
3. Keep ground copper near the contact row for the flash return paths. The bottom-right corner (x > 14 mm, y < 3 mm) is a candidate for a localized cutback if Bluetooth testing or the antenna specification calls for it.
4. Once the antenna part is known, replace these with its datasheet keepout.
5. Bluetooth range is a pass/fail test on the real board, with the squid fitted and removed, in the same place.

## Artwork

The Inkling is white top silkscreen in the free area above the components. The artwork area has a copper keepout on both layers. The exposed-copper study in `artwork/gold-eyes.svg` is deferred pending antenna identification and Bluetooth testing.

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
5. Where the antenna is. The photo suggests a ceramic strip on the inner edge below the row (see Antenna), but nothing confirms it. Check the delivered board and ask Boardsource.
6. The switched rail on pin 5: voltage on USB and battery, polarity of P0.31, how fast it falls when switched off.

## Implementation and physical fit

Draft D uses the Draft B netlist and keeps C2 and R2 DNP. The CAD checks and their settings are recorded in [validation.json](../draft-4/validation.json). Test-print the outline and the contact row at 1:1 and hold it against the plate before ordering.
