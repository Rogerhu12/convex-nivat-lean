"""Count nonblank Lean source lines after removing nested comments.

Only NivatTrial/*.lean is counted; scratch probes, audit commands, and existing
mathlib are excluded. Strings are preserved, including comment-like characters.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent

def uncomment(source):
    out = []
    depth = 0
    string = False
    i = 0
    while i < len(source):
        ch = source[i]
        nxt = source[i:i + 2]
        if depth:
            if nxt == '/-':
                depth += 1
                i += 2
            elif nxt == '-/':
                depth -= 1
                i += 2
            else:
                if ch == '\n':
                    out.append('\n')
                i += 1
        elif string:
            out.append(ch)
            i += 1
            if ch == '\\' and i < len(source):
                out.append(source[i])
                i += 1
            elif ch == '"':
                string = False
        elif nxt == '/-':
            depth = 1
            out.append(' ')
            i += 2
        elif nxt == '--':
            j = source.find('\n', i)
            i = len(source) if j < 0 else j
        else:
            out.append(ch)
            i += 1
            if ch == '"':
                string = True
    if depth:
        raise ValueError('Unclosed block comment')
    return ''.join(out)

def measure():
    rows = []
    for path in sorted((ROOT / 'NivatTrial').glob('*.lean')):
        text = path.read_text(encoding='utf-8-sig')
        code = uncomment(text)
        rows.append(dict(file=path.name, total_lines=len(text.splitlines()),
                         code_lines=sum(bool(line.strip()) for line in code.splitlines())))
    return dict(files=rows, total_lines=sum(r['total_lines'] for r in rows),
                code_lines=sum(r['code_lines'] for r in rows))

if __name__ == '__main__':
    print(json.dumps(measure(), ensure_ascii=False, indent=2))
