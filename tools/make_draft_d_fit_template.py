"""Generate the actual-size Draft D fit template from native PCB geometry."""
import json
import math
from pathlib import Path
import re
from build_placement import nodes, kind

draft=Path(__file__).resolve().parents[1] / 'draft-4'
board=(draft/'steno-squid.kicad_pcb').read_text()
frame=json.loads((draft/'interface.json').read_text())['plate_frame']
pin1=frame['pin_1_x_mm']
ox,oy=frame['kicad_origin_mm']
page_x,page_y=42,108
shapes=[]
for _,_,node in nodes(board):
    if '(layer "Edge.Cuts")' not in node or kind(node) not in ('gr_line','gr_arc'):
        continue
    points={m[0]:(float(m[1])-ox+page_x,float(m[2])-oy+page_y)
            for m in re.findall(r'\((start|mid|end) ([-\d.]+) ([-\d.]+)\)',node)}
    a,c=points['start'],points['end']
    if kind(node)=='gr_line':
        end=f'L {c[0]:.5f} {c[1]:.5f}'
    else:
        b=points['mid']
        u,v=(b[0]-a[0],b[1]-a[1]),(c[0]-b[0],c[1]-b[1])
        cross=u[0]*v[1]-u[1]*v[0]
        radius=math.hypot(*u)*math.hypot(*v)*math.dist(a,c)/(2*abs(cross))
        end=f'A {radius:.5f} {radius:.5f} 0 0 {int(cross>0)} {c[0]:.5f} {c[1]:.5f}'
    shapes.append(f'    <path d="M {a[0]:.5f} {a[1]:.5f} {end}"/>')
assert shapes, 'Draft D Edge.Cuts must contain a board outline'
parts=[]
contact_pads=[]
sizes={'U1':(6,5),'R1':(1.6,.8),'C1':(1.6,.8),'C2':(1.6,.8),'R2':(1.6,.8)}
for _,_,node in nodes(board):
    if kind(node)!='footprint': continue
    ref=re.search(r'\(property "Reference" "(\w+)"',node)[1]
    placement = re.search(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', node)
    x, y = map(float, placement.group(1, 2))
    if ref == 'J1':
        assert float(placement[3]) == 90, 'J1 must run left to right'
        for _, _, pad in nodes(node):
            if kind(pad) != 'pad':
                continue
            number = int(re.search(r'\(pad "(\d+)"', pad)[1])
            px, py = map(float, re.search(r'\(at ([-\d.]+) ([-\d.]+)', pad).groups())
            contact_pads.append((number, x + py - ox, y - px - oy))
        continue
    if ref not in sizes:
        continue
    x,y=x-ox+page_x,y-oy+page_y
    w,h=sizes[ref]
    dnp=ref in ('C2','R2')
    dash=' stroke-dasharray=".6 .4"' if dnp else ''
    parts.append(f'    <rect x="{x-w/2:.3f}" y="{y-h/2:.3f}" width="{w}" height="{h}"{dash}/>')
    parts.append(f'    <text x="{x:.3f}" y="{y-h/2-.65:.3f}" text-anchor="middle" fill="#1d5787" stroke="none" font-size="1.6">{ref}{" DNP" if dnp else ""}</text>')
contacts=[]
assert len(contact_pads) == 8
for number, board_x, board_y in sorted(contact_pads):
    assert math.isclose(board_x, pin1 + 2.54 * (number - 1))
    assert math.isclose(board_y, 0)
    x = page_x + board_x
    ring=(f'<rect x="{x-.85:.3f}" y="{page_y-.85:.3f}" width="1.7" height="1.7"/>'
          if number==1 else f'<circle cx="{x:.3f}" cy="{page_y}" r=".85"/>')
    contacts.extend([f'    {ring}', f'    <circle cx="{x:.3f}" cy="{page_y}" r=".5"/>',
        f'    <text x="{x:.3f}" y="{page_y+4.7}" text-anchor="middle" fill="#111" stroke="none" font-size="1.8">{number}</text>'])
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="185mm" height="140mm" viewBox="0 0 185 140" font-family="sans-serif">
  <title>Steno Squid Draft D actual-size PCB fit template</title>
  <rect width="185" height="140" fill="#fff"/>
  <text x="10" y="14" font-size="5" font-weight="bold">Steno Squid Draft D fit template</text>
  <text x="10" y="23" font-size="3">Print at actual size (100%). Verify the 50 mm bar and the 10 mm square.</text>
  <text x="10" y="29" font-size="3">Left half seen from above, with USB-C at the top and pin 1 at the bottom left.</text>
  <text x="10" y="35" font-size="3">Cut on the black outline. Align the holes over the plate slot.</text>
  <text x="10" y="46" font-size="2.5">50 mm</text>
  <path d="M 10 49 H 60 M 10 47.5 V 50.5 M 60 47.5 V 50.5" stroke="#111" fill="none" stroke-width=".25"/>
  <rect x="81" y="42" width="10" height="10" stroke="#111" fill="none" stroke-width=".25"/>
  <text x="94" y="48" font-size="2.5">10 mm square</text>
  <text x="51.65" y="59.5" text-anchor="middle" font-size="2">USB-C notch</text>
  <rect x="42" y="106.75" width="21.9" height="2.5" fill="#dbe4ec"/>
  <g fill="none" stroke="#111" stroke-width=".20">
OUTLINE
  </g>
  <g fill="none" stroke="#1d5787" stroke-width=".18">
PARTS
  </g>
  <g fill="none" stroke="#111" stroke-width=".14">
CONTACTS
  </g>
  <text x="73" y="88" font-size="2.7">22.9 × 46.32 mm overall</text>
  <text x="73" y="94" font-size="2.7">1.0 mm drills on 2.54 mm pitch</text>
  <text x="73" y="100" font-size="2.7">Pin 1 is PIN_X mm from the slot’s left end (provisional)</text>
  <text x="73" y="109" font-size="2.7">Shaded band shows the estimated 2.5 mm slot.</text>
  <text x="10" y="128" font-size="2.7">Check keycap overhang, USB plug clearance, slot alignment and plate support.</text>
</svg>
'''
for key,value in {'OUTLINE':'\n'.join(shapes),'PARTS':'\n'.join(parts),'CONTACTS':'\n'.join(contacts),'PIN_X':str(pin1)}.items():
    svg=svg.replace(key,value)
(draft/'previews/plate-fit-1to1.svg').write_text(svg)
