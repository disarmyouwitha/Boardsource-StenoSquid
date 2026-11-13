# Attribution

Steno Squid is an independent community accessory for the Boardsource Wireless Corne SMT. The daughterboard layout and custom circuit symbols were created for this project.

## Design references

- **Boardsource** supplied the host expansion pinout and firmware configuration used to check the interface. [Wireless SMT Corne documentation](https://boardsource.xyz/blogs/guides/wireless-smt-corne-docs) · [Boardsource ZMK configuration](https://github.com/boardsource/wireless-corne_zmk_config)
- **nice!keyboards** supplied the nice!view dimensions and pinout used to infer the host header pitch and orientation. [nice!view pinout and dimensions](https://nicekeyboards.com/docs/nice-view/pinout-schematic/)
- **Adafruit** supplied the QSPI breakout used for the proof of concept and the reference schematic consulted for the flash circuit. [Adafruit QSPI DIP Breakout PCB](https://github.com/adafruit/Adafruit-QSPI-DIP-Breakout-PCB)
- **Winbond** supplied the W25Q128JV electrical specifications and package drawing used to create the custom WSON footprint. [Winbond datasheet](https://mm.digikey.com/Volume0/opasdata/d220001/medias/docus/7159/W25Q128JV.pdf)

[Source URLs and reviewed revisions](references/sources.json)

## KiCad library assets

The 0603 capacitor and resistor footprints, the adapted 1×8 header footprint, and the component models used in the previews and STEP export come from the KiCad libraries. These assets are credited to the KiCad library contributors under CC BY-SA 4.0 with the KiCad library exception. [Upstream KiCad license](https://www.kicad.org/libraries/license/) · [License text in this repository](LICENSES/kicad-footprints-LICENSE.md)

## Artwork and project license

The squid silkscreen is a fan illustration drawn for Steno Squid, based on the Inkling from Nintendo’s *Splatoon*. [Editable artwork](artwork/inkling-silkscreen.svg) · [Nintendo character reference](https://splatoon.nintendo.com/en/world/)

The original Steno Squid hardware design has no published redistribution license.
