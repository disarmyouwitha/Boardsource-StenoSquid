# Plate geometry

The [actual-size template](../pcb/previews/plate-fit-1to1.svg) comes from the current KiCad outline and contact row. The [plate-fit estimate](plate-fit-estimate.svg) shows the original photo-derived envelope. Plate dimensions are approximate and can be off by 1–2 mm.

The coordinate origin is the left end of the plate slot on its centerline. In top view on the left half, USB-C is at the top, x increases to the right, and y increases toward USB-C.

| Feature | Estimated geometry |
|---|---|
| Solid plate next to the keys | x = −2.5 to 21.9 mm |
| Top plate edge | y = 45.0 mm |
| Header slot | x = 0 to 21.9 mm, y = ±1.25 mm, open on the right |
| Wide USB-C notch | x = 2.9 to 17.1 mm, y = 42.3 to 45.0 mm |
| Narrow USB-C notch | x = 5.2 to 14.8 mm, y = 35.2 to 40.6 mm |

The 22.9 × 46.32 mm outline wraps around the notch. Its lower edge extends 1.92 mm below the row. Pin 1 is provisionally at x = 2.20 mm and the remaining seven pads follow at 2.54 mm pitch. Each pad is 1.7 mm wide with a 1.0 mm drill. Verify that the underside pad rings and solder fillets clear the slot edges so the board can sit flat.

Measure the plate thickness, plate-to-host gap, host PCB thickness and needed solder tail before choosing pin length. The photo-based stack estimate is 1.2 mm plate + 3.0 mm gap + 1.6 mm host PCB + 1.0 mm tail, or 6.8 mm below the daughterboard. Allow for the daughterboard’s 1.0 mm thickness and its top-side solder joint as well. Check whether the plate is conductive and verify keycap overhang and USB plug clearance on the assembled keyboard.

A white strip near host contacts 7 and 8 is a candidate antenna based on the host photo. Its identity and clearance remain unverified. Ground remains around the contact row for QSPI. The artwork area is copper-free on both layers. [RF review and test plan](design-review.md#antenna-clearance-and-bluetooth-test)
