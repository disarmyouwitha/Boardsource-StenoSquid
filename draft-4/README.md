# Draft D plate-mounted Steno Squid

[KiCad project](steno-squid.kicad_pro) · [Front](previews/front.png) · [Back](previews/back.png) · [1:1 fit template](previews/plate-fit-1to1.svg) · [STEP](steno-squid.step) · [BOM](BOM.csv) · [Validation](validation.json)

The 22.9 × 46.32 mm, 1.0 mm PCB uses the full-ear outline with a stepped USB-C notch and 1 mm corner radii. It sits on the Choc switch plate with the flash, passives and Inkling on top. Viewed from above with the USB-C at the top, the contact row is at the bottom and pin 1 is at the left. The underside is solder-masked except at the contact holes. The mounting concept uses eight bare soldered pins through the plate slot. The model represents the board and its populated SMT parts.

The electrical design keeps the Draft B pin map. U1, C1 and R1 are fitted, while C2 and R2 are DNP until the breadboard rail test. The 0.40 mm supply route from J1 to C1 to U1 stays on the front without vias, and three stitching vias connect the local ground pours. The artwork area has a copper keepout on both layers. The provisional RF corner has no pours or vias and carries only the pads and short approach traces for contacts 6–8. Antenna identification and an on/off Bluetooth comparison on the host remain pending.

KiCad 10.0.7 reports zero ERC, DRC, unconnected items and schematic-parity issues with every DRC category enabled. The 2.54 mm contact pitch, 2.20 mm pin-1 offset and plate envelope still need physical confirmation.

Print the fit template at actual size and verify its 50 mm bar and 10 mm square. Align the contact row to the slot, then check the USB plug clearance, keycap overhang and plate support. The template comes from the rounded KiCad outline and J1 pad coordinates. After measuring, update J1 and its routing if needed, synchronize the pin-1 offset in `interface.json`, and regenerate the template with `python3 tools/make_draft_d_fit_template.py`. Measure the plate and host stack before choosing the pin length. Confirm the switched rail on USB and battery and measure its fall time with the breadboard flash.

[Plate geometry and provisional antenna assumptions](../docs/draft-d-spec.md)
