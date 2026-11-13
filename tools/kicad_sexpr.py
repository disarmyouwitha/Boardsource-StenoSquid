"""Read immediate child expressions from KiCad S-expressions."""
import re


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
