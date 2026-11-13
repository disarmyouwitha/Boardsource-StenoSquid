# Boardsource Steno Squid

A QSPI flash daughterboard for the **left expansion header of the Boardsource Wireless Corne SMT**, intended for onboard Javelin stenography. This is an independent community accessory project.

## Current draft D

Draft D sits flush on top of the left Choc switch plate. The WSON flash and Inkling silkscreen face up, with the contact row along the bottom and pin 1 at the left. The full outline wraps around the USB-C notch. The plate dimensions and contact offset are provisional.

[Front preview](draft-4/previews/front.png) · [Back preview](draft-4/previews/back.png) · [1:1 plate-fit template](draft-4/previews/plate-fit-1to1.svg) · [KiCad and mounting notes](draft-4/README.md)

## Draft B electrical baseline

[KiCad project](draft-2/steno-squid.kicad_pro) · [Front](draft-2/previews/front.png) · [Back](draft-2/previews/back.png) · [Schematic](draft-2/previews/steno-squid.svg) · [STEP](draft-2/steno-squid.step) · [BOM](draft-2/BOM.csv)

- W25Q128JVPIQ, 16 MB, WSON-8 6 × 5 mm, maximum package height 0.80 mm.
- Locked pin map with clock on P0.19, IO1 on P0.23 and IO3 on P0.12.
- 22 × 17 mm outline, provisional 1.0 mm thickness, inferred 2.54 mm eight-contact header pitch.
- 100 nF C1 and 10 kΩ CS pull-up. Optional 1 µF C2 and 100 kΩ bleed resistor R2 are DNP.
- Grounded exposed pad with four paste windows and a track/via keepout. Three ground stitching vias join the pours beside U1 and C1.
- 0.40 mm switched-power traces. The front-side path runs from header contact 5 through C1 to U1 pad 8, with 39.48 mm of copper across the full power network.
- VCC, GND and contacts 1–8 are labeled on both faces, with a back-side pin-1 marker.
- Native KiCad ERC, DRC, schematic parity and unconnected checks all pass. Every DRC category is enabled. [Validation](draft-2/validation.json)

Draft B uses a generic header model and remains the electrical baseline for the plate-mounted layout.

## Draft C back-mounted comparison

Draft C puts the flash and passives on the host-facing back and the Inkling on the outward front, rotated 180° relative to Draft B's artwork. Viewed from the artwork side with the contact row at the top, pin 1 is at the right. [Mounting details and CAD](draft-3/README.md)

| | Draft B | Draft C |
|---|---|---|
| Front | [Components](draft-2/previews/front.png) | [Rotated Inkling](draft-3/previews/front.png) |
| Back | [Inkling](draft-2/previews/back.png) | [Components](draft-3/previews/back.png) |

## Locked interface

The owner locked this map on 2026-11-11. Draft D uses it with the header along the bottom of the component-side view. Confirm the pin-1 end and alignment on the host before fitting it.

| Contact | Host GPIO or rail | Flash signal | Flash pad |
|---|---|---|---|
| 1 | P0.07 | CS# | 1 |
| 2 | P0.21 | IO0 | 5 |
| 3 | P0.12 | IO3 | 7 |
| 4 | P0.23 | IO1 | 2 |
| 5 | VCC switched by P0.31 | VCC | 8 |
| 6 | GND | GND | 4 |
| 7 | P0.19 | CLK | 6 |
| 8 | P0.05 | IO2 | 3 |

All six flash signals have separate contacts. Nordic marks P0.19 for QSPI/SCK and P0.21/P0.23 for QSPI. Assigning IO0/IO1 to those data pins is the review's design judgment. The other accessible signals use the remaining header GPIOs. [Nordic pin assignments](https://docs.nordicsemi.com/bundle/ps_nrf52840/page/pin.html)

Wire the Adafruit proof of concept with eight jumpers according to this table. The firmware's active and sleep pinctrl states now use the same map, with IO2 P0.05 and IO3 P0.12 in the active pull-up group. The stock host matrix stays with its own GPIO assignments.

## Firmware and local build evidence

