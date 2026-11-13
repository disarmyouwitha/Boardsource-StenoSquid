"""Verify current reports and connector mapping, then record CAD hashes."""
from pathlib import Path
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from kicad_sexpr import nodes, kind

output = Path(__file__).resolve().parents[1] / 'pcb'
interface = json.loads((output / 'interface.json').read_text())
drc = json.loads((output / 'checks/drc.json').read_text())
erc = json.loads((output / 'checks/erc.json').read_text())
erc_issues = [issue for sheet in erc['sheets'] for issue in sheet['violations']]
assert not erc_issues
assert not drc['violations']
assert not drc['unconnected_items']
assert not drc['schematic_parity']

netlist = ET.parse(output / 'checks/netlist.xml').getroot()
members = {net.get('name').lstrip('/'): {(node.get('ref'), node.get('pin')) for node in net.findall('node')}
           for net in netlist.findall('./nets/net')}
board = (output / 'steno-squid.kicad_pcb').read_text()
footprints = {}
for _, _, node in nodes(board):
    if kind(node) == 'footprint':
        reference = re.search(r'\(property "Reference" "([^"]+)"', node)[1]
        footprints[reference] = node

def pad_net(reference, number):
    for _, _, node in nodes(footprints[reference]):
        if node.startswith(f'(pad "{number}" '):
            return re.search(r'\(net "([^"]+)"\)', node)[1].lstrip('/')
    raise AssertionError((reference, number))

for contact in interface['contacts']:
    signal = contact['signal']
    for reference, number in [('J1', contact['position']), ('U1', contact['flash_pad'])]:
        assert (reference, str(number)) in members[signal]
        assert pad_net(reference, number) == signal
assert ('C1', '1') in members['VCC_SW'] and ('C1', '2') in members['GND']
assert ('R1', '1') in members['VCC_SW'] and ('R1', '2') in members['CS_N']
assert ('R2', '1') in members['VCC_SW'] and ('R2', '2') in members['GND']
assert ('U1', '9') in members['GND'] and pad_net('U1', 9) == 'GND'
assert not drc['ignored_checks'], 'Every DRC category must be enabled'
for layer in ['F.SilkS', 'B.SilkS']:
    texts = [node for _, _, node in nodes(board) if kind(node) == 'gr_text' and f'(layer "{layer}")' in node]
    for legend in ['VCC', 'GND'] + [str(number) for number in range(1,9)]:
        assert any(node.startswith(f'(gr_text "{legend}"') for node in texts), (layer, legend)
# Parse the frozen pin map independently of the baseline's signal order.
expected = {1: ('CS_N',1), 2: ('IO0',5), 3: ('IO3',7), 4: ('IO1',2),
            5: ('VCC_SW',8), 6: ('GND',4), 7: ('CLK',6), 8: ('IO2',3)}
assert {c['position']: (c['signal'], c['flash_pad']) for c in interface['contacts']} == expected

lengths = {}
segment_counts = {}
minimum_widths = {}
via_counts = {}
for _, _, node in nodes(board):
    if kind(node) not in ['segment', 'via']:
        continue
    net = re.search(r'\(net "([^"]+)"\)', node)[1]
    if kind(node) == 'via':
        via_counts[net] = via_counts.get(net, 0) + 1
    else:
        start = tuple(map(float, re.search(r'\(start ([\d.e+-]+) ([\d.e+-]+)\)', node).groups()))
        end = tuple(map(float, re.search(r'\(end ([\d.e+-]+) ([\d.e+-]+)\)', node).groups()))
        length = sum((a-b)**2 for a,b in zip(start,end)) ** 0.5
        lengths[net] = lengths.get(net, 0) + length
        segment_counts[net] = segment_counts.get(net, 0) + 1
        width = float(re.search(r'\(width ([\d.e+-]+)\)', node)[1])
        minimum_widths[net] = min(width, minimum_widths.get(net, width))

assert minimum_widths['/VCC_SW'] >= 0.4
assert via_counts.get('/GND', 0) >= 3

report = {
    'revision': interface['revision'],
    'review_date': '2026-11-12',
    'ERC_violations': len(erc_issues),
    'DRC_violations': len(drc['violations']),
    'unconnected_items': len(drc['unconnected_items']),
    'schematic_parity_issues': len(drc['schematic_parity']),
    'all_eight_contacts_verified_against_schematic_and_PCB': True,
    'exposed_pad_grounded': True,
    'power_and_contact_labels_on_both_faces': True,
    'configured_ignored_DRC_categories': drc['ignored_checks'],
    'copper_track_lengths_mm': {net: round(value, 3) for net, value in lengths.items()},
    'minimum_track_widths_mm': minimum_widths,
    'track_segment_counts': segment_counts,
    'via_counts': via_counts,
    'host_pitch_verified': False,
    'host_fit_verified': False,
    'host_power_qualified': False,
    'hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
               for p in [output / 'steno-squid.kicad_pcb', output / 'steno-squid.kicad_sch']}
}
(output / 'validation.json').write_text(json.dumps(report, indent=2) + '\n')
print('ERC, DRC, unconnected and parity all zero. All eight contacts match the schematic and PCB.')
