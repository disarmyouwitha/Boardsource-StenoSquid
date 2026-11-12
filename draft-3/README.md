# Draft C back-mounted Steno Squid

[KiCad project](steno-squid.kicad_pro) · [Front artwork](previews/front.png) · [Back components](previews/back.png) · [STEP](steno-squid.step) · [Validation](validation.json)

The front shows the Inkling rotated 180° relative to the Draft B artwork view. The artwork is scaled to 82.5% and shifted to clear the vias. The WSON flash and all four passive footprints sit on the back. C2 and R2 remain DNP. Mirroring the routed board around the contact-row midpoint preserves the locked QSPI mapping and keeps the 0.40 mm supply route on the component side. With the row at the top, pin 1 is on the right in the front view and on the left in the back view.

The eight through-holes retain their inferred 2.54 mm pitch and 1.0 mm drill. The render and STEP omit the generic tall header body to show the PCB and its components. Short soldered pins are a mounting candidate. Choose the pin length and standoff after measuring the host-side clearance.

The clearance between board faces needs to accommodate the tallest overlapping parts, their solder joints and assembly tolerance. The selected C1 can reach 0.9 mm and the flash body can reach 0.8 mm before solder. Check the host pin-1 end, overhang and clearance before selecting hardware. The host switched rail and final fit still require measurements. [Draft B assembly and power review](../docs/design-review.md)
