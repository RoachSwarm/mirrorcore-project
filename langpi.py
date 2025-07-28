# 🌀 LangPi Interpreter Prototype — v0.1
# Rooted in Spiral Logic, π-based Truth, and Sovereign Will

import math

CONSTANTS = {
    'π': math.pi,
    'pi': math.pi
}

CONTEXT = {}

def resolve_value(val):
    if val in CONSTANTS:
        return CONSTANTS[val]
    if val.isdigit():
        return int(val)
    if val in CONTEXT:
        return CONTEXT[val]
    return val

def interpret_line(line):
    line = line.strip()
    if line.startswith('let'):
        # Declaration
        parts = line.split('=')
        var_part = parts[0].replace('let', '').strip()
        val_part = parts[1].strip()
        CONTEXT[var_part] = resolve_value(val_part)
        print(f"🧿 {var_part} bound to {CONTEXT[var_part]}")

    elif line.startswith('if'):
        # Simple if block
        condition = line[line.find('(')+1:line.find(')')]
        if '==' in condition:
            left, right = map(str.strip, condition.split('=='))
            if resolve_value(left) == resolve_value(right):
                print("🜂 Condition met: executing inner will")
                return 'await_block'
            else:
                print("🜄 Condition unmet: skipping potential")
                return 'skip_block'

    elif line.startswith('echo') or 'echo' in line:
        quote_start = line.find('"')
        quote_end = line.rfind('"')
        if quote_start != -1 and quote_end != -1:
            message = line[quote_start+1:quote_end]
            print(f"🔊 {message}")

    elif line.startswith('return'):
        val = line.replace('return', '').strip()
        print(f"✶ Returning: {resolve_value(val)}")
        return 'end'

    else:
        print(f"⚠️ Unrecognized line: {line}")


def run_langpi_script(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        i = 0
        skip = False
        while i < len(lines):
            line = lines[i].strip()
            if skip:
                if line.startswith('return'):
                    interpret_line(line)
                    break
                i += 1
                continue

            result = interpret_line(line)
            if result == 'await_block':
                i += 1
                if i < len(lines):
                    interpret_line(lines[i])
            elif result == 'skip_block':
                skip = True
            elif result == 'end':
                break
            i += 1

    except Exception as e:
        print(f"💥 LangPi Error: {e}")

if __name__ == '__main__':
    print("🌀 LangPi Interpreter — v0.1 Initialized")
    run_langpi_script("test.pi")

