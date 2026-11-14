# Electrical, mechanical and RF review

## Mechanical basis

The daughterboard sits on top of the left Choc switch plate, with eight bare pins through the plate slot. The 2.54 mm pitch and top-view contact order are inferred from Boardsource's expansion pinout and its nice!view compatibility. The plate envelope comes from a scaled image. Verify the host pin-1 position, slot width, USB plug clearance and plate-to-host stack on the actual keyboard. [Boardsource documentation](https://boardsource.xyz/blogs/guides/wireless-smt-corne-docs) · [nice!view drawing](https://nicekeyboards.com/docs/nice-view/pinout-schematic/) · [Board and fit template](../pcb/README.md)

## Circuit and routing

C1 is 100 nF at the flash supply. R1 pulls CS# up to switched VCC through 10 kΩ. C2 and R2 remain unpopulated until rail measurements support a change. A custom DRC rule enforces the 0.40 mm supply minimum. The 0.40 mm front-layer supply runs from J1 contact 5 through C1 to U1 pad 8 without vias. Four stitching vias connect the local ground pours. The added via at KiCad (36.4, 58.9) joins the flash-side ground region to the bottom return plane across the supply trunk from C1. Flash pad 9 is grounded with a track and via keepout under the exposed pad. [Routing measurements](../pcb/validation.json)

## Antenna clearance and Bluetooth test

The suspected host antenna is based on a photo. Its part, exact position and clearance requirements remain unverified. The daughterboard retains ground around contacts 6–8 to support the CLK and IO2 return paths. The artwork area has a copper keepout on both layers. If assembled Bluetooth testing shows a problem or the antenna specification requires more clearance, evaluate a local cutback near the lower-right corner (x > 14 mm, y < 3 mm in the plate frame) and retest QSPI.

Nearby ground copper, pads, traces and bare pins can detune the antenna or change its radiation pattern if they are close enough. The plate material and final stack also matter. Confirm the antenna's actual keepout against the assembled geometry. KiCad checks the layout rules drawn in the board file. Bluetooth performance requires measurement on the assembled keyboard. [Infineon antenna layout guidelines, section 12](https://www.infineon.com/assets/row/public/documents/cross-divisions/42/infineon-an91445-antenna-design-and-rf-layout-guidelines-applicationnotes-en.pdf)

Compare Bluetooth with the module removed and fitted, using the same plate, case, positions, orientations and distances. Check both the left-to-right link and the left-to-host link. Compare RSSI where available, and watch for reduced usable range, dropouts or reconnects. With the module fitted, repeat during flash activity to check whether traffic on the QSPI lines changes the result.

## Host power qualification

Winbond's reviewed datasheet specifies 2.7–3.6 V operation at the lower listed speed range. It lists up to 15 mA read current at the stated 50 MHz test conditions, and 25 mA during program/erase. Qualify host voltage and transient load capability against those limits. P0.31 control is documented, while the actual host switch/regulator circuit and load capability remain unverified. [Winbond datasheet, sections 9.2–9.4](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf)

The same datasheet requires a minimum 20 µs from valid VCC to CS assertion and a 5 ms delay before write instructions. A full power cycle requires the supply below 0.8 V for at least 100 µs. Firmware and rail discharge must meet these requirements. An optional bulk capacitor changes discharge/inrush behavior and therefore stays DNP initially. [Power requirements, section 9.3](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf)

Finish active writes before power removal. Put signal GPIOs into a safe state to prevent signal-pin backpower, then shut down the rail. On wake, restore power, respect startup timing and configure quad mode for the selected flash. Verify actual off-state voltage, leakage and dictionary integrity. Add dedicated discharge or other power circuitry only if the host measurements demonstrate a need.

## Firmware interface

The stock left matrix uses different GPIOs from the expansion signals. Keep that matrix unchanged. The upstream board currently enables SPI2 for nice!view on P0.23 SCK, P0.12 MOSI and P0.19 CS. The left QSPI build must release that display interface and give these pins to QSPI. The right display uses its own half's pins and can keep its display configuration. The tested Boardsource firmware uses the same QSPI assignments in its active and sleep states. The Studio-enabled left, logging left, right and both probes build in CI on the firmware branch. [Boardsource firmware CI](https://github.com/disarmyouwitha/zmk-javelin-steno/actions/workflows/build.yml?query=branch%3Asteno-squid%2Flocked-pin-map) [Upstream board definition](https://github.com/boardsource/wireless-corne_zmk_config/tree/master/boards/boardsource/blecorne)

## Fabrication and prototype strategy

Use black solder mask, white silkscreen and ENIG for the proposed finish. Confirm 1.0 mm thickness with the assembler and selected connector. C1 and R1 have assembly catalog numbers in the BOM. Confirm stock when quoting. Assemble flash, C1 and R1 on the front. Leave C2 and R2 empty initially. Inspect orientation and shorts, verify supply behavior, then read JEDEC ID and SFDP before programming the dictionary. Confirm host contact alignment, plate fit and RF clearance before the first fabrication release.

The public repository contains native CAD, reports, BOM candidates, STEP and previews. Manufacturing Gerbers are deferred until the fit and host supply checks. All ERC and DRC categories are enabled and the current report contains no ignored categories. Passing ERC/DRC establishes the reported CAD checks, while compatibility, signal integrity and firmware behavior still require the prototype.

## Optional discharge resistor

R2 is a 100 kΩ footprint between VCC_SW and GND, DNP initially. At 3.3 V it draws 33 µA when populated. With only the local 100 nF, an ideal RC discharge to 0.8 V takes approximately 14 ms. Populating the optional 1 µF raises that estimate to 156 ms. Host capacitance, leakage, active discharge and backpower can change these times. Choose the resistance and firmware off interval from measured decay, including Winbond's required dwell below the reset threshold.

## WSON land and height review

Visible labels use at least 1.0 mm height and 0.15 mm strokes. Footprint silkscreen lines are 0.15 mm wide, with a 0.15 mm minimum silkscreen clearance. The Pop artwork is rendered as filled front silkscreen polygons. [Editable SVG](../artwork/pop-centered-gaze-silkscreen.svg)

The custom land pattern uses 1.15 × 0.60 mm terminal lands at 1.27 mm pitch and a grounded 3.4 × 4.3 mm exposed pad. Four 1.3 × 1.7 mm paste windows provide about 60% coverage. Have the assembler confirm the terminal lands, stencil and paste volume. The package-P body is at most 0.8 mm high, while the selected C1 can reach 0.9 mm before solder-joint allowance. Check the resulting height above the switch plate against keycap overhang and case clearance. [Winbond package drawing](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf), [Murata capacitor drawing](https://docs.rs-online.com/b196/0900766b8138861e.pdf)

## Assembly handling and panelization

The stepped outline and 22.9 mm width need an assembler-approved carrier or panel arrangement. For JLCPCB standard assembly, allow at least 5 mm handling rails with fiducials and tooling holes as specified for the selected service. Have the assembler choose tab locations and routed spacing so separation preserves the fitted outline, USB notch and header pads. Panelization is pending the fit measurement and assembly quote. [JLCPCB rail guidance](https://jlcpcb.com/help/article/how-to-add-edge-rails-fiducials-for-pcb-assembly-order) · [Irregular board size guidance](https://jlcpcb.com/help/article/pcb-dimensions)
