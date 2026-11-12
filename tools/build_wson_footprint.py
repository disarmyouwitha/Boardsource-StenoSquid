"""Generate the Winbond package-P prototype land pattern from the reviewed drawing."""
from pathlib import Path

output = Path(__file__).resolve().parents[1] / 'draft-2/footprints/StenoSquid.pretty'
name = 'WSON-8_6x5mm_P1.27mm_EP3.4x4.3mm'
items = [f'(footprint "{name}" (version 20260206) (generator "pcbnew") (layer "F.Cu")',
         '(descr "Winbond W25Q128JV package P. Body 6x5mm, maximum height 0.8mm. Prototype lands require assembler review.")',
         '(property "Reference" "REF**" (at 0 -3.4) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))',
         f'(property "Value" "{name}" (at 0 3.4) (layer "F.Fab") (effects (font (size .8 .8) (thickness .12))))',
         '(attr smd)']

def rectangle(x, y, layer, width):
    points = [(-x,-y),(x,-y),(x,y),(-x,y),(-x,-y)]
    for start, end in zip(points, points[1:]):
        items.append(f'(fp_line (start {start[0]} {start[1]}) (end {end[0]} {end[1]}) (stroke (width {width}) (type default)) (layer "{layer}"))')

rectangle(3, 2.5, 'F.Fab', .1)
rectangle(3.65, 2.8, 'F.CrtYd', .05)
# Only the top and bottom outline are exposed beyond the terminal row.
for y in [-2.65, 2.65]:
    items.append(f'(fp_line (start -3.1 {y}) (end 3.1 {y}) (stroke (width .12) (type default)) (layer "F.SilkS"))')
items.append('(fp_circle (center -3.4 -2.65) (end -3.25 -2.65) (stroke (width .12) (type default)) (fill none) (layer "F.SilkS"))')
for number, x, y in [(1,-2.825,-1.905),(2,-2.825,-.635),(3,-2.825,.635),(4,-2.825,1.905),
                     (5,2.825,1.905),(6,2.825,.635),(7,2.825,-.635),(8,2.825,-1.905)]:
    items.append(f'(pad "{number}" smd roundrect (at {x} {y}) (size 1.15 .6) (layers "F.Cu" "F.Paste" "F.Mask") (roundrect_rratio .25))')
# The copper EP is continuous. Four paste windows cover about 60% of its area.
items.append('(pad "9" smd rect (at 0 0) (size 3.4 4.3) (layers "F.Cu" "F.Mask") (zone_connect 2))')
for x in [-.8,.8]:
    for y in [-1,1]:
        items.append(f'(pad "" smd rect (at {x} {y}) (size 1.3 1.7) (layers "F.Paste"))')
items.append('(model "${KICAD10_3DMODEL_DIR}/Package_DFN_QFN.3dshapes/WDFN-8-1EP_6x5mm_P1.27mm_EP3.4x4mm.step" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))')
items.append(')')
(output / (name + '.kicad_mod')).write_text('\n'.join(items) + '\n')
