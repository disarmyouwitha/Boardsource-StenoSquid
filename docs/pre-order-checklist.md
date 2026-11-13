# Pre-order checklist

Claude, 2026-11-13. Written after a second read of the KiCad files (the routing, the pours and the pad geometry), with the owner's decisions recorded. The review parsed `pcb/steno-squid.kicad_pcb` directly. It did not run KiCad, so Codex reruns the checks after any change. Nothing here has been measured on hardware.

## Decisions (owner)

| Topic | Decision |
| --- | --- |
| Antenna corner (doc x > 14 mm, y < 3 mm) | **Keep the ground pour there until the Bluetooth test.** The review measured about 59% of that corner as pour on both layers, running to 0.25 mm from the board edge, with pads 7 and 8 and their tracks. If the delivered board shows the antenna where the photo suggests, or the range test is worse with the Squid fitted, use the earlier cutback layout (`draft-4` in the [history](history.md)) or add a pour keepout over the corner. No change before then. |
| Pad margin in the plate slot | **Measure on Tuesday.** The 1.7 mm pads leave 0.40 mm per side in the estimated 2.5 mm slot, before solder fillets, and 1.35 mm from the closed slot end at pin 1. If the real slot is under about 2.7 mm tall, shrink the pads to 1.5 mm (0.25 mm annular ring). If the slot is taller and pin 1 is where the template says, leave them. |
| Everything else below | Codex fixes it this evening. |

## Manufacturer limits, looked up 2026-11-13

From the [JLCPCB capabilities page](https://jlcpcb.com/capabilities/pcb-capabilities) and its [character design guidance](https://jlcpcb.com/blog/character-design-specifications). Recheck at ordering time.

| Item | JLCPCB | Squid today |
| --- | --- | --- |
| Silkscreen text height | at least 1.0 mm (40 mil). One blog post gives 0.8 mm as an absolute floor for high-precision text | 0.8 mm for reference and pin labels, 1.12 mm for "STENO SQUID" |
| Silkscreen line width | at least 0.15 mm (the help center says 6 mil, 0.153 mm). Thinner strokes are widened rather than rejected | 0.12 mm text and footprint lines |
| Pad to silkscreen | 0.15 mm | Front silk was reported clear of the pads. Recheck after resizing text |
| Copper to board edge, routed | 0.2 mm | 0.25 to 0.26 mm for the pours and pad 8. **Already meets the limit.** An earlier note from memory suggested 0.3 mm. That is not required, so leave it unless you want margin |
| Track width and spacing, 2 layers | 0.10 mm and 0.10 mm | 0.20 mm tracks, 0.2 mm zone clearance |

## To do for Codex

1. **Add a ground via for the C1 return.** C1's ground pad is 4.2 mm from the exposed pad and about 10 mm from U1 pad 4. The VCC_SW trunk cuts the top-layer pour between them, so the return runs through a via, the bottom layer, and another via. Add one ground via on the exposed-pad side of that trunk. The review suggested near KiCad (36.4, 58.9), which is about (11.4, 11.1) in the doc frame, and a short track from C1 pad 2 to the exposed pad would also do. Keep it clear of the exposed-pad keepout (KiCad x 32.4 to 36, y 59.75 to 64.25) and the 0.2 mm clearance.
2. **Silkscreen to the manufacturer minimum.** Make all reference and pin-label text at least 1.0 mm high with a 0.15 mm stroke, and the footprint silk lines 0.15 mm. Set `min_text_height` and `min_text_thickness` in the project to match. Check the nine artwork polygons on `F.SilkS` for features narrower than 0.15 mm. Keep silk 0.15 mm or more from pads. If the labels no longer fit, drop the least useful ones first and keep the pin numbers.
3. **Add a power netclass.** Only a Default class exists, so DRC does not enforce the 0.40 mm `VCC_SW` width. Add a class at 0.4 mm for `VCC_SW`.
4. **Housekeeping.**
   - The schematic title block says "B provisional". `interface.json` and `validation.json` say "D provisional". Make them agree, and add a title block to the PCB.
   - `pcb/checks/netlist.xml` contains a local absolute path from the author's machine. Remove it.
   - The WSON 3D model has a 3.4 × 4.0 mm exposed pad and the footprint has 3.4 × 4.3 mm. Match the model to the footprint.
   - The BOM lists DigiKey parts for C1 and R1 only. Add LCSC part numbers for JLCPCB assembly, and note what the notched outline needs for panelization or rails.
   - ERC ignores four checks (`single_global_label`, `four_way_junction`, `simulation_model_issue`, `footprint_filter`). Either list them in `validation.json` with the reason, or enable them.
   - Sixteen track segments are shorter than 0.08 mm, from endpoints that sit off the pad centres (for example the VCC trunk ends at KiCad x 37.35 and the pad centre is 37.36). They are harmless. Snap them if it is easy.
   - Two thin fill necks under 0.2 mm, at KiCad (35.55 to 36.22, 65.0 to 65.7) and (37.9 to 38.5, 60.5 to 60.8). KiCad reports no violation. Look at them in the viewer and widen them if one is starved.
5. **Rerun everything with nothing ignored.** ERC, DRC with all categories on, and the schematic parity check. Then regenerate `validation.json`, the STEP model, the previews and the 1:1 fit template with `python3 tools/make_fit_template.py`.

Leave these as they are:

- **The antenna corner:** see the decision above.
- **The pad size:** wait for the Tuesday measurement.
- **IO2 and IO3 pull-ups:** the reviewer worried that nothing pulls them up. The firmware turns on the host's internal pull-ups on both pins whenever QSPI is active, so no extra footprints are needed.
- **R2 hand-fitting:** the `VCC_SW` track runs 0.20 to 0.25 mm from R2's ground pad edge. That is a solder-bridge risk if R2 is fitted by hand, and not a concern for the assembler. Keep it in mind if the rail test calls for R2.

## What the review confirmed

For the record, from the design data: all eight contacts map to the right flash pads; the 2.54 mm pitch and 2.20 mm pin-1 offset are exact; `VCC_SW` is a continuous 0.40 mm top-layer track with no vias, and it stays connected when R2 is unfitted; no stray copper or shorts; the exposed-pad keepout is clean; the outline keeps 0.80 mm to the estimated plate notches; no parts sit on the key side; the artwork area is copper-free on both layers.