Firmware `main` builds its nice!nano left target with ZMK Studio enabled. The Boardsource firmware branch also passes CI for the Studio-enabled left, logging left, right, and both flash probes. Its active and sleep QSPI assignments match Draft B. [Main CI run](https://github.com/disarmyouwitha/zmk-javelin-steno/actions/runs/43167755597) · [Boardsource CI run](https://github.com/disarmyouwitha/zmk-javelin-steno/actions/runs/43167852080)

The earlier four local builds and their UF2 hashes are recorded in the [build receipt](https://github.com/disarmyouwitha/zmk-javelin-steno/blob/814ccfacb3aca3e5d9362cc7f57649fa54ed65fe/config/boardsource-wireless-corne/locked-pin-map-build.json). Studio and flash behavior still need a hardware test. Host layout stays in Javelin Steno Tools.

## Package, sourcing and assembly

The custom package-P footprint follows Winbond's 6 × 5 mm body, 1.27 mm terminal pitch and 3.4 × 4.3 mm exposed pad. Pad 9 is grounded, which the datasheet permits. Its four paste windows cover about 60% of the exposed pad. The prototype land/stencil pattern needs assembler review. Reflow assembly is intended. [Winbond drawing, section 10.3](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf)

JLCPCB lists this part as C190862, Extended, for SMT assembly. Recheck stock and quote at ordering time. The reviewed Winbond lifecycle flag remains N, so a larger production run needs a second-source and firmware compatibility review. The IQ part retains the firmware's expected JEDEC ID EF 40 18. [Assembly part](https://jlcpcb.com/partdetail/WinbondElec-W25Q128JVPIQ/C190862)

The 3D flash body uses a representative 6 × 5 × 0.8 mm WDFN model. The custom footprint defines the actual exposed pad and solder lands. Include the selected capacitor height, solder joints and nearby host components in the mounting-gap budget. C1's specified thickness reaches 0.9 mm. [Murata drawing](https://docs.rs-online.com/b196/0900766b8138861e.pdf)

## Hardware checks and remaining decisions

1. Confirm 2.54 mm pitch, 17.78 mm first-to-last span, drill/pad dimensions and the pin-1 end.
2. Establish which face points toward the host and which direction the module overhangs. Check the outline, header, battery, plate, case, antenna and all component heights.
3. Qualify the P0.31 rail on USB and battery, including polarity, voltage, current, shared loads and discharge behavior.
4. Choose R2 population from measured discharge with the intended capacitor configuration and firmware off-time.
5. Test JEDEC/SFDP, readback, quad mode, power cycling, shutdown leakage and dictionary integrity on the target.

The nice!view drawing confirms its 2.54 mm header pitch, and Boardsource documents compatible expansion use. The host pitch remains inferred until the board measurement. [nice!view drawing](https://nicekeyboards.com/docs/nice-view/pinout-schematic/), [Boardsource documentation](https://boardsource.xyz/blogs/guides/wireless-smt-corne-docs)

## Review record and earlier drafts

[Applied and pending review items](docs/review-status.md) · [Electrical/assembly review](docs/design-review.md) · [Original Claude notes](docs/claude-review-2026-11-11.md) · [Claude review of Draft B](docs/claude-review-draft-b-2026-11-11.md) · [Plate, mounting and rail notes](docs/claude-plate-and-mounting-2026-11-12.md) · [Draft D design brief](docs/draft-d-spec.md) · [Draft D plate fit drawing](docs/draft-d-plate-fit.svg)

The Draft B review’s grounding, power routing and firmware documentation items are complete. The host mating face and P0.31 rail measurements remain open before ordering.

Draft A under draft-1 preserves the SOIC version and its original mapping. Draft 0 is the initial electrical proposal. Draft B is the WSON electrical baseline and introduced the hand-drawn Inkling. Draft D enlarges the artwork on the plate-facing assembly's visible side. Independently controlled RGB needs another control path and remains future work. [Draft B back preview](draft-2/previews/back.png) · [Silkscreen vector](artwork/inkling-silkscreen.svg)

Fabrication release follows host fit, power and assembly review. Source credits and the KiCad library exception are in [ATTRIBUTION.md](ATTRIBUTION.md) and [LICENSES](LICENSES). A redistribution license for the original design has yet to be selected.
