# Draft B design review

The direct eight-contact module is the primary design. The host pin order is fixed, while the six QSPI signal assignments are locked by the owner. Draft B and the matching firmware implement the map in the root README.

## Mechanical basis

The known nice!view drawing shows a 2.54 mm pitch. Boardsource documents nice!view support, and its default SPI signals plus supply/ground occupy consecutive expansion positions 3–7 in nice!view order. This supports a 2.54 mm working interface. A dimensioned host expansion drawing was not located in the reviewed public product pages and open-files tree. The user expects the physical board this weekend.

Draft B keeps a 22 × 17 mm rectangle, 1.0 mm thickness, 1.0 mm connector drills and 0.6/0.3 mm vias. These are daughterboard design choices. Host pitch, full row geometry, connector orientation, drill dimensions and case fit remain to be measured. The stock pin-header model is representative and taller than some low-profile options. The final mounting arrangement may place the mating hardware on the opposite face and will require a refreshed assembly model.

Standard pin/header dimensions provide a useful layout starting point. A direct soldered short-pin assembly can lower the stack. A socket permits removal if the height fits. A rigid offset adapter remains an option if the host antenna, plate or neighboring parts require it.

## Circuit and routing

C1 is a populated 100 nF capacitor at the flash supply side. R1 is a 10 kΩ pull-up from CS# to switched VCC. C2 is an optional 1 µF footprint marked DNP pending inrush and host-rail review. IO2 and IO3 each have a dedicated GPIO connection.

The trace width and copper clearance are 0.20 mm, with 0.25 mm minimum copper-to-edge clearance. The back ground plane provides the return path. Signal routing is recorded by net in draft-2/validation.json. Both layers carry ground pours. WSON pad 9 is grounded. A track/via keepout protects the exposed-pad area on both layers, with ground pours permitted. Header contacts provide accessible probe points. The host connector and MCU-side trace geometry still contribute to signal quality and cannot be assessed from this daughterboard alone.

Start bench testing at a conservative supported QSPI clock and increase it only after repeated ID, SFDP and dictionary readback checks. Compare data/CRC across cold start, USB and battery operation, reconnect and sleep/wake. The flash's advertised maximum clock is a component limit rather than a tested interface speed.

## Host power qualification

Winbond's reviewed datasheet specifies 2.7–3.6 V operation at the lower listed speed range. It lists up to 15 mA read current at the stated 50 MHz test conditions, and 25 mA during program/erase. Qualify host voltage and transient load capability against those limits. P0.31 control is documented, while the actual host switch/regulator circuit and load capability remain unverified. [Winbond datasheet, sections 9.2–9.4](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf)

The same datasheet requires a minimum 20 µs from valid VCC to CS assertion and a 5 ms delay before write instructions. A full power cycle requires the supply below 0.8 V for at least 100 µs. Firmware and rail discharge must meet these requirements. An optional bulk capacitor changes discharge/inrush behavior and therefore stays DNP initially. [Power requirements, section 9.3](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf)

Finish active writes before power removal. Put signal GPIOs into a safe state to prevent signal-pin backpower, then shut down the rail. On wake, restore power, respect startup timing and configure quad mode for the selected flash. Verify actual off-state voltage, leakage and dictionary integrity. Add dedicated discharge or other power circuitry only if the host measurements demonstrate a need.

## Firmware interface

The stock left matrix uses different GPIOs from the expansion signals. Keep that matrix unchanged. The upstream board currently enables SPI2 for nice!view on P0.23 SCK, P0.12 MOSI and P0.19 CS. The left QSPI build must release that display interface and give these pins to QSPI. The right display uses its own half's pins and can keep its display configuration. Firmware implementation and compilation are a separate integration step. [Upstream board definition](https://github.com/boardsource/wireless-corne_zmk_config/tree/master/boards/boardsource/blecorne)

## Fabrication and prototype strategy

Use black solder mask, white silkscreen and ENIG for the proposed finish. Confirm 1.0 mm thickness with the assembler and selected connector. Assemble flash, C1 and R1 on the front. Leave C2 and R2 empty initially. Inspect orientation and shorts, verify supply behavior, then read JEDEC ID and SFDP before programming the dictionary. The board and host mating orientation need explicit review before the first fabrication release.

The public repository contains native CAD, reports, BOM candidates, STEP and previews. Manufacturing Gerbers are deferred until the fit and host supply checks. All DRC categories are enabled and the current report contains no ignored categories. Passing ERC/DRC establishes the reported CAD checks, while compatibility, signal integrity and firmware behavior still require the prototype.

## Optional discharge resistor

R2 is a 100 kΩ footprint between VCC_SW and GND, DNP initially. At 3.3 V it draws 33 µA when populated. With only the local 100 nF, an ideal RC discharge to 0.8 V takes approximately 14 ms. Populating the optional 1 µF raises that estimate to 156 ms. Host capacitance, leakage, active discharge and backpower can change these times. Choose the resistance and firmware off interval from measured decay, including Winbond's required dwell below the reset threshold.

## WSON land and height review

The custom land pattern uses 1.15 × 0.60 mm terminal lands at 1.27 mm pitch and a grounded 3.4 × 4.3 mm exposed pad. Four 1.3 × 1.7 mm paste windows provide about 60% coverage. Have the assembler confirm the terminal lands, stencil and paste volume. The package-P body is at most 0.8 mm high, while the selected C1 can reach 0.9 mm before solder-joint allowance. Actual low-profile clearance also depends on components on the host face. [Winbond package drawing](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf), [Murata capacitor drawing](https://docs.rs-online.com/b196/0900766b8138861e.pdf)
