"""Rebuild the provisional placement. This overwrites PCB routing."""
from pathlib import Path
import json
import math
import re
import uuid
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'draft-2'

def new_uuid():
    return str(uuid.uuid4())

def nodes(text):
    depth = 0
    quoted = False
    escaped = False
    start = None
    for index, char in enumerate(text):
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
            continue
        if char == '"':
            quoted = True
        elif char == '(':
            if depth == 1:
                start = index
            depth += 1
        elif char == ')':
            depth -= 1
            if depth == 1 and start is not None:
                yield start, index + 1, text[start:index + 1]
                start = None

def kind(node):
    return re.match(r'\(\s*([^\s()]+)', node)[1]

def replace_nodes(text, edits):
    for start, end, replacement in sorted(edits, reverse=True):
        text = text[:start] + replacement + text[end:]
    return text

def main():
    netlist = ET.parse(OUT / 'checks/netlist.xml').getroot()
    components = {c.get('ref'): c for c in netlist.findall('./components/comp')}
    assignments = {(p.get('ref'), p.get('pin')): n.get('name')
                   for n in netlist.findall('./nets/net') for p in n.findall('node')}
    sheet = (OUT / 'steno-squid.kicad_sch').read_text()
    root_uuid = re.search(r'\(uuid "([^"]+)"\)', sheet)[1]
    placements = {'J1': (25, 25, 90), 'U1': (33.89, 33.5, 0),
                  'C1': (39.3, 30.1, 0), 'R1': (28, 30, 0), 'C2': (40.2, 37.3, 0), 'R2': (28, 37.3, 0)}
    footprints = []
    metadata = []
    for reference, (x, y, angle) in placements.items():
        component = components[reference]
        library_id = component.findtext('footprint')
        name = library_id.split(':')[1]
        text = (OUT / 'footprints/StenoSquid.pretty' / (name + '.kicad_mod')).read_text().strip()
        edits = []
        for start, end, node in nodes(text):
            node_type = kind(node)
            if node_type in ['version', 'generator', 'generator_version']:
                edits.append((start, end, ''))
            elif node_type == 'property':
                if '(property "Reference"' in node:
                    node = re.sub(r'\(property "Reference" "[^"]*"', '(property "Reference" ' + json.dumps(reference), node)
                elif '(property "Value"' in node:
                    node = re.sub(r'\(property "Value" "[^"]*"', '(property "Value" ' + json.dumps(component.findtext('value')), node)
                # Keep the circuit labels in the schematic. The compact board has separate legends.
                if '(hide yes)' not in node:
                    node = node[:-1] + '(hide yes))'
                edits.append((start, end, node))
            elif node_type == 'pad':
                number = re.match(r'\(pad "([^"]*)"', node)[1]
                match = re.search(r'\(at ([-+\d.e]+) ([-+\d.e]+)(?: ([-+\d.e]+))?\)', node)
                local_x, local_y = float(match[1]), float(match[2])
                pad_angle = float(match[3] or 0) + angle
                node = node[:match.start()] + f'(at {local_x} {local_y} {pad_angle})' + node[match.end():]
                net = assignments.get((reference, number))
                net_text = f'(net {json.dumps(net)})' if net else ''
                node = node[:-1] + net_text + f'(uuid "{new_uuid()}"))'
                edits.append((start, end, node))
                radians = math.radians(angle)
                metadata.append({'reference': reference, 'pad': number, 'net': net,
                                 'xy': [x + math.cos(radians)*local_x + math.sin(radians)*local_y,
                                        y - math.sin(radians)*local_x + math.cos(radians)*local_y]})
        text = replace_nodes(text, edits)
        text = re.sub(r'^\(footprint "[^"]+"', f'(footprint "{library_id}" (at {x} {y} {angle}) (uuid "{new_uuid()}")', text)
        if reference in ['C2', 'R2']:
            text = text.replace('(attr smd)', '(attr smd dnp)')
        text = text[:-1] + f'(path "/{root_uuid}/{component.findtext("tstamps")}"))'
        footprints.append(text)
    layers = [(0,'F.Cu','signal'), (2,'B.Cu','signal'), (13,'F.Paste','user'), (15,'B.Paste','user'),
              (5,'F.SilkS','user'),(7,'B.SilkS','user'),(1,'F.Mask','user'),(3,'B.Mask','user'),
              (17,'Dwgs.User','user'),(19,'Cmts.User','user'),(25,'Edge.Cuts','user'),
              (31,'F.CrtYd','user'),(29,'B.CrtYd','user'),(35,'F.Fab','user'),(33,'B.Fab','user')]
    layer_text = '(layers ' + ''.join(f'({number} "{name}" {type_})' for number,name,type_ in layers) + ')'
    outline = [(23,23),(45,23),(45,40),(23,40),(23,23)]
    edge = ''.join(f'(gr_line (start {a[0]} {a[1]}) (end {b[0]} {b[1]}) (stroke (width .05) (type default)) (layer "Edge.Cuts") (uuid "{new_uuid()}"))' for a,b in zip(outline,outline[1:]))
    labels = []
    for index, label in enumerate(['1','2','3','4','5','6','7','8']):
        labels.append(f'(gr_text "{label}" (at {25+2.54*index} 27.7) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))')
    labels.append('(gr_text "Steno Squid B" (at 33.89 38.8) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))')
    for layer in ['F.SilkS', 'B.SilkS']:
        mirror = '(justify mirror)' if layer.startswith('B') else ''
        if layer.startswith('B'):
            for index in range(8):
                labels.append(f'(gr_text "{index+1}" (at {25+2.54*index} 27.7) (layer "{layer}") (effects (font (size .8 .8) (thickness .12)) {mirror}))')
        for x, text in [(35.16, 'VCC'), (37.7, 'GND')]:
            labels.append(f'(gr_text "{text}" (at {x} 28.9) (layer "{layer}") (effects (font (size .8 .8) (thickness .12)) {mirror}))')
    labels.append('(gr_text "2.54mm HEADER INFERRED / HOST FIT PENDING" (at 34 20) (layer "Dwgs.User") (effects (font (size .8 .8) (thickness .12))))')
    keepout_points = [(32.09,31.25),(35.69,31.25),(35.69,35.75),(32.09,35.75)]
    keepout = '(zone (layers "F.Cu" "B.Cu") (uuid "' + new_uuid() + '") (name "EP no tracks or vias") (hatch edge .5) (keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour allowed) (footprints allowed)) (polygon (pts ' + ''.join(f'(xy {x} {y})' for x,y in keepout_points) + ')))'
    board = '(kicad_pcb (version 20260206) (generator "pcbnew") (general (thickness 1.0)) (paper "A4")' + layer_text + '(setup (pad_to_mask_clearance 0))' + ''.join(footprints) + edge + ''.join(labels) + keepout + ')\n'
    (OUT / 'steno-squid.kicad_pcb').write_text(board)
    (OUT / 'placement.json').write_text(json.dumps({'outline':outline,'pads':metadata,'pitch_mm':2.54,'host_pitch_verified':False,'thickness_mm':1.0,'exposed_pad_keepout':keepout_points},indent=2)+'\n')

if __name__ == '__main__':
    main()
