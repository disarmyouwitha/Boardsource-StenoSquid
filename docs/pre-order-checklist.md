# Pre-order checklist

Updated 2026-11-13 after implementing the KiCad review.

## Applied review items

| Item | Result |
|---|---|
| C1 ground return | Added a 0.6/0.3 mm stitching via at KiCad (36.4, 58.9). Both ground pours remain connected, with four ground vias total. |
| Silkscreen | Visible labels are at least 1.0 mm high with 0.15 mm strokes. Footprint lines use 0.15 mm. The project enforces 0.15 mm silkscreen clearance. |
| Pop silkscreen | Imported the centered-gaze SVG. All eleven ink regions remain connected within each region after a 0.15 mm diameter erosion check. |
| Supply width | Added a Power netclass and a custom DRC rule enforcing 0.40 mm on VCC_SW. A temporary 0.20 mm supply segment was rejected by the rule. |
| Revision | The schematic, board title block, interface and validation identify D provisional. |
| Portable netlist | Validation removes the absolute machine path from the exported schematic source field. |
| Flash model | Added a local STEP model with its exposed-pad face extended to 3.4 × 4.3 mm. |
| Assembly sourcing | BOM includes C190862 for U1, C45000 for C1 and C98220 for R1. Confirm stock and assembly eligibility when quoting. |
| ERC | Enabled the four previously ignored categories. |
| Routing cleanup | Snapped short endpoint fragments to pad centers and removed duplicate supply segments. |
| Ground pour review | Inspected both reported narrow regions on both layers. They taper at clearance boundaries and have broad bottom-layer return copper nearby. Both pours remain connected and no starved thermal is reported. |

CAD reports, validation hashes, STEP, previews and the actual-size fit template are regenerated for the current layout. [Validation](../pcb/validation.json) · [Board preview](../pcb/previews/front-pop.png)

## Physical checks and assembly quote

- Measure the plate slot, pin-1 alignment and stack on the delivered host. The 1.7 mm pads and 1.0 mm drills remain the working geometry. Select pad size from the measured alignment and solder-fillet clearance.
- Keep the ground pour near the suspected antenna for the first prototype. Compare both Bluetooth links with the Squid fitted and removed. The earlier cutback is available in [design history](history.md).
- Check the switched supply on USB and battery, including load voltage and fall time. Keep C2 and R2 unpopulated for the breadboard test.
- Confirm the WSON stencil and exposed-pad paste coverage with the assembler. Arrange rails or a carrier for the notched outline. [Assembly notes](design-review.md#assembly-handling-and-panelization)
- Test flash ID, quad reads and dictionary integrity across power cycles and sleep.

IO2 and IO3 use the host's internal pull-ups while QSPI is active. If the rail test calls for hand-fitting R2, inspect for solder bridges to the adjacent supply trace.

## Manufacturing references

The silkscreen targets follow JLCPCB's 1.0 mm text, 0.15 mm line and 0.15 mm pad-clearance guidance. The existing 0.25 mm copper-to-edge margin is retained. [PCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities)

The capacitor and resistor catalog entries match the existing BOM manufacturer parts. [C1 GRM188R71C104KA01D](https://jlcpcb.com/partdetail/MurataElectronics-GRM188R71C104KA01D/C45000) · [R1 RC0603FR-0710KL](https://jlcpcb.com/partdetail/RC0603FR-0710KL/C98220)
